/**
 * Intelligent Financial Intelligence API Routes
 * Provides endpoints for smart company lookup, peer identification, and ML-based risk scoring
 */

const express = require('express');
const IntelligentFinancialService = require('../../services/intelligentFinancialService');

const router = express.Router();
const intelligentFinancialService = new IntelligentFinancialService();

/**
 * Smart Company Lookup
 * POST /api/intelligent-financial/lookup
 */
router.post('/lookup', async (req, res) => {
  try {
    const { identifier, options = {} } = req.body;

    if (!identifier) {
      return res.status(400).json({
        error: 'Company identifier is required',
        message: 'Please provide a company name, ticker symbol, or partial identifier'
      });
    }

    console.log(`[API] Smart company lookup request for: ${identifier}`);

    const lookupResults = await intelligentFinancialService.smartCompanyLookup(identifier, options);

    res.json({
      success: true,
      data: lookupResults,
      message: `Found ${lookupResults.totalResults} companies matching "${identifier}"`
    });

  } catch (error) {
    console.error('[API] Smart company lookup failed:', error.message);
    res.status(500).json({
      error: 'Smart company lookup failed',
      message: error.message,
      details: process.env.NODE_ENV === 'development' ? error.stack : undefined
    });
  }
});

/**
 * Identify Peer Companies
 * POST /api/intelligent-financial/peers
 */
router.post('/peers', async (req, res) => {
  try {
    const { symbol, options = {} } = req.body;

    if (!symbol) {
      return res.status(400).json({
        error: 'Company symbol is required',
        message: 'Please provide a valid stock ticker symbol'
      });
    }

    console.log(`[API] Peer identification request for: ${symbol}`);

    const peerAnalysis = await intelligentFinancialService.identifyPeerCompanies(symbol, options);

    res.json({
      success: true,
      data: peerAnalysis,
      message: `Identified ${peerAnalysis.peersFound} peer companies for ${symbol}`
    });

  } catch (error) {
    console.error('[API] Peer identification failed:', error.message);
    res.status(500).json({
      error: 'Peer identification failed',
      message: error.message,
      details: process.env.NODE_ENV === 'development' ? error.stack : undefined
    });
  }
});

/**
 * Comprehensive Risk Scoring
 * POST /api/intelligent-financial/risk-score
 */
router.post('/risk-score', async (req, res) => {
  try {
    const { symbol, options = {} } = req.body;

    if (!symbol) {
      return res.status(400).json({
        error: 'Company symbol is required',
        message: 'Please provide a valid stock ticker symbol'
      });
    }

    console.log(`[API] Risk scoring request for: ${symbol}`);

    const riskAssessment = await intelligentFinancialService.buildComprehensiveRiskScore(symbol, options);

    res.json({
      success: true,
      data: riskAssessment,
      message: `Risk assessment completed for ${symbol} - Risk Level: ${riskAssessment.riskLevel}`
    });

  } catch (error) {
    console.error('[API] Risk scoring failed:', error.message);
    res.status(500).json({
      error: 'Risk scoring failed',
      message: error.message,
      details: process.env.NODE_ENV === 'development' ? error.stack : undefined
    });
  }
});

/**
 * Combined Intelligence Analysis
 * POST /api/intelligent-financial/analyze
 */
router.post('/analyze', async (req, res) => {
  try {
    const { identifier, options = {} } = req.body;

    if (!identifier) {
      return res.status(400).json({
        error: 'Company identifier is required',
        message: 'Please provide a company name, ticker symbol, or partial identifier'
      });
    }

    const {
      includePeers = true,
      includeRiskScore = true,
      includeFinancials = false,
      maxPeers = 5
    } = options;

    console.log(`[API] Combined intelligence analysis request for: ${identifier}`);

    const analysisResults = {
      identifier,
      timestamp: new Date().toISOString(),
      analysis: {}
    };

    // Step 1: Smart company lookup
    const lookupResults = await intelligentFinancialService.smartCompanyLookup(identifier, {
      includeFinancials,
      includeRiskScore: false, // We'll do this separately for better control
      maxResults: 1
    });

    if (lookupResults.totalResults === 0) {
      return res.status(404).json({
        error: 'Company not found',
        message: `No companies found matching "${identifier}"`,
        suggestions: 'Try using a different company name or ticker symbol'
      });
    }

    const primaryCompany = lookupResults.results[0];
    analysisResults.analysis.companyLookup = {
      company: primaryCompany,
      confidence: lookupResults.confidence,
      dataSources: lookupResults.dataSources
    };

    // Step 2: Risk scoring if requested
    if (includeRiskScore && primaryCompany.symbol) {
      try {
        const riskAssessment = await intelligentFinancialService.buildComprehensiveRiskScore(
          primaryCompany.symbol,
          {
            includePeerComparison: includePeers,
            includeHistoricalTrends: true
          }
        );
        analysisResults.analysis.riskAssessment = riskAssessment;
      } catch (error) {
        console.warn(`[API] Risk scoring failed for ${primaryCompany.symbol}:`, error.message);
        analysisResults.analysis.riskAssessment = {
          error: error.message,
          available: false
        };
      }
    }

    // Step 3: Peer identification if requested
    if (includePeers && primaryCompany.symbol) {
      try {
        const peerAnalysis = await intelligentFinancialService.identifyPeerCompanies(
          primaryCompany.symbol,
          {
            maxPeers,
            includeFinancials: false,
            similarityThreshold: 0.6
          }
        );
        analysisResults.analysis.peerAnalysis = peerAnalysis;
      } catch (error) {
        console.warn(`[API] Peer identification failed for ${primaryCompany.symbol}:`, error.message);
        analysisResults.analysis.peerAnalysis = {
          error: error.message,
          available: false
        };
      }
    }

    // Step 4: Generate executive summary
    analysisResults.executiveSummary = generateExecutiveSummary(analysisResults.analysis);

    res.json({
      success: true,
      data: analysisResults,
      message: `Complete intelligence analysis for ${primaryCompany.name || identifier}`
    });

  } catch (error) {
    console.error('[API] Combined intelligence analysis failed:', error.message);
    res.status(500).json({
      error: 'Intelligence analysis failed',
      message: error.message,
      details: process.env.NODE_ENV === 'development' ? error.stack : undefined
    });
  }
});

/**
 * Test Intelligent Financial Service
 * GET /api/intelligent-financial/test
 */
router.get('/test', async (req, res) => {
  try {
    console.log('[API] Testing intelligent financial service capabilities...');

    const testResults = await intelligentFinancialService.testIntelligentFinancialService();

    res.json({
      success: true,
      data: testResults,
      message: `Service test completed - ${testResults.workingCapabilities} capabilities operational`
    });

  } catch (error) {
    console.error('[API] Service test failed:', error.message);
    res.status(500).json({
      error: 'Service test failed',
      message: error.message,
      details: process.env.NODE_ENV === 'development' ? error.stack : undefined
    });
  }
});

/**
 * Get Service Status and Capabilities
 * GET /api/intelligent-financial/status
 */
router.get('/status', async (req, res) => {
  try {
    const status = {
      service: 'Intelligent Financial Intelligence System',
      version: '1.0.0',
      timestamp: new Date().toISOString(),
      capabilities: [
        'Smart Company Lookup with Multi-Source Fallbacks',
        'Peer Company Identification using Financial Similarity',
        'ML-Based Comprehensive Risk Scoring',
        'Combined Intelligence Analysis'
      ],
      endpoints: [
        'POST /api/intelligent-financial/lookup - Smart company lookup',
        'POST /api/intelligent-financial/peers - Peer company identification',
        'POST /api/intelligent-financial/risk-score - Comprehensive risk scoring',
        'POST /api/intelligent-financial/analyze - Combined intelligence analysis',
        'GET /api/intelligent-financial/test - Service capability testing',
        'GET /api/intelligent-financial/status - Service status'
      ]
    };

    res.json({
      success: true,
      data: status,
      message: 'Intelligent Financial Intelligence System is operational'
    });

  } catch (error) {
    console.error('[API] Status check failed:', error.message);
    res.status(500).json({
      error: 'Status check failed',
      message: error.message
    });
  }
});

/**
 * Generate executive summary from analysis results
 * @param {Object} analysis - Analysis results
 * @returns {Object} Executive summary
 */
function generateExecutiveSummary(analysis) {
  const summary = {
    keyFindings: [],
    riskHighlights: [],
    peerInsights: [],
    recommendations: []
  };

  // Company lookup findings
  if (analysis.companyLookup) {
    const company = analysis.companyLookup.company;
    summary.keyFindings.push(`Company identified: ${company.name} (${company.symbol})`);
    
    if (company.industry) {
      summary.keyFindings.push(`Industry: ${company.industry}`);
    }
    
    if (company.marketCap) {
      const marketCapBillions = (company.marketCap / 1000000000).toFixed(1);
      summary.keyFindings.push(`Market Cap: $${marketCapBillions}B`);
    }
  }

  // Risk assessment highlights
  if (analysis.riskAssessment && !analysis.riskAssessment.error) {
    const risk = analysis.riskAssessment;
    summary.riskHighlights.push(`Overall Risk Level: ${risk.riskLevel} (${risk.overallRiskScore}/100)`);
    
    // Add top risk factors
    const highRiskComponents = Object.entries(risk.riskComponents)
      .filter(([_, data]) => data.level === 'High')
      .map(([name, _]) => name);
    
    if (highRiskComponents.length > 0) {
      summary.riskHighlights.push(`High risk areas: ${highRiskComponents.join(', ')}`);
    }

    // Add peer comparison if available
    if (risk.peerComparison?.available) {
      summary.riskHighlights.push(`Risk vs peers: ${risk.peerComparison.comparison}`);
    }

    // Add recommendations
    if (risk.recommendations) {
      summary.recommendations.push(...risk.recommendations.slice(0, 3)); // Top 3 recommendations
    }
  }

  // Peer analysis insights
  if (analysis.peerAnalysis && !analysis.peerAnalysis.error) {
    const peers = analysis.peerAnalysis;
    summary.peerInsights.push(`${peers.peersFound} peer companies identified`);
    
    if (peers.peers.length > 0) {
      const topPeer = peers.peers[0];
      summary.peerInsights.push(`Most similar peer: ${topPeer.name} (${(topPeer.similarityScore * 100).toFixed(1)}% similarity)`);
    }

    if (peers.insights) {
      summary.peerInsights.push(...peers.insights.slice(0, 2)); // Top 2 insights
    }
  }

  return summary;
}

module.exports = router;