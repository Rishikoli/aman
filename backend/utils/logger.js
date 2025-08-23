const fs = require('fs');
const path = require('path');
const { getConfig } = require('./env-config');

/**
 * Enhanced logging infrastructure for database operations
 */
class Logger {
  constructor(options = {}) {
    this.config = this._loadConfig(options);
    this.logLevels = {
      error: 0,
      warn: 1,
      info: 2,
      debug: 3
    };
    
    this._ensureLogDirectory();
  }

  /**
   * Load logging configuration
   * @param {Object} options - Override options
   * @returns {Object} Logging configuration
   * @private
   */
  _loadConfig(options) {
    const envConfig = getConfig();
    
    return {
      level: options.level || envConfig.logging.level || 'info',
      file: options.file || envConfig.logging.file || './logs/app.log',
      enableConsole: options.enableConsole !== false,
      enableFile: options.enableFile !== false,
      maxFileSize: options.maxFileSize || 10 * 1024 * 1024, // 10MB
      maxFiles: options.maxFiles || 5,
      dateFormat: options.dateFormat || 'YYYY-MM-DD HH:mm:ss',
      includeStack: options.includeStack !== false,
      maskSensitive: options.maskSensitive !== false
    };
  }

  /**
   * Ensure log directory exists
   * @private
   */
  _ensureLogDirectory() {
    if (this.config.enableFile) {
      const logDir = path.dirname(this.config.file);
      if (!fs.existsSync(logDir)) {
        fs.mkdirSync(logDir, { recursive: true });
      }
    }
  }

  /**
   * Check if log level should be logged
   * @param {string} level - Log level to check
   * @returns {boolean} Whether to log
   * @private
   */
  _shouldLog(level) {
    return this.logLevels[level] <= this.logLevels[this.config.level];
  }

  /**
   * Format log message
   * @param {string} level - Log level
   * @param {string} message - Log message
   * @param {Object} data - Additional data
   * @param {Error} error - Error object if applicable
   * @returns {string} Formatted log message
   * @private
   */
  _formatMessage(level, message, data = {}, error = null) {
    const timestamp = new Date().toISOString();
    const logEntry = {
      timestamp,
      level: level.toUpperCase(),
      message,
      ...data
    };

    if (error) {
      logEntry.error = {
        message: error.message,
        code: error.code,
        ...(this.config.includeStack && { stack: error.stack })
      };
    }

    // Mask sensitive information
    if (this.config.maskSensitive) {
      this._maskSensitiveData(logEntry);
    }

    return JSON.stringify(logEntry);
  }

  /**
   * Mask sensitive data in log entry
   * @param {Object} logEntry - Log entry to mask
   * @private
   */
  _maskSensitiveData(logEntry) {
    const sensitiveFields = ['password', 'token', 'secret', 'key', 'auth'];
    
    const maskValue = (obj) => {
      if (typeof obj !== 'object' || obj === null) return;
      
      for (const [key, value] of Object.entries(obj)) {
        if (sensitiveFields.some(field => key.toLowerCase().includes(field))) {
          obj[key] = '***MASKED***';
        } else if (typeof value === 'object') {
          maskValue(value);
        }
      }
    };

    maskValue(logEntry);
  }

  /**
   * Write log to file
   * @param {string} formattedMessage - Formatted log message
   * @private
   */
  _writeToFile(formattedMessage) {
    if (!this.config.enableFile) return;

    try {
      // Check file size and rotate if necessary
      this._rotateLogIfNeeded();
      
      fs.appendFileSync(this.config.file, formattedMessage + '\n');
    } catch (error) {
      console.error('Failed to write to log file:', error.message);
    }
  }

  /**
   * Rotate log file if it exceeds maximum size
   * @private
   */
  _rotateLogIfNeeded() {
    try {
      if (!fs.existsSync(this.config.file)) return;
      
      const stats = fs.statSync(this.config.file);
      if (stats.size < this.config.maxFileSize) return;

      // Rotate existing files
      for (let i = this.config.maxFiles - 1; i > 0; i--) {
        const oldFile = `${this.config.file}.${i}`;
        const newFile = `${this.config.file}.${i + 1}`;
        
        if (fs.existsSync(oldFile)) {
          if (i === this.config.maxFiles - 1) {
            fs.unlinkSync(oldFile); // Delete oldest file
          } else {
            fs.renameSync(oldFile, newFile);
          }
        }
      }

      // Move current file to .1
      fs.renameSync(this.config.file, `${this.config.file}.1`);
    } catch (error) {
      console.error('Failed to rotate log file:', error.message);
    }
  }

  /**
   * Log error message
   * @param {string} message - Error message
   * @param {Error} error - Error object
   * @param {Object} data - Additional data
   */
  error(message, error = null, data = {}) {
    if (!this._shouldLog('error')) return;

    const formattedMessage = this._formatMessage('error', message, data, error);
    
    if (this.config.enableConsole) {
      console.error(formattedMessage);
    }
    
    this._writeToFile(formattedMessage);
  }

  /**
   * Log warning message
   * @param {string} message - Warning message
   * @param {Object} data - Additional data
   */
  warn(message, data = {}) {
    if (!this._shouldLog('warn')) return;

    const formattedMessage = this._formatMessage('warn', message, data);
    
    if (this.config.enableConsole) {
      console.warn(formattedMessage);
    }
    
    this._writeToFile(formattedMessage);
  }

  /**
   * Log info message
   * @param {string} message - Info message
   * @param {Object} data - Additional data
   */
  info(message, data = {}) {
    if (!this._shouldLog('info')) return;

    const formattedMessage = this._formatMessage('info', message, data);
    
    if (this.config.enableConsole) {
      console.log(formattedMessage);
    }
    
    this._writeToFile(formattedMessage);
  }

  /**
   * Log debug message
   * @param {string} message - Debug message
   * @param {Object} data - Additional data
   */
  debug(message, data = {}) {
    if (!this._shouldLog('debug')) return;

    const formattedMessage = this._formatMessage('debug', message, data);
    
    if (this.config.enableConsole) {
      console.debug(formattedMessage);
    }
    
    this._writeToFile(formattedMessage);
  }

  /**
   * Log database query
   * @param {string} query - SQL query
   * @param {Array} params - Query parameters
   * @param {number} duration - Query duration in milliseconds
   * @param {number} rowCount - Number of rows affected/returned
   */
  query(query, params = [], duration, rowCount) {
    if (!this._shouldLog('debug')) return;

    const data = {
      query: query.substring(0, 200) + (query.length > 200 ? '...' : ''),
      paramCount: params.length,
      duration,
      rowCount,
      category: 'database_query'
    };

    this.debug('Database query executed', data);
  }

  /**
   * Log database connection event
   * @param {string} event - Connection event type
   * @param {Object} data - Event data
   */
  connection(event, data = {}) {
    const logData = {
      event,
      category: 'database_connection',
      ...data
    };

    switch (event) {
      case 'connected':
      case 'pool_created':
        this.info(`Database ${event}`, logData);
        break;
      case 'connection_error':
      case 'pool_error':
        this.error(`Database ${event}`, null, logData);
        break;
      case 'slow_query':
        this.warn(`Database ${event}`, logData);
        break;
      default:
        this.debug(`Database ${event}`, logData);
    }
  }

  /**
   * Create a child logger with additional context
   * @param {Object} context - Additional context to include in all logs
   * @returns {Logger} Child logger instance
   */
  child(context = {}) {
    const childLogger = new Logger(this.config);
    const originalFormatMessage = childLogger._formatMessage.bind(childLogger);
    
    childLogger._formatMessage = (level, message, data = {}, error = null) => {
      return originalFormatMessage(level, message, { ...context, ...data }, error);
    };
    
    return childLogger;
  }
}

// Create default logger instance
const defaultLogger = new Logger();

module.exports = {
  Logger,
  logger: defaultLogger
};