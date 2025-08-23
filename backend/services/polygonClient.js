/**
 * Polygon.io API Client
 * Third backup data source for financial information
 */

const axios = require('axios');
const { getConfig } = require('../utils/env-config');

class PolygonClient {
  constructor() {
    this.config = getConfig();
    this.baseURL = 'https://api.polygon.io';
    this.apiKey = process.env.POLYGON_API_KEY || 'demo';
    this.rateLimitDelay = 12000; // 12 seconds between requests for free tier (5 requests per minute)
    this.lastRequestTime = 0;
    
    this.client = axios.create({
      baseURL: this.baseURL,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
        'User-Agent': 'AMAN-Finance-Agent/1.0'
      }
    });

    // Add request interceptor for rate limiting
    this.client.interceptors.request.use(async (config) => {
      await this._enforceRateLimit();
      return config;
    });
  }

  /**
   * Enforce rate limiting for API requests
   * @private
   */
  async _enforceRateLimit() {
    const now = Date.now();
    const timeSinceLastRequest = now - this.lastRequestTime;
    
    if (timeSinceLastRequest < this.rateLimitDelay) {
      const waitTime = this.rateLimitDelay - timeSinceLastRequest;
      console.log(`[Polygon] Rate limiting: waiting ${waitTime}ms`);
      await new Promise(resolve => setTimeout(resolve, waitTime));
    }
    
    this.lastRequestTime = Date.now();
  }

  /**
   * Make API request with error handling
   * @param {string} endpoint - API endpoint
   * @param {Object} params - Query parameters
   * @param {number} retries - Number of retry attempts
   * @returns {Promise<Object>} API response data
   * @private
   */
  async _makeRequest(endpoint, params = {}, retries = 2) {
    const requestParams = {
      ...params,
      apikey: this.apiKey
    };

    for (let attempt = 1; attempt <= retries; attempt++) {
      try {
        console.log(`[Polygon] Making request to ${endpoint} (attempt ${attempt}/${retries})`);
        
        const response = await this.client.get(endpoint, { params: requestParams });
        
        // Check for API error responses
        if (response.data.status === 'ERROR') {
          throw new Error(`Polygon.io Error: ${response.data.error || 'Unknown error'}`);
        }
        
        if (response.data.status === 'NOT_AUTHORIZED') {
          throw new Error('Polygon.io Error: Invalid API key or insufficient permissions');
        }

        console.log(`[Polygon] Request successful: ${endpoint}`);
        return response.data;
        
      } catch (error) {
        console.error(`[Polygon] Request failed (attempt ${attempt}/${retries}):`, error.message);
        
        if (attempt === retries) {
          throw error;
        }
        
        // Wait before retry
        await new Promise(resolve => setTimeout(resolve, 5000));
      }
    }
  }

  /**
   * Get company details (ticker details)
   * @param {string} symbol - Stock ticker symbol
   * @returns {Promise<Object>} Company details data
   */
  async getCompanyDetails(symbol) {
    if (!symbol) {
      throw new Error('Symbol is required for company details');
    }

    const endpoint = `/v3/reference/tickers/${symbol.toUpperCase()}`;
    const data = await this._makeRequest(endpoint);
    
    if (!data.results) {
      throw new Error(`No company details found for symbol: ${symbol}`);
    }

    const result = data.results;
    
    // Transform to match FMP format
    return {
      symbol: result.ticker,
      companyName: result.name,
      description: result.description,
      industry: result.sic_description,
      sector: result.sector || null,
      website: result.homepage_url,
      marketCap: result.market_cap || null,
      shareClassSharesOutstanding: result.share_class_shares_outstanding || null,
      weightedSharesOutstanding: result.weighted_shares_outstanding || null,
      address: result.address ? {
        address1: result.address.address1,
        city: result.address.city,
        state: result.address.state,
        postalCode: result.address.postal_code
      } : null,
      phoneNumber: result.phone_number,
      listDate: result.list_date,
      locale: result.locale,
      primaryExchange: result.primary_exchange,
      type: result.type,
      active: result.active,
      currencyName: result.currency_name,
      cik: result.cik,
      compositeFigi: result.composite_figi,
      shareClassFigi: result.share_class_figi
    };
  }

  /**
   * Get stock financials (quarterly or annual)
   * @param {string} symbol - Stock ticker symbol
   * @param {Object} options - Options for data retrieval
   * @returns {Promise<Array>} Financial data
   */
  async getStockFinancials(symbol, options = {}) {
    if (!symbol) {
      throw new Error('Symbol is required for stock financials');
    }

    const {
      timeframe = 'annual', // 'annual' or 'quarterly'
      limit = 5,
      sort = 'filing_date'
    } = options;

    const params = {
      timeframe,
      limit,
      sort
    };

    const endpoint = `/vX/reference/financials`;
    params['ticker'] = symbol.toUpperCase();
    
    const data = await this._makeRequest(endpoint, params);
    
    if (!data.results || data.results.length === 0) {
      throw new Error(`No financial data found for symbol: ${symbol}`);
    }

    // Transform to match FMP format
    return data.results.map(financial => {
      const financials = financial.financials;
      const incomeStatement = financials.income_statement || {};
      const balanceSheet = financials.balance_sheet || {};
      const cashFlow = financials.cash_flow_statement || {};
      const comprehensiveIncome = financials.comprehensive_income || {};

      return {
        date: financial.end_date,
        symbol: symbol.toUpperCase(),
        reportedCurrency: financial.financials.currency || 'USD',
        cik: financial.cik,
        fillingDate: financial.filing_date,
        acceptedDate: financial.acceptance_datetime,
        calendarYear: new Date(financial.end_date).getFullYear().toString(),
        period: financial.timeframe === 'annual' ? 'FY' : `Q${Math.ceil(new Date(financial.end_date).getMonth() / 3)}`,
        
        // Income Statement
        revenue: incomeStatement.revenues?.value || 0,
        costOfRevenue: incomeStatement.cost_of_revenue?.value || 0,
        grossProfit: incomeStatement.gross_profit?.value || 0,
        operatingExpenses: incomeStatement.operating_expenses?.value || 0,
        operatingIncome: incomeStatement.operating_income_loss?.value || 0,
        netIncome: incomeStatement.net_income_loss?.value || 0,
        eps: incomeStatement.basic_earnings_per_share?.value || 0,
        epsdiluted: incomeStatement.diluted_earnings_per_share?.value || 0,
        
        // Balance Sheet
        totalAssets: balanceSheet.assets?.value || 0,
        currentAssets: balanceSheet.current_assets?.value || 0,
        totalLiabilities: balanceSheet.liabilities?.value || 0,
        currentLiabilities: balanceSheet.current_liabilities?.value || 0,
        totalEquity: balanceSheet.equity?.value || 0,
        cashAndCashEquivalents: balanceSheet.cash_and_cash_equivalents?.value || 0,
        
        // Cash Flow
        operatingCashFlow: cashFlow.net_cash_flow_from_operating_activities?.value || 0,
        investingCashFlow: cashFlow.net_cash_flow_from_investing_activities?.value || 0,
        financingCashFlow: cashFlow.net_cash_flow_from_financing_activities?.value || 0,
        
        // Calculated ratios
        grossProfitRatio: incomeStatement.revenues?.value ? 
          (incomeStatement.gross_profit?.value || 0) / incomeStatement.revenues.value : 0,
        operatingIncomeRatio: incomeStatement.revenues?.value ? 
          (incomeStatement.operating_income_loss?.value || 0) / incomeStatement.revenues.value : 0,
        netIncomeRatio: incomeStatement.revenues?.value ? 
          (incomeStatement.net_income_loss?.value || 0) / incomeStatement.revenues.value : 0
      };
    });
  }

  /**
   * Search for tickers
   * @param {string} query - Search query
   * @param {Object} options - Search options
   * @returns {Promise<Array>} Search results
   */
  async searchTickers(query, options = {}) {
    if (!query) {
      throw new Error('Query is required for ticker search');
    }

    const {
      type = 'CS', // Common Stock
      market = 'stocks',
      active = true,
      limit = 10
    } = options;

    const params = {
      search: query,
      type,
      market,
      active,
      limit
    };

    const endpoint = '/v3/reference/tickers';
    const data = await this._makeRequest(endpoint, params);
    
    if (!data.results) {
      return [];
    }

    // Transform to match FMP format
    return data.results.map(ticker => ({
      symbol: ticker.ticker,
      name: ticker.name,
      market: ticker.market,
      locale: ticker.locale,
      primaryExchange: ticker.primary_exchange,
      type: ticker.type,
      active: ticker.active,
      currencyName: ticker.currency_name,
      cik: ticker.cik,
      compositeFigi: ticker.composite_figi,
      shareClassFigi: ticker.share_class_figi,
      lastUpdatedUtc: ticker.last_updated_utc
    }));
  }

  /**
   * Get market status
   * @returns {Promise<Object>} Market status
   */
  async getMarketStatus() {
    const endpoint = '/v1/marketstatus/now';
    const data = await this._makeRequest(endpoint);
    
    return {
      market: data.market,
      serverTime: data.serverTime,
      exchanges: data.exchanges,
      currencies: data.currencies
    };
  }

  /**
   * Test API connection
   * @returns {Promise<Object>} Connection test result
   */
  async testConnection() {
    try {
      console.log('[Polygon] Testing API connection...');
      
      // Test with market status first (simpler endpoint)
      const marketStatus = await this.getMarketStatus();
      
      // Then test with a company lookup
      const testData = await this.getCompanyDetails('AAPL');
      
      return {
        success: true,
        message: 'Polygon.io API connection successful',
        testData: {
          companyName: testData.companyName,
          symbol: testData.symbol,
          industry: testData.industry,
          marketStatus: marketStatus.market
        }
      };
      
    } catch (error) {
      return {
        success: false,
        message: `Polygon.io API connection failed: ${error.message}`,
        error: error.message
      };
    }
  }
}

module.exports = PolygonClient;