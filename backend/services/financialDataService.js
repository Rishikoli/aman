/**
 * Financial Data Service
 * Orchestrates multiple data sources with fallback logic
 */

const FMPClient = require('./fmpClient');
const AlphaVantageClient = require('./alphaVantageClient');
const PolygonClient = require('./polygonClient');
const { query } = require('../database');

class FinancialDataService {
  constructor() {
    this.fmpClient = new FMPClient();
    this.alphaVantageClient = new AlphaVantageClient();
    this.polygonClient = new PolygonClient();
    this.primarySource = 'FMP';
    this.fallbackSources = ['AlphaVantage', 'Polygon'];
  }

  /**
   * Get company financial data with fallback logic
   * @param {string} symbol - Stock ticker symbol
   * @param {Object} options - Options for data retrieval
   * @returns {Promise<Object>} Financial data from available source
   */
  async getCompanyFinancialData(symbol, options = {}) {
    const {
      period = 'annual',
      limit = 5,
      includeProfile = true,
      includeStatements = true,
      includeRatios = true,
      includeMetrics = true,
      saveToDatabase = true
    } = options;

    console.log(`[FinancialDataService] Fetching financial data for ${symbol}`);

    let result = null;
    let dataSource = null;
    let errors = [];

    // Try primary source (FMP) first
    try {
      console.log(`[FinancialDataService] Trying primary source: ${this.primarySource}`);
      
      if (includeProfile && includeStatements) {
        result = await this.fmpClient.getComprehensiveFinancialData(symbol, {
          period,
          limit,
          includeRatios,
          includeMetrics
        });
      } else if (includeProfile) {
        result = {
          profile: await this.fmpClient.getCompanyProfile(symbol),
          metadata: {
            symbol: symbol.toUpperCase(),
            period,
            limit,
            retrievedAt: new Date().toISOString(),
            source: 'FMP'
          }
        };
      } else if (includeStatements) {
        result = {
          statements: await this.fmpClient.getFinancialStatements(symbol, period, limit),
          metadata: {
            symbol: symbol.toUpperCase(),
            period,
            limit,
            retrievedAt: new Date().toISOString(),
            source: 'FMP'
          }
        };
      }

      dataSource = 'FMP';
      console.log(`[FinancialDataService] Successfully retrieved data from ${dataSource}`);

    } catch (error) {
      console.error(`[FinancialDataService] Primary source failed:`, error.message);
      errors.push({ source: 'FMP', error: error.message });

      // Try fallback sources
      for (const fallbackSource of this.fallbackSources) {
        try {
          console.log(`[FinancialDataService] Trying fallback source: ${fallbackSource}`);
          
          if (fallbackSource === 'AlphaVantage') {
            result = await this._getDataFromAlphaVantage(symbol, options);
            dataSource = 'AlphaVantage';
            console.log(`[FinancialDataService] Successfully retrieved data from ${dataSource}`);
            break;
          } else if (fallbackSource === 'Polygon') {
            result = await this._getDataFromPolygon(symbol, options);
            dataSource = 'Polygon';
            console.log(`[FinancialDataService] Successfully retrieved data from ${dataSource}`);
            break;
          }

        } catch (fallbackError) {
          console.error(`[FinancialDataService] Fallback source ${fallbackSource} failed:`, fallbackError.message);
          errors.push({ source: fallbackSource, error: fallbackError.message });
        }
      }
    }

    // If no source worked, throw error
    if (!result) {
      const errorMessage = `Failed to retrieve financial data for ${symbol} from all sources: ${errors.map(e => `${e.source}: ${e.error}`).join('; ')}`;
      throw new Error(errorMessage);
    }

    // Add source information to result
    result.dataSource = dataSource;
    result.errors = errors.length > 0 ? errors : undefined;

    // Save to database if requested
    if (saveToDatabase) {
      try {
        await this._saveFinancialDataToDatabase(result);
        console.log(`[FinancialDataService] Financial data saved to database for ${symbol}`);
      } catch (dbError) {
        console.error(`[FinancialDataService] Failed to save to database:`, dbError.message);
        // Don't throw error, just log it
      }
    }

    return result;
  }

  /**
   * Get data from Alpha Vantage with proper formatting
   * @param {string} symbol - Stock ticker symbol
   * @param {Object} options - Options for data retrieval
   * @returns {Promise<Object>} Formatted financial data
   * @private
   */
  async _getDataFromAlphaVantage(symbol, options) {
    const {
      period = 'annual',
      limit = 5,
      includeProfile = true,
      includeStatements = true
    } = options;

    const result = {
      metadata: {
        symbol: symbol.toUpperCase(),
        period,
        limit,
        retrievedAt: new Date().toISOString(),
        source: 'AlphaVantage'
      }
    };

    if (includeProfile) {
      result.profile = await this.alphaVantageClient.getCompanyOverview(symbol);
    }

    if (includeStatements) {
      const [incomeStatement, balanceSheet, cashFlow] = await Promise.all([
        this.alphaVantageClient.getIncomeStatement(symbol),
        this.alphaVantageClient.getBalanceSheet(symbol),
        this.alphaVantageClient.getCashFlowStatement(symbol)
      ]);

      result.statements = {
        incomeStatement: incomeStatement.slice(0, limit),
        balanceSheet: balanceSheet.slice(0, limit),
        cashFlow: cashFlow.slice(0, limit)
      };
    }

    return result;
  }

  /**
   * Get data from Polygon.io with proper formatting
   * @param {string} symbol - Stock ticker symbol
   * @param {Object} options - Options for data retrieval
   * @returns {Promise<Object>} Formatted financial data
   * @private
   */
  async _getDataFromPolygon(symbol, options) {
    const {
      period = 'annual',
      limit = 5,
      includeProfile = true,
      includeStatements = true
    } = options;

    const result = {
      metadata: {
        symbol: symbol.toUpperCase(),
        period,
        limit,
        retrievedAt: new Date().toISOString(),
        source: 'Polygon'
      }
    };

    if (includeProfile) {
      result.profile = await this.polygonClient.getCompanyDetails(symbol);
    }

    if (includeStatements) {
      const timeframe = period === 'annual' ? 'annual' : 'quarterly';
      const financials = await this.polygonClient.getStockFinancials(symbol, {
        timeframe,
        limit
      });

      // Group financials by type (similar to FMP structure)
      result.statements = {
        incomeStatement: financials,
        balanceSheet: financials, // Polygon combines all statements
        cashFlow: financials
      };
    }

    return result;
  }

  /**
   * Save financial data to database
   * @param {Object} financialData - Financial data to save
   * @returns {Promise<void>}
   * @private
   */
  async _saveFinancialDataToDatabase(financialData) {
    const { profile, statements, metadata } = financialData;

    try {
      // Save or update company profile
      if (profile) {
        await this._saveCompanyProfile(profile, metadata);
      }

      // Save financial statements
      if (statements) {
        await this._saveFinancialStatements(statements, metadata);
      }

    } catch (error) {
      console.error('[FinancialDataService] Database save error:', error.message);
      throw error;
    }
  }

  /**
   * Save company profile to database
   * @param {Object} profile - Company profile data
   * @param {Object} metadata - Metadata about the data source
   * @returns {Promise<void>}
   * @private
   */
  async _saveCompanyProfile(profile, metadata) {
    const companyData = {
      name: profile.companyName || profile.name,
      ticker_symbol: profile.symbol,
      industry: profile.industry,
      sector: profile.sector,
      company_size: this._determineCompanySize(profile.marketCap),
      headquarters_location: profile.city && profile.state ? `${profile.city}, ${profile.state}` : null,
      employee_count: profile.fullTimeEmployees || null,
      annual_revenue: profile.revenueTTM || null,
      market_cap: profile.marketCap || null,
      description: profile.description,
      website_url: profile.website || profile.officialSite,
      updated_at: new Date()
    };

    // Check if company exists
    const existingCompany = await query(
      'SELECT id FROM companies WHERE ticker_symbol = $1',
      [profile.symbol]
    );

    if (existingCompany.rows.length > 0) {
      // Update existing company
      const updateFields = Object.keys(companyData)
        .filter(key => companyData[key] !== null)
        .map((key, index) => `${key} = $${index + 2}`)
        .join(', ');
      
      const updateValues = Object.keys(companyData)
        .filter(key => companyData[key] !== null)
        .map(key => companyData[key]);

      await query(
        `UPDATE companies SET ${updateFields} WHERE ticker_symbol = $1`,
        [profile.symbol, ...updateValues]
      );

      console.log(`[FinancialDataService] Updated company profile for ${profile.symbol}`);
    } else {
      // Insert new company
      const fields = Object.keys(companyData).join(', ');
      const placeholders = Object.keys(companyData).map((_, index) => `$${index + 1}`).join(', ');
      const values = Object.values(companyData);

      await query(
        `INSERT INTO companies (${fields}) VALUES (${placeholders})`,
        values
      );

      console.log(`[FinancialDataService] Inserted new company profile for ${profile.symbol}`);
    }
  }

  /**
   * Save financial statements to database
   * @param {Object} statements - Financial statements data
   * @param {Object} metadata - Metadata about the data source
   * @returns {Promise<void>}
   * @private
   */
  async _saveFinancialStatements(statements, metadata) {
    // Get company ID
    const companyResult = await query(
      'SELECT id FROM companies WHERE ticker_symbol = $1',
      [metadata.symbol]
    );

    if (companyResult.rows.length === 0) {
      throw new Error(`Company not found for symbol: ${metadata.symbol}`);
    }

    const companyId = companyResult.rows[0].id;

    // Save financial data for each period
    if (statements.incomeStatement && statements.incomeStatement.length > 0) {
      for (const statement of statements.incomeStatement) {
        await this._saveFinancialDataRecord(companyId, statement, metadata);
      }
    }
  }

  /**
   * Save individual financial data record
   * @param {string} companyId - Company UUID
   * @param {Object} statement - Financial statement data
   * @param {Object} metadata - Metadata about the data source
   * @returns {Promise<void>}
   * @private
   */
  async _saveFinancialDataRecord(companyId, statement, metadata) {
    const fiscalYear = parseInt(statement.calendarYear) || new Date(statement.date).getFullYear();
    const fiscalQuarter = statement.period === 'FY' ? null : this._extractQuarter(statement.period);

    const financialData = {
      company_id: companyId,
      fiscal_year: fiscalYear,
      fiscal_quarter: fiscalQuarter,
      revenue: statement.revenue || 0,
      net_income: statement.netIncome || 0,
      total_assets: statement.totalAssets || null,
      total_liabilities: statement.totalLiabilities || null,
      shareholders_equity: statement.totalStockholdersEquity || statement.totalEquity || null,
      cash_and_equivalents: statement.cashAndCashEquivalents || statement.cashAtEndOfPeriod || null,
      total_debt: statement.totalDebt || null,
      operating_cash_flow: statement.operatingCashFlow || statement.netCashProvidedByOperatingActivities || null,
      free_cash_flow: statement.freeCashFlow || null,
      gross_margin: statement.grossProfitRatio || null,
      operating_margin: statement.operatingIncomeRatio || null,
      net_margin: statement.netIncomeRatio || null,
      roe: null, // Will be calculated later
      roa: null, // Will be calculated later
      debt_to_equity: null, // Will be calculated later
      current_ratio: null, // Will be calculated later
      quick_ratio: null, // Will be calculated later
      metadata: {
        source: metadata.source,
        retrievedAt: metadata.retrievedAt,
        originalData: {
          date: statement.date,
          period: statement.period,
          reportedCurrency: statement.reportedCurrency
        }
      },
      updated_at: new Date()
    };

    // Check if record exists
    const existingRecord = await query(
      'SELECT id FROM financial_data WHERE company_id = $1 AND fiscal_year = $2 AND fiscal_quarter IS NOT DISTINCT FROM $3',
      [companyId, fiscalYear, fiscalQuarter]
    );

    if (existingRecord.rows.length > 0) {
      // Update existing record
      const updateFields = Object.keys(financialData)
        .filter(key => financialData[key] !== null)
        .map((key, index) => `${key} = $${index + 4}`)
        .join(', ');
      
      const updateValues = Object.keys(financialData)
        .filter(key => financialData[key] !== null)
        .map(key => financialData[key]);

      await query(
        `UPDATE financial_data SET ${updateFields} WHERE company_id = $1 AND fiscal_year = $2 AND fiscal_quarter IS NOT DISTINCT FROM $3`,
        [companyId, fiscalYear, fiscalQuarter, ...updateValues]
      );

      console.log(`[FinancialDataService] Updated financial data for ${metadata.symbol} ${fiscalYear}${fiscalQuarter ? `Q${fiscalQuarter}` : ''}`);
    } else {
      // Insert new record
      const fields = Object.keys(financialData).join(', ');
      const placeholders = Object.keys(financialData).map((_, index) => `$${index + 1}`).join(', ');
      const values = Object.values(financialData);

      await query(
        `INSERT INTO financial_data (${fields}) VALUES (${placeholders})`,
        values
      );

      console.log(`[FinancialDataService] Inserted financial data for ${metadata.symbol} ${fiscalYear}${fiscalQuarter ? `Q${fiscalQuarter}` : ''}`);
    }
  }

  /**
   * Determine company size based on market cap
   * @param {number} marketCap - Market capitalization
   * @returns {string} Company size category
   * @private
   */
  _determineCompanySize(marketCap) {
    if (!marketCap) return null;
    
    if (marketCap < 300000000) return 'startup';
    if (marketCap < 2000000000) return 'small';
    if (marketCap < 10000000000) return 'medium';
    if (marketCap < 200000000000) return 'large';
    return 'enterprise';
  }

  /**
   * Extract quarter number from period string
   * @param {string} period - Period string (e.g., 'Q1', 'Q2')
   * @returns {number|null} Quarter number
   * @private
   */
  _extractQuarter(period) {
    if (!period) return null;
    const match = period.match(/Q(\d)/);
    return match ? parseInt(match[1]) : null;
  }

  /**
   * Test all data source connections
   * @returns {Promise<Object>} Connection test results
   */
  async testConnections() {
    console.log('[FinancialDataService] Testing all data source connections...');

    const results = {
      timestamp: new Date().toISOString(),
      sources: {}
    };

    // Test FMP
    try {
      const fmpResult = await this.fmpClient.testConnection();
      results.sources.FMP = fmpResult;
    } catch (error) {
      results.sources.FMP = {
        success: false,
        message: `FMP connection failed: ${error.message}`,
        error: error.message
      };
    }

    // Test Alpha Vantage
    try {
      const avResult = await this.alphaVantageClient.testConnection();
      results.sources.AlphaVantage = avResult;
    } catch (error) {
      results.sources.AlphaVantage = {
        success: false,
        message: `Alpha Vantage connection failed: ${error.message}`,
        error: error.message
      };
    }

    // Test Polygon.io
    try {
      const polygonResult = await this.polygonClient.testConnection();
      results.sources.Polygon = polygonResult;
    } catch (error) {
      results.sources.Polygon = {
        success: false,
        message: `Polygon.io connection failed: ${error.message}`,
        error: error.message
      };
    }

    // Overall status
    const successfulSources = Object.values(results.sources).filter(source => source.success);
    results.overallStatus = successfulSources.length > 0 ? 'operational' : 'failed';
    results.availableSources = successfulSources.length;
    results.totalSources = Object.keys(results.sources).length;

    console.log(`[FinancialDataService] Connection test complete: ${results.availableSources}/${results.totalSources} sources available`);

    return results;
  }

  /**
   * Search for companies across all data sources
   * @param {string} query - Search query
   * @param {number} limit - Maximum results
   * @returns {Promise<Array>} Search results
   */
  async searchCompanies(query, limit = 10) {
    console.log(`[FinancialDataService] Searching for companies: ${query}`);

    let results = [];
    let errors = [];

    // Try FMP first
    try {
      const fmpResults = await this.fmpClient.searchCompanies(query, limit);
      results = results.concat(fmpResults.map(result => ({
        ...result,
        source: 'FMP'
      })));
    } catch (error) {
      console.error('[FinancialDataService] FMP search failed:', error.message);
      errors.push({ source: 'FMP', error: error.message });
    }

    // Try Polygon if FMP didn't return enough results
    if (results.length < limit) {
      try {
        const polygonResults = await this.polygonClient.searchTickers(query, {
          limit: limit - results.length
        });
        results = results.concat(polygonResults.map(result => ({
          symbol: result.symbol,
          name: result.name,
          exchange: result.primaryExchange,
          exchangeShortName: result.primaryExchange,
          source: 'Polygon'
        })));
      } catch (error) {
        console.error('[FinancialDataService] Polygon search failed:', error.message);
        errors.push({ source: 'Polygon', error: error.message });
      }
    }

    // Remove duplicates and limit results
    const uniqueResults = results.filter((result, index, self) => 
      index === self.findIndex(r => r.symbol === result.symbol)
    ).slice(0, limit);

    return {
      results: uniqueResults,
      totalResults: uniqueResults.length,
      errors: errors.length > 0 ? errors : undefined
    };
  }
}

module.exports = FinancialDataService;