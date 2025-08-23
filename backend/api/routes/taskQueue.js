const express = require('express');
const router = express.Router();
const taskQueue = require('../../services/taskQueue');
const AgentExecution = require('../../models/AgentExecution');

/**
 * @route GET /api/task-queue/stats
 * @desc Get task queue statistics
 * @access Public
 */
router.get('/stats', async (req, res) => {
  try {
    const stats = await taskQueue.getQueueStats();
    
    res.json({
      success: true,
      data: stats,
      timestamp: new Date()
    });
  } catch (error) {
    console.error('Error getting queue stats:', error);
    res.status(500).json({
      success: false,
      message: 'Failed to get queue statistics',
      error: error.message
    });
  }
});

/**
 * @route POST /api/task-queue/distribute/:dealId
 * @desc Distribute tasks for a specific deal
 * @access Public
 */
router.post('/distribute/:dealId', async (req, res) => {
  try {
    const { dealId } = req.params;
    
    const result = await taskQueue.distributeTasks(dealId);
    
    res.json({
      success: true,
      data: result,
      message: 'Tasks distributed successfully'
    });
  } catch (error) {
    console.error('Error distributing tasks:', error);
    res.status(500).json({
      success: false,
      message: 'Failed to distribute tasks',
      error: error.message
    });
  }
});

/**
 * @route POST /api/task-queue/retry/:dealId
 * @desc Retry failed jobs for a specific deal
 * @access Public
 */
router.post('/retry/:dealId', async (req, res) => {
  try {
    const { dealId } = req.params;
    
    const result = await taskQueue.retryFailedJobs(dealId);
    
    res.json({
      success: true,
      data: result,
      message: `Retried ${result.retriedJobs} failed jobs`
    });
  } catch (error) {
    console.error('Error retrying failed jobs:', error);
    res.status(500).json({
      success: false,
      message: 'Failed to retry failed jobs',
      error: error.message
    });
  }
});

/**
 * @route DELETE /api/task-queue/cancel/:dealId
 * @desc Cancel all jobs for a specific deal
 * @access Public
 */
router.delete('/cancel/:dealId', async (req, res) => {
  try {
    const { dealId } = req.params;
    
    const result = await taskQueue.cancelDealJobs(dealId);
    
    res.json({
      success: true,
      data: result,
      message: `Cancelled ${result.cancelledJobs} jobs`
    });
  } catch (error) {
    console.error('Error cancelling jobs:', error);
    res.status(500).json({
      success: false,
      message: 'Failed to cancel jobs',
      error: error.message
    });
  }
});

/**
 * @route GET /api/task-queue/executions/:dealId
 * @desc Get agent execution status for a deal
 * @access Public
 */
router.get('/executions/:dealId', async (req, res) => {
  try {
    const { dealId } = req.params;
    
    const executions = await AgentExecution.findByDealId(dealId);
    const executionHistory = await AgentExecution.getExecutionHistory(dealId);
    
    // Calculate queue-specific metrics
    const queueMetrics = {
      total_executions: executions.length,
      pending: executions.filter(e => e.status === 'pending').length,
      queued: executions.filter(e => e.status === 'queued').length,
      running: executions.filter(e => e.status === 'running').length,
      completed: executions.filter(e => e.status === 'completed').length,
      failed: executions.filter(e => e.status === 'failed').length,
      cancelled: executions.filter(e => e.status === 'cancelled').length,
    };
    
    // Calculate progress
    const overallProgress = queueMetrics.total_executions > 0 
      ? (queueMetrics.completed / queueMetrics.total_executions) * 100 
      : 0;
    
    res.json({
      success: true,
      data: {
        executions: executions.map(exec => ({
          id: exec.id,
          agent_type: exec.agent_type,
          status: exec.status,
          progress_percentage: exec.progress_percentage,
          queued_at: exec.queued_at,
          start_time: exec.start_time,
          end_time: exec.end_time,
          duration_seconds: exec.duration_seconds,
          error_message: exec.error_message,
          created_at: exec.created_at,
          updated_at: exec.updated_at
        })),
        metrics: queueMetrics,
        progress: {
          overall_percentage: Math.round(overallProgress),
          completed_agents: queueMetrics.completed,
          total_agents: queueMetrics.total_executions
        },
        timeline: executionHistory.timeline
      }
    });
  } catch (error) {
    console.error('Error getting execution status:', error);
    res.status(500).json({
      success: false,
      message: 'Failed to get execution status',
      error: error.message
    });
  }
});

/**
 * @route GET /api/task-queue/active-executions
 * @desc Get all active executions across all deals
 * @access Public
 */
router.get('/active-executions', async (req, res) => {
  try {
    const activeExecutions = await AgentExecution.getActiveExecutions();
    
    // Group by deal
    const executionsByDeal = activeExecutions.reduce((acc, exec) => {
      if (!acc[exec.deal_id]) {
        acc[exec.deal_id] = [];
      }
      acc[exec.deal_id].push(exec);
      return acc;
    }, {});
    
    res.json({
      success: true,
      data: {
        total_active: activeExecutions.length,
        executions_by_deal: executionsByDeal,
        executions: activeExecutions.map(exec => ({
          id: exec.id,
          deal_id: exec.deal_id,
          agent_type: exec.agent_type,
          status: exec.status,
          progress_percentage: exec.progress_percentage,
          queued_at: exec.queued_at,
          start_time: exec.start_time,
          created_at: exec.created_at
        }))
      }
    });
  } catch (error) {
    console.error('Error getting active executions:', error);
    res.status(500).json({
      success: false,
      message: 'Failed to get active executions',
      error: error.message
    });
  }
});

/**
 * @route POST /api/task-queue/cleanup
 * @desc Clean up old completed and failed jobs
 * @access Public
 */
router.post('/cleanup', async (req, res) => {
  try {
    const result = await taskQueue.cleanupJobs();
    
    res.json({
      success: true,
      data: result,
      message: 'Job cleanup completed successfully'
    });
  } catch (error) {
    console.error('Error cleaning up jobs:', error);
    res.status(500).json({
      success: false,
      message: 'Failed to clean up jobs',
      error: error.message
    });
  }
});

/**
 * @route GET /api/task-queue/health
 * @desc Check task queue system health
 * @access Public
 */
router.get('/health', async (req, res) => {
  try {
    const stats = await taskQueue.getQueueStats();
    
    // Simple health check - if we can get stats, the system is healthy
    const isHealthy = stats && typeof stats === 'object';
    
    res.json({
      success: true,
      healthy: isHealthy,
      data: {
        redis_connected: isHealthy,
        queues_operational: isHealthy,
        timestamp: new Date(),
        stats: isHealthy ? stats : null
      }
    });
  } catch (error) {
    console.error('Task queue health check failed:', error);
    res.status(503).json({
      success: false,
      healthy: false,
      message: 'Task queue system is unhealthy',
      error: error.message
    });
  }
});

module.exports = router;