const express = require('express');
const router = express.Router();
const { body, query, param, validationResult } = require('express-validator');
const qaService = require('../../services/qaService');

/**
 * Validation error handler
 */
const handleValidationErrors = (req, res, next) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({
      success: false,
      error: 'Validation failed',
      details: errors.array(),
      timestamp: new Date().toISOString()
    });
  }
  next();
};

/**
 * @route POST /api/v1/qa/ask
 * @desc Ask a factual question about M&A data
 * @access Public
 */
router.post('/ask', [
  body('question').notEmpty().isString().trim().isLength({ min: 5, max: 500 }),
  body('context').optional().isObject(),
  body('context.deal_id').optional().isUUID(),
  body('context.company_id').optional().isUUID(),
  handleValidationErrors
], async (req, res) => {
  try {
    const { question, context = {} } = req.body;

    console.log(`[QA API] Processing question: "${question}"`);
    
    const result = await qaService.processQuery(question, context);

    if (!result.success) {
      return res.status(400).json({
        success: false,
        error: 'Failed to process question',
        message: result.error,
        timestamp: new Date().toISOString()
      });
    }

    res.json({
      success: true,
      data: result,
      timestamp: new Date().toISOString()
    });

  } catch (error) {
    console.error('[QA API] Question processing failed:', error);
    res.status(500).json({
      success: false,
      error: 'Internal server error',
      message: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

/**
 * @route GET /api/v1/qa/suggestions
 * @desc Get suggested questions based on context
 * @access Public
 */
router.get('/suggestions', [
  query('deal_id').optional().isUUID(),
  query('company_id').optional().isUUID(),
  handleValidationErrors
], async (req, res) => {
  try {
    const context = {
      deal_id: req.query.deal_id,
      company_id: req.query.company_id
    };

    console.log('[QA API] Getting suggested queries with context:', context);

    const suggestions = await qaService.getSuggestedQueries(context);

    res.json({
      success: true,
      data: {
        suggestions,
        context,
        total: suggestions.length
      },
      timestamp: new Date().toISOString()
    });

  } catch (error) {
    console.error('[QA API] Failed to get suggestions:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to get suggestions',
      message: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

/**
 * @route GET /api/v1/qa/search
 * @desc Search across all M&A data
 * @access Public
 */
router.get('/search', [
  query('q').notEmpty().isString().trim().isLength({ min: 2, max: 100 }),
  query('category').optional().isIn(['deals', 'companies', 'findings', 'agents', 'all']),
  query('limit').optional().isInt({ min: 1, max: 100 }),
  handleValidationErrors
], async (req, res) => {
  try {
    const { q: searchTerm, category = 'all', limit = 20 } = req.query;

    console.log(`[QA API] Searching for: "${searchTerm}" in category: ${category}`);

    const results = await qaService.searchAll(searchTerm, { category, limit });

    res.json({
      success: true,
      data: {
        searchTerm,
        category,
        results,
        total: results.total
      },
      timestamp: new Date().toISOString()
    });

  } catch (error) {
    console.error('[QA API] Search failed:', error);
    res.status(500).json({
      success: false,
      error: 'Search failed',
      message: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

/**
 * @route POST /api/v1/qa/batch
 * @desc Process multiple questions in batch
 * @access Public
 */
router.post('/batch', [
  body('questions').isArray({ min: 1, max: 10 }),
  body('questions.*.question').notEmpty().isString().trim(),
  body('questions.*.context').optional().isObject(),
  body('context').optional().isObject(),
  handleValidationErrors
], async (req, res) => {
  try {
    const { questions, context: globalContext = {} } = req.body;

    console.log(`[QA API] Processing ${questions.length} questions in batch`);

    const results = await Promise.all(
      questions.map(async (item, index) => {
        try {
          const questionContext = { ...globalContext, ...item.context };
          const result = await qaService.processQuery(item.question, questionContext);
          return {
            index,
            question: item.question,
            ...result
          };
        } catch (error) {
          return {
            index,
            question: item.question,
            success: false,
            error: error.message
          };
        }
      })
    );

    const successful = results.filter(r => r.success).length;
    const failed = results.length - successful;

    res.json({
      success: true,
      data: {
        results,
        summary: {
          total: results.length,
          successful,
          failed
        }
      },
      timestamp: new Date().toISOString()
    });

  } catch (error) {
    console.error('[QA API] Batch processing failed:', error);
    res.status(500).json({
      success: false,
      error: 'Batch processing failed',
      message: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

/**
 * @route GET /api/v1/qa/categories
 * @desc Get available query categories and their descriptions
 * @access Public
 */
router.get('/categories', (req, res) => {
  try {
    const categories = [
      {
        type: 'deal_info',
        name: 'Deal Information',
        description: 'Questions about deal status, progress, and general information',
        examples: [
          'What is the status of deal XYZ?',
          'Show me all active deals',
          'What deals were completed this month?'
        ]
      },
      {
        type: 'company_info',
        name: 'Company Information',
        description: 'Questions about company profiles, basic information, and characteristics',
        examples: [
          'Tell me about Apple Inc.',
          'What industry is Microsoft in?',
          'Show me all technology companies'
        ]
      },
      {
        type: 'financial_data',
        name: 'Financial Analysis',
        description: 'Questions about financial metrics, ratios, and performance',
        examples: [
          'What is the revenue of Apple?',
          'Show me financial ratios for Tesla',
          'Compare the profitability of these companies'
        ]
      },
      {
        type: 'risk_assessment',
        name: 'Risk Assessment',
        description: 'Questions about risks, threats, and critical findings',
        examples: [
          'What are the key risks for this deal?',
          'Show me all critical findings',
          'What financial risks were identified?'
        ]
      },
      {
        type: 'agent_status',
        name: 'Agent Status',
        description: 'Questions about agent execution status and performance',
        examples: [
          'What is the status of all agents?',
          'Which agents are currently running?',
          'Show me failed agent executions'
        ]
      },
      {
        type: 'timeline',
        name: 'Timeline & Progress',
        description: 'Questions about timelines, completion dates, and progress',
        examples: [
          'When will this deal be completed?',
          'What is the estimated timeline?',
          'Show me the project timeline'
        ]
      },
      {
        type: 'findings',
        name: 'Findings & Issues',
        description: 'Questions about specific findings, issues, and discoveries',
        examples: [
          'What issues were found?',
          'Show me legal findings',
          'What problems need attention?'
        ]
      }
    ];

    res.json({
      success: true,
      data: {
        categories,
        total: categories.length
      },
      timestamp: new Date().toISOString()
    });

  } catch (error) {
    console.error('[QA API] Failed to get categories:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to get categories',
      message: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

/**
 * @route GET /api/v1/qa/stats
 * @desc Get Q&A system statistics
 * @access Public
 */
router.get('/stats', async (req, res) => {
  try {
    const { query: dbQuery } = require('../../utils/database');

    // Get basic statistics
    const stats = await Promise.all([
      dbQuery('SELECT COUNT(*) as total FROM deals'),
      dbQuery('SELECT COUNT(*) as total FROM companies'),
      dbQuery('SELECT COUNT(*) as total FROM findings'),
      dbQuery('SELECT COUNT(*) as total FROM agent_executions'),
      dbQuery(`
        SELECT 
          COUNT(*) as total,
          COUNT(CASE WHEN status = 'active' THEN 1 END) as active,
          COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed
        FROM deals
      `),
      dbQuery(`
        SELECT 
          severity,
          COUNT(*) as count
        FROM findings 
        GROUP BY severity
        ORDER BY 
          CASE severity 
            WHEN 'critical' THEN 1 
            WHEN 'high' THEN 2 
            WHEN 'medium' THEN 3 
            WHEN 'low' THEN 4 
          END
      `)
    ]);

    const [
      dealsCount,
      companiesCount,
      findingsCount,
      agentExecutionsCount,
      dealStatus,
      findingsBySeverity
    ] = stats;

    res.json({
      success: true,
      data: {
        overview: {
          totalDeals: parseInt(dealsCount.rows[0].total),
          totalCompanies: parseInt(companiesCount.rows[0].total),
          totalFindings: parseInt(findingsCount.rows[0].total),
          totalAgentExecutions: parseInt(agentExecutionsCount.rows[0].total)
        },
        dealStatus: {
          total: parseInt(dealStatus.rows[0].total),
          active: parseInt(dealStatus.rows[0].active),
          completed: parseInt(dealStatus.rows[0].completed)
        },
        findingsBySeverity: findingsBySeverity.rows.reduce((acc, row) => {
          acc[row.severity] = parseInt(row.count);
          return acc;
        }, {}),
        capabilities: {
          aiEnabled: require('../../services/gemini').isAvailable(),
          searchEnabled: true,
          batchProcessing: true,
          contextAware: true
        }
      },
      timestamp: new Date().toISOString()
    });

  } catch (error) {
    console.error('[QA API] Failed to get stats:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to get statistics',
      message: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

module.exports = router;