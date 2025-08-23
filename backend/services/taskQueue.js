const Queue = require('bull');
const Redis = require('ioredis');
const AgentExecution = require('../models/AgentExecution');
const { query } = require('../utils/database');

class TaskQueueService {
  constructor() {
    // Redis connection configuration
    this.redisConfig = {
      host: process.env.REDIS_HOST || 'localhost',
      port: process.env.REDIS_PORT || 6379,
      password: process.env.REDIS_PASSWORD || undefined,
      db: process.env.REDIS_DB || 0,
      retryDelayOnFailover: 100,
      enableReadyCheck: false,
      maxRetriesPerRequest: null,
    };

    // Initialize Redis client for direct operations
    this.redis = new Redis(this.redisConfig);

    // Initialize Bull queues for different agent types
    this.queues = {};
    this.agentTypes = ['finance', 'legal', 'synergy', 'reputation', 'operations'];
    
    this.initializeQueues();
    this.setupQueueProcessors();
    this.setupQueueEvents();
  }

  /**
   * Initialize Bull queues for each agent type
   */
  initializeQueues() {
    // Main orchestration queue
    this.orchestrationQueue = new Queue('orchestration', {
      redis: this.redisConfig,
      defaultJobOptions: {
        removeOnComplete: 10,
        removeOnFail: 5,
        attempts: 3,
        backoff: {
          type: 'exponential',
          delay: 2000,
        },
      },
    });

    // Agent-specific queues
    this.agentTypes.forEach(agentType => {
      this.queues[agentType] = new Queue(`agent-${agentType}`, {
        redis: this.redisConfig,
        defaultJobOptions: {
          removeOnComplete: 10,
          removeOnFail: 5,
          attempts: 2,
          backoff: {
            type: 'exponential',
            delay: 1000,
          },
        },
      });
    });

    // Timeline update queue
    this.timelineQueue = new Queue('timeline-updates', {
      redis: this.redisConfig,
      defaultJobOptions: {
        removeOnComplete: 20,
        removeOnFail: 10,
        attempts: 1,
      },
    });

    console.log('Task queues initialized successfully');
  }

  /**
   * Set up queue processors
   */
  setupQueueProcessors() {
    // Orchestration queue processor
    this.orchestrationQueue.process('distribute-tasks', async (job) => {
      return await this.processTaskDistribution(job.data);
    });

    this.orchestrationQueue.process('check-dependencies', async (job) => {
      return await this.processDependencyCheck(job.data);
    });

    // Agent queue processors
    this.agentTypes.forEach(agentType => {
      this.queues[agentType].process('execute-analysis', async (job) => {
        return await this.processAgentExecution(agentType, job.data);
      });
    });

    // Timeline queue processor
    this.timelineQueue.process('update-timeline', async (job) => {
      return await this.processTimelineUpdate(job.data);
    });

    console.log('Queue processors set up successfully');
  }

  /**
   * Set up queue event handlers
   */
  setupQueueEvents() {
    // Orchestration queue events
    this.orchestrationQueue.on('completed', (job, result) => {
      console.log(`Orchestration job ${job.id} completed:`, result);
    });

    this.orchestrationQueue.on('failed', (job, err) => {
      console.error(`Orchestration job ${job.id} failed:`, err.message);
    });

    // Agent queue events
    this.agentTypes.forEach(agentType => {
      const queue = this.queues[agentType];
      
      queue.on('completed', async (job, result) => {
        console.log(`${agentType} agent job ${job.id} completed`);
        await this.handleAgentCompletion(agentType, job.data, result);
      });

      queue.on('failed', async (job, err) => {
        console.error(`${agentType} agent job ${job.id} failed:`, err.message);
        await this.handleAgentFailure(agentType, job.data, err);
      });

      queue.on('progress', async (job, progress) => {
        await this.updateAgentProgress(job.data.executionId, progress);
      });
    });

    console.log('Queue event handlers set up successfully');
  }

  /**
   * Distribute tasks for a deal
   * @param {string} dealId - Deal ID
   * @returns {Promise<Object>} Distribution result
   */
  async distributeTasks(dealId) {
    try {
      // Add orchestration job to distribute tasks
      const job = await this.orchestrationQueue.add('distribute-tasks', {
        dealId,
        timestamp: new Date(),
      }, {
        priority: 10,
        delay: 0,
      });

      console.log(`Task distribution job ${job.id} queued for deal ${dealId}`);
      
      return {
        success: true,
        jobId: job.id,
        dealId,
        message: 'Task distribution initiated'
      };
    } catch (error) {
      console.error('Error distributing tasks:', error);
      throw error;
    }
  }

  /**
   * Process task distribution
   * @param {Object} data - Job data
   * @returns {Promise<Object>} Processing result
   */
  async processTaskDistribution(data) {
    const { dealId } = data;
    
    try {
      // Get all agent executions for the deal
      const executions = await AgentExecution.findByDealId(dealId);
      
      if (!executions || executions.length === 0) {
        throw new Error(`No agent executions found for deal ${dealId}`);
      }

      // Separate executions by dependency requirements
      const independentExecutions = executions.filter(exec => 
        this.getAgentDependencies(exec.agent_type).length === 0
      );
      
      const dependentExecutions = executions.filter(exec => 
        this.getAgentDependencies(exec.agent_type).length > 0
      );

      // Queue independent agents immediately
      const queuedJobs = [];
      for (const execution of independentExecutions) {
        if (execution.status === 'pending') {
          const job = await this.queueAgentTask(execution);
          queuedJobs.push(job);
        }
      }

      // Schedule dependency checks for dependent agents
      if (dependentExecutions.length > 0) {
        await this.orchestrationQueue.add('check-dependencies', {
          dealId,
          dependentExecutions: dependentExecutions.map(exec => exec.id),
        }, {
          delay: 5000, // Check dependencies in 5 seconds
          repeat: { every: 10000 }, // Repeat every 10 seconds
        });
      }

      // Update timeline
      await this.timelineQueue.add('update-timeline', {
        dealId,
        event: 'tasks_distributed',
        queuedAgents: queuedJobs.length,
      });

      return {
        success: true,
        dealId,
        queuedAgents: queuedJobs.length,
        pendingDependencies: dependentExecutions.length,
        jobs: queuedJobs.map(job => ({
          jobId: job.id,
          agentType: job.data.agentType,
          priority: job.opts.priority,
        })),
      };
    } catch (error) {
      console.error('Error processing task distribution:', error);
      throw error;
    }
  }

  /**
   * Process dependency checks
   * @param {Object} data - Job data
   * @returns {Promise<Object>} Processing result
   */
  async processDependencyCheck(data) {
    const { dealId, dependentExecutions } = data;
    
    try {
      const readyExecutions = [];
      
      for (const executionId of dependentExecutions) {
        const execution = await AgentExecution.findById(executionId);
        
        if (!execution || execution.status !== 'pending') {
          continue;
        }

        // Check if all dependencies are completed
        const dependencies = this.getAgentDependencies(execution.agent_type);
        const dependencyStatuses = await this.checkDependencyStatuses(dealId, dependencies);
        
        const allDependenciesCompleted = dependencyStatuses.every(status => 
          status.status === 'completed'
        );

        if (allDependenciesCompleted) {
          // Queue the agent task
          const job = await this.queueAgentTask(execution);
          readyExecutions.push({
            executionId: execution.id,
            agentType: execution.agent_type,
            jobId: job.id,
          });
        }
      }

      // Check if all agents are queued or completed
      const allExecutions = await AgentExecution.findByDealId(dealId);
      const pendingCount = allExecutions.filter(exec => exec.status === 'pending').length;
      
      if (pendingCount === 0) {
        // Remove the recurring dependency check job
        const jobs = await this.orchestrationQueue.getRepeatableJobs();
        const dependencyCheckJobs = jobs.filter(job => 
          job.name === 'check-dependencies' && 
          job.data && 
          job.data.dealId === dealId
        );
        
        for (const job of dependencyCheckJobs) {
          await this.orchestrationQueue.removeRepeatableByKey(job.key);
        }
      }

      return {
        success: true,
        dealId,
        readyExecutions,
        remainingPending: pendingCount,
      };
    } catch (error) {
      console.error('Error processing dependency check:', error);
      throw error;
    }
  }

  /**
   * Queue an agent task
   * @param {AgentExecution} execution - Agent execution record
   * @returns {Promise<Object>} Queued job
   */
  async queueAgentTask(execution) {
    const agentType = execution.agent_type;
    const queue = this.queues[agentType];
    
    if (!queue) {
      throw new Error(`No queue found for agent type: ${agentType}`);
    }

    // Update execution status to queued
    execution.status = 'queued';
    execution.queued_at = new Date();
    await execution.update();

    // Add job to agent queue
    const job = await queue.add('execute-analysis', {
      executionId: execution.id,
      dealId: execution.deal_id,
      agentType: execution.agent_type,
      inputData: execution.input_data,
    }, {
      priority: this.getAgentPriority(agentType),
      attempts: 2,
    });

    console.log(`Queued ${agentType} agent task for deal ${execution.deal_id}, job ID: ${job.id}`);
    
    return job;
  }

  /**
   * Process agent execution (placeholder - actual agent logic would be implemented separately)
   * @param {string} agentType - Agent type
   * @param {Object} data - Job data
   * @returns {Promise<Object>} Execution result
   */
  async processAgentExecution(agentType, data) {
    const { executionId, dealId, inputData } = data;
    
    try {
      // Update execution status to running
      const execution = await AgentExecution.findById(executionId);
      if (!execution) {
        throw new Error(`Agent execution ${executionId} not found`);
      }

      execution.status = 'running';
      execution.start_time = new Date();
      await execution.update();

      // Simulate agent processing (in real implementation, this would call actual agent services)
      console.log(`Starting ${agentType} agent execution for deal ${dealId}`);
      
      // Update progress periodically
      const progressUpdates = [25, 50, 75, 90];
      for (let i = 0; i < progressUpdates.length; i++) {
        await new Promise(resolve => setTimeout(resolve, 1000)); // Simulate work
        await this.updateAgentProgress(executionId, progressUpdates[i]);
      }

      // Simulate completion
      const result = {
        executionId,
        agentType,
        dealId,
        findings: [`Sample ${agentType} finding 1`, `Sample ${agentType} finding 2`],
        riskScore: Math.floor(Math.random() * 100),
        confidence: 0.85,
        processingTime: 2.5,
        status: 'completed',
      };

      return result;
    } catch (error) {
      console.error(`Error in ${agentType} agent execution:`, error);
      throw error;
    }
  }

  /**
   * Handle agent completion
   * @param {string} agentType - Agent type
   * @param {Object} jobData - Job data
   * @param {Object} result - Execution result
   */
  async handleAgentCompletion(agentType, jobData, result) {
    const { executionId, dealId } = jobData;
    
    try {
      // Update execution record
      const execution = await AgentExecution.findById(executionId);
      if (execution) {
        execution.status = 'completed';
        execution.end_time = new Date();
        execution.progress_percentage = 100;
        execution.output_data = result;
        execution.duration_seconds = execution.end_time - execution.start_time;
        await execution.update();
      }

      // Update timeline
      await this.timelineQueue.add('update-timeline', {
        dealId,
        event: 'agent_completed',
        agentType,
        executionId,
        result,
      });

      // Check if this completion unblocks other agents
      await this.orchestrationQueue.add('check-dependencies', {
        dealId,
        dependentExecutions: await this.getDependentExecutions(dealId, agentType),
      });

      console.log(`${agentType} agent completed for deal ${dealId}`);
    } catch (error) {
      console.error('Error handling agent completion:', error);
    }
  }

  /**
   * Handle agent failure
   * @param {string} agentType - Agent type
   * @param {Object} jobData - Job data
   * @param {Error} error - Failure error
   */
  async handleAgentFailure(agentType, jobData, error) {
    const { executionId, dealId } = jobData;
    
    try {
      // Update execution record
      const execution = await AgentExecution.findById(executionId);
      if (execution) {
        execution.status = 'failed';
        execution.end_time = new Date();
        execution.error_message = error.message;
        execution.duration_seconds = execution.end_time - execution.start_time;
        await execution.update();
      }

      // Update timeline
      await this.timelineQueue.add('update-timeline', {
        dealId,
        event: 'agent_failed',
        agentType,
        executionId,
        error: error.message,
      });

      console.error(`${agentType} agent failed for deal ${dealId}:`, error.message);
    } catch (updateError) {
      console.error('Error handling agent failure:', updateError);
    }
  }

  /**
   * Update agent progress
   * @param {string} executionId - Execution ID
   * @param {number} progress - Progress percentage
   */
  async updateAgentProgress(executionId, progress) {
    try {
      const execution = await AgentExecution.findById(executionId);
      if (execution) {
        execution.progress_percentage = progress;
        await execution.update();
      }
    } catch (error) {
      console.error('Error updating agent progress:', error);
    }
  }

  /**
   * Process timeline updates
   * @param {Object} data - Timeline update data
   * @returns {Promise<Object>} Update result
   */
  async processTimelineUpdate(data) {
    const { dealId, event, ...eventData } = data;
    
    try {
      // Store timeline event in database
      const sql = `
        INSERT INTO timeline_events (deal_id, event_type, event_data, created_at)
        VALUES ($1, $2, $3, $4)
        RETURNING id
      `;
      
      const result = await query(sql, [
        dealId,
        event,
        JSON.stringify(eventData),
        new Date(),
      ]);

      console.log(`Timeline updated for deal ${dealId}: ${event}`);
      
      return {
        success: true,
        eventId: result.rows[0].id,
        dealId,
        event,
      };
    } catch (error) {
      console.error('Error updating timeline:', error);
      throw error;
    }
  }

  /**
   * Get agent dependencies
   * @param {string} agentType - Agent type
   * @returns {Array} Array of dependency agent types
   */
  getAgentDependencies(agentType) {
    const dependencies = {
      'finance': [],
      'legal': [],
      'synergy': ['finance'],
      'reputation': [],
      'operations': ['finance', 'legal']
    };
    
    return dependencies[agentType] || [];
  }

  /**
   * Get agent priority for queue processing
   * @param {string} agentType - Agent type
   * @returns {number} Priority value (higher = more priority)
   */
  getAgentPriority(agentType) {
    const priorities = {
      'finance': 10,
      'legal': 9,
      'reputation': 8,
      'synergy': 7,
      'operations': 6
    };
    
    return priorities[agentType] || 5;
  }

  /**
   * Check dependency statuses
   * @param {string} dealId - Deal ID
   * @param {Array} dependencies - Dependency agent types
   * @returns {Promise<Array>} Dependency statuses
   */
  async checkDependencyStatuses(dealId, dependencies) {
    const statuses = [];
    
    for (const depType of dependencies) {
      const execution = await AgentExecution.findByDealIdAndType(dealId, depType);
      statuses.push({
        agentType: depType,
        status: execution ? execution.status : 'not_found',
        executionId: execution ? execution.id : null,
      });
    }
    
    return statuses;
  }

  /**
   * Get executions that depend on a specific agent type
   * @param {string} dealId - Deal ID
   * @param {string} completedAgentType - Completed agent type
   * @returns {Promise<Array>} Array of dependent execution IDs
   */
  async getDependentExecutions(dealId, completedAgentType) {
    const allExecutions = await AgentExecution.findByDealId(dealId);
    
    return allExecutions
      .filter(exec => {
        const dependencies = this.getAgentDependencies(exec.agent_type);
        return dependencies.includes(completedAgentType) && exec.status === 'pending';
      })
      .map(exec => exec.id);
  }

  /**
   * Get queue statistics
   * @returns {Promise<Object>} Queue statistics
   */
  async getQueueStats() {
    const stats = {
      orchestration: await this.getQueueInfo(this.orchestrationQueue),
      timeline: await this.getQueueInfo(this.timelineQueue),
      agents: {},
    };

    for (const agentType of this.agentTypes) {
      stats.agents[agentType] = await this.getQueueInfo(this.queues[agentType]);
    }

    return stats;
  }

  /**
   * Get queue information
   * @param {Queue} queue - Bull queue instance
   * @returns {Promise<Object>} Queue information
   */
  async getQueueInfo(queue) {
    const [waiting, active, completed, failed, delayed] = await Promise.all([
      queue.getWaiting(),
      queue.getActive(),
      queue.getCompleted(),
      queue.getFailed(),
      queue.getDelayed(),
    ]);

    return {
      name: queue.name,
      waiting: waiting.length,
      active: active.length,
      completed: completed.length,
      failed: failed.length,
      delayed: delayed.length,
    };
  }

  /**
   * Retry failed jobs for a deal
   * @param {string} dealId - Deal ID
   * @returns {Promise<Object>} Retry result
   */
  async retryFailedJobs(dealId) {
    const failedExecutions = await AgentExecution.findByDealIdAndStatus(dealId, 'failed');
    const retriedJobs = [];

    for (const execution of failedExecutions) {
      // Reset execution status
      execution.status = 'pending';
      execution.error_message = null;
      execution.start_time = null;
      execution.end_time = null;
      execution.progress_percentage = 0;
      await execution.update();

      // Re-queue the job
      const job = await this.queueAgentTask(execution);
      retriedJobs.push({
        executionId: execution.id,
        agentType: execution.agent_type,
        jobId: job.id,
      });
    }

    return {
      success: true,
      dealId,
      retriedJobs: retriedJobs.length,
      jobs: retriedJobs,
    };
  }

  /**
   * Cancel all jobs for a deal
   * @param {string} dealId - Deal ID
   * @returns {Promise<Object>} Cancellation result
   */
  async cancelDealJobs(dealId) {
    let cancelledCount = 0;

    // Cancel jobs in all queues
    const allQueues = [
      this.orchestrationQueue,
      this.timelineQueue,
      ...Object.values(this.queues),
    ];

    for (const queue of allQueues) {
      const jobs = await queue.getJobs(['waiting', 'active', 'delayed']);
      
      for (const job of jobs) {
        if (job.data && job.data.dealId === dealId) {
          await job.remove();
          cancelledCount++;
        }
      }
    }

    // Update execution statuses
    await AgentExecution.cancelPendingExecutions(dealId);

    return {
      success: true,
      dealId,
      cancelledJobs: cancelledCount,
    };
  }

  /**
   * Clean up completed and failed jobs
   * @returns {Promise<Object>} Cleanup result
   */
  async cleanupJobs() {
    let cleanedCount = 0;

    const allQueues = [
      this.orchestrationQueue,
      this.timelineQueue,
      ...Object.values(this.queues),
    ];

    for (const queue of allQueues) {
      await queue.clean(24 * 60 * 60 * 1000, 'completed'); // Clean completed jobs older than 24 hours
      await queue.clean(7 * 24 * 60 * 60 * 1000, 'failed'); // Clean failed jobs older than 7 days
      cleanedCount++;
    }

    return {
      success: true,
      cleanedQueues: cleanedCount,
    };
  }

  /**
   * Gracefully close all queues and Redis connections
   */
  async close() {
    console.log('Closing task queue service...');

    // Close all queues
    const allQueues = [
      this.orchestrationQueue,
      this.timelineQueue,
      ...Object.values(this.queues),
    ];

    await Promise.all(allQueues.map(queue => queue.close()));

    // Close Redis connection
    await this.redis.disconnect();

    console.log('Task queue service closed successfully');
  }
}

module.exports = new TaskQueueService();