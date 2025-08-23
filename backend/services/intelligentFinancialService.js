/**
 * Intelligent Financial Intelligence System
 * Provides smart company lookup, peer identification, and ML-based risk scoring
 */

const FinancialDataService = require('./financialDataService');
const { query } = require('../database');

class IntelligentFinancialService {
  constructor() {
    this.financialDataService = new FinancialDataService();
    this.industryClassifications = new Map();
    this.peerSimilarityThreshold = 0.7;
  }

  /**
   * Smart company lookup with multiple data source fallbacks
   * @param {string} identifier - Company name, ticker, or partial identifier
   * @param {Object} options - Lookup options
   * @returns {Promise<Object>} Company lookup results with fallback data
   */
  async smartCompanyLookup(identifier, options = {}) {
    const {
      includeFinancials = true,
      includePeers = false,
      includeRiskScore = true,
      maxResults = 10
    } = options;

    console.log(`[IntelligentFinancialService] Smart lookup for: ${identifier}`);

    try {
      const lookupResults = {
        query: identifier,
        timestamp: new Date().toISOString(),
        results: [],
        dataSources: [],
        errors: []
      };

      // Step 1: Try exact ticker match first
      if (this._isValidTicker(identifier)) {
        try {
          const exactMatch = await this._getExactTickerMatch(identifier, {
            includeFinancials,
            includeRiskScore
          });
          if (exactMatch) {
            lookupResults.results.push(exactMatch);
            lookupResults.dataSources.push('exact_ticker_match');
          }
        } catch (error) {
          lookupResults.errors.push({
            source: 'exact_ticker_match',
            error: error.message
          });
        }
      }

      // Step 2: Search across multiple data sources if no exact match or need more results
      if (lookupResults.results.length === 0 || lookupResults.results.length < maxResults) {
        try {
          const searchResults = await this.financialDataService.searchCompanies(
            identifier, 
            maxResults - lookupResults.results.length
          );
          
          for (const result of searchResults.results) {
            // Enhance each result with additional intelligence
            const enhancedResult = await this._enhanceCompanyResult(result, {
              includeFinancials,
              includeRiskScore
            });
            lookupResults.results.push(enhancedResult);
          }
          
          lookupResults.dataSources.push('multi_source_search');
          if (searchResults.errors) {
            lookupResults.errors.push(...searchResults.errors);
          }
        } catch (error) {
          lookupResults.errors.push({
            source: 'multi_source_search',
            error: error.message
          });
        }
      }

      // Step 3: Try fuzzy matching in local database
      if (lookupResults.results.length === 0) {
        try {
          const fuzzyResults = await this._fuzzySearchDatabase(identifier, maxResults);
          lookupResults.results.push(...fuzzyResults);
          lookupResults.dataSources.push('fuzzy_database_search');
        } catch (error) {
          lookupResults.errors.push({
            source: 'fuzzy_database_search',
            error: error.message
          });
        }
      }

      // Step 4: Add peer companies if requested
      if (includePeers && lookupResults.results.length > 0) {
        try {
          const primaryCompany = lookupResults.results[0];
          const peers = await this.identifyPeerCompanies(primaryCompany.symbol, {
            maxPeers: 5,
            includeFinancials: false
          });
          lookupResults.peerCompanies = peers.peers;
        } catch (error) {
          lookupResults.errors.push({
            source: 'peer_identification',
            error: error.message
          });
        }
      }

      // Step 5: Calculate lookup confidence score
      lookupResults.confidence = this._calculateLookupConfidence(lookupResults);
      lookupResults.totalResults = lookupResults.results.length;

      console.log(`[IntelligentFinancialService] Smart lookup completed: ${lookupResults.totalResults} results found`);
      return lookupResults;

    } catch (error) {
      console.error(`[IntelligentFinancialService] Smart lookup failed:`, error.message);
      throw new Error(`Smart company lookup failed: ${error.message}`);
    }
  }

  /**
   * Identify peer companies using financial similarity algorithms
   * @param {string} targetSymbol - Target company ticker symbol
   * @param {Object} options - Peer identification options
   * @returns {Promise<Object>} Peer company analysis results
   */
  async identifyPeerCompanies(targetSymbol, options = {}) {
    const {
      maxPeers = 10,
      includeFinancials = true,
      similarityThreshold = this.peerSimilarityThreshold,
      industryFilter = true
    } = options;

    console.log(`[IntelligentFinancialService] Identifying peers for: ${targetSymbol}`);

    try {
      // Step 1: Get target company financial data
      const targetData = await this.financialDataService.getCompanyFinancialData(targetSymbol, {
        includeProfile: true,
        includeStatements: true,
        includeRatios: true,
        saveToDatabase: false
      });

      if (!targetData.profile) {
        throw new Error(`Unable to retrieve profile data for ${targetSymbol}`);
      }

      const peerAnalysis = {
        targetCompany: {
          symbol: targetSymbol,
          name: targetData.profile.companyName,
          industry: targetData.profile.industry,
          sector: targetData.profile.sector,
          marketCap: targetData.profile.marketCap
        },
        peers: [],
        similarityMetrics: {},
        analysisDate: new Date().toISOString()
      };

      // Step 2: Find potential peer companies
      let potentialPeers = [];

      // First try industry-based filtering
      if (industryFilter && targetData.profile.industry) {
        potentialPeers = await this._findCompaniesByIndustry(
          targetData.profile.industry,
          targetData.profile.sector,
          maxPeers * 3 // Get more candidates for filtering
        );
      }

      // If not enough industry peers, expand search
      if (potentialPeers.length < maxPeers) {
        const additionalPeers = await this._findCompaniesByMarketCap(
          targetData.profile.marketCap,
          maxPeers * 2
        );
        potentialPeers = [...potentialPeers, ...additionalPeers];
      }

      // Step 3: Calculate financial similarity for each potential peer
      const similarityScores = [];
      
      for (const peer of potentialPeers) {
        if (peer.symbol === targetSymbol) continue; // Skip self
        
        try {
          const peerData = await this.financialDataService.getCompanyFinancialData(peer.symbol, {
            includeProfile: true,
            includeStatements: true,
            saveToDatabase: false
          });

          const similarity = await this._calculateFinancialSimilarity(targetData, peerData);
          
          if (similarity.overallScore >= similarityThreshold) {
            similarityScores.push({
              ...peer,
              similarityScore: similarity.overallScore,
              similarityBreakdown: similarity.breakdown,
              financialData: includeFinancials ? peerData : null
            });
          }
        } catch (error) {
          console.warn(`[IntelligentFinancialService] Failed to analyze peer ${peer.symbol}:`, error.message);
        }
      }

      // Step 4: Sort by similarity and take top peers
      similarityScores.sort((a, b) => b.similarityScore - a.similarityScore);
      peerAnalysis.peers = similarityScores.slice(0, maxPeers);

      // Step 5: Generate peer analysis insights
      peerAnalysis.insights = this._generatePeerInsights(peerAnalysis);
      peerAnalysis.totalPeersAnalyzed = potentialPeers.length;
      peerAnalysis.peersFound = peerAnalysis.peers.length;

      console.log(`[IntelligentFinancialService] Peer identification completed: ${peerAnalysis.peersFound} peers found`);
      return peerAnalysis;

    } catch (error) {
      console.error(`[IntelligentFinancialService] Peer identification failed:`, error.message);
      throw new Error(`Peer identification failed: ${error.message}`);
    }
  }

  /**
   * Build comprehensive financial risk scoring with ML-based insights
   * @param {string} symbol - Company ticker symbol
   * @param {Object} options - Risk scoring options
   * @returns {Promise<Object>} Comprehensive risk assessment
   */
  async buildComprehensiveRiskScore(symbol, options = {}) {
    const {
      includePeerComparison = true,
      includeHistoricalTrends = true,
      includeMarketFactors = true,
      riskHorizon = '1year' // '1year', '3year', '5year'
    } = options;

    console.log(`[IntelligentFinancialService] Building comprehensive risk score for: ${symbol}`);

    try {
      // Step 1: Get comprehensive financial data
      const financialData = await this.financialDataService.getCompanyFinancialData(symbol, {
        includeProfile: true,
        includeStatements: true,
        includeRatios: true,
        includeMetrics: true,
        saveToDatabase: true
      });

      const riskAssessment = {
        company: {
          symbol: symbol,
          name: financialData.profile?.companyName || 'Unknown',
          industry: financialData.profile?.industry,
          sector: financialData.profile?.sector
        },
        overallRiskScore: 0,
        riskLevel: 'Unknown',
        riskComponents: {},
        insights: [],
        recommendations: [],
        analysisDate: new Date().toISOString(),
        riskHorizon
      };

      // Step 2: Calculate individual risk components
      console.log(`[IntelligentFinancialService] Calculating risk components...`);

      // Financial Health Risk (40% weight)
      const financialHealthRisk = await this._calculateFinancialHealthRisk(financialData);
      riskAssessment.riskComponents.financialHealth = {
        score: financialHealthRisk.score,
        level: financialHealthRisk.level,
        factors: financialHealthRisk.factors,
        weight: 0.4
      };

      // Liquidity Risk (25% weight)
      const liquidityRisk = await this._calculateLiquidityRisk(financialData);
      riskAssessment.riskComponents.liquidity = {
        score: liquidityRisk.score,
        level: liquidityRisk.level,
        factors: liquidityRisk.factors,
        weight: 0.25
      };

      // Leverage Risk (20% weight)
      const leverageRisk = await this._calculateLeverageRisk(financialData);
      riskAssessment.riskComponents.leverage = {
        score: leverageRisk.score,
        level: leverageRisk.level,
        factors: leverageRisk.factors,
        weight: 0.2
      };

      // Profitability Risk (15% weight)
      const profitabilityRisk = await this._calculateProfitabilityRisk(financialData);
      riskAssessment.riskComponents.profitability = {
        score: profitabilityRisk.score,
        level: profitabilityRisk.level,
        factors: profitabilityRisk.factors,
        weight: 0.15
      };

      // Step 3: Calculate weighted overall risk score
      riskAssessment.overallRiskScore = this._calculateWeightedRiskScore(riskAssessment.riskComponents);
      riskAssessment.riskLevel = this._determineRiskLevel(riskAssessment.overallRiskScore);

      // Step 4: Add peer comparison if requested
      if (includePeerComparison) {
        try {
          const peerComparison = await this._calculatePeerRiskComparison(symbol, riskAssessment.overallRiskScore);
          riskAssessment.peerComparison = peerComparison;
        } catch (error) {
          console.warn(`[IntelligentFinancialService] Peer comparison failed:`, error.message);
        }
      }

      // Step 5: Generate insights and recommendations
      riskAssessment.insights = this._generateRiskInsights(riskAssessment);
      riskAssessment.recommendations = this._generateRiskRecommendations(riskAssessment);

      // Step 6: Add confidence metrics
      riskAssessment.confidence = this._calculateRiskConfidence(financialData, riskAssessment);

      console.log(`[IntelligentFinancialService] Risk assessment completed - Overall Risk: ${riskAssessment.riskLevel} (${riskAssessment.overallRiskScore})`);
      return riskAssessment;

    } catch (error) {
      console.error(`[IntelligentFinancialService] Risk scoring failed:`, error.message);
      throw new Error(`Comprehensive risk scoring failed: ${error.message}`);
    }
  }

  // Private helper methods

  /**
   * Check if identifier is a valid ticker symbol
   * @param {string} identifier - Potential ticker symbol
   * @returns {boolean} True if valid ticker format
   * @private
   */
  _isValidTicker(identifier) {
    // Basic ticker validation: 1-5 uppercase letters
    return /^[A-Z]{1,5}$/.test(identifier.toUpperCase());
  }

  /**
   * Get exact ticker match with enhanced data
   * @param {string} ticker - Stock ticker symbol
   * @param {Object} options - Enhancement options
   * @returns {Promise<Object>} Enhanced company data
   * @private
   */
  async _getExactTickerMatch(ticker, options) {
    const financialData = await this.financialDataService.getCompanyFinancialData(ticker, {
      includeProfile: true,
      includeStatements: options.includeFinancials,
      saveToDatabase: false
    });

    const result = {
      symbol: ticker.toUpperCase(),
      name: financialData.profile?.companyName || 'Unknown',
      exchange: financialData.profile?.exchangeShortName,
      industry: financialData.profile?.industry,
      sector: financialData.profile?.sector,
      marketCap: financialData.profile?.marketCap,
      matchType: 'exact_ticker',
      confidence: 1.0,
      dataSource: financialData.dataSource
    };

    if (options.includeRiskScore) {
      try {
        const riskScore = await this.buildComprehensiveRiskScore(ticker, {
          includePeerComparison: false,
          includeHistoricalTrends: false
        });
        result.riskScore = riskScore.overallRiskScore;
        result.riskLevel = riskScore.riskLevel;
      } catch (error) {
        console.warn(`[IntelligentFinancialService] Risk scoring failed for ${ticker}:`, error.message);
      }
    }

    return result;
  }

  /**
   * Enhance company search result with additional intelligence
   * @param {Object} result - Basic search result
   * @param {Object} options - Enhancement options
   * @returns {Promise<Object>} Enhanced result
   * @private
   */
  async _enhanceCompanyResult(result, options) {
    const enhanced = {
      ...result,
      matchType: 'search_result',
      confidence: this._calculateSearchConfidence(result)
    };

    if (options.includeFinancials || options.includeRiskScore) {
      try {
        const financialData = await this.financialDataService.getCompanyFinancialData(result.symbol, {
          includeProfile: true,
          includeStatements: options.includeFinancials,
          saveToDatabase: false
        });

        if (options.includeRiskScore) {
          const riskScore = await this.buildComprehensiveRiskScore(result.symbol, {
            includePeerComparison: false
          });
          enhanced.riskScore = riskScore.overallRiskScore;
          enhanced.riskLevel = riskScore.riskLevel;
        }
      } catch (error) {
        console.warn(`[IntelligentFinancialService] Enhancement failed for ${result.symbol}:`, error.message);
      }
    }

    return enhanced;
  }

  /**
   * Perform fuzzy search in local database
   * @param {string} query - Search query
   * @param {number} limit - Maximum results
   * @returns {Promise<Array>} Fuzzy search results
   * @private
   */
  async _fuzzySearchDatabase(query, limit) {
    try {
      const searchResults = await query(
        `SELECT ticker_symbol, name, industry, sector, market_cap 
         FROM companies 
         WHERE name ILIKE $1 OR ticker_symbol ILIKE $2
         ORDER BY 
           CASE 
             WHEN ticker_symbol ILIKE $3 THEN 1
             WHEN name ILIKE $4 THEN 2
             ELSE 3
           END
         LIMIT $5`,
        [`%${query}%`, `%${query}%`, `${query}%`, `${query}%`, limit]
      );

      return searchResults.rows.map(row => ({
        symbol: row.ticker_symbol,
        name: row.name,
        industry: row.industry,
        sector: row.sector,
        marketCap: row.market_cap,
        matchType: 'fuzzy_database',
        confidence: this._calculateFuzzyConfidence(query, row.name, row.ticker_symbol)
      }));
    } catch (error) {
      console.error(`[IntelligentFinancialService] Database fuzzy search failed:`, error.message);
      return [];
    }
  }

  /**
   * Calculate lookup confidence score
   * @param {Object} lookupResults - Lookup results object
   * @returns {number} Confidence score (0-1)
   * @private
   */
  _calculateLookupConfidence(lookupResults) {
    if (lookupResults.results.length === 0) return 0;

    const hasExactMatch = lookupResults.results.some(r => r.matchType === 'exact_ticker');
    const hasMultipleSources = lookupResults.dataSources.length > 1;
    const errorRate = lookupResults.errors.length / (lookupResults.dataSources.length || 1);

    let confidence = 0.5; // Base confidence

    if (hasExactMatch) confidence += 0.4;
    if (hasMultipleSources) confidence += 0.2;
    confidence -= errorRate * 0.3;

    return Math.max(0, Math.min(1, confidence));
  }

  /**
   * Calculate search result confidence
   * @param {Object} result - Search result
   * @returns {number} Confidence score (0-1)
   * @private
   */
  _calculateSearchConfidence(result) {
    let confidence = 0.7; // Base confidence for search results

    if (result.exchange) confidence += 0.1;
    if (result.industry) confidence += 0.1;
    if (result.marketCap) confidence += 0.1;

    return Math.min(1, confidence);
  }

  /**
   * Calculate fuzzy search confidence
   * @param {string} query - Original query
   * @param {string} name - Company name
   * @param {string} ticker - Ticker symbol
   * @returns {number} Confidence score (0-1)
   * @private
   */
  _calculateFuzzyConfidence(query, name, ticker) {
    const queryLower = query.toLowerCase();
    const nameLower = name.toLowerCase();
    const tickerLower = ticker.toLowerCase();

    if (tickerLower === queryLower) return 0.9;
    if (nameLower === queryLower) return 0.8;
    if (tickerLower.includes(queryLower)) return 0.7;
    if (nameLower.includes(queryLower)) return 0.6;

    return 0.4; // Base fuzzy match confidence
  }

  /**
   * Find companies by industry and sector
   * @param {string} industry - Industry name
   * @param {string} sector - Sector name
   * @param {number} limit - Maximum results
   * @returns {Promise<Array>} Industry peer companies
   * @private
   */
  async _findCompaniesByIndustry(industry, sector, limit) {
    try {
      const industryResults = await query(
        `SELECT ticker_symbol, name, industry, sector, market_cap
         FROM companies 
         WHERE industry = $1 OR sector = $2
         ORDER BY market_cap DESC NULLS LAST
         LIMIT $3`,
        [industry, sector, limit]
      );

      return industryResults.rows.map(row => ({
        symbol: row.ticker_symbol,
        name: row.name,
        industry: row.industry,
        sector: row.sector,
        marketCap: row.market_cap
      }));
    } catch (error) {
      console.error(`[IntelligentFinancialService] Industry search failed:`, error.message);
      return [];
    }
  }

  /**
   * Find companies by similar market cap
   * @param {number} targetMarketCap - Target market capitalization
   * @param {number} limit - Maximum results
   * @returns {Promise<Array>} Market cap peer companies
   * @private
   */
  async _findCompaniesByMarketCap(targetMarketCap, limit) {
    if (!targetMarketCap) return [];

    try {
      // Find companies within 50% of target market cap
      const lowerBound = targetMarketCap * 0.5;
      const upperBound = targetMarketCap * 1.5;

      const marketCapResults = await query(
        `SELECT ticker_symbol, name, industry, sector, market_cap
         FROM companies 
         WHERE market_cap BETWEEN $1 AND $2
         ORDER BY ABS(market_cap - $3)
         LIMIT $4`,
        [lowerBound, upperBound, targetMarketCap, limit]
      );

      return marketCapResults.rows.map(row => ({
        symbol: row.ticker_symbol,
        name: row.name,
        industry: row.industry,
        sector: row.sector,
        marketCap: row.market_cap
      }));
    } catch (error) {
      console.error(`[IntelligentFinancialService] Market cap search failed:`, error.message);
      return [];
    }
  }

  /**
   * Calculate financial similarity between two companies
   * @param {Object} targetData - Target company financial data
   * @param {Object} peerData - Peer company financial data
   * @returns {Promise<Object>} Similarity analysis
   * @private
   */
  async _calculateFinancialSimilarity(targetData, peerData) {
    const similarity = {
      overallScore: 0,
      breakdown: {
        industry: 0,
        size: 0,
        profitability: 0,
        leverage: 0,
        liquidity: 0
      }
    };

    try {
      // Industry similarity (30% weight)
      if (targetData.profile?.industry === peerData.profile?.industry) {
        similarity.breakdown.industry = 1.0;
      } else if (targetData.profile?.sector === peerData.profile?.sector) {
        similarity.breakdown.industry = 0.7;
      } else {
        similarity.breakdown.industry = 0.0;
      }

      // Size similarity (25% weight) - based on market cap
      const targetMarketCap = targetData.profile?.marketCap || 0;
      const peerMarketCap = peerData.profile?.marketCap || 0;
      
      if (targetMarketCap > 0 && peerMarketCap > 0) {
        const ratio = Math.min(targetMarketCap, peerMarketCap) / Math.max(targetMarketCap, peerMarketCap);
        similarity.breakdown.size = ratio;
      }

      // Financial ratios similarity (45% weight total)
      const targetStatements = targetData.statements?.incomeStatement?.[0];
      const peerStatements = peerData.statements?.incomeStatement?.[0];

      if (targetStatements && peerStatements) {
        // Profitability similarity (15% weight)
        const targetNetMargin = (targetStatements.netIncome || 0) / (targetStatements.revenue || 1);
        const peerNetMargin = (peerStatements.netIncome || 0) / (peerStatements.revenue || 1);
        similarity.breakdown.profitability = this._calculateRatioSimilarity(targetNetMargin, peerNetMargin);

        // Leverage similarity (15% weight)
        const targetBalance = targetData.statements?.balanceSheet?.[0];
        const peerBalance = peerData.statements?.balanceSheet?.[0];
        
        if (targetBalance && peerBalance) {
          const targetDebtRatio = (targetBalance.totalDebt || 0) / (targetBalance.totalAssets || 1);
          const peerDebtRatio = (peerBalance.totalDebt || 0) / (peerBalance.totalAssets || 1);
          similarity.breakdown.leverage = this._calculateRatioSimilarity(targetDebtRatio, peerDebtRatio);

          // Liquidity similarity (15% weight)
          const targetCurrentRatio = (targetBalance.totalCurrentAssets || 0) / (targetBalance.totalCurrentLiabilities || 1);
          const peerCurrentRatio = (peerBalance.totalCurrentAssets || 0) / (peerBalance.totalCurrentLiabilities || 1);
          similarity.breakdown.liquidity = this._calculateRatioSimilarity(targetCurrentRatio, peerCurrentRatio);
        }
      }

      // Calculate weighted overall score
      similarity.overallScore = (
        similarity.breakdown.industry * 0.30 +
        similarity.breakdown.size * 0.25 +
        similarity.breakdown.profitability * 0.15 +
        similarity.breakdown.leverage * 0.15 +
        similarity.breakdown.liquidity * 0.15
      );

      return similarity;

    } catch (error) {
      console.error(`[IntelligentFinancialService] Similarity calculation failed:`, error.message);
      return { overallScore: 0, breakdown: similarity.breakdown };
    }
  }

  /**
   * Calculate similarity between two financial ratios
   * @param {number} ratio1 - First ratio
   * @param {number} ratio2 - Second ratio
   * @returns {number} Similarity score (0-1)
   * @private
   */
  _calculateRatioSimilarity(ratio1, ratio2) {
    if (ratio1 === 0 && ratio2 === 0) return 1.0;
    if (ratio1 === 0 || ratio2 === 0) return 0.0;

    const ratio = Math.min(Math.abs(ratio1), Math.abs(ratio2)) / Math.max(Math.abs(ratio1), Math.abs(ratio2));
    return ratio;
  }

  /**
   * Generate peer analysis insights
   * @param {Object} peerAnalysis - Peer analysis results
   * @returns {Array} Array of insights
   * @private
   */
  _generatePeerInsights(peerAnalysis) {
    const insights = [];

    if (peerAnalysis.peers.length === 0) {
      insights.push("No similar peer companies found with current criteria");
      return insights;
    }

    const avgSimilarity = peerAnalysis.peers.reduce((sum, peer) => sum + peer.similarityScore, 0) / peerAnalysis.peers.length;
    insights.push(`Average peer similarity score: ${(avgSimilarity * 100).toFixed(1)}%`);

    const industryPeers = peerAnalysis.peers.filter(peer => 
      peer.industry === peerAnalysis.targetCompany.industry
    );
    if (industryPeers.length > 0) {
      insights.push(`${industryPeers.length} peers found in same industry (${peerAnalysis.targetCompany.industry})`);
    }

    const topPeer = peerAnalysis.peers[0];
    if (topPeer) {
      insights.push(`Most similar peer: ${topPeer.name} (${(topPeer.similarityScore * 100).toFixed(1)}% similarity)`);
    }

    return insights;
  }

  /**
   * Calculate financial health risk component
   * @param {Object} financialData - Company financial data
   * @returns {Promise<Object>} Financial health risk assessment
   * @private
   */
  async _calculateFinancialHealthRisk(financialData) {
    const risk = {
      score: 50, // Default medium risk
      level: 'Medium',
      factors: []
    };

    try {
      const statements = financialData.statements;
      if (!statements?.incomeStatement?.[0]) {
        risk.factors.push('Insufficient financial data for health assessment');
        risk.score = 70;
        risk.level = 'High';
        return risk;
      }

      const latestIncome = statements.incomeStatement[0];
      const latestBalance = statements.balanceSheet?.[0];

      // Revenue trend analysis
      if (statements.incomeStatement.length >= 2) {
        const currentRevenue = latestIncome.revenue || 0;
        const previousRevenue = statements.incomeStatement[1].revenue || 0;
        
        if (previousRevenue > 0) {
          const revenueGrowth = (currentRevenue - previousRevenue) / previousRevenue;
          if (revenueGrowth < -0.1) {
            risk.factors.push('Declining revenue trend (>10% decrease)');
            risk.score += 15;
          } else if (revenueGrowth > 0.1) {
            risk.factors.push('Strong revenue growth (>10% increase)');
            risk.score -= 10;
          }
        }
      }

      // Profitability analysis
      const netIncome = latestIncome.netIncome || 0;
      const revenue = latestIncome.revenue || 1;
      const netMargin = netIncome / revenue;

      if (netMargin < 0) {
        risk.factors.push('Negative net profit margin');
        risk.score += 20;
      } else if (netMargin > 0.15) {
        risk.factors.push('Strong profit margins (>15%)');
        risk.score -= 10;
      }

      // Asset quality
      if (latestBalance) {
        const totalAssets = latestBalance.totalAssets || 0;
        const cash = latestBalance.cashAndCashEquivalents || 0;
        
        if (totalAssets > 0) {
          const cashRatio = cash / totalAssets;
          if (cashRatio < 0.05) {
            risk.factors.push('Low cash reserves relative to assets');
            risk.score += 10;
          } else if (cashRatio > 0.2) {
            risk.factors.push('Strong cash position');
            risk.score -= 5;
          }
        }
      }

      // Determine risk level
      if (risk.score >= 70) {
        risk.level = 'High';
      } else if (risk.score >= 40) {
        risk.level = 'Medium';
      } else {
        risk.level = 'Low';
      }

      return risk;

    } catch (error) {
      console.error(`[IntelligentFinancialService] Financial health risk calculation failed:`, error.message);
      risk.factors.push('Error calculating financial health risk');
      risk.score = 60;
      risk.level = 'Medium';
      return risk;
    }
  }

  /**
   * Calculate liquidity risk component
   * @param {Object} financialData - Company financial data
   * @returns {Promise<Object>} Liquidity risk assessment
   * @private
   */
  async _calculateLiquidityRisk(financialData) {
    const risk = {
      score: 50,
      level: 'Medium',
      factors: []
    };

    try {
      const balanceSheet = financialData.statements?.balanceSheet?.[0];
      if (!balanceSheet) {
        risk.factors.push('No balance sheet data available for liquidity analysis');
        risk.score = 60;
        return risk;
      }

      // Current ratio analysis
      const currentAssets = balanceSheet.totalCurrentAssets || 0;
      const currentLiabilities = balanceSheet.totalCurrentLiabilities || 1;
      const currentRatio = currentAssets / currentLiabilities;

      if (currentRatio < 1.0) {
        risk.factors.push('Current ratio below 1.0 - potential liquidity issues');
        risk.score += 25;
      } else if (currentRatio > 2.0) {
        risk.factors.push('Strong current ratio (>2.0)');
        risk.score -= 15;
      }

      // Cash position analysis
      const cash = balanceSheet.cashAndCashEquivalents || 0;
      const totalAssets = balanceSheet.totalAssets || 1;
      const cashRatio = cash / totalAssets;

      if (cashRatio < 0.05) {
        risk.factors.push('Low cash reserves (<5% of assets)');
        risk.score += 15;
      } else if (cashRatio > 0.15) {
        risk.factors.push('Adequate cash reserves (>15% of assets)');
        risk.score -= 10;
      }

      // Quick ratio (if we have inventory data)
      // Note: This is simplified as we may not have detailed current asset breakdown
      const quickRatio = currentRatio * 0.8; // Rough approximation
      if (quickRatio < 0.8) {
        risk.factors.push('Estimated quick ratio below 0.8');
        risk.score += 10;
      }

      // Determine risk level
      if (risk.score >= 70) {
        risk.level = 'High';
      } else if (risk.score >= 40) {
        risk.level = 'Medium';
      } else {
        risk.level = 'Low';
      }

      return risk;

    } catch (error) {
      console.error(`[IntelligentFinancialService] Liquidity risk calculation failed:`, error.message);
      risk.factors.push('Error calculating liquidity risk');
      return risk;
    }
  }

  /**
   * Calculate leverage risk component
   * @param {Object} financialData - Company financial data
   * @returns {Promise<Object>} Leverage risk assessment
   * @private
   */
  async _calculateLeverageRisk(financialData) {
    const risk = {
      score: 50,
      level: 'Medium',
      factors: []
    };

    try {
      const balanceSheet = financialData.statements?.balanceSheet?.[0];
      if (!balanceSheet) {
        risk.factors.push('No balance sheet data available for leverage analysis');
        risk.score = 60;
        return risk;
      }

      // Debt-to-equity ratio
      const totalDebt = balanceSheet.totalDebt || 0;
      const equity = balanceSheet.totalStockholdersEquity || 1;
      const debtToEquity = totalDebt / equity;

      if (debtToEquity > 2.0) {
        risk.factors.push('High debt-to-equity ratio (>2.0)');
        risk.score += 25;
      } else if (debtToEquity < 0.5) {
        risk.factors.push('Conservative debt levels (<0.5 D/E)');
        risk.score -= 15;
      }

      // Debt-to-assets ratio
      const totalAssets = balanceSheet.totalAssets || 1;
      const debtToAssets = totalDebt / totalAssets;

      if (debtToAssets > 0.6) {
        risk.factors.push('High debt-to-assets ratio (>60%)');
        risk.score += 20;
      } else if (debtToAssets < 0.3) {
        risk.factors.push('Low debt-to-assets ratio (<30%)');
        risk.score -= 10;
      }

      // Interest coverage (if available)
      const incomeStatement = financialData.statements?.incomeStatement?.[0];
      if (incomeStatement) {
        const operatingIncome = incomeStatement.operatingIncome || 0;
        const interestExpense = incomeStatement.interestExpense || 1;
        
        if (interestExpense > 0) {
          const interestCoverage = operatingIncome / interestExpense;
          if (interestCoverage < 2.0) {
            risk.factors.push('Low interest coverage ratio (<2.0)');
            risk.score += 15;
          } else if (interestCoverage > 5.0) {
            risk.factors.push('Strong interest coverage (>5.0)');
            risk.score -= 10;
          }
        }
      }

      // Determine risk level
      if (risk.score >= 70) {
        risk.level = 'High';
      } else if (risk.score >= 40) {
        risk.level = 'Medium';
      } else {
        risk.level = 'Low';
      }

      return risk;

    } catch (error) {
      console.error(`[IntelligentFinancialService] Leverage risk calculation failed:`, error.message);
      risk.factors.push('Error calculating leverage risk');
      return risk;
    }
  }

  /**
   * Calculate profitability risk component
   * @param {Object} financialData - Company financial data
   * @returns {Promise<Object>} Profitability risk assessment
   * @private
   */
  async _calculateProfitabilityRisk(financialData) {
    const risk = {
      score: 50,
      level: 'Medium',
      factors: []
    };

    try {
      const incomeStatements = financialData.statements?.incomeStatement;
      if (!incomeStatements?.[0]) {
        risk.factors.push('No income statement data available');
        risk.score = 60;
        return risk;
      }

      const latest = incomeStatements[0];
      
      // Net margin analysis
      const netMargin = (latest.netIncome || 0) / (latest.revenue || 1);
      if (netMargin < 0) {
        risk.factors.push('Negative net profit margin');
        risk.score += 30;
      } else if (netMargin < 0.05) {
        risk.factors.push('Low net profit margin (<5%)');
        risk.score += 15;
      } else if (netMargin > 0.15) {
        risk.factors.push('Strong net profit margin (>15%)');
        risk.score -= 15;
      }

      // Operating margin analysis
      const operatingMargin = (latest.operatingIncome || 0) / (latest.revenue || 1);
      if (operatingMargin < 0) {
        risk.factors.push('Negative operating margin');
        risk.score += 20;
      } else if (operatingMargin > 0.2) {
        risk.factors.push('Strong operating margin (>20%)');
        risk.score -= 10;
      }

      // Profitability trend (if multiple periods available)
      if (incomeStatements.length >= 2) {
        const currentNet = latest.netIncome || 0;
        const previousNet = incomeStatements[1].netIncome || 0;
        
        if (previousNet !== 0) {
          const netIncomeGrowth = (currentNet - previousNet) / Math.abs(previousNet);
          if (netIncomeGrowth < -0.2) {
            risk.factors.push('Declining profitability trend (>20% decrease)');
            risk.score += 15;
          } else if (netIncomeGrowth > 0.2) {
            risk.factors.push('Growing profitability (>20% increase)');
            risk.score -= 10;
          }
        }
      }

      // Determine risk level
      if (risk.score >= 70) {
        risk.level = 'High';
      } else if (risk.score >= 40) {
        risk.level = 'Medium';
      } else {
        risk.level = 'Low';
      }

      return risk;

    } catch (error) {
      console.error(`[IntelligentFinancialService] Profitability risk calculation failed:`, error.message);
      risk.factors.push('Error calculating profitability risk');
      return risk;
    }
  }

  /**
   * Calculate weighted overall risk score
   * @param {Object} riskComponents - Individual risk components
   * @returns {number} Weighted risk score (0-100)
   * @private
   */
  _calculateWeightedRiskScore(riskComponents) {
    let weightedScore = 0;
    let totalWeight = 0;

    for (const [component, data] of Object.entries(riskComponents)) {
      if (data.score !== undefined && data.weight !== undefined) {
        weightedScore += data.score * data.weight;
        totalWeight += data.weight;
      }
    }

    return totalWeight > 0 ? Math.round(weightedScore / totalWeight) : 50;
  }

  /**
   * Determine risk level from numeric score
   * @param {number} score - Risk score (0-100)
   * @returns {string} Risk level
   * @private
   */
  _determineRiskLevel(score) {
    if (score >= 70) return 'High';
    if (score >= 40) return 'Medium';
    return 'Low';
  }

  /**
   * Calculate peer risk comparison
   * @param {string} symbol - Target company symbol
   * @param {number} targetRiskScore - Target company risk score
   * @returns {Promise<Object>} Peer risk comparison
   * @private
   */
  async _calculatePeerRiskComparison(symbol, targetRiskScore) {
    try {
      const peers = await this.identifyPeerCompanies(symbol, {
        maxPeers: 5,
        includeFinancials: false
      });

      const peerRiskScores = [];
      for (const peer of peers.peers.slice(0, 3)) { // Limit to top 3 peers for performance
        try {
          const peerRisk = await this.buildComprehensiveRiskScore(peer.symbol, {
            includePeerComparison: false
          });
          peerRiskScores.push({
            symbol: peer.symbol,
            name: peer.name,
            riskScore: peerRisk.overallRiskScore,
            riskLevel: peerRisk.riskLevel
          });
        } catch (error) {
          console.warn(`[IntelligentFinancialService] Peer risk calculation failed for ${peer.symbol}`);
        }
      }

      if (peerRiskScores.length === 0) {
        return {
          available: false,
          message: 'No peer risk data available for comparison'
        };
      }

      const avgPeerRisk = peerRiskScores.reduce((sum, peer) => sum + peer.riskScore, 0) / peerRiskScores.length;
      const relativeToPeers = targetRiskScore - avgPeerRisk;

      return {
        available: true,
        targetRiskScore,
        averagePeerRisk: Math.round(avgPeerRisk),
        relativeToPeers: Math.round(relativeToPeers),
        comparison: relativeToPeers > 10 ? 'Higher risk than peers' : 
                   relativeToPeers < -10 ? 'Lower risk than peers' : 
                   'Similar risk to peers',
        peerRiskScores
      };

    } catch (error) {
      console.error(`[IntelligentFinancialService] Peer risk comparison failed:`, error.message);
      return {
        available: false,
        error: error.message
      };
    }
  }

  /**
   * Generate risk insights
   * @param {Object} riskAssessment - Risk assessment results
   * @returns {Array} Array of insights
   * @private
   */
  _generateRiskInsights(riskAssessment) {
    const insights = [];

    // Overall risk insight
    insights.push(`Overall financial risk level: ${riskAssessment.riskLevel} (${riskAssessment.overallRiskScore}/100)`);

    // Component-specific insights
    const components = riskAssessment.riskComponents;
    const highRiskComponents = Object.entries(components)
      .filter(([_, data]) => data.level === 'High')
      .map(([name, _]) => name);

    if (highRiskComponents.length > 0) {
      insights.push(`High risk areas: ${highRiskComponents.join(', ')}`);
    }

    const lowRiskComponents = Object.entries(components)
      .filter(([_, data]) => data.level === 'Low')
      .map(([name, _]) => name);

    if (lowRiskComponents.length > 0) {
      insights.push(`Strong areas: ${lowRiskComponents.join(', ')}`);
    }

    // Peer comparison insight
    if (riskAssessment.peerComparison?.available) {
      insights.push(`Risk vs peers: ${riskAssessment.peerComparison.comparison}`);
    }

    return insights;
  }

  /**
   * Generate risk recommendations
   * @param {Object} riskAssessment - Risk assessment results
   * @returns {Array} Array of recommendations
   * @private
   */
  _generateRiskRecommendations(riskAssessment) {
    const recommendations = [];

    // Overall recommendations based on risk level
    switch (riskAssessment.riskLevel) {
      case 'High':
        recommendations.push('Immediate financial review and risk mitigation required');
        recommendations.push('Consider engaging financial advisors for restructuring options');
        break;
      case 'Medium':
        recommendations.push('Monitor key financial metrics closely');
        recommendations.push('Develop contingency plans for identified risk areas');
        break;
      case 'Low':
        recommendations.push('Maintain current financial management practices');
        recommendations.push('Continue regular financial health monitoring');
        break;
    }

    // Component-specific recommendations
    const components = riskAssessment.riskComponents;
    
    if (components.liquidity?.level === 'High') {
      recommendations.push('Improve liquidity position through cash management or credit facilities');
    }
    
    if (components.leverage?.level === 'High') {
      recommendations.push('Consider debt reduction strategies and refinancing options');
    }
    
    if (components.profitability?.level === 'High') {
      recommendations.push('Focus on cost reduction and revenue optimization initiatives');
    }

    return recommendations;
  }

  /**
   * Calculate risk assessment confidence
   * @param {Object} financialData - Original financial data
   * @param {Object} riskAssessment - Risk assessment results
   * @returns {Object} Confidence metrics
   * @private
   */
  _calculateRiskConfidence(financialData, riskAssessment) {
    let dataQualityScore = 0.5; // Base score
    let completenessScore = 0;
    let totalComponents = 0;

    // Check data completeness
    if (financialData.statements?.incomeStatement?.[0]) {
      completenessScore += 0.3;
    }
    if (financialData.statements?.balanceSheet?.[0]) {
      completenessScore += 0.3;
    }
    if (financialData.profile) {
      completenessScore += 0.2;
    }
    if (financialData.statements?.incomeStatement?.length >= 2) {
      completenessScore += 0.2; // Historical data available
    }

    // Check component calculation success
    for (const [component, data] of Object.entries(riskAssessment.riskComponents)) {
      totalComponents++;
      if (!data.factors.some(factor => factor.includes('Error'))) {
        dataQualityScore += 0.1;
      }
    }

    const overallConfidence = (dataQualityScore + completenessScore) / 2;

    return {
      overall: Math.min(1, overallConfidence),
      dataCompleteness: completenessScore,
      calculationReliability: dataQualityScore,
      level: overallConfidence > 0.8 ? 'High' : 
             overallConfidence > 0.6 ? 'Medium' : 'Low'
    };
  }

  /**
   * Test the intelligent financial service capabilities
   * @returns {Promise<Object>} Test results
   */
  async testIntelligentFinancialService() {
    console.log('[IntelligentFinancialService] Testing service capabilities...');

    const testResults = {
      timestamp: new Date().toISOString(),
      capabilities: {},
      overallStatus: 'unknown'
    };

    // Test smart company lookup
    try {
      const lookupTest = await this.smartCompanyLookup('AAPL', {
        includeFinancials: false,
        includeRiskScore: false,
        maxResults: 1
      });
      testResults.capabilities.smartLookup = {
        status: 'working',
        resultsFound: lookupTest.totalResults,
        confidence: lookupTest.confidence
      };
    } catch (error) {
      testResults.capabilities.smartLookup = {
        status: 'error',
        error: error.message
      };
    }

    // Test peer identification
    try {
      const peerTest = await this.identifyPeerCompanies('AAPL', {
        maxPeers: 2,
        includeFinancials: false
      });
      testResults.capabilities.peerIdentification = {
        status: 'working',
        peersFound: peerTest.peersFound
      };
    } catch (error) {
      testResults.capabilities.peerIdentification = {
        status: 'error',
        error: error.message
      };
    }

    // Test risk scoring
    try {
      const riskTest = await this.buildComprehensiveRiskScore('AAPL', {
        includePeerComparison: false,
        includeHistoricalTrends: false
      });
      testResults.capabilities.riskScoring = {
        status: 'working',
        riskLevel: riskTest.riskLevel,
        riskScore: riskTest.overallRiskScore
      };
    } catch (error) {
      testResults.capabilities.riskScoring = {
        status: 'error',
        error: error.message
      };
    }

    // Determine overall status
    const workingCapabilities = Object.values(testResults.capabilities)
      .filter(cap => cap.status === 'working').length;
    const totalCapabilities = Object.keys(testResults.capabilities).length;

    testResults.overallStatus = workingCapabilities > 0 ? 'operational' : 'failed';
    testResults.workingCapabilities = `${workingCapabilities}/${totalCapabilities}`;

    console.log(`[IntelligentFinancialService] Test completed: ${testResults.workingCapabilities} capabilities working`);
    return testResults;
  }
}

module.exports = IntelligentFinancialService;