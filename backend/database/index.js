const { DatabaseManager, DatabaseError } = require('./DatabaseManager');
const { ConfigValidator } = require('./ConfigValidator');
const { logger } = require('../utils/logger');

/**
 * Database module entry point - provides enhanced database functionality
 * while maintaining backward compatibility with existing code
 */

// Global database manager instance
let globalDatabaseManager = null;

/**
 * Initialize the global database manager
 * @param {Object} config - Optional configuration override
 * @returns {Promise<DatabaseManager>} Initialized database manager
 */
async function initializeDatabaseManager(config = null) {
  if (globalDatabaseManager && globalDatabaseManager.isInitialized) {
    logger.warn('Database manager already initialized');
    return globalDatabaseManager;
  }

  try {
    logger.info('Initializing enhanced database manager...');
    
    // Validate configuration if provided
    if (config) {
      const validator = new ConfigValidator();
      const validationResult = validator.validateForEnvironment(config);
      
      if (validationResult.warnings.length > 0) {
        logger.warn('Configuration warnings:', validationResult.warnings);
      }
      
      logger.info('Configuration validation passed');
    }

    // Create and initialize database manager
    globalDatabaseManager = new DatabaseManager(config);
    
    // Set up event listeners for monitoring
    setupDatabaseEventListeners(globalDatabaseManager);
    
    await globalDatabaseManager.initialize();
    
    logger.info('Enhanced database manager initialized successfully');
    return globalDatabaseManager;
    
  } catch (error) {
    logger.error('Failed to initialize database manager', error);
    throw error;
  }
}

/**
 * Get the global database manager instance
 * @returns {DatabaseManager} Database manager instance
 * @throws {DatabaseError} If not initialized
 */
function getDatabaseManager() {
  if (!globalDatabaseManager || !globalDatabaseManager.isInitialized) {
    throw new DatabaseError(
      'NOT_INITIALIZED',
      'Database manager not initialized. Call initializeDatabaseManager() first.'
    );
  }
  
  return globalDatabaseManager;
}

/**
 * Set up event listeners for database monitoring and logging
 * @param {DatabaseManager} dbManager - Database manager instance
 */
function setupDatabaseEventListeners(dbManager) {
  // Log initialization events
  dbManager.on('initialized', () => {
    logger.info('Database manager initialized');
  });

  dbManager.on('shutdown', () => {
    logger.info('Database manager shutdown');
  });

  // Log connection events
  dbManager.on('clientConnect', () => {
    logger.debug('New database client connected');
  });

  dbManager.on('clientAcquire', () => {
    logger.debug('Database client acquired from pool');
  });

  dbManager.on('clientRemove', () => {
    logger.debug('Database client removed from pool');
  });

  // Log performance events
  dbManager.on('slowQuery', (data) => {
    logger.warn('Slow query detected', {
      query: data.text.substring(0, 100),
      duration: data.duration,
      threshold: dbManager.config.monitoring.slowQueryThreshold
    });
  });

  // Log error events
  dbManager.on('poolError', (error) => {
    logger.error('Database pool error', error);
  });
}

/**
 * Execute a database query with enhanced error handling and logging
 * @param {string} text - SQL query text
 * @param {Array} params - Query parameters
 * @param {Object} options - Query options
 * @returns {Promise<Object>} Query result
 */
async function query(text, params = [], options = {}) {
  const dbManager = getDatabaseManager();
  return await dbManager.query(text, params, options);
}

/**
 * Get a database connection from the pool
 * @param {Object} options - Connection options
 * @returns {Promise<Object>} Database client
 */
async function getConnection(options = {}) {
  const dbManager = getDatabaseManager();
  return await dbManager.getConnection(options);
}

/**
 * Execute operation within a transaction
 * @param {Function} callback - Transaction callback
 * @param {Object} options - Transaction options
 * @returns {Promise<*>} Transaction result
 */
async function withTransaction(callback, options = {}) {
  const dbManager = getDatabaseManager();
  return await dbManager.withTransaction(callback, options);
}

/**
 * Execute operation with retry logic
 * @param {Function} operation - Operation to execute
 * @param {Object} options - Retry options
 * @returns {Promise<*>} Operation result
 */
async function withRetry(operation, options = {}) {
  const dbManager = getDatabaseManager();
  return await dbManager.withRetry(operation, options);
}

/**
 * Perform database health check
 * @returns {Promise<Object>} Health check result
 */
async function healthCheck() {
  const dbManager = getDatabaseManager();
  return await dbManager.healthCheck();
}

/**
 * Get database connection pool metrics
 * @returns {Object} Pool metrics
 */
function getPoolMetrics() {
  const dbManager = getDatabaseManager();
  return dbManager.getPoolMetrics();
}

/**
 * Gracefully shutdown the database manager
 * @returns {Promise<void>}
 */
async function shutdown() {
  if (globalDatabaseManager && globalDatabaseManager.isInitialized) {
    await globalDatabaseManager.shutdown();
    globalDatabaseManager = null;
  }
}

/**
 * Backward compatibility functions for existing code
 */

/**
 * Legacy connectDB function - enhanced with new manager
 * @returns {Promise<DatabaseManager>} Database manager instance
 */
async function connectDB() {
  try {
    if (!globalDatabaseManager) {
      await initializeDatabaseManager();
    }
    
    // Perform health check to ensure connection is working
    const health = await healthCheck();
    if (health.status !== 'healthy') {
      throw new DatabaseError('CONNECTION_UNHEALTHY', 'Database health check failed');
    }
    
    logger.info('Database connection established successfully');
    return globalDatabaseManager;
    
  } catch (error) {
    logger.error('Database connection failed', error);
    throw error;
  }
}

/**
 * Legacy getClient function - returns enhanced client
 * @returns {Promise<Object>} Database client
 */
async function getClient() {
  return await getConnection();
}

/**
 * Legacy closeDB function
 * @returns {Promise<void>}
 */
async function closeDB() {
  await shutdown();
}

/**
 * Legacy getPool function - returns pool metrics instead
 * @returns {Object} Pool information
 */
function getPool() {
  try {
    const dbManager = getDatabaseManager();
    return {
      // Provide pool-like interface for backward compatibility
      query: (text, params) => dbManager.query(text, params),
      connect: () => dbManager.getConnection(),
      end: () => dbManager.shutdown(),
      
      // Include metrics for monitoring
      ...dbManager.getPoolMetrics()
    };
  } catch (error) {
    logger.warn('Database manager not initialized, returning null');
    return null;
  }
}

// Export enhanced database interface
module.exports = {
  // Enhanced functions
  initializeDatabaseManager,
  getDatabaseManager,
  query,
  getConnection,
  withTransaction,
  withRetry,
  healthCheck,
  getPoolMetrics,
  shutdown,
  
  // Backward compatibility functions
  connectDB,
  getClient,
  closeDB,
  getPool,
  
  // Classes and utilities
  DatabaseManager,
  DatabaseError,
  ConfigValidator,
  
  // For testing and advanced usage
  setupDatabaseEventListeners
};