/**
 * Alpha Vantage API Client
 * Backup data source for financial information
 */

const axios = require('axios');
const { getConfig } = require('../utils/env-config');

class AlphaVantageClient {
  constructor() {
    this.config = getConfig();
    this.baseURL = 'https://www.alphavantage.co/query';
    this.apiKey = process.env.ALPHA_VANTAGE_API_KEY || 'demo';
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
      console.log(`[AlphaVantage] Rate limiting: waiting ${waitTime}ms`);
      await new Promise(resolve => setTimeout(resolve, waitTime));
    }
    
    this.lastRequestTime = Date.now();
  }

  /**
   * Make API request with error handling
   * @param {Object} params - Query parameters
   * @param {number} retries - Number of retry attempts
   * @returns {Promise<Object>} API response data
   * @private
   */
  async _makeRequest(params, retries = 2) {
    const requestParams = {
      ...params,
      apikey: this.apiKey
    };

    for (let attempt = 1; attempt <= retries; attempt++) {
      try {
        console.log(`[AlphaVantage] Making request (attempt ${attempt}/${retries}):`, params.function);
        
        const response = await this.client.get('', { params: requestParams });
        
        // Check for API error responses
        if (response.data['Error Message']) {
          throw new Error(`Alpha Vantage Error: ${response.data['Error Message']}`);
        }
        
        if (response.data['Note']) {
          throw new Error(`Alpha Vantage Rate Limit: ${response.data['Note']}`);
        }

        console.log(`[AlphaVantage] Request successful:`, params.function);
        return response.data;
        
      } catch (error) {
        console.error(`[AlphaVantage] Request failed (attempt ${attempt}/${retries}):`, error.message);
        
        if (attempt === retries) {
          throw error;
        }
        
        // Wait before retry
        await new Promise(resolve => setTimeout(resolve, 5000));
      }
    }
  }

  /**
   * Get company overview (similar to FMP company profile)
   * @param {string} symbol - Stock ticker symbol
   * @returns {Promise<Object>} Company overview data
   */
  async getCompanyOverview(symbol) {
    if (!symbol) {
      throw new Error('Symbol is required for company overview');
    }

    const params = {
      function: 'OVERVIEW',
      symbol: symbol.toUpperCase()
    };

    const data = await this._makeRequest(params);
    
    if (!data.Symbol) {
      throw new Error(`No company overview found for symbol: ${symbol}`);
    }

    // Transform to match FMP format
    return {
      symbol: data.Symbol,
      companyName: data.Name,
      industry: data.Industry,
      sector: data.Sector,
      description: data.Description,
      website: data.OfficialSite,
      marketCap: parseFloat(data.MarketCapitalization) || null,
      peRatio: parseFloat(data.PERatio) || null,
      pegRatio: parseFloat(data.PEGRatio) || null,
      bookValue: parseFloat(data.BookValue) || null,
      dividendYield: parseFloat(data.DividendYield) || null,
      eps: parseFloat(data.EPS) || null,
      revenuePerShareTTM: parseFloat(data.RevenuePerShareTTM) || null,
      profitMargin: parseFloat(data.ProfitMargin) || null,
      operatingMarginTTM: parseFloat(data.OperatingMarginTTM) || null,
      returnOnAssetsTTM: parseFloat(data.ReturnOnAssetsTTM) || null,
      returnOnEquityTTM: parseFloat(data.ReturnOnEquityTTM) || null,
      revenueTTM: parseFloat(data.RevenueTTM) || null,
      grossProfitTTM: parseFloat(data.GrossProfitTTM) || null,
      dilutedEPSTTM: parseFloat(data.DilutedEPSTTM) || null,
      quarterlyEarningsGrowthYOY: parseFloat(data.QuarterlyEarningsGrowthYOY) || null,
      quarterlyRevenueGrowthYOY: parseFloat(data.QuarterlyRevenueGrowthYOY) || null,
      analystTargetPrice: parseFloat(data.AnalystTargetPrice) || null,
      trailingPE: parseFloat(data.TrailingPE) || null,
      forwardPE: parseFloat(data.ForwardPE) || null,
      priceToSalesRatioTTM: parseFloat(data.PriceToSalesRatioTTM) || null,
      priceToBookRatio: parseFloat(data.PriceToBookRatio) || null,
      evToRevenue: parseFloat(data.EVToRevenue) || null,
      evToEBITDA: parseFloat(data.EVToEBITDA) || null,
      beta: parseFloat(data.Beta) || null,
      week52High: parseFloat(data['52WeekHigh']) || null,
      week52Low: parseFloat(data['52WeekLow']) || null,
      day50MovingAverage: parseFloat(data['50DayMovingAverage']) || null,
      day200MovingAverage: parseFloat(data['200DayMovingAverage']) || null,
      sharesOutstanding: parseFloat(data.SharesOutstanding) || null,
      dividendDate: data.DividendDate,
      exDividendDate: data.ExDividendDate
    };
  }

  /**
   * Get income statement data
   * @param {string} symbol - Stock ticker symbol
   * @returns {Promise<Array>} Income statement data
   */
  async getIncomeStatement(symbol) {
    if (!symbol) {
      throw new Error('Symbol is required for income statement');
    }

    const params = {
      function: 'INCOME_STATEMENT',
      symbol: symbol.toUpperCase()
    };

    const data = await this._makeRequest(params);
    
    if (!data.annualReports) {
      throw new Error(`No income statement found for symbol: ${symbol}`);
    }

    // Transform to match FMP format
    return data.annualReports.map(report => ({
      date: report.fiscalDateEnding,
      symbol: symbol.toUpperCase(),
      reportedCurrency: report.reportedCurrency,
      cik: data.cik,
      fillingDate: report.fiscalDateEnding,
      acceptedDate: report.fiscalDateEnding,
      calendarYear: new Date(report.fiscalDateEnding).getFullYear().toString(),
      period: 'FY',
      revenue: parseFloat(report.totalRevenue) || 0,
      costOfRevenue: parseFloat(report.costOfRevenue) || 0,
      grossProfit: parseFloat(report.grossProfit) || 0,
      grossProfitRatio: parseFloat(report.grossProfit) / parseFloat(report.totalRevenue) || 0,
      researchAndDevelopmentExpenses: parseFloat(report.researchAndDevelopment) || 0,
      generalAndAdministrativeExpenses: parseFloat(report.sellingGeneralAndAdministrative) || 0,
      sellingAndMarketingExpenses: 0, // Not available in Alpha Vantage
      sellingGeneralAndAdministrativeExpenses: parseFloat(report.sellingGeneralAndAdministrative) || 0,
      otherExpenses: parseFloat(report.otherOperatingExpenses) || 0,
      operatingExpenses: parseFloat(report.operatingExpenses) || 0,
      costAndExpenses: parseFloat(report.costOfRevenue) + parseFloat(report.operatingExpenses) || 0,
      interestIncome: parseFloat(report.interestIncome) || 0,
      interestExpense: parseFloat(report.interestExpense) || 0,
      depreciationAndAmortization: parseFloat(report.depreciationAndAmortization) || 0,
      ebitda: parseFloat(report.ebitda) || 0,
      ebitdaratio: parseFloat(report.ebitda) / parseFloat(report.totalRevenue) || 0,
      operatingIncome: parseFloat(report.operatingIncome) || 0,
      operatingIncomeRatio: parseFloat(report.operatingIncome) / parseFloat(report.totalRevenue) || 0,
      totalOtherIncomeExpensesNet: parseFloat(report.totalOtherIncomeExpenseNet) || 0,
      incomeBeforeTax: parseFloat(report.incomeBeforeTax) || 0,
      incomeBeforeTaxRatio: parseFloat(report.incomeBeforeTax) / parseFloat(report.totalRevenue) || 0,
      incomeTaxExpense: parseFloat(report.incomeTaxExpense) || 0,
      netIncome: parseFloat(report.netIncome) || 0,
      netIncomeRatio: parseFloat(report.netIncome) / parseFloat(report.totalRevenue) || 0,
      eps: parseFloat(report.reportedEPS) || 0,
      epsdiluted: parseFloat(report.reportedEPS) || 0,
      weightedAverageShsOut: parseFloat(report.commonStockSharesOutstanding) || 0,
      weightedAverageShsOutDil: parseFloat(report.commonStockSharesOutstanding) || 0
    }));
  }

  /**
   * Get balance sheet data
   * @param {string} symbol - Stock ticker symbol
   * @returns {Promise<Array>} Balance sheet data
   */
  async getBalanceSheet(symbol) {
    if (!symbol) {
      throw new Error('Symbol is required for balance sheet');
    }

    const params = {
      function: 'BALANCE_SHEET',
      symbol: symbol.toUpperCase()
    };

    const data = await this._makeRequest(params);
    
    if (!data.annualReports) {
      throw new Error(`No balance sheet found for symbol: ${symbol}`);
    }

    // Transform to match FMP format
    return data.annualReports.map(report => ({
      date: report.fiscalDateEnding,
      symbol: symbol.toUpperCase(),
      reportedCurrency: report.reportedCurrency,
      cik: data.cik,
      fillingDate: report.fiscalDateEnding,
      acceptedDate: report.fiscalDateEnding,
      calendarYear: new Date(report.fiscalDateEnding).getFullYear().toString(),
      period: 'FY',
      cashAndCashEquivalents: parseFloat(report.cashAndCashEquivalentsAtCarryingValue) || 0,
      shortTermInvestments: parseFloat(report.shortTermInvestments) || 0,
      cashAndShortTermInvestments: (parseFloat(report.cashAndCashEquivalentsAtCarryingValue) || 0) + (parseFloat(report.shortTermInvestments) || 0),
      netReceivables: parseFloat(report.currentNetReceivables) || 0,
      inventory: parseFloat(report.inventory) || 0,
      otherCurrentAssets: parseFloat(report.otherCurrentAssets) || 0,
      totalCurrentAssets: parseFloat(report.totalCurrentAssets) || 0,
      propertyPlantEquipmentNet: parseFloat(report.propertyPlantAndEquipmentNet) || 0,
      goodwill: parseFloat(report.goodwill) || 0,
      intangibleAssets: parseFloat(report.intangibleAssets) || 0,
      goodwillAndIntangibleAssets: (parseFloat(report.goodwill) || 0) + (parseFloat(report.intangibleAssets) || 0),
      longTermInvestments: parseFloat(report.longTermInvestments) || 0,
      taxAssets: 0, // Not available in Alpha Vantage
      otherNonCurrentAssets: parseFloat(report.otherNonCurrentAssets) || 0,
      totalNonCurrentAssets: parseFloat(report.totalNonCurrentAssets) || 0,
      otherAssets: parseFloat(report.otherAssets) || 0,
      totalAssets: parseFloat(report.totalAssets) || 0,
      accountPayables: parseFloat(report.currentAccountsPayable) || 0,
      shortTermDebt: parseFloat(report.shortTermDebt) || 0,
      taxPayables: 0, // Not available in Alpha Vantage
      deferredRevenue: parseFloat(report.deferredRevenue) || 0,
      otherCurrentLiabilities: parseFloat(report.otherCurrentLiabilities) || 0,
      totalCurrentLiabilities: parseFloat(report.totalCurrentLiabilities) || 0,
      longTermDebt: parseFloat(report.longTermDebt) || 0,
      deferredRevenueNonCurrent: 0, // Not available in Alpha Vantage
      deferredTaxLiabilitiesNonCurrent: 0, // Not available in Alpha Vantage
      otherNonCurrentLiabilities: parseFloat(report.otherNonCurrentLiabilities) || 0,
      totalNonCurrentLiabilities: parseFloat(report.totalNonCurrentLiabilities) || 0,
      otherLiabilities: 0, // Not available in Alpha Vantage
      capitalLeaseObligations: parseFloat(report.capitalLeaseObligations) || 0,
      totalLiabilities: parseFloat(report.totalLiabilities) || 0,
      preferredStock: parseFloat(report.preferredStock) || 0,
      commonStock: parseFloat(report.commonStock) || 0,
      retainedEarnings: parseFloat(report.retainedEarnings) || 0,
      accumulatedOtherComprehensiveIncomeLoss: parseFloat(report.accumulatedOtherComprehensiveIncomeLoss) || 0,
      othertotalStockholdersEquity: 0, // Not available in Alpha Vantage
      totalStockholdersEquity: parseFloat(report.totalShareholderEquity) || 0,
      totalEquity: parseFloat(report.totalShareholderEquity) || 0,
      totalLiabilitiesAndStockholdersEquity: parseFloat(report.totalLiabilitiesAndShareholderEquity) || 0,
      minorityInterest: parseFloat(report.minorityInterest) || 0,
      totalLiabilitiesAndTotalEquity: parseFloat(report.totalLiabilitiesAndShareholderEquity) || 0,
      totalInvestments: (parseFloat(report.shortTermInvestments) || 0) + (parseFloat(report.longTermInvestments) || 0),
      totalDebt: (parseFloat(report.shortTermDebt) || 0) + (parseFloat(report.longTermDebt) || 0),
      netDebt: ((parseFloat(report.shortTermDebt) || 0) + (parseFloat(report.longTermDebt) || 0)) - (parseFloat(report.cashAndCashEquivalentsAtCarryingValue) || 0)
    }));
  }

  /**
   * Get cash flow statement data
   * @param {string} symbol - Stock ticker symbol
   * @returns {Promise<Array>} Cash flow statement data
   */
  async getCashFlowStatement(symbol) {
    if (!symbol) {
      throw new Error('Symbol is required for cash flow statement');
    }

    const params = {
      function: 'CASH_FLOW',
      symbol: symbol.toUpperCase()
    };

    const data = await this._makeRequest(params);
    
    if (!data.annualReports) {
      throw new Error(`No cash flow statement found for symbol: ${symbol}`);
    }

    // Transform to match FMP format
    return data.annualReports.map(report => ({
      date: report.fiscalDateEnding,
      symbol: symbol.toUpperCase(),
      reportedCurrency: report.reportedCurrency,
      cik: data.cik,
      fillingDate: report.fiscalDateEnding,
      acceptedDate: report.fiscalDateEnding,
      calendarYear: new Date(report.fiscalDateEnding).getFullYear().toString(),
      period: 'FY',
      netIncome: parseFloat(report.netIncome) || 0,
      depreciationAndAmortization: parseFloat(report.depreciationDepletionAndAmortization) || 0,
      deferredIncomeTax: parseFloat(report.deferredIncomeTax) || 0,
      stockBasedCompensation: parseFloat(report.stockBasedCompensation) || 0,
      changeInWorkingCapital: parseFloat(report.changeInOperatingLiabilities) - parseFloat(report.changeInOperatingAssets) || 0,
      accountsReceivables: parseFloat(report.changeInReceivables) || 0,
      inventory: parseFloat(report.changeInInventory) || 0,
      accountsPayables: parseFloat(report.changeInAccountsPayable) || 0,
      otherWorkingCapital: parseFloat(report.changeInOtherOperatingActivities) || 0,
      otherNonCashItems: parseFloat(report.otherNonCashItems) || 0,
      netCashProvidedByOperatingActivities: parseFloat(report.operatingCashflow) || 0,
      investmentsInPropertyPlantAndEquipment: parseFloat(report.capitalExpenditures) || 0,
      acquisitionsNet: 0, // Not available in Alpha Vantage
      purchasesOfInvestments: parseFloat(report.investmentsInMarketableSecurities) || 0,
      salesMaturitiesOfInvestments: 0, // Not available in Alpha Vantage
      otherInvestingActivites: parseFloat(report.otherInvestingActivities) || 0,
      netCashUsedForInvestingActivites: parseFloat(report.cashflowFromInvestment) || 0,
      debtRepayment: 0, // Not available in Alpha Vantage
      commonStockIssued: 0, // Not available in Alpha Vantage
      commonStockRepurchased: 0, // Not available in Alpha Vantage
      dividendsPaid: parseFloat(report.dividendPayout) || 0,
      otherFinancingActivites: parseFloat(report.otherFinancingActivities) || 0,
      netCashUsedProvidedByFinancingActivities: parseFloat(report.cashflowFromFinancing) || 0,
      effectOfForexChangesOnCash: 0, // Not available in Alpha Vantage
      netChangeInCash: parseFloat(report.changeInCashAndCashEquivalents) || 0,
      cashAtEndOfPeriod: parseFloat(report.cashAndCashEquivalentsAtCarryingValue) || 0,
      cashAtBeginningOfPeriod: (parseFloat(report.cashAndCashEquivalentsAtCarryingValue) || 0) - (parseFloat(report.changeInCashAndCashEquivalents) || 0),
      operatingCashFlow: parseFloat(report.operatingCashflow) || 0,
      capitalExpenditure: parseFloat(report.capitalExpenditures) || 0,
      freeCashFlow: (parseFloat(report.operatingCashflow) || 0) - (parseFloat(report.capitalExpenditures) || 0)
    }));
  }

  /**
   * Test API connection
   * @returns {Promise<Object>} Connection test result
   */
  async testConnection() {
    try {
      console.log('[AlphaVantage] Testing API connection...');
      
      const testData = await this.getCompanyOverview('AAPL');
      
      return {
        success: true,
        message: 'Alpha Vantage API connection successful',
        testData: {
          companyName: testData.companyName,
          symbol: testData.symbol,
          industry: testData.industry
        }
      };
      
    } catch (error) {
      return {
        success: false,
        message: `Alpha Vantage API connection failed: ${error.message}`,
        error: error.message
      };
    }
  }
}

module.exports = AlphaVantageClient;