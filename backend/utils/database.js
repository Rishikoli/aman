// Enhanced database utilities using the new DatabaseManager
// This file maintains backward compatibility while providing enhanced functionality

const { 
  connectDB: enhancedConnectDB,
  query: enhancedQuery,
  getClient: enhancedGetClient,
  closeDB: enhancedCloseDB,
  getPool: enhancedGetPool,
  initializeDatabaseManager,
  healthCheck,
  getPoolMetrics
} = require('../database');

// Legacy compatibility layer
let isEnhancedManagerInitialized = false;

/**
 * Initialize enhanced database manager if not already done
 * @private
 */
async function ensureEnhancedManager() {
  if (!isEnhancedManagerInitialized) {
    try {
      await initializeDatabaseManager();
      isEnhancedManagerInitialized = true;
      console.log('Enhanced database manager initialized');
    } catch (error) {
      console.error('Failed to initialize enhanced database manager:', error.message);
      throw error;
    }
  }
}

/**
 * Initialize PostgreSQL connection pool (legacy compatibility)
 * @returns {Object} Pool-like object with enhanced functionality
 * @deprecated Use initializeDatabaseManager() instead
 */
async function initializePool() {
  await ensureEnhancedManager();
  return enhancedGetPool();
}

/**
 * Get database connection pool (legacy compatibility)
 * @returns {Object} Pool-like object with enhanced functionality
 * @deprecated Use getDatabaseManager() instead
 */
function getPool() {
  if (!isEnhancedManagerInitialized) {
    console.warn('Enhanced database manager not initialized. Call connectDB() first.');
    return null;
  }
  return enhancedGetPool();
}

/**
 * Connect to database and test connection
 * @returns {Promise<Object>} Database manager instance
 */
async function connectDB() {
  await ensureEnhancedManager();
  return await enhancedConnectDB();
}

/**
 * Execute a query with parameters
 * @param {string} text - SQL query text
 * @param {Array} params - Query parameters
 * @returns {Promise<Object>} Query result
 */
async function query(text, params = []) {
  await ensureEnhancedManager();
  return await enhancedQuery(text, params);
}

/**
 * Get a client from the pool for transactions
 * @returns {Promise<Object>} Database client
 */
async function getClient() {
  await ensureEnhancedManager();
  return await enhancedGetClient();
}

/**
 * Close all database connections
 * @returns {Promise<void>}
 */
async function closeDB() {
  if (isEnhancedManagerInitialized) {
    await enhancedCloseDB();
    isEnhancedManagerInitialized = false;
    console.log('Enhanced database connections closed');
  }
}

module.exports = {
  connectDB,
  query,
  getClient,
  getPool,
  closeDB
};