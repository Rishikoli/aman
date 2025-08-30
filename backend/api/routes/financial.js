/**
 * Financial Data API Routes
 * Endpoints for retrieving and managing financial data
 */

const express = require('express');
const FinancialDataService = require('../../services/financialDataService');
const MLFinancialAnalysisService = require('../../services/mlFinancialAnalysisService');
const FinancialAnalysis = require('../../models/FinancialAnalysis');
const { query, pool } = require('../../database');

const router = express.Router();
const financialDataService = new FinancialDataService();
const mlAnalysisService = new MLFinancialAnalysisService();
const financialAnalysisModel = new FinancialAnalysis(pool);

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
 * M&A Analysis Endpoints
 */

/**
 * Create M&A analysis for a deal
 * POST /api/financial/ma-analysis
 */
router.post('/ma-analysis', async (req, res) => {
  try {
    const { acquirer, target, dealValue, analysisType = 'acquisition' } = req.body;

    if (!acquirer || !target) {
      return res.status(400).json({
        success: false,
        message: 'Both acquirer and target company information are required'
      });
    }

    console.log(`[Financial API] Starting M&A analysis: ${acquirer.name} + ${target.name}`);

    // Create or get companies
    const acquirerCompany = await getOrCreateCompany(acquirer);
    const targetCompany = await getOrCreateCompany(target);

    // Create deal record
    const dealResult = await query(
      `INSERT INTO deals (name, description, acquirer_id, target_id, deal_value, status, created_by)
       VALUES ($1, $2, $3, $4, $5, $6, $7) RETURNING *`,
      [
        `${acquirer.name} ${analysisType} ${target.name}`,
        `M&A analysis between ${acquirer.name} and ${target.name}`,
        acquirerCompany.id,
        targetCompany.id,
        dealValue || null,
        'draft',
        'ma-analyzer'
      ]
    );

    const deal = dealResult.rows[0];

    // Generate comprehensive financial analysis
    const analysisData = await generateMAAnalysis(acquirerCompany, targetCompany, deal);

    // Save analysis to database
    const savedAnalysis = await financialAnalysisModel.createAnalysis(
      deal.id,
      targetCompany.id,
      analysisData
    );

    res.json({
      success: true,
      message: 'M&A analysis completed successfully',
      data: {
        dealId: deal.id,
        analysis: savedAnalysis,
        acquirer: acquirerCompany,
        target: targetCompany
      }
    });

  } catch (error) {
    console.error('[Financial API] M&A analysis failed:', error.message);
    res.status(500).json({
      success: false,
      message: 'M&A analysis failed',
      error: error.message
    });
  }
});

/**
 * Get financial analysis for a deal
 * GET /api/deals/:dealId/financial-analysis
 */
router.get('/deals/:dealId/financial-analysis', async (req, res) => {
  try {
    const { dealId } = req.params;

    console.log(`[Financial API] Retrieving financial analysis for deal: ${dealId}`);

    const analysis = await financialAnalysisModel.getAnalysisByDealId(dealId);

    if (!analysis) {
      return res.status(404).json({
        success: false,
        message: 'Financial analysis not found for this deal'
      });
    }

    res.json({
      success: true,
      message: 'Financial analysis retrieved successfully',
      data: analysis
    });

  } catch (error) {
    console.error('[Financial API] Failed to retrieve financial analysis:', error.message);
    res.status(500).json({
      success: false,
      message: 'Failed to retrieve financial analysis',
      error: error.message
    });
  }
});

/**
 * Get financial metrics for a deal
 * GET /api/deals/:dealId/financial-metrics
 */
router.get('/deals/:dealId/financial-metrics', async (req, res) => {
  try {
    const { dealId } = req.params;
    const { category } = req.query;

    const analysis = await financialAnalysisModel.getAnalysisByDealId(dealId);
    if (!analysis) {
      return res.status(404).json({
        success: false,
        message: 'Financial analysis not found'
      });
    }

    let metrics = await financialAnalysisModel.getMetricsByAnalysisId(analysis.id);
    
    if (category && category !== 'all') {
      metrics = metrics.filter(m => m.category === category);
    }

    res.json({
      success: true,
      data: metrics
    });

  } catch (error) {
    console.error('[Financial API] Failed to retrieve metrics:', error.message);
    res.status(500).json({
      success: false,
      message: 'Failed to retrieve financial metrics',
      error: error.message
    });
  }
});

/**
 * Get financial trends for a deal
 * GET /api/deals/:dealId/financial-trends
 */
router.get('/deals/:dealId/financial-trends', async (req, res) => {
  try {
    const { dealId } = req.params;

    const analysis = await financialAnalysisModel.getAnalysisByDealId(dealId);
    if (!analysis) {
      return res.status(404).json({
        success: false,
        message: 'Financial analysis not found'
      });
    }

    const trends = await financialAnalysisModel.getTrendDataByAnalysisId(analysis.id);

    res.json({
      success: true,
      data: trends
    });

  } catch (error) {
    console.error('[Financial API] Failed to retrieve trends:', error.message);
    res.status(500).json({
      success: false,
      message: 'Failed to retrieve financial trends',
      error: error.message
    });
  }
});

/**
 * Get financial anomalies for a deal
 * GET /api/deals/:dealId/financial-anomalies
 */
router.get('/deals/:dealId/financial-anomalies', async (req, res) => {
  try {
    const { dealId } = req.params;
    const { severity } = req.query;

    const analysis = await financialAnalysisModel.getAnalysisByDealId(dealId);
    if (!analysis) {
      return res.status(404).json({
        success: false,
        message: 'Financial analysis not found'
      });
    }

    let anomalies = await financialAnalysisModel.getAnomaliesByAnalysisId(analysis.id);
    
    if (severity) {
      const severityLevels = severity.split(',');
      anomalies = anomalies.filter(a => severityLevels.includes(a.severity));
    }

    res.json({
      success: true,
      data: anomalies
    });

  } catch (error) {
    console.error('[Financial API] Failed to retrieve anomalies:', error.message);
    res.status(500).json({
      success: false,
      message: 'Failed to retrieve financial anomalies',
      error: error.message
    });
  }
});

/**
 * Get financial forecasts for a deal
 * GET /api/deals/:dealId/financial-forecasts
 */
router.get('/deals/:dealId/financial-forecasts', async (req, res) => {
  try {
    const { dealId } = req.params;
    const { scenarios } = req.query;

    const analysis = await financialAnalysisModel.getAnalysisByDealId(dealId);
    if (!analysis) {
      return res.status(404).json({
        success: false,
        message: 'Financial analysis not found'
      });
    }

    let forecasts = await financialAnalysisModel.getForecastsByAnalysisId(analysis.id);
    
    if (scenarios) {
      const scenarioList = scenarios.split(',');
      forecasts = forecasts.filter(f => scenarioList.includes(f.scenario));
    }

    res.json({
      success: true,
      data: forecasts
    });

  } catch (error) {
    console.error('[Financial API] Failed to retrieve forecasts:', error.message);
    res.status(500).json({
      success: false,
      message: 'Failed to retrieve financial forecasts',
      error: error.message
    });
  }
});

/**
 * Get risk assessment for a deal
 * GET /api/deals/:dealId/risk-assessment
 */
router.get('/deals/:dealId/risk-assessment', async (req, res) => {
  try {
    const { dealId } = req.params;

    const analysis = await financialAnalysisModel.getAnalysisByDealId(dealId);
    if (!analysis) {
      return res.status(404).json({
        success: false,
        message: 'Financial analysis not found'
      });
    }

    const riskFactors = await financialAnalysisModel.getRiskFactorsByAnalysisId(analysis.id);
    
    // Calculate risk distribution
    const riskDistribution = riskFactors.reduce((acc, risk) => {
      const existing = acc.find(item => item.category === risk.category);
      if (existing) {
        existing.count++;
        existing.averageScore = (existing.averageScore + risk.risk_score) / 2;
      } else {
        acc.push({
          category: risk.category,
          count: 1,
          averageScore: risk.risk_score
        });
      }
      return acc;
    }, []);

    const overallRiskScore = riskFactors.length > 0 
      ? riskFactors.reduce((sum, risk) => sum + risk.risk_score, 0) / riskFactors.length
      : 0;

    const riskLevel = overallRiskScore > 70 ? 'critical' : 
                     overallRiskScore > 50 ? 'high' : 
                     overallRiskScore > 30 ? 'medium' : 'low';

    const riskAssessment = {
      overallRiskScore,
      riskLevel,
      riskFactors,
      riskDistribution,
      recommendations: [
        'Establish comprehensive risk monitoring framework',
        'Develop detailed integration timeline with key milestones',
        'Create contingency plans for high-impact risks',
        'Regular stakeholder communication and updates'
      ]
    };

    res.json({
      success: true,
      data: riskAssessment
    });

  } catch (error) {
    console.error('[Financial API] Failed to retrieve risk assessment:', error.message);
    res.status(500).json({
      success: false,
      message: 'Failed to retrieve risk assessment',
      error: error.message
    });
  }
});

/**
 * Helper Functions
 */

async function getOrCreateCompany(companyData) {
  try {
    // Try to find existing company
    let company;
    if (companyData.ticker) {
      const result = await query(
        'SELECT * FROM companies WHERE ticker_symbol = $1',
        [companyData.ticker.toUpperCase()]
      );
      company = result.rows[0];
    }

    if (!company) {
      // Create new company
      const result = await query(
        `INSERT INTO companies (name, ticker_symbol, description)
         VALUES ($1, $2, $3) RETURNING *`,
        [
          companyData.name,
          companyData.ticker?.toUpperCase() || null,
          `Company created for M&A analysis`
        ]
      );
      company = result.rows[0];
    }

    return company;
  } catch (error) {
    console.error('Error getting or creating company:', error);
    throw error;
  }
}

async function generateMAAnalysis(acquirer, target, deal) {
  // This would integrate with real financial data services and ML models
  // For now, we'll generate realistic mock data
  
  const MockFinancialDataService = require('../../services/mockFinancialDataService');
  return MockFinancialDataService.generateFinancialAnalysis(deal.id, target.id);
}

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