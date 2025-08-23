const express = require('express');
const { body, param, query, validationResult } = require('express-validator');
const router = express.Router();

const Company = require('../../models/Company');

// Validation middleware
const handleValidationErrors = (req, res, next) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({
      error: 'Validation failed',
      details: errors.array()
    });
  }
  next();
};

// GET /api/v1/companies - Get all companies
router.get('/', [
  query('industry').optional().isString(),
  query('sector').optional().isString(),
  query('company_size').optional().isIn(['startup', 'small', 'medium', 'large', 'enterprise']),
  query('search').optional().isString(),
  query('limit').optional().isInt({ min: 1, max: 100 }),
  handleValidationErrors
], async (req, res) => {
  try {
    const filters = {
      industry: req.query.industry,
      sector: req.query.sector,
      company_size: req.query.company_size,
      search: req.query.search,
      limit: req.query.limit ? parseInt(req.query.limit) : undefined
    };

    // Remove undefined values
    Object.keys(filters).forEach(key => {
      if (filters[key] === undefined) {
        delete filters[key];
      }
    });

    const companies = await Company.findAll(filters);
    const statistics = await Company.getStatistics();

    res.json({
      success: true,
      data: {
        companies,
        statistics,
        total: companies.length
      }
    });
  } catch (error) {
    console.error('Error fetching companies:', error);
    res.status(500).json({ 
      success: false,
      error: 'Failed to fetch companies',
      message: error.message 
    });
  }
});

// POST /api/v1/companies - Create new company
router.post('/', [
  body('name').notEmpty().trim().isLength({ min: 1, max: 255 }),
  body('ticker_symbol').optional().matches(/^[A-Z]{1,5}$/),
  body('industry').optional().isString(),
  body('sector').optional().isString(),
  body('company_size').optional().isIn(['startup', 'small', 'medium', 'large', 'enterprise']),
  body('headquarters_location').optional().isString(),
  body('founded_year').optional().isInt({ min: 1800, max: new Date().getFullYear() }),
  body('employee_count').optional().isInt({ min: 0 }),
  body('annual_revenue').optional().isFloat({ min: 0 }),
  body('market_cap').optional().isFloat({ min: 0 }),
  body('description').optional().isString(),
  body('website_url').optional().isURL(),
  handleValidationErrors
], async (req, res) => {
  try {
    const companyData = {
      name: req.body.name,
      ticker_symbol: req.body.ticker_symbol?.toUpperCase(),
      industry: req.body.industry,
      sector: req.body.sector,
      company_size: req.body.company_size,
      headquarters_location: req.body.headquarters_location,
      founded_year: req.body.founded_year,
      employee_count: req.body.employee_count,
      annual_revenue: req.body.annual_revenue,
      market_cap: req.body.market_cap,
      description: req.body.description,
      website_url: req.body.website_url
    };

    // Check if ticker symbol already exists
    if (companyData.ticker_symbol) {
      const existingCompany = await Company.findByTicker(companyData.ticker_symbol);
      if (existingCompany) {
        return res.status(400).json({
          success: false,
          error: 'Ticker symbol already exists',
          message: `Company with ticker ${companyData.ticker_symbol} already exists`
        });
      }
    }

    const company = new Company(companyData);
    await company.save();

    res.status(201).json({
      success: true,
      message: 'Company created successfully',
      data: { company }
    });
  } catch (error) {
    console.error('Error creating company:', error);
    res.status(400).json({ 
      success: false,
      error: 'Failed to create company',
      message: error.message 
    });
  }
});

// GET /api/v1/companies/:id - Get specific company
router.get('/:id', [
  param('id').isUUID(),
  handleValidationErrors
], async (req, res) => {
  try {
    const { id } = req.params;
    const company = await Company.findById(id);

    if (!company) {
      return res.status(404).json({
        success: false,
        error: 'Company not found'
      });
    }

    res.json({
      success: true,
      data: { company }
    });
  } catch (error) {
    console.error('Error fetching company:', error);
    res.status(500).json({ 
      success: false,
      error: 'Failed to fetch company',
      message: error.message 
    });
  }
});

// PUT /api/v1/companies/:id - Update company
router.put('/:id', [
  param('id').isUUID(),
  body('name').optional().trim().isLength({ min: 1, max: 255 }),
  body('ticker_symbol').optional().matches(/^[A-Z]{1,5}$/),
  body('industry').optional().isString(),
  body('sector').optional().isString(),
  body('company_size').optional().isIn(['startup', 'small', 'medium', 'large', 'enterprise']),
  body('headquarters_location').optional().isString(),
  body('founded_year').optional().isInt({ min: 1800, max: new Date().getFullYear() }),
  body('employee_count').optional().isInt({ min: 0 }),
  body('annual_revenue').optional().isFloat({ min: 0 }),
  body('market_cap').optional().isFloat({ min: 0 }),
  body('description').optional().isString(),
  body('website_url').optional().isURL(),
  handleValidationErrors
], async (req, res) => {
  try {
    const { id } = req.params;
    const company = await Company.findById(id);
    
    if (!company) {
      return res.status(404).json({
        success: false,
        error: 'Company not found'
      });
    }

    // Check if ticker symbol already exists (if being updated)
    if (req.body.ticker_symbol && req.body.ticker_symbol !== company.ticker_symbol) {
      const existingCompany = await Company.findByTicker(req.body.ticker_symbol);
      if (existingCompany) {
        return res.status(400).json({
          success: false,
          error: 'Ticker symbol already exists',
          message: `Company with ticker ${req.body.ticker_symbol} already exists`
        });
      }
    }

    // Update company properties
    Object.keys(req.body).forEach(key => {
      if (req.body[key] !== undefined) {
        if (key === 'ticker_symbol') {
          company[key] = req.body[key].toUpperCase();
        } else {
          company[key] = req.body[key];
        }
      }
    });

    await company.update();

    res.json({
      success: true,
      message: 'Company updated successfully',
      data: { company }
    });
  } catch (error) {
    console.error('Error updating company:', error);
    res.status(500).json({ 
      success: false,
      error: 'Failed to update company',
      message: error.message 
    });
  }
});

// DELETE /api/v1/companies/:id - Delete company
router.delete('/:id', [
  param('id').isUUID(),
  handleValidationErrors
], async (req, res) => {
  try {
    const { id } = req.params;
    const deleted = await Company.deleteById(id);
    
    if (!deleted) {
      return res.status(404).json({
        success: false,
        error: 'Company not found'
      });
    }

    res.json({
      success: true,
      message: 'Company deleted successfully'
    });
  } catch (error) {
    console.error('Error deleting company:', error);
    res.status(500).json({ 
      success: false,
      error: 'Failed to delete company',
      message: error.message 
    });
  }
});

// GET /api/v1/companies/search/:term - Search companies
router.get('/search/:term', [
  param('term').notEmpty().trim(),
  query('limit').optional().isInt({ min: 1, max: 50 }),
  handleValidationErrors
], async (req, res) => {
  try {
    const { term } = req.params;
    const limit = req.query.limit ? parseInt(req.query.limit) : 10;
    
    const companies = await Company.search(term, limit);

    res.json({
      success: true,
      data: {
        companies,
        search_term: term,
        total: companies.length
      }
    });
  } catch (error) {
    console.error('Error searching companies:', error);
    res.status(500).json({ 
      success: false,
      error: 'Failed to search companies',
      message: error.message 
    });
  }
});

// GET /api/v1/companies/ticker/:ticker - Get company by ticker
router.get('/ticker/:ticker', [
  param('ticker').matches(/^[A-Z]{1,5}$/),
  handleValidationErrors
], async (req, res) => {
  try {
    const { ticker } = req.params;
    const company = await Company.findByTicker(ticker);

    if (!company) {
      return res.status(404).json({
        success: false,
        error: 'Company not found',
        message: `No company found with ticker ${ticker}`
      });
    }

    res.json({
      success: true,
      data: { company }
    });
  } catch (error) {
    console.error('Error fetching company by ticker:', error);
    res.status(500).json({ 
      success: false,
      error: 'Failed to fetch company',
      message: error.message 
    });
  }
});

// GET /api/v1/companies/industry/:industry - Get companies by industry
router.get('/industry/:industry', [
  param('industry').notEmpty().trim(),
  handleValidationErrors
], async (req, res) => {
  try {
    const { industry } = req.params;
    const companies = await Company.findByIndustry(industry);

    res.json({
      success: true,
      data: {
        companies,
        industry,
        total: companies.length
      }
    });
  } catch (error) {
    console.error('Error fetching companies by industry:', error);
    res.status(500).json({ 
      success: false,
      error: 'Failed to fetch companies',
      message: error.message 
    });
  }
});

// GET /api/v1/companies/meta/industries - Get all industries
router.get('/meta/industries', async (req, res) => {
  try {
    const industries = await Company.getIndustries();

    res.json({
      success: true,
      data: {
        industries,
        total: industries.length
      }
    });
  } catch (error) {
    console.error('Error fetching industries:', error);
    res.status(500).json({ 
      success: false,
      error: 'Failed to fetch industries',
      message: error.message 
    });
  }
});

// GET /api/v1/companies/meta/sectors - Get all sectors
router.get('/meta/sectors', async (req, res) => {
  try {
    const sectors = await Company.getSectors();

    res.json({
      success: true,
      data: {
        sectors,
        total: sectors.length
      }
    });
  } catch (error) {
    console.error('Error fetching sectors:', error);
    res.status(500).json({ 
      success: false,
      error: 'Failed to fetch sectors',
      message: error.message 
    });
  }
});

module.exports = router;