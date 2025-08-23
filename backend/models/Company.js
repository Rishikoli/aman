const { query } = require('../utils/database');
const { v4: uuidv4 } = require('uuid');

class Company {
  constructor(data = {}) {
    this.id = data.id || uuidv4();
    this.name = data.name;
    this.ticker_symbol = data.ticker_symbol;
    this.industry = data.industry;
    this.sector = data.sector;
    this.company_size = data.company_size;
    this.headquarters_location = data.headquarters_location;
    this.founded_year = data.founded_year;
    this.employee_count = data.employee_count;
    this.annual_revenue = data.annual_revenue;
    this.market_cap = data.market_cap;
    this.description = data.description;
    this.website_url = data.website_url;
    this.created_at = data.created_at;
    this.updated_at = data.updated_at;
  }

  /**
   * Create a new company
   * @returns {Promise<Company>} Created company
   */
  async save() {
    const sql = `
      INSERT INTO companies (
        id, name, ticker_symbol, industry, sector, company_size,
        headquarters_location, founded_year, employee_count, annual_revenue,
        market_cap, description, website_url
      ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13)
      RETURNING *
    `;
    
    const values = [
      this.id, this.name, this.ticker_symbol, this.industry, this.sector,
      this.company_size, this.headquarters_location, this.founded_year,
      this.employee_count, this.annual_revenue, this.market_cap,
      this.description, this.website_url
    ];

    const result = await query(sql, values);
    const savedCompany = result.rows[0];
    
    Object.assign(this, savedCompany);
    return this;
  }

  /**
   * Update existing company
   * @returns {Promise<Company>} Updated company
   */
  async update() {
    const sql = `
      UPDATE companies SET 
        name = $2, ticker_symbol = $3, industry = $4, sector = $5,
        company_size = $6, headquarters_location = $7, founded_year = $8,
        employee_count = $9, annual_revenue = $10, market_cap = $11,
        description = $12, website_url = $13, updated_at = CURRENT_TIMESTAMP
      WHERE id = $1
      RETURNING *
    `;
    
    const values = [
      this.id, this.name, this.ticker_symbol, this.industry, this.sector,
      this.company_size, this.headquarters_location, this.founded_year,
      this.employee_count, this.annual_revenue, this.market_cap,
      this.description, this.website_url
    ];

    const result = await query(sql, values);
    if (result.rows.length === 0) {
      throw new Error(`Company with id ${this.id} not found`);
    }
    
    Object.assign(this, result.rows[0]);
    return this;
  }

  /**
   * Find company by ID
   * @param {string} id - Company ID
   * @returns {Promise<Company|null>} Company instance or null
   */
  static async findById(id) {
    const sql = 'SELECT * FROM companies WHERE id = $1';
    const result = await query(sql, [id]);
    
    if (result.rows.length === 0) {
      return null;
    }
    
    return new Company(result.rows[0]);
  }

  /**
   * Find company by ticker symbol
   * @param {string} ticker - Ticker symbol
   * @returns {Promise<Company|null>} Company instance or null
   */
  static async findByTicker(ticker) {
    const sql = 'SELECT * FROM companies WHERE ticker_symbol = $1';
    const result = await query(sql, [ticker.toUpperCase()]);
    
    if (result.rows.length === 0) {
      return null;
    }
    
    return new Company(result.rows[0]);
  }

  /**
   * Find all companies with optional filters
   * @param {Object} filters - Filter options
   * @returns {Promise<Company[]>} Array of companies
   */
  static async findAll(filters = {}) {
    let sql = 'SELECT * FROM companies';
    const conditions = [];
    const values = [];
    let paramCount = 0;

    if (filters.industry) {
      paramCount++;
      conditions.push(`industry = $${paramCount}`);
      values.push(filters.industry);
    }

    if (filters.sector) {
      paramCount++;
      conditions.push(`sector = $${paramCount}`);
      values.push(filters.sector);
    }

    if (filters.company_size) {
      paramCount++;
      conditions.push(`company_size = $${paramCount}`);
      values.push(filters.company_size);
    }

    if (filters.search) {
      paramCount++;
      conditions.push(`(name ILIKE $${paramCount} OR ticker_symbol ILIKE $${paramCount})`);
      values.push(`%${filters.search}%`);
    }

    if (conditions.length > 0) {
      sql += ' WHERE ' + conditions.join(' AND ');
    }

    sql += ' ORDER BY name ASC';

    if (filters.limit) {
      paramCount++;
      sql += ` LIMIT $${paramCount}`;
      values.push(filters.limit);
    }

    const result = await query(sql, values);
    return result.rows.map(row => new Company(row));
  }

  /**
   * Search companies by name or ticker
   * @param {string} searchTerm - Search term
   * @param {number} limit - Result limit
   * @returns {Promise<Company[]>} Array of matching companies
   */
  static async search(searchTerm, limit = 10) {
    const sql = `
      SELECT * FROM companies 
      WHERE name ILIKE $1 OR ticker_symbol ILIKE $1
      ORDER BY 
        CASE 
          WHEN name ILIKE $2 THEN 1
          WHEN ticker_symbol ILIKE $2 THEN 2
          ELSE 3
        END,
        name ASC
      LIMIT $3
    `;
    
    const values = [`%${searchTerm}%`, `${searchTerm}%`, limit];
    const result = await query(sql, values);
    return result.rows.map(row => new Company(row));
  }

  /**
   * Delete company by ID
   * @param {string} id - Company ID
   * @returns {Promise<boolean>} Success status
   */
  static async deleteById(id) {
    const sql = 'DELETE FROM companies WHERE id = $1';
    const result = await query(sql, [id]);
    return result.rowCount > 0;
  }

  /**
   * Get company statistics
   * @returns {Promise<Object>} Company statistics
   */
  static async getStatistics() {
    const sql = `
      SELECT 
        COUNT(*) as total_companies,
        COUNT(CASE WHEN ticker_symbol IS NOT NULL THEN 1 END) as public_companies,
        COUNT(CASE WHEN ticker_symbol IS NULL THEN 1 END) as private_companies,
        COUNT(DISTINCT industry) as unique_industries,
        COUNT(DISTINCT sector) as unique_sectors,
        AVG(employee_count) as avg_employee_count,
        AVG(annual_revenue) as avg_annual_revenue
      FROM companies
    `;
    
    const result = await query(sql);
    return result.rows[0];
  }

  /**
   * Get companies by industry
   * @param {string} industry - Industry name
   * @returns {Promise<Company[]>} Array of companies
   */
  static async findByIndustry(industry) {
    const sql = 'SELECT * FROM companies WHERE industry = $1 ORDER BY name ASC';
    const result = await query(sql, [industry]);
    return result.rows.map(row => new Company(row));
  }

  /**
   * Get all unique industries
   * @returns {Promise<string[]>} Array of industry names
   */
  static async getIndustries() {
    const sql = 'SELECT DISTINCT industry FROM companies WHERE industry IS NOT NULL ORDER BY industry ASC';
    const result = await query(sql);
    return result.rows.map(row => row.industry);
  }

  /**
   * Get all unique sectors
   * @returns {Promise<string[]>} Array of sector names
   */
  static async getSectors() {
    const sql = 'SELECT DISTINCT sector FROM companies WHERE sector IS NOT NULL ORDER BY sector ASC';
    const result = await query(sql);
    return result.rows.map(row => row.sector);
  }

  /**
   * Validate company data
   * @param {Object} data - Company data to validate
   * @returns {Object} Validation result
   */
  static validate(data) {
    const errors = [];

    if (!data.name || data.name.trim().length === 0) {
      errors.push('Company name is required');
    }

    if (data.ticker_symbol && !/^[A-Z]{1,5}$/.test(data.ticker_symbol)) {
      errors.push('Ticker symbol must be 1-5 uppercase letters');
    }

    if (data.founded_year && (data.founded_year < 1800 || data.founded_year > new Date().getFullYear())) {
      errors.push('Founded year must be between 1800 and current year');
    }

    if (data.employee_count && (isNaN(data.employee_count) || data.employee_count < 0)) {
      errors.push('Employee count must be a positive number');
    }

    if (data.annual_revenue && (isNaN(data.annual_revenue) || data.annual_revenue < 0)) {
      errors.push('Annual revenue must be a positive number');
    }

    if (data.market_cap && (isNaN(data.market_cap) || data.market_cap < 0)) {
      errors.push('Market cap must be a positive number');
    }

    const validSizes = ['startup', 'small', 'medium', 'large', 'enterprise'];
    if (data.company_size && !validSizes.includes(data.company_size)) {
      errors.push('Invalid company size');
    }

    if (data.website_url && !isValidUrl(data.website_url)) {
      errors.push('Invalid website URL');
    }

    return {
      isValid: errors.length === 0,
      errors
    };
  }
}

/**
 * Validate URL format
 * @param {string} url - URL to validate
 * @returns {boolean} Is valid URL
 */
function isValidUrl(url) {
  try {
    new URL(url);
    return true;
  } catch {
    return false;
  }
}

module.exports = Company;