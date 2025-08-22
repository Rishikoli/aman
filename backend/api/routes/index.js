const express = require('express');
const router = express.Router();

// Import route modules
const dealsRoutes = require('./deals');
const companiesRoutes = require('./companies');
const agentsRoutes = require('./agents');

// API version info
router.get('/', (req, res) => {
  res.json({
    message: 'AMAN Backend API v1',
    version: '1.0.0',
    timestamp: new Date().toISOString(),
    endpoints: {
      deals: '/api/v1/deals',
      companies: '/api/v1/companies',
      agents: '/api/v1/agents'
    }
  });
});

// Mount route modules
router.use('/deals', dealsRoutes);
router.use('/companies', companiesRoutes);
router.use('/agents', agentsRoutes);

module.exports = router;