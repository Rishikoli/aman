/**
 * Financial Modeling Prep (FMP) API Client
 * Handles financial data retrieval with error handling and rate limiting
 */

const axios = require('axios');
const { getConfig } = require('../utils/env-config');

class FMPClient {
  constructor() {
    this.config = getConfig();
    this.baseURL = 'https://financialmodelingprep.com/api/v3';
    this.apiKey = this.config.apiKeys.fmp;
    this.rateLimitDelay = 1000; // 1 second between requests for free tier
    this.lastRequestTime = 0;
    
    // Initialize axios instance
    this.client = axios.create({
      baseURL: this.baseURL,
      timeout: 30000, // 30 second timeout
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

    // Add response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error) => this._handleError(error)
    );
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
      await new Promise(resolve => setTimeout(resolve, waitTime));
    }
    
    this.lastRequestTime = Date.now();
  }

  /**
   * Handle API errors with detailed error information
   * @param {Error} error - Axios error object
   * @private
   */
  _handleError(error) {
    if (error.response) {
      // Server responded with error status
      const { status, data } = error.response;
      
      switch (status) {
        case 401:
          throw new Error('FMP API: Invalid API key or authentication failed');
        case 403:
          throw new Error('FMP API: Access forbidden - check API key permissions');
        case 429:
          throw new Error('FMP API: Rate limit exceeded - please wait before retrying');
        case 404:
          throw new Error(`FMP API: Data not found for the requested symbol`);
        case 500:
          throw new Error('FMP API: Internal server error - please try again later');
        default:
          throw new Error(`FMP API Error ${status}: ${data?.message || 'Unknown error'}`);
      }
    } else if (error.request) {
      // Network error
      throw new Error('FMP API: Network error - please check your internet connection');
    } else {
      // Other error
      throw new Error(`FMP API: ${error.message}`);
    }
  }

  /**
   * Make API request with automatic retry logic
   * @param {string} endpoint - API endpoint
   * @param {Object} params - Query parameters
   * @param {number} retries - Number of retry attempts
   * @returns {Promise<Object>} API response data
   * @private
   */
  async _makeRequest(endpoint, params = {}, retries = 3) {
    const requestParams = {
      ...params,
      apikey: this.apiKey
    };

    for (let attempt = 1; attempt <= retries; attempt++) {
      try {
        console.log(`[FMP] Making request to ${endpoint} (attempt ${attempt}/${retries})`);
        
        const response = await this.client.get(endpoint, { params: requestParams });
        
        // Check if response contains error message
        if (response.data?.error) {
          throw new Error(`FMP API Error: ${response.data.error}`);
        }

        console.log(`[FMP] Request successful: ${endpoint}`);
        return response.data;
        
      } catch (error) {
        console.error(`[FMP] Request failed (attempt ${attempt}/${retries}):`, error.message);
        
        if (attempt === retries) {
          throw error;
        }
        
        // Wait before retry with exponential backoff
        const waitTime = Math.pow(2, attempt) * 1000;
        await new Promise(resolve => setTimeout(resolve, waitTime));
      }
    }
  }

  /**
   * Get company profile information
   * @param {string} symbol - Stock ticker symbol
   * @returns {Promise<Object>} Company profile data
   */
  async getCompanyProfile(symbol) {
    if (!symbol) {
      throw new Error('Symbol is required for company profile lookup');
    }

    const data = await this._makeRequest(`/profile/${symbol.toUpperCase()}`);
    
    if (!data || data.length === 0) {
      throw new Error(`No company profile found for symbol: ${symbol}`);
    }

    return data[0]; // FMP returns array, we want the first item
  }

  /**
   * Get financial statements (Income Statement, Balance Sheet, Cash Flow)
   * @param {string} symbol - Stock ticker symbol
   * @param {string} period - 'annual' or 'quarter'
   * @param {number} limit - Number of periods to retrieve (default: 5)
   * @returns {Promise<Object>} Financial statements data
   */
  async getFinancialStatements(symbol, period = 'annual', limit = 5) {
    if (!symbol) {
      throw new Error('Symbol is required for financial statements');
    }

    if (!['annual', 'quarter'].includes(period)) {
      throw new Error('Period must be either "annual" or "quarter"');
    }

    const params = { period, limit };
    
    // Get all three financial statements in parallel
    const [incomeStatement, balanceSheet, cashFlow] = await Promise.all([
      this._makeRequest(`/income-statement/${symbol.toUpperCase()}`, params),
      this._makeRequest(`/balance-sheet-statement/${symbol.toUpperCase()}`, params),
      this._makeRequest(`/cash-flow-statement/${symbol.toUpperCase()}`, params)
    ]);

    return {
      incomeStatement: incomeStatement || [],
      balanceSheet: balanceSheet || [],
      cashFlow: cashFlow || []
    };
  }

  /**
   * Get key financial ratios
   * @param {string} symbol - Stock ticker symbol
   * @param {string} period - 'annual' or 'quarter'
   * @param {number} limit - Number of periods to retrieve (default: 5)
   * @returns {Promise<Array>} Financial ratios data
   */
  async getFinancialRatios(symbol, period = 'annual', limit = 5) {
    if (!symbol) {
      throw new Error('Symbol is required for financial ratios');
    }

    const params = { period, limit };
    const data = await this._makeRequest(`/ratios/${symbol.toUpperCase()}`, params);
    
    return data || [];
  }

  /**
   * Get key financial metrics
   * @param {string} symbol - Stock ticker symbol
   * @param {string} period - 'annual' or 'quarter'
   * @param {number} limit - Number of periods to retrieve (default: 5)
   * @returns {Promise<Array>} Key metrics data
   */
  async getKeyMetrics(symbol, period = 'annual', limit = 5) {
    if (!symbol) {
      throw new Error('Symbol is required for key metrics');
    }

    const params = { period, limit };
    const data = await this._makeRequest(`/key-metrics/${symbol.toUpperCase()}`, params);
    
    return data || [];
  }

  /**
   * Get enterprise value data
   * @param {string} symbol - Stock ticker symbol
   * @param {string} period - 'annual' or 'quarter'
   * @param {number} limit - Number of periods to retrieve (default: 5)
   * @returns {Promise<Array>} Enterprise value data
   */
  async getEnterpriseValue(symbol, period = 'annual', limit = 5) {
    if (!symbol) {
      throw new Error('Symbol is required for enterprise value');
    }

    const params = { period, limit };
    const data = await this._makeRequest(`/enterprise-values/${symbol.toUpperCase()}`, params);
    
    return data || [];
  }

  /**
   * Get financial growth metrics
   * @param {string} symbol - Stock ticker symbol
   * @param {string} period - 'annual' or 'quarter'
   * @param {number} limit - Number of periods to retrieve (default: 5)
   * @returns {Promise<Array>} Financial growth data
   */
  async getFinancialGrowth(symbol, period = 'annual', limit = 5) {
    if (!symbol) {
      throw new Error('Symbol is required for financial growth');
    }

    const params = { period, limit };
    const data = await this._makeRequest(`/financial-growth/${symbol.toUpperCase()}`, params);
    
    return data || [];
  }

  /**
   * Search for companies by name or symbol
   * @param {string} query - Search query (company name or symbol)
   * @param {number} limit - Maximum number of results (default: 10)
   * @returns {Promise<Array>} Search results
   */
  async searchCompanies(query, limit = 10) {
    if (!query) {
      throw new Error('Query is required for company search');
    }

    const params = { query, limit };
    const data = await this._makeRequest('/search', params);
    
    return data || [];
  }

  /**
   * Get comprehensive financial data for a company
   * @param {string} symbol - Stock ticker symbol
   * @param {Object} options - Options for data retrieval
   * @returns {Promise<Object>} Comprehensive financial data
   */
  async getComprehensiveFinancialData(symbol, options = {}) {
    const {
      period = 'annual',
      limit = 5,
      includeRatios = true,
      includeMetrics = true,
      includeGrowth = true,
      includeEnterpriseValue = true
    } = options;

    console.log(`[FMP] Fetching comprehensive financial data for ${symbol}`);

    try {
      // Get basic company profile first
      const profile = await this.getCompanyProfile(symbol);
      
      // Get financial statements
      const statements = await this.getFinancialStatements(symbol, period, limit);
      
      // Get additional data based on options
      const additionalData = {};
      
      if (includeRatios) {
        additionalData.ratios = await this.getFinancialRatios(symbol, period, limit);
      }
      
      if (includeMetrics) {
        additionalData.keyMetrics = await this.getKeyMetrics(symbol, period, limit);
      }
      
      if (includeGrowth) {
        additionalData.growth = await this.getFinancialGrowth(symbol, period, limit);
      }
      
      if (includeEnterpriseValue) {
        additionalData.enterpriseValue = await this.getEnterpriseValue(symbol, period, limit);
      }

      return {
        profile,
        statements,
        ...additionalData,
        metadata: {
          symbol: symbol.toUpperCase(),
          period,
          limit,
          retrievedAt: new Date().toISOString(),
          source: 'FMP'
        }
      };

    } catch (error) {
      console.error(`[FMP] Failed to fetch comprehensive data for ${symbol}:`, error.message);
      throw error;
    }
  }

  /**
   * Test API connection and key validity
   * @returns {Promise<Object>} Connection test result
   */
  async testConnection() {
    try {
      console.log('[FMP] Testing API connection...');
      
      // Test with a well-known symbol
      const testData = await this.getCompanyProfile('AAPL');
      
      return {
        success: true,
        message: 'FMP API connection successful',
        testData: {
          companyName: testData.companyName,
          symbol: testData.symbol,
          industry: testData.industry
        }
      };
      
    } catch (error) {
      return {
        success: false,
        message: `FMP API connection failed: ${error.message}`,
        error: error.message
      };
    }
  }
}

module.exports = FMPClient;