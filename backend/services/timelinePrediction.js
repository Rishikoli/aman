const { query } = require('../utils/database');
const Deal = require('../models/Deal');
const AgentExecution = require('../models/AgentExecution');

/**
 * Timeline Prediction Engine for M&A Due Diligence
 * Implements document complexity analysis, workload estimation, and bottleneck identification
 */
class TimelinePredictionService {
  constructor() {
    // Base agent processing times (in hours) for standard complexity
    this.baseAgentDurations = {
      'finance': 2.5,
      'legal': 3.0,
      'synergy': 1.5,
      'reputation': 1.0,
      'operations': 2.0
    };

    // Complexity multipliers based on document analysis
    this.complexityMultipliers = {
      'low': 0.7,
      'medium': 1.0,
      'high': 1.5,
      'very_high': 2.2
    };

    // Agent dependencies for timeline calculation
    this.agentDependencies = {
      'finance': [],
      'legal': [],
      'synergy': ['finance'],
      'reputation': [],
      'operations': ['finance', 'legal']
    };
  }

  /**
   * Analyze document complexity to estimate processing time
   * @param {Object} documentData - Document metadata and content info
   * @returns {Object} Complexity analysis result
   */
  analyzeDocumentComplexity(documentData) {
    const analysis = {
      overall_complexity: 'medium',
      complexity_score: 0,
      factors: {},
      estimated_multiplier: 1.0
    };

    let complexityScore = 0;
    const factors = {};

    // Document volume analysis
    const totalDocuments = documentData.document_count || 0;
    const totalPages = documentData.total_pages || 0;
    const totalSizeMB = documentData.total_size_mb || 0;

    // Volume complexity scoring
    if (totalDocuments > 100) {
      factors.document_volume = 'high';
      complexityScore += 30;
    } else if (totalDocuments > 50) {
      factors.document_volume = 'medium';
      complexityScore += 15;
    } else {
      factors.document_volume = 'low';
      complexityScore += 5;
    }

    // Page count complexity
    if (totalPages > 1000) {
      factors.page_volume = 'high';
      complexityScore += 25;
    } else if (totalPages > 500) {
      factors.page_volume = 'medium';
      complexityScore += 12;
    } else {
      factors.page_volume = 'low';
      complexityScore += 3;
    }

    // File size complexity
    if (totalSizeMB > 500) {
      factors.file_size = 'high';
      complexityScore += 20;
    } else if (totalSizeMB > 100) {
      factors.file_size = 'medium';
      complexityScore += 10;
    } else {
      factors.file_size = 'low';
      complexityScore += 2;
    }

    // Data quality assessment
    const dataQuality = documentData.data_quality || 'medium';
    if (dataQuality === 'poor') {
      factors.data_quality = 'poor';
      complexityScore += 30;
    } else if (dataQuality === 'fair') {
      factors.data_quality = 'fair';
      complexityScore += 15;
    } else if (dataQuality === 'good') {
      factors.data_quality = 'good';
      complexityScore += 5;
    } else {
      factors.data_quality = 'excellent';
      complexityScore += 0;
    }

    // Determine overall complexity level
    let overallComplexity;
    let multiplier;

    if (complexityScore >= 120) {
      overallComplexity = 'very_high';
      multiplier = this.complexityMultipliers.very_high;
    } else if (complexityScore >= 80) {
      overallComplexity = 'high';
      multiplier = this.complexityMultipliers.high;
    } else if (complexityScore >= 40) {
      overallComplexity = 'medium';
      multiplier = this.complexityMultipliers.medium;
    } else {
      overallComplexity = 'low';
      multiplier = this.complexityMultipliers.low;
    }

    analysis.overall_complexity = overallComplexity;
    analysis.complexity_score = complexityScore;
    analysis.factors = factors;
    analysis.estimated_multiplier = multiplier;

    return analysis;
  }

  /**
   * Calculate timeline estimates for a deal
   * @param {string} dealId - Deal ID
   * @param {Object} documentData - Document complexity data
   * @param {Array} externalMilestones - External milestones
   * @returns {Promise<Object>} Timeline estimation result
   */
  async calculateTimeline(dealId, documentData = {}, externalMilestones = []) {
    const deal = await Deal.findById(dealId);
    if (!deal) {
      throw new Error(`Deal with ID ${dealId} not found`);
    }

    // Analyze document complexity
    const complexityAnalysis = this.analyzeDocumentComplexity(documentData);

    // Get current agent executions
    const executions = await AgentExecution.findByDealId(dealId);

    // Calculate agent-specific estimates
    const agentEstimates = this.calculateAgentEstimates(executions, complexityAnalysis);

    // Build execution phases considering dependencies
    const executionPhases = this.buildExecutionPhases(agentEstimates);

    // Calculate total timeline
    const totalEstimatedHours = this.calculateTotalDuration(executionPhases);

    // Identify bottlenecks
    const bottlenecks = this.identifyTimelineBottlenecks(agentEstimates, executionPhases);

    // Calculate confidence level
    const confidenceLevel = this.calculateConfidenceLevel(complexityAnalysis, executions);

    const timeline = {
      deal_id: dealId,
      total_estimated_hours: totalEstimatedHours,
      estimated_completion_date: this.calculateCompletionDate(totalEstimatedHours),
      complexity_analysis: complexityAnalysis,
      agent_estimates: agentEstimates,
      execution_phases: executionPhases,
      external_milestones: externalMilestones,
      bottlenecks: bottlenecks,
      confidence_level: confidenceLevel,
      last_updated: new Date()
    };

    // Store timeline in database
    await this.storeTimelineEstimate(timeline);

    return timeline;
  }

  /**
   * Calculate agent-specific time estimates
   * @param {Array} executions - Agent executions
   * @param {Object} complexityAnalysis - Document complexity analysis
   * @returns {Array} Agent estimates
   */
  calculateAgentEstimates(executions, complexityAnalysis) {
    const estimates = [];

    // Create estimates for all agent types
    Object.keys(this.baseAgentDurations).forEach(agentType => {
      const execution = executions.find(exec => exec.agent_type === agentType);
      const baseDuration = this.baseAgentDurations[agentType];
      const complexityMultiplier = complexityAnalysis.estimated_multiplier;

      // Apply agent-specific complexity adjustments
      let agentSpecificMultiplier = 1.0;
      
      if (agentType === 'legal' && complexityAnalysis.factors.document_types === 'high') {
        agentSpecificMultiplier *= 1.3;
      }
      
      if (agentType === 'finance' && complexityAnalysis.factors.data_quality === 'poor') {
        agentSpecificMultiplier *= 1.4;
      }

      const estimatedHours = baseDuration * complexityMultiplier * agentSpecificMultiplier;

      const estimate = {
        agent_type: agentType,
        base_duration_hours: baseDuration,
        complexity_multiplier: complexityMultiplier,
        agent_specific_multiplier: agentSpecificMultiplier,
        estimated_hours: Math.round(estimatedHours * 10) / 10,
        dependencies: this.agentDependencies[agentType],
        status: execution ? execution.status : 'not_started',
        actual_start_time: execution ? execution.start_time : null,
        actual_end_time: execution ? execution.end_time : null,
        actual_duration_seconds: execution ? execution.duration_seconds : null
      };

      estimates.push(estimate);
    });

    return estimates;
  }

  /**
   * Build execution phases considering dependencies
   * @param {Array} agentEstimates - Agent estimates
   * @returns {Array} Execution phases
   */
  buildExecutionPhases(agentEstimates) {
    const phases = [];
    const processed = new Set();
    let phaseNumber = 1;

    while (processed.size < agentEstimates.length) {
      const currentPhase = {
        phase: phaseNumber,
        agents: [],
        can_run_parallel: true,
        estimated_duration_hours: 0,
        dependencies_satisfied: true
      };

      // Find agents that can run in this phase
      agentEstimates.forEach(estimate => {
        if (processed.has(estimate.agent_type)) return;

        // Check if all dependencies are satisfied
        const dependenciesSatisfied = estimate.dependencies.every(dep => 
          processed.has(dep)
        );

        if (dependenciesSatisfied) {
          currentPhase.agents.push(estimate);
          processed.add(estimate.agent_type);
        }
      });

      if (currentPhase.agents.length === 0) {
        // Circular dependency or error - break to avoid infinite loop
        break;
      }

      // Calculate phase duration (max for parallel)
      if (currentPhase.can_run_parallel) {
        currentPhase.estimated_duration_hours = Math.max(
          ...currentPhase.agents.map(agent => agent.estimated_hours)
        );
      }

      phases.push(currentPhase);
      phaseNumber++;
    }

    return phases;
  }

  /**
   * Calculate total duration from execution phases
   * @param {Array} executionPhases - Execution phases
   * @returns {number} Total duration in hours
   */
  calculateTotalDuration(executionPhases) {
    return executionPhases.reduce((total, phase) => 
      total + phase.estimated_duration_hours, 0
    );
  }

  /**
   * Identify timeline bottlenecks
   * @param {Array} agentEstimates - Agent estimates
   * @param {Array} executionPhases - Execution phases
   * @returns {Array} Bottlenecks
   */
  identifyTimelineBottlenecks(agentEstimates, executionPhases) {
    const bottlenecks = [];

    // Find longest running agents in each phase
    executionPhases.forEach(phase => {
      if (phase.can_run_parallel && phase.agents.length > 1) {
        const longestAgent = phase.agents.reduce((max, agent) => 
          agent.estimated_hours > max.estimated_hours ? agent : max
        );

        if (longestAgent.estimated_hours > 3.0) { // More than 3 hours
          bottlenecks.push({
            type: 'long_running_agent',
            phase: phase.phase,
            agent_type: longestAgent.agent_type,
            estimated_hours: longestAgent.estimated_hours,
            description: `${longestAgent.agent_type} agent is the bottleneck in phase ${phase.phase}`,
            severity: longestAgent.estimated_hours > 5.0 ? 'high' : 'medium'
          });
        }
      }
    });

    return bottlenecks;
  }

  /**
   * Calculate confidence level for timeline estimate
   * @param {Object} complexityAnalysis - Complexity analysis
   * @param {Array} executions - Agent executions
   * @returns {number} Confidence level (0-100)
   */
  calculateConfidenceLevel(complexityAnalysis, executions) {
    let confidence = 80; // Base confidence

    // Adjust based on complexity
    if (complexityAnalysis.overall_complexity === 'very_high') {
      confidence -= 25;
    } else if (complexityAnalysis.overall_complexity === 'high') {
      confidence -= 15;
    } else if (complexityAnalysis.overall_complexity === 'low') {
      confidence += 10;
    }

    // Adjust based on data quality
    if (complexityAnalysis.factors.data_quality === 'poor') {
      confidence -= 20;
    } else if (complexityAnalysis.factors.data_quality === 'excellent') {
      confidence += 10;
    }

    return Math.max(10, Math.min(95, Math.round(confidence)));
  }

  /**
   * Calculate estimated completion date
   * @param {number} totalHours - Total estimated hours
   * @returns {Date} Estimated completion date
   */
  calculateCompletionDate(totalHours) {
    const now = new Date();
    const workingHoursPerDay = 8; // Assume 8-hour work days
    const workingDays = Math.ceil(totalHours / workingHoursPerDay);
    
    // Add working days (skip weekends)
    let completionDate = new Date(now);
    let addedDays = 0;
    
    while (addedDays < workingDays) {
      completionDate.setDate(completionDate.getDate() + 1);
      const dayOfWeek = completionDate.getDay();
      if (dayOfWeek !== 0 && dayOfWeek !== 6) { // Not Sunday (0) or Saturday (6)
        addedDays++;
      }
    }
    
    return completionDate;
  }

  /**
   * Store timeline estimate in database
   * @param {Object} timeline - Timeline estimate
   * @returns {Promise<void>}
   */
  async storeTimelineEstimate(timeline) {
    const sql = `
      INSERT INTO timeline_estimates (
        deal_id, total_estimated_hours, estimated_completion_date,
        complexity_analysis, agent_estimates, execution_phases,
        external_milestones, bottlenecks, confidence_level, created_at
      ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
      ON CONFLICT (deal_id) DO UPDATE SET
        total_estimated_hours = EXCLUDED.total_estimated_hours,
        estimated_completion_date = EXCLUDED.estimated_completion_date,
        complexity_analysis = EXCLUDED.complexity_analysis,
        agent_estimates = EXCLUDED.agent_estimates,
        execution_phases = EXCLUDED.execution_phases,
        external_milestones = EXCLUDED.external_milestones,
        bottlenecks = EXCLUDED.bottlenecks,
        confidence_level = EXCLUDED.confidence_level,
        updated_at = CURRENT_TIMESTAMP
    `;

    const values = [
      timeline.deal_id,
      timeline.total_estimated_hours,
      timeline.estimated_completion_date,
      JSON.stringify(timeline.complexity_analysis),
      JSON.stringify(timeline.agent_estimates),
      JSON.stringify(timeline.execution_phases),
      JSON.stringify(timeline.external_milestones),
      JSON.stringify(timeline.bottlenecks),
      timeline.confidence_level,
      timeline.last_updated
    ];

    await query(sql, values);
  }

  /**
   * Update timeline with real-time progress
   * @param {string} dealId - Deal ID
   * @returns {Promise<Object>} Updated timeline
   */
  async updateTimelineProgress(dealId) {
    const deal = await Deal.findById(dealId);
    if (!deal) {
      throw new Error(`Deal with ID ${dealId} not found`);
    }

    // Get current executions
    const executions = await AgentExecution.findByDealId(dealId);

    // Get stored timeline estimate
    const storedTimeline = await this.getStoredTimelineEstimate(dealId);
    if (!storedTimeline) {
      throw new Error(`No timeline estimate found for deal ${dealId}`);
    }

    // Identify current bottlenecks
    const currentBottlenecks = this.identifyCurrentBottlenecks(executions, storedTimeline.agent_estimates);

    const updatedTimeline = {
      ...storedTimeline,
      current_bottlenecks: currentBottlenecks,
      overall_progress: this.calculateOverallProgress(storedTimeline.agent_estimates),
      last_updated: new Date()
    };

    return updatedTimeline;
  }

  /**
   * Identify current bottlenecks based on real-time status
   * @param {Array} executions - Current agent executions
   * @param {Array} agentEstimates - Agent estimates
   * @returns {Array} Current bottlenecks
   */
  identifyCurrentBottlenecks(executions, agentEstimates) {
    const bottlenecks = [];

    // Check for failed agents
    const failedExecutions = executions.filter(exec => exec.status === 'failed');
    if (failedExecutions.length > 0) {
      bottlenecks.push({
        type: 'failed_agents',
        agents: failedExecutions.map(exec => exec.agent_type),
        count: failedExecutions.length,
        severity: 'high',
        description: `${failedExecutions.length} agent(s) have failed and need attention`
      });
    }

    return bottlenecks;
  }

  /**
   * Calculate overall progress percentage
   * @param {Array} agentEstimates - Agent estimates
   * @returns {number} Overall progress percentage
   */
  calculateOverallProgress(agentEstimates) {
    if (agentEstimates.length === 0) return 0;

    const totalProgress = agentEstimates.reduce((sum, estimate) => {
      if (estimate.status === 'completed') return sum + 100;
      if (estimate.status === 'running') return sum + (estimate.progress_percentage || 0);
      return sum;
    }, 0);

    return Math.round(totalProgress / agentEstimates.length);
  }

  /**
   * Get stored timeline estimate
   * @param {string} dealId - Deal ID
   * @returns {Promise<Object|null>} Stored timeline estimate
   */
  async getStoredTimelineEstimate(dealId) {
    const sql = `
      SELECT * FROM timeline_estimates 
      WHERE deal_id = $1 
      ORDER BY updated_at DESC 
      LIMIT 1
    `;
    
    const result = await query(sql, [dealId]);
    if (result.rows.length === 0) {
      return null;
    }

    const row = result.rows[0];
    return {
      deal_id: row.deal_id,
      total_estimated_hours: row.total_estimated_hours,
      estimated_completion_date: row.estimated_completion_date,
      complexity_analysis: JSON.parse(row.complexity_analysis),
      agent_estimates: JSON.parse(row.agent_estimates),
      execution_phases: JSON.parse(row.execution_phases),
      external_milestones: JSON.parse(row.external_milestones || '[]'),
      bottlenecks: JSON.parse(row.bottlenecks || '[]'),
      confidence_level: row.confidence_level,
      last_updated: row.updated_at
    };
  }

  /**
   * Get timeline history for a deal
   * @param {string} dealId - Deal ID
   * @returns {Promise<Array>} Timeline history
   */
  async getTimelineHistory(dealId) {
    const sql = `
      SELECT 
        total_estimated_hours,
        estimated_completion_date,
        confidence_level,
        created_at,
        updated_at
      FROM timeline_estimates 
      WHERE deal_id = $1 
      ORDER BY created_at ASC
    `;
    
    const result = await query(sql, [dealId]);
    return result.rows;
  }
}

module.exports = new TimelinePredictionService();