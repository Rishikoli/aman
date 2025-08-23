const { query, getClient } = require('../utils/database');
const { v4: uuidv4 } = require('uuid');

class Deal {
  constructor(data = {}) {
    this.id = data.id || uuidv4();
    this.name = data.name;
    this.description = data.description;
    this.acquirer_id = data.acquirer_id;
    this.target_id = data.target_id;
    this.deal_value = data.deal_value;
    this.currency = data.currency || 'USD';
    this.status = data.status || 'draft';
    this.created_by = data.created_by;
    this.estimated_completion_date = data.estimated_completion_date;
    this.actual_completion_date = data.actual_completion_date;
    this.priority = data.priority || 5;
    this.metadata = data.metadata || {};
    this.created_at = data.created_at;
    this.updated_at = data.updated_at;
  }

  /**
   * Create a new deal
   * @returns {Promise<Deal>} Created deal
   */
  async save() {
    const sql = `
      INSERT INTO deals (
        id, name, description, acquirer_id, target_id, deal_value, 
        currency, status, created_by, estimated_completion_date, 
        priority, metadata
      ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
      RETURNING *
    `;
    
    const values = [
      this.id, this.name, this.description, this.acquirer_id, this.target_id,
      this.deal_value, this.currency, this.status, this.created_by,
      this.estimated_completion_date, this.priority, JSON.stringify(this.metadata)
    ];

    const result = await query(sql, values);
    const savedDeal = result.rows[0];
    
    // Update instance with saved data
    Object.assign(this, savedDeal);
    return this;
  }

  /**
   * Update existing deal
   * @returns {Promise<Deal>} Updated deal
   */
  async update() {
    const sql = `
      UPDATE deals SET 
        name = $2, description = $3, acquirer_id = $4, target_id = $5,
        deal_value = $6, currency = $7, status = $8, created_by = $9,
        estimated_completion_date = $10, actual_completion_date = $11,
        priority = $12, metadata = $13, updated_at = CURRENT_TIMESTAMP
      WHERE id = $1
      RETURNING *
    `;
    
    const values = [
      this.id, this.name, this.description, this.acquirer_id, this.target_id,
      this.deal_value, this.currency, this.status, this.created_by,
      this.estimated_completion_date, this.actual_completion_date,
      this.priority, JSON.stringify(this.metadata)
    ];

    const result = await query(sql, values);
    if (result.rows.length === 0) {
      throw new Error(`Deal with id ${this.id} not found`);
    }
    
    Object.assign(this, result.rows[0]);
    return this;
  }

  /**
   * Find deal by ID
   * @param {string} id - Deal ID
   * @returns {Promise<Deal|null>} Deal instance or null
   */
  static async findById(id) {
    const sql = `
      SELECT d.*, 
             ac.name as acquirer_name, ac.ticker_symbol as acquirer_ticker,
             tc.name as target_name, tc.ticker_symbol as target_ticker
      FROM deals d
      LEFT JOIN companies ac ON d.acquirer_id = ac.id
      LEFT JOIN companies tc ON d.target_id = tc.id
      WHERE d.id = $1
    `;
    
    const result = await query(sql, [id]);
    if (result.rows.length === 0) {
      return null;
    }
    
    return new Deal(result.rows[0]);
  }

  /**
   * Find all deals with optional filters
   * @param {Object} filters - Filter options
   * @returns {Promise<Deal[]>} Array of deals
   */
  static async findAll(filters = {}) {
    let sql = `
      SELECT d.*, 
             ac.name as acquirer_name, ac.ticker_symbol as acquirer_ticker,
             tc.name as target_name, tc.ticker_symbol as target_ticker
      FROM deals d
      LEFT JOIN companies ac ON d.acquirer_id = ac.id
      LEFT JOIN companies tc ON d.target_id = tc.id
    `;
    
    const conditions = [];
    const values = [];
    let paramCount = 0;

    if (filters.status) {
      paramCount++;
      conditions.push(`d.status = $${paramCount}`);
      values.push(filters.status);
    }

    if (filters.created_by) {
      paramCount++;
      conditions.push(`d.created_by = $${paramCount}`);
      values.push(filters.created_by);
    }

    if (filters.priority) {
      paramCount++;
      conditions.push(`d.priority = $${paramCount}`);
      values.push(filters.priority);
    }

    if (conditions.length > 0) {
      sql += ' WHERE ' + conditions.join(' AND ');
    }

    sql += ' ORDER BY d.created_at DESC';

    if (filters.limit) {
      paramCount++;
      sql += ` LIMIT $${paramCount}`;
      values.push(filters.limit);
    }

    const result = await query(sql, values);
    return result.rows.map(row => new Deal(row));
  }

  /**
   * Delete deal by ID
   * @param {string} id - Deal ID
   * @returns {Promise<boolean>} Success status
   */
  static async deleteById(id) {
    const sql = 'DELETE FROM deals WHERE id = $1';
    const result = await query(sql, [id]);
    return result.rowCount > 0;
  }

  /**
   * Get deal statistics
   * @returns {Promise<Object>} Deal statistics
   */
  static async getStatistics() {
    const sql = `
      SELECT 
        COUNT(*) as total_deals,
        COUNT(CASE WHEN status = 'active' THEN 1 END) as active_deals,
        COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_deals,
        COUNT(CASE WHEN status = 'draft' THEN 1 END) as draft_deals,
        AVG(deal_value) as avg_deal_value,
        SUM(deal_value) as total_deal_value
      FROM deals
    `;
    
    const result = await query(sql);
    return result.rows[0];
  }

  /**
   * Get deals with agent execution status
   * @param {string} dealId - Deal ID
   * @returns {Promise<Object>} Deal with agent status
   */
  static async findWithAgentStatus(dealId) {
    const deal = await Deal.findById(dealId);
    if (!deal) {
      return null;
    }

    const agentStatusSql = `
      SELECT 
        agent_type,
        status,
        start_time,
        end_time,
        progress_percentage,
        error_message
      FROM agent_executions 
      WHERE deal_id = $1 
      ORDER BY created_at DESC
    `;
    
    const agentResult = await query(agentStatusSql, [dealId]);
    deal.agent_executions = agentResult.rows;
    
    return deal;
  }

  /**
   * Validate deal data
   * @param {Object} data - Deal data to validate
   * @returns {Object} Validation result
   */
  static validate(data) {
    const errors = [];

    if (!data.name || data.name.trim().length === 0) {
      errors.push('Deal name is required');
    }

    if (!data.acquirer_id) {
      errors.push('Acquirer company ID is required');
    }

    if (!data.target_id) {
      errors.push('Target company ID is required');
    }

    if (data.acquirer_id === data.target_id) {
      errors.push('Acquirer and target companies must be different');
    }

    if (data.deal_value && (isNaN(data.deal_value) || data.deal_value < 0)) {
      errors.push('Deal value must be a positive number');
    }

    if (data.priority && (data.priority < 1 || data.priority > 10)) {
      errors.push('Priority must be between 1 and 10');
    }

    const validStatuses = ['draft', 'active', 'completed', 'cancelled', 'on_hold'];
    if (data.status && !validStatuses.includes(data.status)) {
      errors.push('Invalid deal status');
    }

    return {
      isValid: errors.length === 0,
      errors
    };
  }
}

module.exports = Deal;