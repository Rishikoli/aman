const fs = require('fs');
const path = require('path');
const { query, connectDB, closeDB } = require('../utils/database');

/**
 * Initialize database with schema
 */
async function initializeDatabase() {
  try {
    console.log('Connecting to database...');
    await connectDB();

    console.log('Reading schema file...');
    const schemaPath = path.join(__dirname, '../database/schema.sql');
    const schema = fs.readFileSync(schemaPath, 'utf8');

    console.log('Executing schema...');
    await query(schema);

    console.log('Database schema initialized successfully!');
    
    // Insert some sample data for testing
    await insertSampleData();
    
    console.log('Sample data inserted successfully!');
    
  } catch (error) {
    console.error('Error initializing database:', error);
    process.exit(1);
  } finally {
    await closeDB();
  }
}

/**
 * Insert sample data for testing
 */
async function insertSampleData() {
  console.log('Inserting sample companies...');
  
  // Sample companies
  const companies = [
    {
      name: 'TechCorp Inc.',
      ticker_symbol: 'TECH',
      industry: 'Technology',
      sector: 'Software',
      company_size: 'large',
      headquarters_location: 'San Francisco, CA',
      founded_year: 2010,
      employee_count: 5000,
      annual_revenue: 2500000000,
      market_cap: 15000000000,
      description: 'Leading technology company specializing in cloud computing and AI solutions.',
      website_url: 'https://techcorp.com'
    },
    {
      name: 'FinanceFirst LLC',
      ticker_symbol: 'FINF',
      industry: 'Financial Services',
      sector: 'Banking',
      company_size: 'medium',
      headquarters_location: 'New York, NY',
      founded_year: 2005,
      employee_count: 2500,
      annual_revenue: 800000000,
      market_cap: 4500000000,
      description: 'Regional banking and financial services provider.',
      website_url: 'https://financefirst.com'
    },
    {
      name: 'GreenEnergy Solutions',
      ticker_symbol: 'GREN',
      industry: 'Energy',
      sector: 'Renewable Energy',
      company_size: 'medium',
      headquarters_location: 'Austin, TX',
      founded_year: 2015,
      employee_count: 1200,
      annual_revenue: 450000000,
      market_cap: 2800000000,
      description: 'Solar and wind energy solutions provider.',
      website_url: 'https://greenenergy.com'
    },
    {
      name: 'HealthTech Innovations',
      industry: 'Healthcare',
      sector: 'Medical Technology',
      company_size: 'startup',
      headquarters_location: 'Boston, MA',
      founded_year: 2020,
      employee_count: 150,
      annual_revenue: 25000000,
      description: 'AI-powered medical diagnostic tools and platforms.',
      website_url: 'https://healthtech-innovations.com'
    }
  ];

  for (const company of companies) {
    const sql = `
      INSERT INTO companies (
        name, ticker_symbol, industry, sector, company_size,
        headquarters_location, founded_year, employee_count, annual_revenue,
        market_cap, description, website_url
      ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
      ON CONFLICT DO NOTHING
    `;
    
    const values = [
      company.name, company.ticker_symbol, company.industry, company.sector,
      company.company_size, company.headquarters_location, company.founded_year,
      company.employee_count, company.annual_revenue, company.market_cap,
      company.description, company.website_url
    ];

    await query(sql, values);
  }

  console.log('Sample companies inserted.');

  // Get company IDs for creating sample deals
  const companiesResult = await query('SELECT id, name FROM companies LIMIT 4');
  const companyIds = companiesResult.rows;

  if (companyIds.length >= 2) {
    console.log('Inserting sample deals...');
    
    const deals = [
      {
        name: 'TechCorp Acquisition of HealthTech',
        description: 'Strategic acquisition to expand into healthcare AI market',
        acquirer_id: companyIds[0].id,
        target_id: companyIds[3].id,
        deal_value: 500000000,
        currency: 'USD',
        status: 'active',
        created_by: 'john.doe@example.com',
        priority: 8
      },
      {
        name: 'FinanceFirst Merger with GreenEnergy',
        description: 'Merger to create integrated financial services for renewable energy sector',
        acquirer_id: companyIds[1].id,
        target_id: companyIds[2].id,
        deal_value: 1200000000,
        currency: 'USD',
        status: 'draft',
        created_by: 'jane.smith@example.com',
        priority: 6
      }
    ];

    for (const deal of deals) {
      const sql = `
        INSERT INTO deals (
          name, description, acquirer_id, target_id, deal_value,
          currency, status, created_by, priority
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
        ON CONFLICT DO NOTHING
      `;
      
      const values = [
        deal.name, deal.description, deal.acquirer_id, deal.target_id,
        deal.deal_value, deal.currency, deal.status, deal.created_by, deal.priority
      ];

      await query(sql, values);
    }

    console.log('Sample deals inserted.');
  }
}

/**
 * Drop all tables (for reset)
 */
async function dropTables() {
  try {
    console.log('Dropping all tables...');
    
    const dropSql = `
      DROP TABLE IF EXISTS deal_timeline_estimates CASCADE;
      DROP TABLE IF EXISTS financial_data CASCADE;
      DROP TABLE IF EXISTS findings CASCADE;
      DROP TABLE IF EXISTS agent_executions CASCADE;
      DROP TABLE IF EXISTS deals CASCADE;
      DROP TABLE IF EXISTS companies CASCADE;
      
      DROP TYPE IF EXISTS deal_status CASCADE;
      DROP TYPE IF EXISTS company_size CASCADE;
      DROP TYPE IF EXISTS execution_status CASCADE;
      DROP TYPE IF EXISTS risk_category CASCADE;
      DROP TYPE IF EXISTS severity_level CASCADE;
      DROP TYPE IF EXISTS agent_type CASCADE;
      
      DROP FUNCTION IF EXISTS update_updated_at_column() CASCADE;
    `;
    
    await query(dropSql);
    console.log('All tables dropped successfully!');
    
  } catch (error) {
    console.error('Error dropping tables:', error);
    throw error;
  }
}

/**
 * Reset database (drop and recreate)
 */
async function resetDatabase() {
  try {
    console.log('Resetting database...');
    await connectDB();
    await dropTables();
    await initializeDatabase();
    console.log('Database reset completed!');
  } catch (error) {
    console.error('Error resetting database:', error);
    process.exit(1);
  } finally {
    await closeDB();
  }
}

// Command line interface
const command = process.argv[2];

switch (command) {
  case 'init':
    initializeDatabase();
    break;
  case 'reset':
    resetDatabase();
    break;
  case 'drop':
    (async () => {
      try {
        await connectDB();
        await dropTables();
      } finally {
        await closeDB();
      }
    })();
    break;
  default:
    console.log('Usage: node initDatabase.js [init|reset|drop]');
    console.log('  init  - Initialize database with schema and sample data');
    console.log('  reset - Drop all tables and reinitialize');
    console.log('  drop  - Drop all tables');
    process.exit(1);
}

module.exports = {
  initializeDatabase,
  resetDatabase,
  dropTables,
  insertSampleData
};