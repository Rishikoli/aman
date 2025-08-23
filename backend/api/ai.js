const express = require('express');
const router = express.Router();
const geminiService = require('../services/gemini');
const { body, validationResult } = require('express-validator');

/**
 * @route GET /api/ai/status
 * @desc Get AI service status
 * @access Public
 */
router.get('/status', (req, res) => {
  try {
    const status = geminiService.getStatus();
    res.json({
      success: true,
      data: status,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('AI status error:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to get AI service status',
      timestamp: new Date().toISOString()
    });
  }
});

/**
 * @route POST /api/ai/analyze-deal
 * @desc Analyze M&A deal using AI
 * @access Public
 */
router.post('/analyze-deal', [
  body('targetCompany').optional().isString().trim(),
  body('acquiringCompany').optional().isString().trim(),
  body('dealValue').optional().isString().trim(),
  body('industry').optional().isString().trim(),
  body('dealType').optional().isString().trim()
], async (req, res) => {
  try {
    // Check validation results
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        error: 'Validation failed',
        details: errors.array(),
        timestamp: new Date().toISOString()
      });
    }

    if (!geminiService.isAvailable()) {
      return res.status(503).json({
        success: false,
        error: 'AI service not available',
        timestamp: new Date().toISOString()
      });
    }

    const dealData = req.body;
    const analysis = await geminiService.analyzeDeal(dealData);

    res.json({
      success: true,
      data: analysis,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Deal analysis error:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to analyze deal',
      message: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

/**
 * @route POST /api/ai/research-company
 * @desc Research company using AI
 * @access Public
 */
router.post('/research-company', [
  body('companyName').notEmpty().isString().trim(),
  body('industry').optional().isString().trim(),
  body('revenue').optional().isString().trim(),
  body('employees').optional().isString().trim(),
  body('founded').optional().isString().trim()
], async (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        error: 'Validation failed',
        details: errors.array(),
        timestamp: new Date().toISOString()
      });
    }

    if (!geminiService.isAvailable()) {
      return res.status(503).json({
        success: false,
        error: 'AI service not available',
        timestamp: new Date().toISOString()
      });
    }

    const { companyName, ...companyData } = req.body;
    const research = await geminiService.researchCompany(companyName, companyData);

    res.json({
      success: true,
      data: research,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Company research error:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to research company',
      message: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

/**
 * @route POST /api/ai/market-intelligence
 * @desc Generate market intelligence report
 * @access Public
 */
router.post('/market-intelligence', [
  body('industry').notEmpty().isString().trim(),
  body('focusAreas').optional().isArray()
], async (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        error: 'Validation failed',
        details: errors.array(),
        timestamp: new Date().toISOString()
      });
    }

    if (!geminiService.isAvailable()) {
      return res.status(503).json({
        success: false,
        error: 'AI service not available',
        timestamp: new Date().toISOString()
      });
    }

    const { industry, focusAreas } = req.body;
    const intelligence = await geminiService.generateMarketIntelligence(industry, { focusAreas });

    res.json({
      success: true,
      data: intelligence,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Market intelligence error:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to generate market intelligence',
      message: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

/**
 * @route POST /api/ai/generate-text
 * @desc Generate text using AI
 * @access Public
 */
router.post('/generate-text', [
  body('prompt').notEmpty().isString().trim(),
  body('temperature').optional().isFloat({ min: 0, max: 2 }),
  body('maxTokens').optional().isInt({ min: 1, max: 4096 })
], async (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        error: 'Validation failed',
        details: errors.array(),
        timestamp: new Date().toISOString()
      });
    }

    if (!geminiService.isAvailable()) {
      return res.status(503).json({
        success: false,
        error: 'AI service not available',
        timestamp: new Date().toISOString()
      });
    }

    const { prompt, temperature, maxTokens } = req.body;
    const text = await geminiService.generateText(prompt, { temperature, maxTokens });

    res.json({
      success: true,
      data: { text },
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Text generation error:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to generate text',
      message: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

module.exports = router;