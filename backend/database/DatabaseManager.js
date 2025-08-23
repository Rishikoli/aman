const { Pool } = require('pg');
const EventEmitter = require('events');
const { getConfig } = require('../utils/env-config');

/**
 * Enhanced Database Manager with connection lifecycle management,
 * configuration validation, and comprehensive error handling
 */
class DatabaseManager extends EventEmitter {
  constructor(config = null) {
    super();

    this.config = config ? this._loadProvidedConfiguration(config) : this._loadConfiguration();
    this.pool = null;
    this.isInitialized = false;
    this.connectionAttempts = 0;
    this.maxConnectionAttempts = 3;
    this.retryDelay = 1000; // Base delay in milliseconds
    this.backoffMultiplier = 2;

    // Bind methods to preserve context
    this._handlePoolError = this._handlePoolError.bind(this);
    this._handlePoolConnect = this._handlePoolConnect.bind(this);
    this._handlePoolAcquire = this._handlePoolAcquire.bind(this);
    this._handlePoolRemove = this._handlePoolRemove.bind(this);
  }

  /**
   * Load and validate database configuration
   * @returns {Object} Validated configuration object
   * @private
   */
  _loadConfiguration() {
    try {
      const envConfig = getConfig();

      // Enhanced database configuration with defaults
      const dbConfig = {
        // Connection settings
        host: envConfig.database.host,
        port: envConfig.database.port,
        database: envConfig.database.name,
        user: envConfig.database.user,
        password: envConfig.database.password,

        // Pool settings
        max: parseInt(process.env.DB_POOL_MAX, 10) || 20,
        min: parseInt(process.env.DB_POOL_MIN, 10) || 5,
        idleTimeoutMillis: parseInt(process.env.DB_IDLE_TIMEOUT, 10) || 30000,
        connectionTimeoutMillis: parseInt(process.env.DB_CONNECTION_TIMEOUT, 10) || 5000,
        acquireTimeoutMillis: parseInt(process.env.DB_ACQUIRE_TIMEOUT, 10) || 60000,
        maxUses: parseInt(process.env.DB_MAX_USES, 10) || 7500,

        // SSL configuration
        ssl: process.env.NODE_ENV === 'production' ? {
          rejectUnauthorized: process.env.DB_SSL_REJECT_UNAUTHORIZED !== 'false'
        } : false,

        // Retry configuration
        retry: {
          attempts: parseInt(process.env.DB_RETRY_ATTEMPTS, 10) || 3,
          delay: parseInt(process.env.DB_RETRY_DELAY, 10) || 1000,
          backoffMultiplier: parseFloat(process.env.DB_RETRY_BACKOFF, 10) || 2
        },

        // Monitoring configuration
        monitoring: {
          healthCheckInterval: parseInt(process.env.DB_HEALTH_CHECK_INTERVAL, 10) || 30000,
          slowQueryThreshold: parseInt(process.env.DB_SLOW_QUERY_THRESHOLD, 10) || 1000,
          enableQueryLogging: process.env.DB_ENABLE_QUERY_LOGGING === 'true'
        }
      };

      this._validateConfiguration(dbConfig);
      return dbConfig;
    } catch (error) {
      this._logError('Configuration loading failed', error);
      throw new DatabaseError('CONFIGURATION_ERROR', 'Failed to load database configuration', error);
    }
  }

  /**
   * Load configuration from provided config object
   * @param {Object} config - Configuration object
   * @returns {Object} Validated configuration object
   * @private
   */
  _loadProvidedConfiguration(config) {
    try {
      // Apply defaults to provided configuration
      const dbConfig = {
        // Connection settings (required)
        host: config.host,
        port: config.port,
        database: config.database,
        user: config.user,
        password: config.password,

        // Pool settings (with defaults)
        max: config.max || 20,
        min: config.min || 5,
        idleTimeoutMillis: config.idleTimeoutMillis || 30000,
        connectionTimeoutMillis: config.connectionTimeoutMillis || 5000,
        acquireTimeoutMillis: config.acquireTimeoutMillis || 60000,
        maxUses: config.maxUses || 7500,

        // SSL configuration
        ssl: config.ssl || false,

        // Retry configuration
        retry: {
          attempts: config.retry?.attempts || 3,
          delay: config.retry?.delay || 1000,
          backoffMultiplier: config.retry?.backoffMultiplier || 2
        },

        // Monitoring configuration
        monitoring: {
          healthCheckInterval: config.monitoring?.healthCheckInterval || 30000,
          slowQueryThreshold: config.monitoring?.slowQueryThreshold || 1000,
          enableQueryLogging: config.monitoring?.enableQueryLogging || false
        }
      };

      this._validateConfiguration(dbConfig);
      return dbConfig;
    } catch (error) {
      this._logError('Configuration loading failed', error);
      throw new DatabaseError('CONFIGURATION_ERROR', 'Failed to load database configuration', error);
    }
  }

  /**
   * Validate database configuration
   * @param {Object} config - Configuration object to validate
   * @throws {DatabaseError} If configuration is invalid
   * @private
   */
  _validateConfiguration(config) {
    const requiredFields = ['host', 'port', 'database', 'user', 'password'];
    const missingFields = requiredFields.filter(field => !config[field]);

    if (missingFields.length > 0) {
      throw new DatabaseError(
        'INVALID_CONFIGURATION',
        `Missing required configuration fields: ${missingFields.join(', ')}`
      );
    }

    // Validate numeric values
    const numericFields = {
      port: { min: 1, max: 65535 },
      max: { min: 1, max: 100 },
      min: { min: 0, max: config.max - 1 },
      idleTimeoutMillis: { min: 1000, max: 300000 },
      connectionTimeoutMillis: { min: 1000, max: 60000 },
      acquireTimeoutMillis: { min: 1000, max: 300000 }
    };

    for (const [field, limits] of Object.entries(numericFields)) {
      const value = config[field];
      if (typeof value !== 'number' || value < limits.min || value > limits.max) {
        throw new DatabaseError(
          'INVALID_CONFIGURATION',
          `Invalid ${field}: must be a number between ${limits.min} and ${limits.max}`
        );
      }
    }

    this._logInfo('Database configuration validated successfully');
  }

  /**
   * Initialize the database connection pool
   * @param {Object} options - Initialization options
   * @returns {Promise<void>}
   */
  async initialize(options = {}) {
    if (this.isInitialized) {
      this._logWarn('Database manager already initialized');
      return;
    }

    try {
      this._logInfo('Initializing database manager...');

      // Create connection pool
      this.pool = new Pool(this.config);

      // Set up event listeners
      this._setupEventListeners();

      // Test initial connection
      await this._testConnection();

      this.isInitialized = true;
      this.connectionAttempts = 0;

      this._logInfo('Database manager initialized successfully');
      this.emit('initialized');

    } catch (error) {
      this._logError('Database initialization failed', error);
      await this._cleanup();
      throw new DatabaseError('INITIALIZATION_ERROR', 'Failed to initialize database manager', error);
    }
  }

  /**
   * Set up event listeners for the connection pool
   * @private
   */
  _setupEventListeners() {
    this.pool.on('error', this._handlePoolError);
    this.pool.on('connect', this._handlePoolConnect);
    this.pool.on('acquire', this._handlePoolAcquire);
    this.pool.on('remove', this._handlePoolRemove);
  }

  /**
   * Test database connection
   * @returns {Promise<void>}
   * @private
   */
  async _testConnection() {
    const client = await this.pool.connect();
    try {
      const result = await client.query('SELECT NOW() as current_time, version() as pg_version');
      this._logInfo('Database connection test successful', {
        currentTime: result.rows[0].current_time,
        version: result.rows[0].pg_version ? result.rows[0].pg_version.split(' ')[0] : 'Unknown'
      });
    } finally {
      client.release();
    }
  }

  /**
   * Get a database connection from the pool
   * @param {Object} options - Connection options
   * @returns {Promise<Object>} Database client
   */
  async getConnection(options = {}) {
    if (!this.isInitialized) {
      throw new DatabaseError('NOT_INITIALIZED', 'Database manager not initialized');
    }

    const timeout = options.timeout || this.config.acquireTimeoutMillis;
    const startTime = Date.now();

    try {
      const client = await Promise.race([
        this.pool.connect(),
        new Promise((_, reject) =>
          setTimeout(() => reject(new Error('Connection timeout')), timeout)
        )
      ]);

      const acquisitionTime = Date.now() - startTime;
      this._logDebug('Connection acquired', { acquisitionTime });

      // Wrap client with enhanced functionality
      return this._wrapClient(client);

    } catch (error) {
      this._logError('Failed to acquire connection', error);
      throw new DatabaseError('CONNECTION_ERROR', 'Failed to acquire database connection', error);
    }
  }

  /**
   * Wrap database client with enhanced functionality
   * @param {Object} client - Raw database client
   * @returns {Object} Enhanced client
   * @private
   */
  _wrapClient(client) {
    const originalQuery = client.query.bind(client);
    const originalRelease = client.release.bind(client);

    client.query = async (text, params = []) => {
      const startTime = Date.now();
      try {
        const result = await originalQuery(text, params);
        const duration = Date.now() - startTime;

        if (this.config.monitoring.enableQueryLogging) {
          this._logQuery(text, params, duration, result.rowCount);
        }

        if (duration > this.config.monitoring.slowQueryThreshold) {
          this._logWarn('Slow query detected', { text, duration, params: params.length });
          this.emit('slowQuery', { text, duration, params });
        }

        return result;
      } catch (error) {
        const duration = Date.now() - startTime;
        this._logError('Query execution failed', error, { text, duration });
        throw new DatabaseError('QUERY_ERROR', 'Query execution failed', error);
      }
    };

    client.release = (error) => {
      if (error) {
        this._logError('Client released with error', error);
      }
      return originalRelease(error);
    };

    return client;
  }

  /**
   * Execute a query with automatic retry logic
   * @param {string} text - SQL query text
   * @param {Array} params - Query parameters
   * @param {Object} options - Query options
   * @returns {Promise<Object>} Query result
   */
  async query(text, params = [], options = {}) {
    return this.withRetry(async () => {
      const client = await this.getConnection();
      try {
        return await client.query(text, params);
      } finally {
        client.release();
      }
    }, options);
  }

  /**
   * Execute operation with automatic retry logic
   * @param {Function} operation - Operation to execute
   * @param {Object} options - Retry options
   * @returns {Promise<*>} Operation result
   */
  async withRetry(operation, options = {}) {
    const maxAttempts = options.maxAttempts || this.config.retry.attempts;
    const baseDelay = options.delay || this.config.retry.delay;
    const backoffMultiplier = options.backoffMultiplier || this.config.retry.backoffMultiplier;

    let lastError;

    for (let attempt = 1; attempt <= maxAttempts; attempt++) {
      try {
        return await operation();
      } catch (error) {
        lastError = error;

        if (attempt === maxAttempts || !this._isRetryableError(error)) {
          break;
        }

        const delay = baseDelay * Math.pow(backoffMultiplier, attempt - 1);
        this._logWarn(`Operation failed, retrying in ${delay}ms (attempt ${attempt}/${maxAttempts})`, error);

        await this._sleep(delay);
      }
    }

    throw new DatabaseError('RETRY_EXHAUSTED', 'Operation failed after all retry attempts', lastError);
  }

  /**
   * Execute operation within a transaction
   * @param {Function} callback - Transaction callback
   * @param {Object} options - Transaction options
   * @returns {Promise<*>} Transaction result
   */
  async withTransaction(callback, options = {}) {
    const client = await this.getConnection();

    try {
      await client.query('BEGIN');
      this._logDebug('Transaction started');

      const result = await callback(client);

      await client.query('COMMIT');
      this._logDebug('Transaction committed');

      return result;
    } catch (error) {
      await client.query('ROLLBACK');
      this._logError('Transaction rolled back', error);
      throw new DatabaseError('TRANSACTION_ERROR', 'Transaction failed', error);
    } finally {
      client.release();
    }
  }

  /**
   * Perform health check
   * @returns {Promise<Object>} Health check result
   */
  async healthCheck() {
    const startTime = Date.now();
    const health = {
      status: 'healthy',
      timestamp: new Date().toISOString(),
      checks: {},
      metrics: {}
    };

    try {
      // Test basic connectivity
      const connectStart = Date.now();
      const client = await this.getConnection({ timeout: 5000 });
      const connectTime = Date.now() - connectStart;

      try {
        // Test query execution
        const queryStart = Date.now();
        const result = await client.query('SELECT 1 as test, NOW() as current_time');
        const queryTime = Date.now() - queryStart;

        health.checks.connectivity = true;
        health.checks.queryExecution = true;
        health.metrics.connectionTime = connectTime;
        health.metrics.queryTime = queryTime;
        health.metrics.totalTime = Date.now() - startTime;

      } finally {
        client.release();
      }

      // Get pool metrics
      health.metrics.pool = this.getPoolMetrics();

    } catch (error) {
      health.status = 'unhealthy';
      health.checks.connectivity = false;
      health.error = {
        message: error.message,
        code: error.code || 'UNKNOWN_ERROR'
      };
      this._logError('Health check failed', error);
    }

    return health;
  }

  /**
   * Get connection pool metrics
   * @returns {Object} Pool metrics
   */
  getPoolMetrics() {
    if (!this.pool) {
      return { status: 'not_initialized' };
    }

    return {
      totalCount: this.pool.totalCount,
      idleCount: this.pool.idleCount,
      waitingCount: this.pool.waitingCount,
      maxConnections: this.config.max,
      minConnections: this.config.min
    };
  }

  /**
   * Gracefully shutdown the database manager
   * @returns {Promise<void>}
   */
  async shutdown() {
    if (!this.isInitialized) {
      this._logWarn('Database manager not initialized, nothing to shutdown');
      return;
    }

    try {
      this._logInfo('Shutting down database manager...');

      await this._cleanup();

      this.isInitialized = false;
      this._logInfo('Database manager shutdown complete');
      this.emit('shutdown');

    } catch (error) {
      this._logError('Error during shutdown', error);
      throw new DatabaseError('SHUTDOWN_ERROR', 'Failed to shutdown database manager', error);
    }
  }

  /**
   * Clean up resources
   * @returns {Promise<void>}
   * @private
   */
  async _cleanup() {
    if (this.pool) {
      await this.pool.end();
      this.pool = null;
    }
  }

  // Event Handlers
  _handlePoolError(error) {
    this._logError('Pool error occurred', error);
    this.emit('poolError', error);
  }

  _handlePoolConnect(client) {
    this._logDebug('New client connected to pool');
    this.emit('clientConnect', client);
  }

  _handlePoolAcquire(client) {
    this._logDebug('Client acquired from pool');
    this.emit('clientAcquire', client);
  }

  _handlePoolRemove(client) {
    this._logDebug('Client removed from pool');
    this.emit('clientRemove', client);
  }

  // Utility Methods
  _isRetryableError(error) {
    const retryableCodes = [
      'ECONNRESET',
      'ENOTFOUND',
      'ETIMEDOUT',
      'ECONNREFUSED',
      'connection terminated'
    ];

    return retryableCodes.some(code =>
      error.code === code || error.message.includes(code)
    );
  }

  _sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  // Logging Methods
  _logInfo(message, data = {}) {
    console.log(`[DatabaseManager] INFO: ${message}`, data);
  }

  _logWarn(message, data = {}) {
    console.warn(`[DatabaseManager] WARN: ${message}`, data);
  }

  _logError(message, error, data = {}) {
    console.error(`[DatabaseManager] ERROR: ${message}`, {
      error: error.message,
      stack: error.stack,
      ...data
    });
  }

  _logDebug(message, data = {}) {
    if (process.env.NODE_ENV === 'development' || process.env.DB_DEBUG === 'true') {
      console.debug(`[DatabaseManager] DEBUG: ${message}`, data);
    }
  }

  _logQuery(text, params, duration, rowCount) {
    this._logDebug('Query executed', {
      query: text.substring(0, 100) + (text.length > 100 ? '...' : ''),
      paramCount: params.length,
      duration,
      rowCount
    });
  }
}

/**
 * Custom Database Error class
 */
class DatabaseError extends Error {
  constructor(code, message, originalError = null) {
    super(message);
    this.name = 'DatabaseError';
    this.code = code;
    this.originalError = originalError;
    this.timestamp = new Date().toISOString();

    if (originalError && originalError.stack) {
      this.stack = originalError.stack;
    }
  }

  toJSON() {
    return {
      name: this.name,
      code: this.code,
      message: this.message,
      timestamp: this.timestamp,
      originalError: this.originalError ? {
        message: this.originalError.message,
        code: this.originalError.code
      } : null
    };
  }
}

module.exports = {
  DatabaseManager,
  DatabaseError
};