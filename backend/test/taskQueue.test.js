const request = require('supertest');
const express = require('express');
const taskQueueRoutes = require('../api/routes/taskQueue');

// Mock the task queue service
jest.mock('../services/taskQueue', () => ({
  getQueueStats: jest.fn(),
  distributeTasks: jest.fn(),
  retryFailedJobs: jest.fn(),
  cancelDealJobs: jest.fn(),
  cleanupJobs: jest.fn(),
}));

// Mock the AgentExecution model
jest.mock('../models/AgentExecution', () => ({
  findByDealId: jest.fn(),
  getExecutionHistory: jest.fn(),
  getActiveExecutions: jest.fn(),
}));

const taskQueue = require('../services/taskQueue');
const AgentExecution = require('../models/AgentExecution');

describe('Task Queue API Routes', () => {
  let app;

  beforeEach(() => {
    app = express();
    app.use(express.json());
    app.use('/api/task-queue', taskQueueRoutes);
    
    // Clear all mocks
    jest.clearAllMocks();
  });

  describe('GET /api/task-queue/stats', () => {
    it('should return queue statistics', async () => {
      const mockStats = {
        orchestration: { waiting: 0, active: 1, completed: 5, failed: 0 },
        agents: {
          finance: { waiting: 2, active: 0, completed: 3, failed: 1 },
          legal: { waiting: 1, active: 1, completed: 2, failed: 0 }
        }
      };

      taskQueue.getQueueStats.mockResolvedValue(mockStats);

      const response = await request(app)
        .get('/api/task-queue/stats')
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.data).toEqual(mockStats);
      expect(taskQueue.getQueueStats).toHaveBeenCalledTimes(1);
    });

    it('should handle errors when getting queue stats', async () => {
      taskQueue.getQueueStats.mockRejectedValue(new Error('Redis connection failed'));

      const response = await request(app)
        .get('/api/task-queue/stats')
        .expect(500);

      expect(response.body.success).toBe(false);
      expect(response.body.message).toBe('Failed to get queue statistics');
    });
  });

  describe('POST /api/task-queue/distribute/:dealId', () => {
    it('should distribute tasks for a deal', async () => {
      const dealId = 'test-deal-123';
      const mockResult = {
        success: true,
        jobId: 'job-456',
        dealId,
        message: 'Task distribution initiated'
      };

      taskQueue.distributeTasks.mockResolvedValue(mockResult);

      const response = await request(app)
        .post(`/api/task-queue/distribute/${dealId}`)
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.data).toEqual(mockResult);
      expect(taskQueue.distributeTasks).toHaveBeenCalledWith(dealId);
    });

    it('should handle errors when distributing tasks', async () => {
      const dealId = 'test-deal-123';
      taskQueue.distributeTasks.mockRejectedValue(new Error('Deal not found'));

      const response = await request(app)
        .post(`/api/task-queue/distribute/${dealId}`)
        .expect(500);

      expect(response.body.success).toBe(false);
      expect(response.body.message).toBe('Failed to distribute tasks');
    });
  });

  describe('POST /api/task-queue/retry/:dealId', () => {
    it('should retry failed jobs for a deal', async () => {
      const dealId = 'test-deal-123';
      const mockResult = {
        success: true,
        dealId,
        retriedJobs: 2,
        jobs: [
          { executionId: 'exec-1', agentType: 'finance', jobId: 'job-1' },
          { executionId: 'exec-2', agentType: 'legal', jobId: 'job-2' }
        ]
      };

      taskQueue.retryFailedJobs.mockResolvedValue(mockResult);

      const response = await request(app)
        .post(`/api/task-queue/retry/${dealId}`)
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.data).toEqual(mockResult);
      expect(taskQueue.retryFailedJobs).toHaveBeenCalledWith(dealId);
    });
  });

  describe('DELETE /api/task-queue/cancel/:dealId', () => {
    it('should cancel all jobs for a deal', async () => {
      const dealId = 'test-deal-123';
      const mockResult = {
        success: true,
        dealId,
        cancelledJobs: 3
      };

      taskQueue.cancelDealJobs.mockResolvedValue(mockResult);

      const response = await request(app)
        .delete(`/api/task-queue/cancel/${dealId}`)
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.data).toEqual(mockResult);
      expect(taskQueue.cancelDealJobs).toHaveBeenCalledWith(dealId);
    });
  });

  describe('GET /api/task-queue/executions/:dealId', () => {
    it('should return execution status for a deal', async () => {
      const dealId = 'test-deal-123';
      const mockExecutions = [
        {
          id: 'exec-1',
          agent_type: 'finance',
          status: 'completed',
          progress_percentage: 100,
          queued_at: new Date(),
          start_time: new Date(),
          end_time: new Date(),
          duration_seconds: 120,
          error_message: null,
          created_at: new Date(),
          updated_at: new Date()
        },
        {
          id: 'exec-2',
          agent_type: 'legal',
          status: 'running',
          progress_percentage: 75,
          queued_at: new Date(),
          start_time: new Date(),
          end_time: null,
          duration_seconds: null,
          error_message: null,
          created_at: new Date(),
          updated_at: new Date()
        }
      ];

      const mockHistory = {
        timeline: {
          total_executions: 2,
          completed_executions: 1,
          failed_executions: 0,
          total_duration_seconds: 120,
          avg_duration_seconds: 120
        }
      };

      AgentExecution.findByDealId.mockResolvedValue(mockExecutions);
      AgentExecution.getExecutionHistory.mockResolvedValue(mockHistory);

      const response = await request(app)
        .get(`/api/task-queue/executions/${dealId}`)
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.data.executions).toHaveLength(2);
      expect(response.body.data.metrics.total_executions).toBe(2);
      expect(response.body.data.metrics.completed).toBe(1);
      expect(response.body.data.metrics.running).toBe(1);
      expect(response.body.data.progress.overall_percentage).toBe(50);
    });
  });

  describe('GET /api/task-queue/active-executions', () => {
    it('should return all active executions', async () => {
      const mockActiveExecutions = [
        {
          id: 'exec-1',
          deal_id: 'deal-1',
          agent_type: 'finance',
          status: 'running',
          progress_percentage: 50,
          queued_at: new Date(),
          start_time: new Date(),
          created_at: new Date()
        },
        {
          id: 'exec-2',
          deal_id: 'deal-2',
          agent_type: 'legal',
          status: 'pending',
          progress_percentage: 0,
          queued_at: null,
          start_time: null,
          created_at: new Date()
        }
      ];

      AgentExecution.getActiveExecutions.mockResolvedValue(mockActiveExecutions);

      const response = await request(app)
        .get('/api/task-queue/active-executions')
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.data.total_active).toBe(2);
      expect(response.body.data.executions).toHaveLength(2);
      expect(response.body.data.executions_by_deal).toHaveProperty('deal-1');
      expect(response.body.data.executions_by_deal).toHaveProperty('deal-2');
    });
  });

  describe('POST /api/task-queue/cleanup', () => {
    it('should clean up old jobs', async () => {
      const mockResult = {
        success: true,
        cleanedQueues: 7
      };

      taskQueue.cleanupJobs.mockResolvedValue(mockResult);

      const response = await request(app)
        .post('/api/task-queue/cleanup')
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.data).toEqual(mockResult);
      expect(taskQueue.cleanupJobs).toHaveBeenCalledTimes(1);
    });
  });

  describe('GET /api/task-queue/health', () => {
    it('should return healthy status when queue system is operational', async () => {
      const mockStats = {
        orchestration: { waiting: 0, active: 0, completed: 5, failed: 0 },
        agents: {}
      };

      taskQueue.getQueueStats.mockResolvedValue(mockStats);

      const response = await request(app)
        .get('/api/task-queue/health')
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.healthy).toBe(true);
      expect(response.body.data.redis_connected).toBe(true);
      expect(response.body.data.queues_operational).toBe(true);
    });

    it('should return unhealthy status when queue system fails', async () => {
      taskQueue.getQueueStats.mockRejectedValue(new Error('Redis connection failed'));

      const response = await request(app)
        .get('/api/task-queue/health')
        .expect(503);

      expect(response.body.success).toBe(false);
      expect(response.body.healthy).toBe(false);
      expect(response.body.message).toBe('Task queue system is unhealthy');
    });
  });
});