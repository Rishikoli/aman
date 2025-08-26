const { query } = require('../utils/database');
const geminiService = require('./gemini');

class QAService {
  constructor() {
    this.queryTypes = {
      DEAL_INFO: 'deal_info',
      COMPANY_INFO: 'company_info',
      FINANCIAL_DATA: 'financial_data',
      RISK_ASSESSMENT: 'risk_assessment',
      AGENT_STATUS: 'agent_status',
      TIMELINE: 'timeline',
      FINDINGS: 'findings'
    };

    this.suggestedQueries = [
      "What are the key risks for deal [deal_name]?",
      "Show me financial metrics for [company_name]",
      "What is the status of all agents for deal [deal_id]?",
      "What findings have been flagged as critical?",
      "When is the estimated completion date for [deal_name]?",
      "What are the revenue synergies for this deal?",
      "Show me all legal findings for [company_name]",
      "What is the risk score for [deal_name]?",
      "Which deals are currently active?",
      "What are the latest agent execution results?"
    ];
  }

  /**
   * Process a natural language query and return structured results
   * @param {string} question - The user's question
   * @param {Object} context - Optional context (deal_id, company_id, etc.)
   * @returns {Promise<Object>} Structured answer with supporting data
   */
  async processQuery(question, context = {}) {
    try {
      // First, classify the query type
      const queryType = await this.classifyQuery(question);
      
      // Extract entities from the question
      const entities = await this.extractEntities(question);
      
      // Get relevant data based on query type and entities
      const data = await this.fetchRelevantData(queryType, entities, context);
      
      // Generate a direct answer using AI
      const answer = await this.generateAnswer(question, data, queryType);
      
      return {
        success: true,
        question,
        answer: answer.text,
        queryType,
        entities,
        supportingData: data,
        confidence: answer.confidence,
        sources: data.sources || [],
        timestamp: new Date().toISOString()
      };
    } catch (error) {
      console.error('QA Service Error:', error);
      return {
        success: false,
        question,
        error: error.message,
        timestamp: new Date().toISOString()
      };
    }
  }

  /**
   * Classify the type of query to determine data sources
   * @param {string} question - The user's question
   * @returns {Promise<string>} Query type
   */
  async classifyQuery(question) {
    const lowerQuestion = question.toLowerCase();
    
    // Simple keyword-based classification
    if (lowerQuestion.includes('risk') || lowerQuestion.includes('threat')) {
      return this.queryTypes.RISK_ASSESSMENT;
    }
    if (lowerQuestion.includes('financial') || lowerQuestion.includes('revenue') || lowerQuestion.includes('profit')) {
      return this.queryTypes.FINANCIAL_DATA;
    }
    if (lowerQuestion.includes('deal') && (lowerQuestion.includes('status') || lowerQuestion.includes('progress'))) {
      return this.queryTypes.DEAL_INFO;
    }
    if (lowerQuestion.includes('agent') || lowerQuestion.includes('execution')) {
      return this.queryTypes.AGENT_STATUS;
    }
    if (lowerQuestion.includes('timeline') || lowerQuestion.includes('completion') || lowerQuestion.includes('when')) {
      return this.queryTypes.TIMELINE;
    }
    if (lowerQuestion.includes('finding') || lowerQuestion.includes('issue') || lowerQuestion.includes('problem')) {
      return this.queryTypes.FINDINGS;
    }
    if (lowerQuestion.includes('company') || lowerQuestion.includes('organization')) {
      return this.queryTypes.COMPANY_INFO;
    }
    
    // Default to general deal info
    return this.queryTypes.DEAL_INFO;
  }

  /**
   * Extract entities (company names, deal names, etc.) from the question
   * @param {string} question - The user's question
   * @returns {Promise<Object>} Extracted entities
   */
  async extractEntities(question) {
    const entities = {
      companies: [],
      deals: [],
      agents: [],
      timeframes: [],
      metrics: []
    };

    // Simple entity extraction using database lookups
    try {
      // Look for company names in the database
      const companyResult = await query(`
        SELECT name, ticker_symbol FROM companies 
        WHERE name ILIKE ANY($1) OR ticker_symbol ILIKE ANY($1)
        LIMIT 10
      `, [this.extractPotentialNames(question)]);
      
      entities.companies = companyResult.rows;

      // Look for deal names
      const dealResult = await query(`
        SELECT id, name FROM deals 
        WHERE name ILIKE ANY($1)
        LIMIT 10
      `, [this.extractPotentialNames(question)]);
      
      entities.deals = dealResult.rows;

      // Extract agent types
      const agentTypes = ['finance', 'legal', 'synergy', 'reputation', 'operations'];
      entities.agents = agentTypes.filter(agent => 
        question.toLowerCase().includes(agent)
      );

      // Extract time-related terms
      const timeTerms = ['today', 'yesterday', 'week', 'month', 'year', 'recent', 'latest'];
      entities.timeframes = timeTerms.filter(term => 
        question.toLowerCase().includes(term)
      );

    } catch (error) {
      console.error('Entity extraction error:', error);
    }

    return entities;
  }

  /**
   * Extract potential names from question for entity matching
   * @param {string} question - The user's question
   * @returns {Array<string>} Potential names
   */
  extractPotentialNames(question) {
    // Simple approach: look for capitalized words that might be names
    const words = question.split(/\s+/);
    const potentialNames = words
      .filter(word => /^[A-Z][a-zA-Z]+/.test(word))
      .map(word => `%${word}%`);
    
    return potentialNames.length > 0 ? potentialNames : ['%'];
  }

  /**
   * Fetch relevant data based on query type and entities
   * @param {string} queryType - Type of query
   * @param {Object} entities - Extracted entities
   * @param {Object} context - Additional context
   * @returns {Promise<Object>} Relevant data
   */
  async fetchRelevantData(queryType, entities, context) {
    const data = { sources: [] };

    try {
      switch (queryType) {
        case this.queryTypes.DEAL_INFO:
          data.deals = await this.fetchDealData(entities, context);
          data.sources.push('deals');
          break;

        case this.queryTypes.COMPANY_INFO:
          data.companies = await this.fetchCompanyData(entities, context);
          data.sources.push('companies');
          break;

        case this.queryTypes.FINANCIAL_DATA:
          data.financial = await this.fetchFinancialData(entities, context);
          data.sources.push('financial_data');
          break;

        case this.queryTypes.RISK_ASSESSMENT:
          data.findings = await this.fetchRiskFindings(entities, context);
          data.sources.push('findings');
          break;

        case this.queryTypes.AGENT_STATUS:
          data.agents = await this.fetchAgentStatus(entities, context);
          data.sources.push('agent_executions');
          break;

        case this.queryTypes.TIMELINE:
          data.timeline = await this.fetchTimelineData(entities, context);
          data.sources.push('timeline_estimates');
          break;

        case this.queryTypes.FINDINGS:
          data.findings = await this.fetchFindings(entities, context);
          data.sources.push('findings');
          break;

        default:
          // Fetch general data
          data.deals = await this.fetchDealData(entities, context);
          data.sources.push('deals');
      }
    } catch (error) {
      console.error('Data fetching error:', error);
      data.error = error.message;
    }

    return data;
  }

  /**
   * Fetch deal-related data
   */
  async fetchDealData(entities, context) {
    let sql = `
      SELECT d.*, 
             ac.name as acquirer_name, 
             tc.name as target_name
      FROM deals d
      LEFT JOIN companies ac ON d.acquirer_id = ac.id
      LEFT JOIN companies tc ON d.target_id = tc.id
      WHERE 1=1
    `;
    const values = [];
    let paramCount = 0;

    if (context.deal_id) {
      paramCount++;
      sql += ` AND d.id = $${paramCount}`;
      values.push(context.deal_id);
    }

    if (entities.deals && entities.deals.length > 0) {
      paramCount++;
      sql += ` AND d.name ILIKE $${paramCount}`;
      values.push(`%${entities.deals[0].name}%`);
    }

    sql += ` ORDER BY d.created_at DESC LIMIT 10`;

    const result = await query(sql, values);
    return result.rows;
  }

  /**
   * Fetch company-related data
   */
  async fetchCompanyData(entities, context) {
    let sql = `SELECT * FROM companies WHERE 1=1`;
    const values = [];
    let paramCount = 0;

    if (context.company_id) {
      paramCount++;
      sql += ` AND id = $${paramCount}`;
      values.push(context.company_id);
    }

    if (entities.companies && entities.companies.length > 0) {
      paramCount++;
      sql += ` AND (name ILIKE $${paramCount} OR ticker_symbol ILIKE $${paramCount})`;
      values.push(`%${entities.companies[0].name}%`);
    }

    sql += ` ORDER BY created_at DESC LIMIT 10`;

    const result = await query(sql, values);
    return result.rows;
  }

  /**
   * Fetch financial data
   */
  async fetchFinancialData(entities, context) {
    let sql = `
      SELECT fd.*, c.name as company_name 
      FROM financial_data fd
      JOIN companies c ON fd.company_id = c.id
      WHERE 1=1
    `;
    const values = [];
    let paramCount = 0;

    if (context.company_id) {
      paramCount++;
      sql += ` AND fd.company_id = $${paramCount}`;
      values.push(context.company_id);
    }

    if (entities.companies && entities.companies.length > 0) {
      paramCount++;
      sql += ` AND c.name ILIKE $${paramCount}`;
      values.push(`%${entities.companies[0].name}%`);
    }

    sql += ` ORDER BY fd.fiscal_year DESC, fd.fiscal_quarter DESC LIMIT 20`;

    const result = await query(sql, values);
    return result.rows;
  }

  /**
   * Fetch risk-related findings
   */
  async fetchRiskFindings(entities, context) {
    let sql = `
      SELECT f.*, d.name as deal_name 
      FROM findings f
      JOIN deals d ON f.deal_id = d.id
      WHERE f.severity IN ('high', 'critical')
    `;
    const values = [];
    let paramCount = 0;

    if (context.deal_id) {
      paramCount++;
      sql += ` AND f.deal_id = $${paramCount}`;
      values.push(context.deal_id);
    }

    sql += ` ORDER BY f.severity DESC, f.created_at DESC LIMIT 20`;

    const result = await query(sql, values);
    return result.rows;
  }

  /**
   * Fetch agent execution status
   */
  async fetchAgentStatus(entities, context) {
    let sql = `
      SELECT ae.*, d.name as deal_name 
      FROM agent_executions ae
      JOIN deals d ON ae.deal_id = d.id
      WHERE 1=1
    `;
    const values = [];
    let paramCount = 0;

    if (context.deal_id) {
      paramCount++;
      sql += ` AND ae.deal_id = $${paramCount}`;
      values.push(context.deal_id);
    }

    if (entities.agents && entities.agents.length > 0) {
      paramCount++;
      sql += ` AND ae.agent_type = $${paramCount}`;
      values.push(entities.agents[0]);
    }

    sql += ` ORDER BY ae.created_at DESC LIMIT 20`;

    const result = await query(sql, values);
    return result.rows;
  }

  /**
   * Fetch timeline data
   */
  async fetchTimelineData(entities, context) {
    let sql = `
      SELECT te.*, d.name as deal_name 
      FROM timeline_estimates te
      JOIN deals d ON te.deal_id = d.id
      WHERE 1=1
    `;
    const values = [];
    let paramCount = 0;

    if (context.deal_id) {
      paramCount++;
      sql += ` AND te.deal_id = $${paramCount}`;
      values.push(context.deal_id);
    }

    sql += ` ORDER BY te.updated_at DESC LIMIT 10`;

    const result = await query(sql, values);
    return result.rows;
  }

  /**
   * Fetch general findings
   */
  async fetchFindings(entities, context) {
    let sql = `
      SELECT f.*, d.name as deal_name 
      FROM findings f
      JOIN deals d ON f.deal_id = d.id
      WHERE 1=1
    `;
    const values = [];
    let paramCount = 0;

    if (context.deal_id) {
      paramCount++;
      sql += ` AND f.deal_id = $${paramCount}`;
      values.push(context.deal_id);
    }

    if (entities.timeframes.includes('recent') || entities.timeframes.includes('latest')) {
      sql += ` AND f.created_at >= NOW() - INTERVAL '7 days'`;
    }

    sql += ` ORDER BY f.created_at DESC LIMIT 20`;

    const result = await query(sql, values);
    return result.rows;
  }

  /**
   * Generate a natural language answer using AI
   * @param {string} question - Original question
   * @param {Object} data - Supporting data
   * @param {string} queryType - Type of query
   * @returns {Promise<Object>} Generated answer with confidence
   */
  async generateAnswer(question, data, queryType) {
    if (!geminiService.isAvailable()) {
      return {
        text: this.generateFallbackAnswer(question, data, queryType),
        confidence: 0.6
      };
    }

    try {
      const prompt = `
You are an AI assistant for an M&A due diligence system. Answer the user's question based on the provided data.

Question: ${question}
Query Type: ${queryType}

Supporting Data:
${JSON.stringify(data, null, 2)}

Instructions:
1. Provide a direct, factual answer to the question
2. Reference specific data points from the supporting data
3. If the data is insufficient, clearly state what information is missing
4. Keep the answer concise but comprehensive
5. Include relevant numbers, dates, and specific details
6. If no relevant data is found, explain what data would be needed

Answer format:
- Start with a direct answer to the question
- Provide supporting details with specific references
- End with any important caveats or limitations

Answer:`;

      const response = await geminiService.generateText(prompt, { 
        temperature: 0.3,
        maxTokens: 1024 
      });

      return {
        text: response,
        confidence: 0.8
      };
    } catch (error) {
      console.error('AI answer generation failed:', error);
      return {
        text: this.generateFallbackAnswer(question, data, queryType),
        confidence: 0.5
      };
    }
  }

  /**
   * Generate a fallback answer when AI is not available
   */
  generateFallbackAnswer(question, data, queryType) {
    const dataKeys = Object.keys(data).filter(key => key !== 'sources' && key !== 'error');
    
    if (dataKeys.length === 0 || dataKeys.every(key => !data[key] || data[key].length === 0)) {
      return "I couldn't find specific data to answer your question. Please try rephrasing your question or provide more specific details like company names or deal IDs.";
    }

    let answer = "Based on the available data:\n\n";

    // Generate basic answers based on query type
    switch (queryType) {
      case this.queryTypes.DEAL_INFO:
        if (data.deals && data.deals.length > 0) {
          const deal = data.deals[0];
          answer += `Deal "${deal.name}" is currently ${deal.status}. `;
          if (deal.acquirer_name && deal.target_name) {
            answer += `${deal.acquirer_name} is acquiring ${deal.target_name}. `;
          }
          if (deal.deal_value) {
            answer += `Deal value: ${deal.currency || 'USD'} ${deal.deal_value}. `;
          }
        }
        break;

      case this.queryTypes.FINANCIAL_DATA:
        if (data.financial && data.financial.length > 0) {
          const latest = data.financial[0];
          answer += `Latest financial data for ${latest.company_name}: `;
          if (latest.revenue) answer += `Revenue: $${latest.revenue}M, `;
          if (latest.net_income) answer += `Net Income: $${latest.net_income}M, `;
          if (latest.total_assets) answer += `Total Assets: $${latest.total_assets}M`;
        }
        break;

      case this.queryTypes.RISK_ASSESSMENT:
        if (data.findings && data.findings.length > 0) {
          const criticalFindings = data.findings.filter(f => f.severity === 'critical');
          const highFindings = data.findings.filter(f => f.severity === 'high');
          answer += `Found ${criticalFindings.length} critical and ${highFindings.length} high-severity risk findings. `;
          if (criticalFindings.length > 0) {
            answer += `Critical issues include: ${criticalFindings.slice(0, 3).map(f => f.title).join(', ')}.`;
          }
        }
        break;

      default:
        answer += `Found ${dataKeys.reduce((total, key) => total + (data[key]?.length || 0), 0)} relevant records. `;
        answer += "Please ask a more specific question for detailed analysis.";
    }

    return answer;
  }

  /**
   * Get suggested queries based on available data
   * @param {Object} context - Current context (deal_id, company_id, etc.)
   * @returns {Promise<Array<string>>} Array of suggested queries
   */
  async getSuggestedQueries(context = {}) {
    const suggestions = [...this.suggestedQueries];

    try {
      // Add context-specific suggestions
      if (context.deal_id) {
        const dealResult = await query('SELECT name FROM deals WHERE id = $1', [context.deal_id]);
        if (dealResult.rows.length > 0) {
          const dealName = dealResult.rows[0].name;
          suggestions.unshift(
            `What are the key risks for deal ${dealName}?`,
            `What is the timeline for ${dealName}?`,
            `Show me all findings for ${dealName}`
          );
        }
      }

      if (context.company_id) {
        const companyResult = await query('SELECT name FROM companies WHERE id = $1', [context.company_id]);
        if (companyResult.rows.length > 0) {
          const companyName = companyResult.rows[0].name;
          suggestions.unshift(
            `Show me financial metrics for ${companyName}`,
            `What are the risks associated with ${companyName}?`
          );
        }
      }

      // Add dynamic suggestions based on recent activity
      const recentDeals = await query(`
        SELECT name FROM deals 
        WHERE created_at >= NOW() - INTERVAL '30 days' 
        ORDER BY created_at DESC LIMIT 3
      `);

      recentDeals.rows.forEach(deal => {
        suggestions.push(`What is the status of ${deal.name}?`);
      });

    } catch (error) {
      console.error('Error generating suggested queries:', error);
    }

    // Return unique suggestions, limited to 10
    return [...new Set(suggestions)].slice(0, 10);
  }

  /**
   * Search across all findings and data
   * @param {string} searchTerm - Search term
   * @param {Object} filters - Search filters
   * @returns {Promise<Object>} Search results
   */
  async searchAll(searchTerm, filters = {}) {
    const results = {
      deals: [],
      companies: [],
      findings: [],
      agents: [],
      total: 0
    };

    try {
      const searchPattern = `%${searchTerm}%`;

      // Search deals
      const dealResults = await query(`
        SELECT d.*, ac.name as acquirer_name, tc.name as target_name
        FROM deals d
        LEFT JOIN companies ac ON d.acquirer_id = ac.id
        LEFT JOIN companies tc ON d.target_id = tc.id
        WHERE d.name ILIKE $1 OR d.description ILIKE $1
        ORDER BY d.created_at DESC
        LIMIT 20
      `, [searchPattern]);
      results.deals = dealResults.rows;

      // Search companies
      const companyResults = await query(`
        SELECT * FROM companies
        WHERE name ILIKE $1 OR description ILIKE $1 OR industry ILIKE $1
        ORDER BY created_at DESC
        LIMIT 20
      `, [searchPattern]);
      results.companies = companyResults.rows;

      // Search findings
      const findingResults = await query(`
        SELECT f.*, d.name as deal_name
        FROM findings f
        JOIN deals d ON f.deal_id = d.id
        WHERE f.title ILIKE $1 OR f.description ILIKE $1
        ORDER BY f.created_at DESC
        LIMIT 20
      `, [searchPattern]);
      results.findings = findingResults.rows;

      // Search agent executions - fix enum comparison
      const agentResults = await query(`
        SELECT ae.*, d.name as deal_name
        FROM agent_executions ae
        JOIN deals d ON ae.deal_id = d.id
        WHERE ae.agent_type::text ILIKE $1 OR ae.error_message ILIKE $1
        ORDER BY ae.created_at DESC
        LIMIT 20
      `, [searchPattern]);
      results.agents = agentResults.rows;

      results.total = results.deals.length + results.companies.length + 
                     results.findings.length + results.agents.length;

    } catch (error) {
      console.error('Search error:', error);
      throw error;
    }

    return results;
  }
}

module.exports = new QAService();