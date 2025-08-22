const { Pool } = require('pg');
const { getConfig } = require('./env-config');

let pool = null;

/**
 * Initialize PostgreSQL connection pool
 * @returns {Pool} PostgreSQL connection pool
 */
function initializePool() {
  if (pool) {
    return pool;
  }

  const config = getConfig();
  
  // Create connection pool
  pool = new Pool({
    host: config.database.host,
    port: config.database.port,
    database: config.database.name,
    user: config.database.user,
    password: config.database.password,
    max: 20, // Maximum number of clients in the pool
    idleTimeoutMillis: 30000, // Close idle clients after 30 seconds
    connectionTimeoutMillis: 2000, // Return an error after 2 seconds if connection could not be established
    maxUses: 7500, // Close (and replace) a connection after it has been used 7500 times
  });

  // Handle pool errors
  pool.on('error', (err) => {
    console.error('Unexpected error on idle client', err);
    process.exit(-1);
  });

  return pool;
}

/**
 * Get database connection pool
 * @returns {Pool} PostgreSQL connection pool
 */
function getPool() {
  if (!pool) {
    return initializePool();
  }
  return pool;
}

/**
 * Connect to database and test connection
 * @returns {Promise<void>}
 */
async function connectDB() {
  try {
    const dbPool = getPool();
    
    // Test the connection
    const client = await dbPool.connect();
    const result = await client.query('SELECT NOW()');
    client.release();
    
    console.log('Database connection established at:', result.rows[0].now);
    return dbPool;
  } catch (error) {
    console.error('Database connection failed:', error.message);
    throw error;
  }
}

/**
 * Execute a query with parameters
 * @param {string} text - SQL query text
 * @param {Array} params - Query parameters
 * @returns {Promise<Object>} Query result
 */
async function query(text, params = []) {
  const dbPool = getPool();
  const start = Date.now();
  
  try {
    const result = await dbPool.query(text, params);
    const duration = Date.now() - start;
    
    console.log('Executed query', { text, duration, rows: result.rowCount });
    return result;
  } catch (error) {
    console.error('Query error:', { text, error: error.message });
    throw error;
  }
}

/**
 * Get a client from the pool for transactions
 * @returns {Promise<Object>} Database client
 */
async function getClient() {
  const dbPool = getPool();
  return await dbPool.connect();
}

/**
 * Close all database connections
 * @returns {Promise<void>}
 */
async function closeDB() {
  if (pool) {
    await pool.end();
    pool = null;
    console.log('Database connections closed');
  }
}

module.exports = {
  connectDB,
  query,
  getClient,
  getPool,
  closeDB
};