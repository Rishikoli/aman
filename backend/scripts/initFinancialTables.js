/**
 * Initialize Financial Analysis Tables
 * Creates the new tables for M&A financial analysis
 */

const { Pool } = require('pg');
const fs = require('fs');
const path = require('path');
require('dotenv').config();

const pool = new Pool({
  user: process.env.DB_USER,
  host: process.env.DB_HOST,
  database: process.env.DB_NAME,
  password: process.env.DB_PASSWORD,
  port: process.env.DB_PORT,
});

async function initFinancialTables() {
  const client = await pool.connect();
  
  try {
    console.log('🚀 Initializing financial analysis tables...');

    // Read and execute the schema
    const schemaPath = path.join(__dirname, '../database/schema.sql');
    const schema = fs.readFileSync(schemaPath, 'utf8');
    
    // Split schema into individual statements
    const statements = schema
      .split(';')
      .map(stmt => stmt.trim())
      .filter(stmt => stmt.length > 0 && !stmt.startsWith('--'));

    for (const statement of statements) {
      try {
        await client.query(statement);
        console.log('✅ Executed statement successfully');
      } catch (error) {
        if (error.message.includes('already exists')) {
          console.log('⚠️  Table/function already exists, skipping...');
        } else {
          console.error('❌ Error executing statement:', error.message);
          console.error('Statement:', statement.substring(0, 100) + '...');
        }
      }
    }

    // Insert sample companies for testing
    await insertSampleCompanies(client);

    console.log('🎉 Financial analysis tables initialized successfully!');

  } catch (error) {
    console.error('❌ Failed to initialize financial tables:', error);
    throw error;
  } finally {
    client.release();
  }
}

async function insertSampleCompanies(client) {
  console.log('📊 Inserting sample companies...');

  const sampleCompanies = [
    {
      name: 'Apple Inc.',
      ticker: 'AAPL',
      industry: 'Technology',
      sector: 'Consumer Electronics',
      size: 'enterprise',
      headquarters: 'Cupertino, CA',
      founded: 1976,
      employees: 164000,
      revenue: 394328000000,
      marketCap: 3000000000000
    },
    {
      name: 'Microsoft Corporation',
      ticker: 'MSFT',
      industry: 'Technology',
      sector: 'Software',
      size: 'enterprise',
      headquarters: 'Redmond, WA',
      founded: 1975,
      employees: 221000,
      revenue: 211915000000,
      marketCap: 2800000000000
    },
    {
      name: 'Amazon.com Inc.',
      ticker: 'AMZN',
      industry: 'Technology',
      sector: 'E-commerce',
      size: 'enterprise',
      headquarters: 'Seattle, WA',
      founded: 1994,
      employees: 1541000,
      revenue: 513983000000,
      marketCap: 1500000000000
    },
    {
      name: 'Alphabet Inc.',
      ticker: 'GOOGL',
      industry: 'Technology',
      sector: 'Internet Services',
      size: 'enterprise',
      headquarters: 'Mountain View, CA',
      founded: 1998,
      employees: 190000,
      revenue: 307394000000,
      marketCap: 1700000000000
    },
    {
      name: 'Tesla Inc.',
      ticker: 'TSLA',
      industry: 'Automotive',
      sector: 'Electric Vehicles',
      size: 'large',
      headquarters: 'Austin, TX',
      founded: 2003,
      employees: 140000,
      revenue: 96773000000,
      marketCap: 800000000000
    },
    {
      name: 'Meta Platforms Inc.',
      ticker: 'META',
      industry: 'Technology',
      sector: 'Social Media',
      size: 'enterprise',
      headquarters: 'Menlo Park, CA',
      founded: 2004,
      employees: 86482,
      revenue: 134902000000,
      marketCap: 900000000000
    },
    {
      name: 'NVIDIA Corporation',
      ticker: 'NVDA',
      industry: 'Technology',
      sector: 'Semiconductors',
      size: 'large',
      headquarters: 'Santa Clara, CA',
      founded: 1993,
      employees: 29600,
      revenue: 79775000000,
      marketCap: 1800000000000
    },
    {
      name: 'Netflix Inc.',
      ticker: 'NFLX',
      industry: 'Technology',
      sector: 'Streaming',
      size: 'large',
      headquarters: 'Los Gatos, CA',
      founded: 1997,
      employees: 12800,
      revenue: 33723000000,
      marketCap: 200000000000
    },
    {
      name: 'Adobe Inc.',
      ticker: 'ADBE',
      industry: 'Technology',
      sector: 'Software',
      size: 'large',
      headquarters: 'San Jose, CA',
      founded: 1982,
      employees: 28000,
      revenue: 19411000000,
      marketCap: 250000000000
    },
    {
      name: 'Salesforce Inc.',
      ticker: 'CRM',
      industry: 'Technology',
      sector: 'Cloud Software',
      size: 'large',
      headquarters: 'San Francisco, CA',
      founded: 1999,
      employees: 79000,
      revenue: 31352000000,
      marketCap: 220000000000
    }
  ];

  for (const company of sampleCompanies) {
    try {
      // Check if company already exists
      const existingResult = await client.query(
        'SELECT id FROM companies WHERE ticker_symbol = $1',
        [company.ticker]
      );

      if (existingResult.rows.length === 0) {
        await client.query(
          `INSERT INTO companies (
            name, ticker_symbol, industry, sector, company_size,
            headquarters_location, founded_year, employee_count,
            annual_revenue, market_cap, description
          ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)`,
          [
            company.name,
            company.ticker,
            company.industry,
            company.sector,
            company.size,
            company.headquarters,
            company.founded,
            company.employees,
            company.revenue,
            company.marketCap,
            `${company.name} - Major ${company.sector} company`
          ]
        );
        console.log(`✅ Inserted ${company.name} (${company.ticker})`);
      } else {
        console.log(`⚠️  ${company.name} (${company.ticker}) already exists`);
      }
    } catch (error) {
      console.error(`❌ Failed to insert ${company.name}:`, error.message);
    }
  }
}

// Run the initialization
if (require.main === module) {
  initFinancialTables()
    .then(() => {
      console.log('✅ Database initialization completed');
      process.exit(0);
    })
    .catch((error) => {
      console.error('❌ Database initialization failed:', error);
      process.exit(1);
    });
}

module.exports = { initFinancialTables };