const Deal = require('../models/Deal');
const Company = require('../models/Company');
const AgentExecution = require('../models/AgentExecution');
const taskQueue = require('./taskQueue');
const timelinePrediction = require('./timelinePrediction');
const { query } = require('../utils/database');

class DealOrchestratorService {
  constructor() {
    this.agentTypes = ['finance', 'legal', 'synergy', 'reputation', 'operations'];
    this.agentDependencies = {
      'finance': [],
      'legal': [],
      'synergy': ['finance'],
      'reputation': [],
      'operations': ['finance', 'legal']
    };
  }

  /**
   * Create a new deal and initialize agent orchestration
   * @param {Object} dealData - Deal creation data
   * @returns {Promise<Object>} Created deal with orchestration plan
   */
  async createDeal(dealData) {
    // Validate deal data
    const validation = Deal.validate(dealData);
    if (!validation.isValid) {
      throw new Error(`Deal validation failed: ${validation.errors.join(', ')}`);
    }

    // Verify companies exist
    const acquirer = await Company.findById(dealData.acquirer_id);
    const target = await Company.findById(dealData.target_id);
    
    if (!acquirer) {
      throw new Error(`Acquirer company with ID ${dealData.acquirer_id} not found`);
    }
    
    if (!target) {
      throw new Error(`Target company with ID ${dealData.target_id} not found`);
    }

    // Create the deal
    const deal = new Deal(dealData);
    await deal.save();

    // Create orchestration plan
    const orchestrationPlan = await this.createOrchestrationPlan(deal.id);

    return {
      deal,
      orchestration_plan: orchestrationPlan,
      acquirer: acquirer,
      target: target
    };
  }

  /**
   * Create orchestration plan for a deal
   * @param {string} dealId - Deal ID
   * @returns {Promise<Object>} Orchestration plan with agent tasks
   */
  async createOrchestrationPlan(dealId) {
    const deal = await Deal.findById(dealId);
    if (!deal) {
      throw new Error(`Deal with ID ${dealId} not found`);
    }

    // Create agent execution records
    const agentExecutions = [];
    
    for (const agentType of this.agentTypes) {
      const execution = new AgentExecution({
        deal_id: dealId,
        agent_type: agentType,
        agent_id: `${agentType}-agent-${Date.now()}`,
        status: 'pending',
        input_data: {
          deal_id: dealId,
          agent_dependencies: this.agentDependencies[agentType]
        }
      });
      
      await execution.save();
      agentExecutions.push(execution);
    }

    // Create execution plan with dependencies
    const executionPlan = this.buildExecutionPlan(agentExecutions);

    // Distribute tasks to the queue system
    const distributionResult = await taskQueue.distributeTasks(dealId);

    // Calculate initial timeline estimate
    try {
      const timelineEstimate = await timelinePrediction.calculateTimeline(dealId);
      executionPlan.timeline_estimate = timelineEstimate;
    } catch (error) {
      console.error('Failed to calculate initial timeline estimate:', error);
      // Continue without timeline estimate
    }

    return {
      deal_id: dealId,
      total_agents: agentExecutions.length,
      execution_plan: executionPlan,
      estimated_duration_hours: this.estimateExecutionDuration(agentExecutions),
      task_distribution: distributionResult,
      created_at: new Date()
    };
  }

  /**
   * Build execution plan considering agent dependencies
   * @param {AgentExecution[]} executions - Agent executions
   * @returns {Object} Execution plan with phases
   */
  buildExecutionPlan(executions) {
    const phases = [];
    const executionMap = new Map();
    
    // Map executions by agent type
    executions.forEach(exec => {
      executionMap.set(exec.agent_type, exec);
    });

    // Phase 1: Independent agents (no dependencies)
    const phase1 = executions.filter(exec => 
      this.agentDependencies[exec.agent_type].length === 0
    );
    
    if (phase1.length > 0) {
      phases.push({
        phase: 1,
        description: 'Independent analysis agents',
        agents: phase1.map(exec => exec.agent_type),
        can_run_parallel: true,
        estimated_duration_hours: Math.max(...phase1.map(exec => 
          this.getAgentEstimatedDuration(exec.agent_type)
        ))
      });
    }

    // Phase 2: Dependent agents
    const phase2 = executions.filter(exec => 
      this.agentDependencies[exec.agent_type].length > 0
    );
    
    if (phase2.length > 0) {
      phases.push({
        phase: 2,
        description: 'Dependent analysis agents',
        agents: phase2.map(exec => exec.agent_type),
        dependencies: phase2.reduce((deps, exec) => {
          deps[exec.agent_type] = this.agentDependencies[exec.agent_type];
          return deps;
        }, {}),
        can_run_parallel: false,
        estimated_duration_hours: phase2.reduce((total, exec) => 
          total + this.getAgentEstimatedDuration(exec.agent_type), 0
        )
      });
    }

    return {
      total_phases: phases.length,
      phases: phases,
      total_estimated_hours: phases.reduce((total, phase) => 
        total + phase.estimated_duration_hours, 0
      )
    };
  }

  /**
   * Get estimated duration for an agent type
   * @param {string} agentType - Agent type
   * @returns {number} Estimated duration in hours
   */
  getAgentEstimatedDuration(agentType) {
    const durations = {
      'finance': 2.5,
      'legal': 3.0,
      'synergy': 1.5,
      'reputation': 1.0,
      'operations': 2.0
    };
    
    return durations[agentType] || 2.0;
  }

  /**
   * Estimate total execution duration
   * @param {AgentExecution[]} executions - Agent executions
   * @returns {number} Estimated duration in hours
   */
  estimateExecutionDuration(executions) {
    // Phase 1 agents can run in parallel
    const phase1Duration = Math.max(
      ...executions
        .filter(exec => this.agentDependencies[exec.agent_type].length === 0)
        .map(exec => this.getAgentEstimatedDuration(exec.agent_type))
    );

    // Phase 2 agents run sequentially
    const phase2Duration = executions
      .filter(exec => this.agentDependencies[exec.agent_type].length > 0)
      .reduce((total, exec) => total + this.getAgentEstimatedDuration(exec.agent_type), 0);

    return phase1Duration + phase2Duration;
  }

  /**
   * Get deal status with agent progress
   * @param {string} dealId - Deal ID
   * @returns {Promise<Object>} Deal status with agent progress
   */
  async getDealStatus(dealId) {
    const deal = await Deal.findById(dealId);
    if (!deal) {
      throw new Error(`Deal with ID ${dealId} not found`);
    }

    const executions = await AgentExecution.findByDealId(dealId);
    const executionHistory = await AgentExecution.getExecutionHistory(dealId);

    // Calculate overall progress
    const totalAgents = executions.length;
    const completedAgents = executions.filter(exec => exec.status === 'completed').length;
    const failedAgents = executions.filter(exec => exec.status === 'failed').length;
    const runningAgents = executions.filter(exec => exec.status === 'running').length;
    const pendingAgents = executions.filter(exec => exec.status === 'pending').length;

    const overallProgress = totalAgents > 0 ? (completedAgents / totalAgents) * 100 : 0;

    // Identify bottlenecks
    const bottlenecks = this.identifyBottlenecks(executions);

    // Check if recursive analysis is needed
    const recursiveAnalysisNeeded = await this.checkRecursiveAnalysisNeeded(dealId);

    return {
      deal,
      progress: {
        overall_percentage: Math.round(overallProgress),
        completed_agents: completedAgents,
        failed_agents: failedAgents,
        running_agents: runningAgents,
        pending_agents: pendingAgents,
        total_agents: totalAgents
      },
      agent_status: executions.map(exec => ({
        agent_type: exec.agent_type,
        status: exec.status,
        progress_percentage: exec.progress_percentage,
        start_time: exec.start_time,
        end_time: exec.end_time,
        duration_seconds: exec.duration_seconds,
        error_message: exec.error_message
      })),
      timeline: executionHistory.timeline,
      bottlenecks,
      recursive_analysis_needed: recursiveAnalysisNeeded,
      next_actions: this.getNextActions(executions, bottlenecks)
    };
  }

  /**
   * Identify bottlenecks in agent execution
   * @param {AgentExecution[]} executions - Agent executions
   * @returns {Array} Array of bottleneck descriptions
   */
  identifyBottlenecks(executions) {
    const bottlenecks = [];
    
    // Check for failed agents
    const failedAgents = executions.filter(exec => exec.status === 'failed');
    if (failedAgents.length > 0) {
      bottlenecks.push({
        type: 'failed_agents',
        description: `${failedAgents.length} agent(s) have failed`,
        agents: failedAgents.map(exec => exec.agent_type),
        severity: 'high'
      });
    }

    // Check for long-running agents
    const longRunningAgents = executions.filter(exec => {
      if (exec.status !== 'running' || !exec.start_time) return false;
      const runningTime = (new Date() - new Date(exec.start_time)) / (1000 * 60 * 60); // hours
      const expectedDuration = this.getAgentEstimatedDuration(exec.agent_type);
      return runningTime > expectedDuration * 1.5; // 50% over expected time
    });

    if (longRunningAgents.length > 0) {
      bottlenecks.push({
        type: 'long_running_agents',
        description: `${longRunningAgents.length} agent(s) are taking longer than expected`,
        agents: longRunningAgents.map(exec => exec.agent_type),
        severity: 'medium'
      });
    }

    // Check for dependency blocks
    const dependentAgents = executions.filter(exec => 
      this.agentDependencies[exec.agent_type].length > 0 && exec.status === 'pending'
    );

    dependentAgents.forEach(exec => {
      const dependencies = this.agentDependencies[exec.agent_type];
      const blockedBy = dependencies.filter(depType => {
        const depExecution = executions.find(e => e.agent_type === depType);
        return depExecution && depExecution.status !== 'completed';
      });

      if (blockedBy.length > 0) {
        bottlenecks.push({
          type: 'dependency_block',
          description: `${exec.agent_type} agent is blocked by incomplete dependencies`,
          agent: exec.agent_type,
          blocked_by: blockedBy,
          severity: 'low'
        });
      }
    });

    return bottlenecks;
  }

  /**
   * Check if recursive analysis is needed
   * @param {string} dealId - Deal ID
   * @returns {Promise<boolean>} Whether recursive analysis is needed
   */
  async checkRecursiveAnalysisNeeded(dealId) {
    const sql = `
      SELECT COUNT(*) as recursive_findings
      FROM findings 
      WHERE deal_id = $1 AND requires_recursion = true
    `;
    
    const result = await query(sql, [dealId]);
    return parseInt(result.rows[0].recursive_findings) > 0;
  }

  /**
   * Get next recommended actions
   * @param {AgentExecution[]} executions - Agent executions
   * @param {Array} bottlenecks - Identified bottlenecks
   * @returns {Array} Array of recommended actions
   */
  getNextActions(executions, bottlenecks) {
    const actions = [];

    // Handle failed agents
    const failedAgents = executions.filter(exec => exec.status === 'failed');
    if (failedAgents.length > 0) {
      actions.push({
        action: 'retry_failed_agents',
        description: 'Retry failed agent executions',
        priority: 'high',
        agents: failedAgents.map(exec => exec.agent_type)
      });
    }

    // Handle ready-to-run agents
    const readyAgents = executions.filter(exec => {
      if (exec.status !== 'pending') return false;
      const dependencies = this.agentDependencies[exec.agent_type];
      return dependencies.every(depType => {
        const depExecution = executions.find(e => e.agent_type === depType);
        return depExecution && depExecution.status === 'completed';
      });
    });

    if (readyAgents.length > 0) {
      actions.push({
        action: 'start_ready_agents',
        description: 'Start agents that have all dependencies completed',
        priority: 'medium',
        agents: readyAgents.map(exec => exec.agent_type)
      });
    }

    // Handle completed analysis
    const completedAgents = executions.filter(exec => exec.status === 'completed');
    if (completedAgents.length === executions.length) {
      actions.push({
        action: 'generate_final_report',
        description: 'All agents completed - generate final due diligence report',
        priority: 'high'
      });
    }

    return actions;
  }

  /**
   * Update deal status
   * @param {string} dealId - Deal ID
   * @param {string} status - New status
   * @returns {Promise<Deal>} Updated deal
   */
  async updateDealStatus(dealId, status) {
    const deal = await Deal.findById(dealId);
    if (!deal) {
      throw new Error(`Deal with ID ${dealId} not found`);
    }

    deal.status = status;
    if (status === 'completed') {
      deal.actual_completion_date = new Date();
    }

    return await deal.update();
  }

  /**
   * Get all deals with their orchestration status
   * @param {Object} filters - Filter options
   * @returns {Promise<Array>} Array of deals with status
   */
  async getAllDealsWithStatus(filters = {}) {
    const deals = await Deal.findAll(filters);
    
    const dealsWithStatus = await Promise.all(
      deals.map(async (deal) => {
        const executions = await AgentExecution.findByDealId(deal.id);
        const completedAgents = executions.filter(exec => exec.status === 'completed').length;
        const totalAgents = executions.length;
        const overallProgress = totalAgents > 0 ? (completedAgents / totalAgents) * 100 : 0;

        return {
          ...deal,
          orchestration_status: {
            total_agents: totalAgents,
            completed_agents: completedAgents,
            overall_progress: Math.round(overallProgress),
            has_active_executions: executions.some(exec => 
              exec.status === 'running' || exec.status === 'pending'
            )
          }
        };
      })
    );

    return dealsWithStatus;
  }

  /**
   * Cancel deal orchestration
   * @param {string} dealId - Deal ID
   * @returns {Promise<Object>} Cancellation result
   */
  async cancelDealOrchestration(dealId) {
    const deal = await Deal.findById(dealId);
    if (!deal) {
      throw new Error(`Deal with ID ${dealId} not found`);
    }

    // Cancel pending executions
    const cancelledCount = await AgentExecution.cancelPendingExecutions(dealId);

    // Update deal status
    deal.status = 'cancelled';
    await deal.update();

    return {
      deal,
      cancelled_executions: cancelledCount,
      message: `Deal orchestration cancelled. ${cancelledCount} pending executions were cancelled.`
    };
  }
}

module.exports = new DealOrchestratorService();