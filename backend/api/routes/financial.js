/**
 * Financial Data API Routes
 * Endpoints for retrieving and managing financial data
 */

const express = require('express');
const FinancialDataService = require('../../services/financialDataService');
const MLFinancialAnalysisService = require('../../services/mlFinancialAnalysisService');
const { query } = require('../../database');

const router = express.Router();
const financialDataService = new FinancialDataService();
const mlAnalysisService = new MLFinancialAnalysisService();

/**
 * Test financial data sources connection
 * GET /api/financial/test-connections
 */
router.get('/test-connections', async (req, res) => {
  try {
    console.log('[Financial API] Testing data source connections...');
    
    const testResults = await financialDataService.testConnections();
    
    res.json({
      success: true,
      message: 'Connection test completed',
      data: testResults
    });

  } catch (error) {
    console.error('[Financial API] Connection test failed:', error.message);
    res.status(500).json({
      success: false,
      message: 'Connection test failed',
      error: error.message
    });
  }
});

/**
 * Search for companies
 * GET /api/financial/search?q=query&limit=10
 */
router.get('/search', async (req, res) => {
  try {
    const { q: query, limit = 10 } = req.query;
    
    if (!query) {
      return res.status(400).json({
        success: false,
        message: 'Query parameter "q" is required'
      });
    }

    console.log(`[Financial API] Searching companies: ${query}`);
    
    const searchResults = await financialDataService.searchCompanies(query, parseInt(limit));
    
    res.json({
      success: true,
      message: 'Company search completed',
      data: searchResults
    });

  } catch (error) {
    console.error('[Financial API] Company search failed:', error.message);
    res.status(500).json({
      success: false,
      message: 'Company search failed',
      error: error.message
    });
  }
});

/**
 * Get company financial data
 * GET /api/financial/company/:symbol
 */
router.get('/company/:symbol', async (req, res) => {
  try {
    const { symbol } = req.params;
    const {
      period = 'annual',
      limit = 5,
      includeProfile = 'true',
      includeStatements = 'true',
      includeRatios = 'true',
      includeMetrics = 'true',
      saveToDatabase = 'true'
    } = req.query;

    if (!symbol) {
      return res.status(400).json({
        success: false,
        message: 'Symbol parameter is required'
      });
    }

    console.log(`[Financial API] Fetching financial data for ${symbol}`);
    
    const options = {
      period,
      limit: parseInt(limit),
      includeProfile: includeProfile === 'true',
      includeStatements: includeStatements === 'true',
      includeRatios: includeRatios === 'true',
      includeMetrics: includeMetrics === 'true',
      saveToDatabase: saveToDatabase === 'true'
    };

    const financialData = await financialDataService.getCompanyFinancialData(symbol, options);
    
    res.json({
      success: true,
      message: `Financial data retrieved for ${symbol}`,
      data: financialData
    });

  } catch (error) {
    console.error(`[Financial API] Failed to fetch financial data for ${req.params.symbol}:`, error.message);
    
    // Determine appropriate status code
    let statusCode = 500;
    if (error.message.includes('not found') || error.message.includes('No company')) {
      statusCode = 404;
    } else if (error.message.includes('Invalid') || error.message.includes('required')) {
      statusCode = 400;
    }

    res.status(statusCode).json({
      success: false,
      message: 'Failed to retrieve financial data',
      error: error.message
    });
  }
});

/**
 * Get company profile only
 * GET /api/financial/company/:symbol/profile
 */
router.get('/company/:symbol/profile', async (req, res) => {
  try {
    const { symbol } = req.params;
    
    console.log(`[Financial API] Fetching company profile for ${symbol}`);
    
    const options = {
      includeProfile: true,
      includeStatements: false,
      includeRatios: false,
      includeMetrics: false,
      saveToDatabase: true
    };

    const financialData = await financialDataService.getCompanyFinancialData(symbol, options);
    
    res.json({
      success: true,
      message: `Company profile retrieved for ${symbol}`,
      data: {
        profile: financialData.profile,
        dataSource: financialData.dataSource,
        metadata: financialData.metadata
      }
    });

  } catch (error) {
    console.error(`[Financial API] Failed to fetch company profile for ${req.params.symbol}:`, error.message);
    
    let statusCode = 500;
    if (error.message.includes('not found') || error.message.includes('No company')) {
      statusCode = 404;
    }

    res.status(statusCode).json({
      success: false,
      message: 'Failed to retrieve company profile',
      error: error.message
    });
  }
});

/**
 * Get financial statements only
 * GET /api/financial/company/:symbol/statements
 */
router.get('/company/:symbol/statements', async (req, res) => {
  try {
    const { symbol } = req.params;
    const { period = 'annual', limit = 5 } = req.query;
    
    console.log(`[Financial API] Fetching financial statements for ${symbol}`);
    
    const options = {
      period,
      limit: parseInt(limit),
      includeProfile: false,
      includeStatements: true,
      includeRatios: false,
      includeMetrics: false,
      saveToDatabase: true
    };

    const financialData = await financialDataService.getCompanyFinancialData(symbol, options);
    
    res.json({
      success: true,
      message: `Financial statements retrieved for ${symbol}`,
      data: {
        statements: financialData.statements,
        dataSource: financialData.dataSource,
        metadata: financialData.metadata
      }
    });

  } catch (error) {
    console.error(`[Financial API] Failed to fetch financial statements for ${req.params.symbol}:`, error.message);
    
    let statusCode = 500;
    if (error.message.includes('not found') || error.message.includes('No company')) {
      statusCode = 404;
    }

    res.status(statusCode).json({
      success: false,
      message: 'Failed to retrieve financial statements',
      error: error.message
    });
  }
});

/**
 * Get stored financial data from database
 * GET /api/financial/stored/:symbol
 */
router.get('/stored/:symbol', async (req, res) => {
  try {
    const { symbol } = req.params;
    const { limit = 5 } = req.query;
    
    console.log(`[Financial API] Fetching stored financial data for ${symbol}`);
    
    // Get company info
    const companyResult = await query(
      'SELECT * FROM companies WHERE ticker_symbol = $1',
      [symbol.toUpperCase()]
    );

    if (companyResult.rows.length === 0) {
      return res.status(404).json({
        success: false,
        message: `No stored data found for symbol: ${symbol}`
      });
    }

    const company = companyResult.rows[0];

    // Get financial data
    const financialResult = await query(
      `SELECT * FROM financial_data 
       WHERE company_id = $1 
       ORDER BY fiscal_year DESC, fiscal_quarter DESC NULLS LAST 
       LIMIT $2`,
      [company.id, parseInt(limit)]
    );

    res.json({
      success: true,
      message: `Stored financial data retrieved for ${symbol}`,
      data: {
        company,
        financialData: financialResult.rows,
        totalRecords: financialResult.rows.length
      }
    });

  } catch (error) {
    console.error(`[Financial API] Failed to fetch stored financial data for ${req.params.symbol}:`, error.message);
    res.status(500).json({
      success: false,
      message: 'Failed to retrieve stored financial data',
      error: error.message
    });
  }
});

/**
 * Get all companies with financial data
 * GET /api/financial/companies
 */
router.get('/companies', async (req, res) => {
  try {
    const { limit = 50, offset = 0 } = req.query;
    
    console.log('[Financial API] Fetching companies with financial data...');
    
    const companiesResult = await query(
      `SELECT c.*, 
              COUNT(fd.id) as financial_records_count,
              MAX(fd.fiscal_year) as latest_fiscal_year
       FROM companies c
       LEFT JOIN financial_data fd ON c.id = fd.company_id
       GROUP BY c.id
       ORDER BY c.updated_at DESC
       LIMIT $1 OFFSET $2`,
      [parseInt(limit), parseInt(offset)]
    );

    // Get total count
    const countResult = await query('SELECT COUNT(*) as total FROM companies');
    const totalCount = parseInt(countResult.rows[0].total);

    res.json({
      success: true,
      message: 'Companies retrieved successfully',
      data: {
        companies: companiesResult.rows,
        pagination: {
          total: totalCount,
          limit: parseInt(limit),
          offset: parseInt(offset),
          hasMore: (parseInt(offset) + parseInt(limit)) < totalCount
        }
      }
    });

  } catch (error) {
    console.error('[Financial API] Failed to fetch companies:', error.message);
    res.status(500).json({
      success: false,
      message: 'Failed to retrieve companies',
      error: error.message
    });
  }
});

/**
 * Delete stored financial data for a company
 * DELETE /api/financial/stored/:symbol
 */
router.delete('/stored/:symbol', async (req, res) => {
  try {
    const { symbol } = req.params;
    
    console.log(`[Financial API] Deleting stored financial data for ${symbol}`);
    
    // Get company ID
    const companyResult = await query(
      'SELECT id FROM companies WHERE ticker_symbol = $1',
      [symbol.toUpperCase()]
    );

    if (companyResult.rows.length === 0) {
      return res.status(404).json({
        success: false,
        message: `No company found for symbol: ${symbol}`
      });
    }

    const companyId = companyResult.rows[0].id;

    // Delete financial data
    const deleteResult = await query(
      'DELETE FROM financial_data WHERE company_id = $1',
      [companyId]
    );

    res.json({
      success: true,
      message: `Deleted ${deleteResult.rowCount} financial records for ${symbol}`,
      data: {
        deletedRecords: deleteResult.rowCount
      }
    });

  } catch (error) {
    console.error(`[Financial API] Failed to delete financial data for ${req.params.symbol}:`, error.message);
    res.status(500).json({
      success: false,
      message: 'Failed to delete financial data',
      error: error.message
    });
  }
});

/**
 * ML-powered comprehensive financial analysis
 * POST /api/financial/ml-analysis/:symbol
 */
router.post('/ml-analysis/:symbol', async (req, res) => {
  try {
    const { symbol } = req.params;
    const {
      period = 'annual',
      limit = 5,
      forecast_years = 3,
      include_narrative_analysis = true
    } = req.body;

    console.log(`[Financial API] Starting ML analysis for ${symbol}`);

    // First get the financial data
    const financialData = await financialDataService.getCompanyFinancialData(symbol, {
      period,
      limit: parseInt(limit),
      includeProfile: true,
      includeStatements: true,
      includeRatios: true,
      includeMetrics: true,
      saveToDatabase: true
    });

    // Check if ML analysis is available
    const mlAvailable = await mlAnalysisService.isAvailable();
    if (!mlAvailable) {
      return res.status(503).json({
        success: false,
        message: 'ML analysis service is not available',
        data: financialData // Return basic financial data
      });
    }

    // Perform ML analysis
    const mlAnalysis = await mlAnalysisService.analyzeCompanyFinancials(financialData, {
      forecast_years: parseInt(forecast_years),
      include_narrative_analysis: include_narrative_analysis === true || include_narrative_analysis === 'true'
    });

    res.json({
      success: true,
      message: `ML-powered financial analysis completed for ${symbol}`,
      data: {
        basic_financial_data: financialData,
        ml_analysis: mlAnalysis
      }
    });

  } catch (error) {
    console.error(`[Financial API] ML analysis failed for ${req.params.symbol}:`, error.message);
    
    let statusCode = 500;
    if (error.message.includes('not found') || error.message.includes('No company')) {
      statusCode = 404;
    }

    res.status(statusCode).json({
      success: false,
      message: 'ML financial analysis failed',
      error: error.message
    });
  }
});

/**
 * Quick ML-powered financial health check
 * GET /api/financial/health-check/:symbol
 */
router.get('/health-check/:symbol', async (req, res) => {
  try {
    const { symbol } = req.params;

    console.log(`[Financial API] Quick health check for ${symbol}`);

    // Get financial data
    const financialData = await financialDataService.getCompanyFinancialData(symbol, {
      period: 'annual',
      limit: 5,
      includeProfile: true,
      includeStatements: true,
      saveToDatabase: false // Don't save for quick checks
    });

    // Check if ML analysis is available
    const mlAvailable = await mlAnalysisService.isAvailable();
    if (!mlAvailable) {
      return res.status(503).json({
        success: false,
        message: 'ML health check service is not available'
      });
    }

    // Perform quick health check
    const healthCheck = await mlAnalysisService.quickHealthCheck(financialData);

    res.json({
      success: true,
      message: `Financial health check completed for ${symbol}`,
      data: healthCheck
    });

  } catch (error) {
    console.error(`[Financial API] Health check failed for ${req.params.symbol}:`, error.message);
    
    let statusCode = 500;
    if (error.message.includes('not found')) {
      statusCode = 404;
    }

    res.status(statusCode).json({
      success: false,
      message: 'Financial health check failed',
      error: error.message
    });
  }
});

/**
 * Compare multiple companies using ML analysis
 * POST /api/financial/compare
 */
router.post('/compare', async (req, res) => {
  try {
    const { symbols, period = 'annual', limit = 5 } = req.body;

    if (!symbols || !Array.isArray(symbols) || symbols.length < 2) {
      return res.status(400).json({
        success: false,
        message: 'At least 2 company symbols are required for comparison'
      });
    }

    console.log(`[Financial API] Comparing companies: ${symbols.join(', ')}`);

    // Check if ML analysis is available
    const mlAvailable = await mlAnalysisService.isAvailable();
    if (!mlAvailable) {
      return res.status(503).json({
        success: false,
        message: 'ML comparison service is not available'
      });
    }

    // Get financial data for all companies
    const companyDataList = [];
    const errors = [];

    for (const symbol of symbols) {
      try {
        const financialData = await financialDataService.getCompanyFinancialData(symbol, {
          period,
          limit: parseInt(limit),
          includeProfile: true,
          includeStatements: true,
          saveToDatabase: false
        });
        companyDataList.push(financialData);
      } catch (error) {
        errors.push({ symbol, error: error.message });
      }
    }

    if (companyDataList.length < 2) {
      return res.status(400).json({
        success: false,
        message: 'Could not retrieve data for at least 2 companies',
        errors
      });
    }

    // Perform ML comparison
    const comparison = await mlAnalysisService.compareCompanies(companyDataList);

    res.json({
      success: true,
      message: `Company comparison completed for ${companyDataList.length} companies`,
      data: {
        comparison,
        companies_analyzed: companyDataList.length,
        errors: errors.length > 0 ? errors : undefined
      }
    });

  } catch (error) {
    console.error('[Financial API] Company comparison failed:', error.message);
    res.status(500).json({
      success: false,
      message: 'Company comparison failed',
      error: error.message
    });
  }
});

/**
 * Test ML analysis capabilities
 * GET /api/financial/ml-test
 */
router.get('/ml-test', async (req, res) => {
  try {
    console.log('[Financial API] Testing ML analysis capabilities...');

    const mlAvailable = await mlAnalysisService.isAvailable();
    if (!mlAvailable) {
      return res.json({
        success: false,
        message: 'ML analysis service is not available',
        ml_available: false
      });
    }

    const testResults = await mlAnalysisService.testCapabilities();

    res.json({
      success: true,
      message: 'ML analysis capability test completed',
      data: testResults
    });

  } catch (error) {
    console.error('[Financial API] ML test failed:', error.message);
    res.status(500).json({
      success: false,
      message: 'ML analysis test failed',
      error: error.message
    });
  }
});

/**
 * Health check endpoint
 * GET /api/financial/health
 */
router.get('/health', async (req, res) => {
  try {
    // Test database connection
    const dbTest = await query('SELECT NOW() as current_time');
    
    // Test data sources (quick test)
    const sourceTests = await financialDataService.testConnections();
    
    // Test ML analysis availability
    const mlAvailable = await mlAnalysisService.isAvailable();
    let mlTest = { available: mlAvailable };
    
    if (mlAvailable) {
      try {
        mlTest = await mlAnalysisService.testCapabilities();
      } catch (error) {
        mlTest = { available: false, error: error.message };
      }
    }
    
    res.json({
      success: true,
      message: 'Financial API is healthy',
      data: {
        database: {
          status: 'connected',
          currentTime: dbTest.rows[0].current_time
        },
        dataSources: sourceTests,
        mlAnalysis: mlTest
      }
    });

  } catch (error) {
    console.error('[Financial API] Health check failed:', error.message);
    res.status(503).json({
      success: false,
      message: 'Financial API health check failed',
      error: error.message
    });
  }
});

module.exports = router;