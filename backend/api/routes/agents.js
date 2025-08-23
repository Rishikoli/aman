const express = require('express');
const { body, param, query, validationResult } = require('express-validator');
const router = express.Router();

const AgentExecution = require('../../models/AgentExecution');

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

// GET /api/v1/agents - Get all agent executions with status
router.get('/', [
  query('agent_type').optional().isIn(['finance', 'legal', 'synergy', 'reputation', 'operations', 'orchestrator']),
  query('status').optional().isIn(['pending', 'running', 'completed', 'failed', 'cancelled']),
  query('deal_id').optional().isUUID(),
  query('limit').optional().isInt({ min: 1, max: 100 }),
  handleValidationErrors
], async (req, res) => {
  try {
    const filters = {
      agent_type: req.query.agent_type,
      status: req.query.status,
      deal_id: req.query.deal_id,
      limit: req.query.limit ? parseInt(req.query.limit) : undefined
    };

    // Remove undefined values
    Object.keys(filters).forEach(key => {
      if (filters[key] === undefined) {
        delete filters[key];
      }
    });

    let executions;
    if (filters.agent_type) {
      executions = await AgentExecution.findByAgentType(filters.agent_type, filters);
    } else if (filters.deal_id) {
      executions = await AgentExecution.findByDealId(filters.deal_id);
    } else {
      // Get all active executions if no specific filters
      executions = await AgentExecution.getActiveExecutions();
    }

    const statistics = await AgentExecution.getStatistics(filters);

    res.json({
      success: true,
      data: {
        executions,
        statistics,
        total: executions.length
      }
    });
  } catch (error) {
    console.error('Error fetching agent executions:', error);
    res.status(500).json({ 
      success: false,
      error: 'Failed to fetch agent executions',
      message: error.message 
    });
  }
});

// GET /api/v1/agents/:executionId - Get specific agent execution
router.get('/:executionId', [
  param('executionId').isUUID(),
  handleValidationErrors
], async (req, res) => {
  try {
    const { executionId } = req.params;
    const execution = await AgentExecution.findById(executionId);

    if (!execution) {
      return res.status(404).json({
        success: false,
        error: 'Agent execution not found'
      });
    }

    res.json({
      success: true,
      data: { execution }
    });
  } catch (error) {
    console.error('Error fetching agent execution:', error);
    res.status(500).json({ 
      success: false,
      error: 'Failed to fetch agent execution',
      message: error.message 
    });
  }
});

// POST /api/v1/agents/execute - Create and start new agent execution
router.post('/execute', [
  body('deal_id').isUUID(),
  body('agent_type').isIn(['finance', 'legal', 'synergy', 'reputation', 'operations', 'orchestrator']),
  body('agent_id').notEmpty().trim(),
  body('input_data').optional().isObject(),
  body('recursion_level').optional().isInt({ min: 0, max: 10 }),
  body('parent_execution_id').optional().isUUID(),
  handleValidationErrors
], async (req, res) => {
  try {
    const executionData = {
      deal_id: req.body.deal_id,
      agent_type: req.body.agent_type,
      agent_id: req.body.agent_id,
      input_data: req.body.input_data || {},
      recursion_level: req.body.recursion_level || 0,
      parent_execution_id: req.body.parent_execution_id,
      status: 'pending'
    };

    const execution = new AgentExecution(executionData);
    await execution.save();

    res.status(201).json({
      success: true,
      message: 'Agent execution created successfully',
      data: { execution }
    });
  } catch (error) {
    console.error('Error creating agent execution:', error);
    res.status(400).json({ 
      success: false,
      error: 'Failed to create agent execution',
      message: error.message 
    });
  }
});

// PUT /api/v1/agents/:executionId/start - Start agent execution
router.put('/:executionId/start', [
  param('executionId').isUUID(),
  handleValidationErrors
], async (req, res) => {
  try {
    const { executionId } = req.params;
    const execution = await AgentExecution.findById(executionId);

    if (!execution) {
      return res.status(404).json({
        success: false,
        error: 'Agent execution not found'
      });
    }

    if (execution.status !== 'pending') {
      return res.status(400).json({
        success: false,
        error: 'Agent execution cannot be started',
        message: `Execution is in ${execution.status} status`
      });
    }

    await execution.start();

    res.json({
      success: true,
      message: 'Agent execution started',
      data: { execution }
    });
  } catch (error) {
    console.error('Error starting agent execution:', error);
    res.status(500).json({ 
      success: false,
      error: 'Failed to start agent execution',
      message: error.message 
    });
  }
});

// PUT /api/v1/agents/:executionId/progress - Update agent execution progress
router.put('/:executionId/progress', [
  param('executionId').isUUID(),
  body('progress_percentage').isInt({ min: 0, max: 100 }),
  handleValidationErrors
], async (req, res) => {
  try {
    const { executionId } = req.params;
    const { progress_percentage } = req.body;
    
    const execution = await AgentExecution.findById(executionId);

    if (!execution) {
      return res.status(404).json({
        success: false,
        error: 'Agent execution not found'
      });
    }

    if (execution.status !== 'running') {
      return res.status(400).json({
        success: false,
        error: 'Cannot update progress',
        message: `Execution is in ${execution.status} status`
      });
    }

    await execution.updateProgress(progress_percentage);

    res.json({
      success: true,
      message: 'Progress updated successfully',
      data: { execution }
    });
  } catch (error) {
    console.error('Error updating progress:', error);
    res.status(500).json({ 
      success: false,
      error: 'Failed to update progress',
      message: error.message 
    });
  }
});

// PUT /api/v1/agents/:executionId/complete - Complete agent execution
router.put('/:executionId/complete', [
  param('executionId').isUUID(),
  body('output_data').optional().isObject(),
  handleValidationErrors
], async (req, res) => {
  try {
    const { executionId } = req.params;
    const { output_data } = req.body;
    
    const execution = await AgentExecution.findById(executionId);

    if (!execution) {
      return res.status(404).json({
        success: false,
        error: 'Agent execution not found'
      });
    }

    if (execution.status !== 'running') {
      return res.status(400).json({
        success: false,
        error: 'Cannot complete execution',
        message: `Execution is in ${execution.status} status`
      });
    }

    await execution.complete(output_data || {});

    res.json({
      success: true,
      message: 'Agent execution completed successfully',
      data: { execution }
    });
  } catch (error) {
    console.error('Error completing agent execution:', error);
    res.status(500).json({ 
      success: false,
      error: 'Failed to complete agent execution',
      message: error.message 
    });
  }
});

// PUT /api/v1/agents/:executionId/fail - Fail agent execution
router.put('/:executionId/fail', [
  param('executionId').isUUID(),
  body('error_message').notEmpty().trim(),
  handleValidationErrors
], async (req, res) => {
  try {
    const { executionId } = req.params;
    const { error_message } = req.body;
    
    const execution = await AgentExecution.findById(executionId);

    if (!execution) {
      return res.status(404).json({
        success: false,
        error: 'Agent execution not found'
      });
    }

    if (execution.status === 'completed') {
      return res.status(400).json({
        success: false,
        error: 'Cannot fail completed execution'
      });
    }

    await execution.fail(error_message);

    res.json({
      success: true,
      message: 'Agent execution marked as failed',
      data: { execution }
    });
  } catch (error) {
    console.error('Error failing agent execution:', error);
    res.status(500).json({ 
      success: false,
      error: 'Failed to update agent execution',
      message: error.message 
    });
  }
});

// GET /api/v1/agents/types/:agentType - Get executions by agent type
router.get('/types/:agentType', [
  param('agentType').isIn(['finance', 'legal', 'synergy', 'reputation', 'operations', 'orchestrator']),
  query('status').optional().isIn(['pending', 'running', 'completed', 'failed', 'cancelled']),
  query('deal_id').optional().isUUID(),
  query('limit').optional().isInt({ min: 1, max: 100 }),
  handleValidationErrors
], async (req, res) => {
  try {
    const { agentType } = req.params;
    const filters = {
      status: req.query.status,
      deal_id: req.query.deal_id,
      limit: req.query.limit ? parseInt(req.query.limit) : undefined
    };

    // Remove undefined values
    Object.keys(filters).forEach(key => {
      if (filters[key] === undefined) {
        delete filters[key];
      }
    });

    const executions = await AgentExecution.findByAgentType(agentType, filters);
    const statistics = await AgentExecution.getStatistics({ agent_type: agentType });

    res.json({
      success: true,
      data: {
        agent_type: agentType,
        executions,
        statistics,
        total: executions.length
      }
    });
  } catch (error) {
    console.error('Error fetching agent executions by type:', error);
    res.status(500).json({ 
      success: false,
      error: 'Failed to fetch agent executions',
      message: error.message 
    });
  }
});

// GET /api/v1/agents/active - Get all active agent executions
router.get('/status/active', async (req, res) => {
  try {
    const executions = await AgentExecution.getActiveExecutions();

    res.json({
      success: true,
      data: {
        executions,
        total: executions.length
      }
    });
  } catch (error) {
    console.error('Error fetching active executions:', error);
    res.status(500).json({ 
      success: false,
      error: 'Failed to fetch active executions',
      message: error.message 
    });
  }
});

// GET /api/v1/agents/statistics - Get agent execution statistics
router.get('/stats/overview', [
  query('agent_type').optional().isIn(['finance', 'legal', 'synergy', 'reputation', 'operations', 'orchestrator']),
  query('deal_id').optional().isUUID(),
  handleValidationErrors
], async (req, res) => {
  try {
    const filters = {
      agent_type: req.query.agent_type,
      deal_id: req.query.deal_id
    };

    // Remove undefined values
    Object.keys(filters).forEach(key => {
      if (filters[key] === undefined) {
        delete filters[key];
      }
    });

    const statistics = await AgentExecution.getStatistics(filters);

    res.json({
      success: true,
      data: {
        statistics,
        filters
      }
    });
  } catch (error) {
    console.error('Error fetching agent statistics:', error);
    res.status(500).json({ 
      success: false,
      error: 'Failed to fetch agent statistics',
      message: error.message 
    });
  }
});

module.exports = router;