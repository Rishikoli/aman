const express = require('express');
const router = express.Router();

// Import route modules
const dealsRoutes = require('./deals');
const companiesRoutes = require('./companies');
const agentsRoutes = require('./agents');
const taskQueueRoutes = require('./taskQueue');
const timelineRoutes = require('./timeline');
const financialRoutes = require('./financial');
const intelligentFinancialRoutes = require('./intelligentFinancial');
const qaRoutes = require('./qa');
const aiRoutes = require('../ai');

// API version info
router.get('/', (req, res) => {
  res.json({
    message: 'AMAN Backend API v1',
    version: '1.0.0',
    timestamp: new Date().toISOString(),
    endpoints: {
      deals: '/api/v1/deals',
      companies: '/api/v1/companies',
      agents: '/api/v1/agents',
      taskQueue: '/api/v1/task-queue',
      timeline: '/api/v1/timeline',
      financial: '/api/v1/financial',
      intelligentFinancial: '/api/v1/intelligent-financial',
      qa: '/api/v1/qa',
      ai: '/api/v1/ai'
    }
  });
});

// Mount route modules
router.use('/deals', dealsRoutes);
router.use('/companies', companiesRoutes);
router.use('/agents', agentsRoutes);
router.use('/task-queue', taskQueueRoutes);
router.use('/timeline', timelineRoutes);
router.use('/financial', financialRoutes);
router.use('/intelligent-financial', intelligentFinancialRoutes);
router.use('/qa', qaRoutes);
router.use('/ai', aiRoutes);

module.exports = router;