const { query } = require('../utils/database');
const { v4: uuidv4 } = require('uuid');

class AgentExecution {
  constructor(data = {}) {
    this.id = data.id || uuidv4();
    this.deal_id = data.deal_id;
    this.agent_type = data.agent_type;
    this.agent_id = data.agent_id;
    this.status = data.status || 'pending';
    this.queued_at = data.queued_at;
    this.start_time = data.start_time;
    this.end_time = data.end_time;
    this.duration_seconds = data.duration_seconds;
    this.recursion_level = data.recursion_level || 0;
    this.parent_execution_id = data.parent_execution_id;
    this.input_data = data.input_data || {};
    this.output_data = data.output_data || {};
    this.error_message = data.error_message;
    this.progress_percentage = data.progress_percentage || 0;
    this.created_at = data.created_at;
    this.updated_at = data.updated_at;
  }

  /**
   * Create a new agent execution
   * @returns {Promise<AgentExecution>} Created execution
   */
  async save() {
    const sql = `
      INSERT INTO agent_executions (
        id, deal_id, agent_type, agent_id, status, queued_at, start_time,
        recursion_level, parent_execution_id, input_data, progress_percentage
      ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
      RETURNING *
    `;
    
    const values = [
      this.id, this.deal_id, this.agent_type, this.agent_id, this.status,
      this.queued_at, this.start_time, this.recursion_level, this.parent_execution_id,
      JSON.stringify(this.input_data), this.progress_percentage
    ];

    const result = await query(sql, values);
    const savedExecution = result.rows[0];
    
    Object.assign(this, savedExecution);
    return this;
  }

  /**
   * Update existing agent execution
   * @returns {Promise<AgentExecution>} Updated execution
   */
  async update() {
    const sql = `
      UPDATE agent_executions SET 
        status = $2, queued_at = $3, start_time = $4, end_time = $5, duration_seconds = $6,
        output_data = $7, error_message = $8, progress_percentage = $9,
        updated_at = CURRENT_TIMESTAMP
      WHERE id = $1
      RETURNING *
    `;
    
    const values = [
      this.id, this.status, this.queued_at, this.start_time, this.end_time, this.duration_seconds,
      JSON.stringify(this.output_data), this.error_message, this.progress_percentage
    ];

    const result = await query(sql, values);
    if (result.rows.length === 0) {
      throw new Error(`Agent execution with id ${this.id} not found`);
    }
    
    Object.assign(this, result.rows[0]);
    return this;
  }

  /**
   * Start the execution
   * @returns {Promise<AgentExecution>} Updated execution
   */
  async start() {
    this.status = 'running';
    this.start_time = new Date();
    this.progress_percentage = 0;
    return await this.update();
  }

  /**
   * Complete the execution successfully
   * @param {Object} outputData - Execution output data
   * @returns {Promise<AgentExecution>} Updated execution
   */
  async complete(outputData = {}) {
    this.status = 'completed';
    this.end_time = new Date();
    this.output_data = outputData;
    this.progress_percentage = 100;
    
    if (this.start_time) {
      this.duration_seconds = Math.floor((this.end_time - new Date(this.start_time)) / 1000);
    }
    
    return await this.update();
  }

  /**
   * Fail the execution
   * @param {string} errorMessage - Error message
   * @returns {Promise<AgentExecution>} Updated execution
   */
  async fail(errorMessage) {
    this.status = 'failed';
    this.end_time = new Date();
    this.error_message = errorMessage;
    
    if (this.start_time) {
      this.duration_seconds = Math.floor((this.end_time - new Date(this.start_time)) / 1000);
    }
    
    return await this.update();
  }

  /**
   * Update progress
   * @param {number} percentage - Progress percentage (0-100)
   * @returns {Promise<AgentExecution>} Updated execution
   */
  async updateProgress(percentage) {
    this.progress_percentage = Math.max(0, Math.min(100, percentage));
    return await this.update();
  }

  /**
   * Find execution by ID
   * @param {string} id - Execution ID
   * @returns {Promise<AgentExecution|null>} Execution instance or null
   */
  static async findById(id) {
    const sql = 'SELECT * FROM agent_executions WHERE id = $1';
    const result = await query(sql, [id]);
    
    if (result.rows.length === 0) {
      return null;
    }
    
    return new AgentExecution(result.rows[0]);
  }

  /**
   * Find executions by deal ID
   * @param {string} dealId - Deal ID
   * @returns {Promise<AgentExecution[]>} Array of executions
   */
  static async findByDealId(dealId) {
    const sql = `
      SELECT * FROM agent_executions 
      WHERE deal_id = $1 
      ORDER BY created_at DESC
    `;
    const result = await query(sql, [dealId]);
    return result.rows.map(row => new AgentExecution(row));
  }

  /**
   * Find executions by agent type
   * @param {string} agentType - Agent type
   * @param {Object} filters - Additional filters
   * @returns {Promise<AgentExecution[]>} Array of executions
   */
  static async findByAgentType(agentType, filters = {}) {
    let sql = 'SELECT * FROM agent_executions WHERE agent_type = $1';
    const values = [agentType];
    let paramCount = 1;

    if (filters.status) {
      paramCount++;
      sql += ` AND status = $${paramCount}`;
      values.push(filters.status);
    }

    if (filters.deal_id) {
      paramCount++;
      sql += ` AND deal_id = $${paramCount}`;
      values.push(filters.deal_id);
    }

    sql += ' ORDER BY created_at DESC';

    if (filters.limit) {
      paramCount++;
      sql += ` LIMIT $${paramCount}`;
      values.push(filters.limit);
    }

    const result = await query(sql, values);
    return result.rows.map(row => new AgentExecution(row));
  }

  /**
   * Get execution statistics
   * @param {Object} filters - Filter options
   * @returns {Promise<Object>} Execution statistics
   */
  static async getStatistics(filters = {}) {
    let sql = `
      SELECT 
        COUNT(*) as total_executions,
        COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_executions,
        COUNT(CASE WHEN status = 'failed' THEN 1 END) as failed_executions,
        COUNT(CASE WHEN status = 'running' THEN 1 END) as running_executions,
        COUNT(CASE WHEN status = 'pending' THEN 1 END) as pending_executions,
        AVG(duration_seconds) as avg_duration_seconds,
        AVG(progress_percentage) as avg_progress
      FROM agent_executions
    `;
    
    const conditions = [];
    const values = [];
    let paramCount = 0;

    if (filters.agent_type) {
      paramCount++;
      conditions.push(`agent_type = $${paramCount}`);
      values.push(filters.agent_type);
    }

    if (filters.deal_id) {
      paramCount++;
      conditions.push(`deal_id = $${paramCount}`);
      values.push(filters.deal_id);
    }

    if (conditions.length > 0) {
      sql += ' WHERE ' + conditions.join(' AND ');
    }

    const result = await query(sql, values);
    return result.rows[0];
  }

  /**
   * Get active executions
   * @returns {Promise<AgentExecution[]>} Array of active executions
   */
  static async getActiveExecutions() {
    const sql = `
      SELECT * FROM agent_executions 
      WHERE status IN ('pending', 'running') 
      ORDER BY created_at ASC
    `;
    const result = await query(sql);
    return result.rows.map(row => new AgentExecution(row));
  }

  /**
   * Get execution history for a deal
   * @param {string} dealId - Deal ID
   * @returns {Promise<Object>} Execution history with timeline
   */
  static async getExecutionHistory(dealId) {
    const sql = `
      SELECT 
        ae.*,
        d.name as deal_name
      FROM agent_executions ae
      JOIN deals d ON ae.deal_id = d.id
      WHERE ae.deal_id = $1
      ORDER BY ae.created_at ASC
    `;
    
    const result = await query(sql, [dealId]);
    const executions = result.rows.map(row => new AgentExecution(row));
    
    // Calculate timeline metrics
    const timeline = {
      total_executions: executions.length,
      completed_executions: executions.filter(e => e.status === 'completed').length,
      failed_executions: executions.filter(e => e.status === 'failed').length,
      total_duration_seconds: executions
        .filter(e => e.duration_seconds)
        .reduce((sum, e) => sum + e.duration_seconds, 0),
      avg_duration_seconds: 0,
      start_time: executions.length > 0 ? executions[0].created_at : null,
      last_activity: executions.length > 0 ? executions[executions.length - 1].updated_at : null
    };
    
    if (timeline.completed_executions > 0) {
      timeline.avg_duration_seconds = timeline.total_duration_seconds / timeline.completed_executions;
    }

    return {
      executions,
      timeline
    };
  }

  /**
   * Cancel pending executions for a deal
   * @param {string} dealId - Deal ID
   * @returns {Promise<number>} Number of cancelled executions
   */
  static async cancelPendingExecutions(dealId) {
    const sql = `
      UPDATE agent_executions 
      SET status = 'cancelled', updated_at = CURRENT_TIMESTAMP
      WHERE deal_id = $1 AND status = 'pending'
    `;
    const result = await query(sql, [dealId]);
    return result.rowCount;
  }

  /**
   * Find execution by deal ID and agent type
   * @param {string} dealId - Deal ID
   * @param {string} agentType - Agent type
   * @returns {Promise<AgentExecution|null>} Execution instance or null
   */
  static async findByDealIdAndType(dealId, agentType) {
    const sql = `
      SELECT * FROM agent_executions 
      WHERE deal_id = $1 AND agent_type = $2 
      ORDER BY created_at DESC 
      LIMIT 1
    `;
    const result = await query(sql, [dealId, agentType]);
    
    if (result.rows.length === 0) {
      return null;
    }
    
    return new AgentExecution(result.rows[0]);
  }

  /**
   * Find executions by deal ID and status
   * @param {string} dealId - Deal ID
   * @param {string} status - Execution status
   * @returns {Promise<AgentExecution[]>} Array of executions
   */
  static async findByDealIdAndStatus(dealId, status) {
    const sql = `
      SELECT * FROM agent_executions 
      WHERE deal_id = $1 AND status = $2 
      ORDER BY created_at DESC
    `;
    const result = await query(sql, [dealId, status]);
    return result.rows.map(row => new AgentExecution(row));
  }

  /**
   * Validate execution data
   * @param {Object} data - Execution data to validate
   * @returns {Object} Validation result
   */
  static validate(data) {
    const errors = [];

    if (!data.deal_id) {
      errors.push('Deal ID is required');
    }

    if (!data.agent_type) {
      errors.push('Agent type is required');
    }

    if (!data.agent_id) {
      errors.push('Agent ID is required');
    }

    const validAgentTypes = ['finance', 'legal', 'synergy', 'reputation', 'operations', 'orchestrator'];
    if (data.agent_type && !validAgentTypes.includes(data.agent_type)) {
      errors.push('Invalid agent type');
    }

    const validStatuses = ['pending', 'queued', 'running', 'completed', 'failed', 'cancelled'];
    if (data.status && !validStatuses.includes(data.status)) {
      errors.push('Invalid execution status');
    }

    if (data.progress_percentage && (data.progress_percentage < 0 || data.progress_percentage > 100)) {
      errors.push('Progress percentage must be between 0 and 100');
    }

    if (data.recursion_level && (data.recursion_level < 0 || data.recursion_level > 10)) {
      errors.push('Recursion level must be between 0 and 10');
    }

    return {
      isValid: errors.length === 0,
      errors
    };
  }
}

module.exports = AgentExecution;