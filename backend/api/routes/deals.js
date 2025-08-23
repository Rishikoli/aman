const express = require('express');
const { body, param, query, validationResult } = require('express-validator');
const router = express.Router();

const Deal = require('../../models/Deal');
const Company = require('../../models/Company');
const AgentExecution = require('../../models/AgentExecution');
const dealOrchestrator = require('../../services/dealOrchestrator');

// Validation middleware
const handleValidationErrors = (req, res, next) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({
      error: 'Validation failed',
      details: errors.array()
    });
  }
  next();
};

// GET /api/v1/deals - Get all deals with orchestration status
router.get('/', [
  query('status').optional().isIn(['draft', 'active', 'completed', 'cancelled', 'on_hold']),
  query('created_by').optional().isString(),
  query('priority').optional().isInt({ min: 1, max: 10 }),
  query('limit').optional().isInt({ min: 1, max: 100 }),
  handleValidationErrors
], async (req, res) => {
  try {
    const filters = {
      status: req.query.status,
      created_by: req.query.created_by,
      priority: req.query.priority ? parseInt(req.query.priority) : undefined,
      limit: req.query.limit ? parseInt(req.query.limit) : undefined
    };

    // Remove undefined values
    Object.keys(filters).forEach(key => {
      if (filters[key] === undefined) {
        delete filters[key];
      }
    });

    const deals = await dealOrchestrator.getAllDealsWithStatus(filters);
    const statistics = await Deal.getStatistics();

    res.json({
      success: true,
      data: {
        deals,
        statistics,
        total: deals.length
      }
    });
  } catch (error) {
    console.error('Error fetching deals:', error);
    res.status(500).json({ 
      success: false,
      error: 'Failed to fetch deals',
      message: error.message 
    });
  }
});

// POST /api/v1/deals - Create new deal with orchestration
router.post('/', [
  body('name').notEmpty().trim().isLength({ min: 1, max: 255 }),
  body('description').optional().isString(),
  body('acquirer_id').isUUID(),
  body('target_id').isUUID(),
  body('deal_value').optional().isFloat({ min: 0 }),
  body('currency').optional().isLength({ min: 3, max: 3 }),
  body('created_by').notEmpty().trim(),
  body('estimated_completion_date').optional().isISO8601(),
  body('priority').optional().isInt({ min: 1, max: 10 }),
  handleValidationErrors
], async (req, res) => {
  try {
    const dealData = {
      name: req.body.name,
      description: req.body.description,
      acquirer_id: req.body.acquirer_id,
      target_id: req.body.target_id,
      deal_value: req.body.deal_value,
      currency: req.body.currency || 'USD',
      created_by: req.body.created_by,
      estimated_completion_date: req.body.estimated_completion_date,
      priority: req.body.priority || 5,
      status: 'draft'
    };

    const result = await dealOrchestrator.createDeal(dealData);

    res.status(201).json({
      success: true,
      message: 'Deal created successfully with orchestration plan',
      data: result
    });
  } catch (error) {
    console.error('Error creating deal:', error);
    res.status(400).json({ 
      success: false,
      error: 'Failed to create deal',
      message: error.message 
    });
  }
});

// GET /api/v1/deals/:id - Get specific deal with full status
router.get('/:id', [
  param('id').isUUID(),
  handleValidationErrors
], async (req, res) => {
  try {
    const { id } = req.params;
    const dealStatus = await dealOrchestrator.getDealStatus(id);

    res.json({
      success: true,
      data: dealStatus
    });
  } catch (error) {
    console.error('Error fetching deal:', error);
    if (error.message.includes('not found')) {
      res.status(404).json({ 
        success: false,
        error: 'Deal not found',
        message: error.message 
      });
    } else {
      res.status(500).json({ 
        success: false,
        error: 'Failed to fetch deal',
        message: error.message 
      });
    }
  }
});

// PUT /api/v1/deals/:id - Update deal
router.put('/:id', [
  param('id').isUUID(),
  body('name').optional().trim().isLength({ min: 1, max: 255 }),
  body('description').optional().isString(),
  body('deal_value').optional().isFloat({ min: 0 }),
  body('currency').optional().isLength({ min: 3, max: 3 }),
  body('status').optional().isIn(['draft', 'active', 'completed', 'cancelled', 'on_hold']),
  body('estimated_completion_date').optional().isISO8601(),
  body('priority').optional().isInt({ min: 1, max: 10 }),
  handleValidationErrors
], async (req, res) => {
  try {
    const { id } = req.params;
    const deal = await Deal.findById(id);
    
    if (!deal) {
      return res.status(404).json({
        success: false,
        error: 'Deal not found'
      });
    }

    // Update deal properties
    Object.keys(req.body).forEach(key => {
      if (req.body[key] !== undefined) {
        deal[key] = req.body[key];
      }
    });

    await deal.update();

    // If status changed to active, ensure orchestration is ready
    if (req.body.status === 'active') {
      const executions = await AgentExecution.findByDealId(id);
      if (executions.length === 0) {
        await dealOrchestrator.createOrchestrationPlan(id);
      }
    }

    const updatedDealStatus = await dealOrchestrator.getDealStatus(id);

    res.json({
      success: true,
      message: 'Deal updated successfully',
      data: updatedDealStatus
    });
  } catch (error) {
    console.error('Error updating deal:', error);
    res.status(500).json({ 
      success: false,
      error: 'Failed to update deal',
      message: error.message 
    });
  }
});

// DELETE /api/v1/deals/:id - Delete deal
router.delete('/:id', [
  param('id').isUUID(),
  handleValidationErrors
], async (req, res) => {
  try {
    const { id } = req.params;
    const deleted = await Deal.deleteById(id);
    
    if (!deleted) {
      return res.status(404).json({
        success: false,
        error: 'Deal not found'
      });
    }

    res.json({
      success: true,
      message: 'Deal deleted successfully'
    });
  } catch (error) {
    console.error('Error deleting deal:', error);
    res.status(500).json({ 
      success: false,
      error: 'Failed to delete deal',
      message: error.message 
    });
  }
});

// POST /api/v1/deals/:id/start - Start deal orchestration
router.post('/:id/start', [
  param('id').isUUID(),
  handleValidationErrors
], async (req, res) => {
  try {
    const { id } = req.params;
    
    // Update deal status to active
    await dealOrchestrator.updateDealStatus(id, 'active');
    
    // Get updated status
    const dealStatus = await dealOrchestrator.getDealStatus(id);

    res.json({
      success: true,
      message: 'Deal orchestration started',
      data: dealStatus
    });
  } catch (error) {
    console.error('Error starting deal orchestration:', error);
    res.status(500).json({ 
      success: false,
      error: 'Failed to start deal orchestration',
      message: error.message 
    });
  }
});

// POST /api/v1/deals/:id/cancel - Cancel deal orchestration
router.post('/:id/cancel', [
  param('id').isUUID(),
  handleValidationErrors
], async (req, res) => {
  try {
    const { id } = req.params;
    const result = await dealOrchestrator.cancelDealOrchestration(id);

    res.json({
      success: true,
      message: result.message,
      data: result
    });
  } catch (error) {
    console.error('Error cancelling deal orchestration:', error);
    res.status(500).json({ 
      success: false,
      error: 'Failed to cancel deal orchestration',
      message: error.message 
    });
  }
});

// GET /api/v1/deals/:id/executions - Get agent executions for a deal
router.get('/:id/executions', [
  param('id').isUUID(),
  handleValidationErrors
], async (req, res) => {
  try {
    const { id } = req.params;
    const executionHistory = await AgentExecution.getExecutionHistory(id);

    res.json({
      success: true,
      data: executionHistory
    });
  } catch (error) {
    console.error('Error fetching execution history:', error);
    res.status(500).json({ 
      success: false,
      error: 'Failed to fetch execution history',
      message: error.message 
    });
  }
});

// GET /api/v1/deals/statistics - Get deal statistics
router.get('/stats/overview', async (req, res) => {
  try {
    const statistics = await Deal.getStatistics();
    const agentStats = await AgentExecution.getStatistics();

    res.json({
      success: true,
      data: {
        deals: statistics,
        agent_executions: agentStats
      }
    });
  } catch (error) {
    console.error('Error fetching statistics:', error);
    res.status(500).json({ 
      success: false,
      error: 'Failed to fetch statistics',
      message: error.message 
    });
  }
});

module.exports = router;