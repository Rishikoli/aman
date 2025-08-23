const { DatabaseError } = require('./DatabaseManager');

/**
 * Database configuration validator with comprehensive validation rules
 */
class ConfigValidator {
  constructor() {
    this.validationRules = this._defineValidationRules();
  }

  /**
   * Define validation rules for database configuration
   * @returns {Object} Validation rules
   * @private
   */
  _defineValidationRules() {
    return {
      // Connection settings
      host: {
        required: true,
        type: 'string',
        minLength: 1,
        maxLength: 255,
        pattern: /^[a-zA-Z0-9.-]+$/,
        description: 'Database host address'
      },
      port: {
        required: true,
        type: 'number',
        min: 1,
        max: 65535,
        description: 'Database port number'
      },
      database: {
        required: true,
        type: 'string',
        minLength: 1,
        maxLength: 63,
        pattern: /^[a-zA-Z0-9_]+$/,
        description: 'Database name'
      },
      user: {
        required: true,
        type: 'string',
        minLength: 1,
        maxLength: 63,
        description: 'Database username'
      },
      password: {
        required: true,
        type: 'string',
        minLength: 1,
        maxLength: 255,
        description: 'Database password'
      },

      // Pool settings
      max: {
        required: false,
        type: 'number',
        min: 1,
        max: 100,
        default: 20,
        description: 'Maximum number of connections in pool'
      },
      min: {
        required: false,
        type: 'number',
        min: 0,
        max: 50,
        default: 5,
        description: 'Minimum number of connections in pool'
      },
      idleTimeoutMillis: {
        required: false,
        type: 'number',
        min: 1000,
        max: 300000,
        default: 30000,
        description: 'Idle connection timeout in milliseconds'
      },
      connectionTimeoutMillis: {
        required: false,
        type: 'number',
        min: 1000,
        max: 60000,
        default: 5000,
        description: 'Connection timeout in milliseconds'
      },
      acquireTimeoutMillis: {
        required: false,
        type: 'number',
        min: 1000,
        max: 300000,
        default: 60000,
        description: 'Connection acquisition timeout in milliseconds'
      },
      maxUses: {
        required: false,
        type: 'number',
        min: 1,
        max: 50000,
        default: 7500,
        description: 'Maximum uses per connection before replacement'
      },

      // SSL settings
      ssl: {
        required: false,
        type: 'object',
        default: false,
        description: 'SSL configuration object'
      },

      // Retry settings
      retry: {
        required: false,
        type: 'object',
        properties: {
          attempts: {
            type: 'number',
            min: 1,
            max: 10,
            default: 3
          },
          delay: {
            type: 'number',
            min: 100,
            max: 10000,
            default: 1000
          },
          backoffMultiplier: {
            type: 'number',
            min: 1,
            max: 5,
            default: 2
          }
        },
        description: 'Retry configuration'
      },

      // Monitoring settings
      monitoring: {
        required: false,
        type: 'object',
        properties: {
          healthCheckInterval: {
            type: 'number',
            min: 5000,
            max: 300000,
            default: 30000
          },
          slowQueryThreshold: {
            type: 'number',
            min: 100,
            max: 60000,
            default: 1000
          },
          enableQueryLogging: {
            type: 'boolean',
            default: false
          }
        },
        description: 'Monitoring configuration'
      }
    };
  }

  /**
   * Validate complete database configuration
   * @param {Object} config - Configuration object to validate
   * @returns {Object} Validation result with normalized config
   * @throws {DatabaseError} If validation fails
   */
  validate(config) {
    if (!config || typeof config !== 'object') {
      throw new DatabaseError(
        'INVALID_CONFIGURATION',
        'Configuration must be a non-null object'
      );
    }

    const result = {
      isValid: true,
      errors: [],
      warnings: [],
      normalizedConfig: {}
    };

    // Validate each field
    for (const [fieldName, rule] of Object.entries(this.validationRules)) {
      try {
        const fieldResult = this._validateField(fieldName, config[fieldName], rule);
        result.normalizedConfig[fieldName] = fieldResult.value;
        
        if (fieldResult.warnings.length > 0) {
          result.warnings.push(...fieldResult.warnings);
        }
      } catch (error) {
        result.isValid = false;
        result.errors.push({
          field: fieldName,
          message: error.message,
          value: config[fieldName]
        });
      }
    }

    // Cross-field validation
    this._validateCrossFields(result.normalizedConfig, result);

    if (!result.isValid) {
      const errorMessage = `Configuration validation failed:\n${
        result.errors.map(e => `- ${e.field}: ${e.message}`).join('\n')
      }`;
      throw new DatabaseError('INVALID_CONFIGURATION', errorMessage);
    }

    return result;
  }

  /**
   * Validate individual field
   * @param {string} fieldName - Field name
   * @param {*} value - Field value
   * @param {Object} rule - Validation rule
   * @returns {Object} Field validation result
   * @private
   */
  _validateField(fieldName, value, rule) {
    const result = {
      value: value,
      warnings: []
    };

    // Handle undefined values
    if (value === undefined || value === null) {
      if (rule.required) {
        throw new Error(`${rule.description || fieldName} is required`);
      }
      
      if (rule.default !== undefined) {
        result.value = rule.default;
        result.warnings.push(`Using default value for ${fieldName}: ${rule.default}`);
      }
      
      return result;
    }

    // Type validation
    if (rule.type && !this._validateType(value, rule.type)) {
      throw new Error(`${rule.description || fieldName} must be of type ${rule.type}`);
    }

    // Specific validations based on type
    switch (rule.type) {
      case 'string':
        this._validateString(value, rule, fieldName);
        break;
      case 'number':
        this._validateNumber(value, rule, fieldName);
        break;
      case 'object':
        if (rule.properties) {
          result.value = this._validateObject(value, rule, fieldName);
        }
        break;
    }

    return result;
  }

  /**
   * Validate type
   * @param {*} value - Value to validate
   * @param {string} expectedType - Expected type
   * @returns {boolean} Whether type is valid
   * @private
   */
  _validateType(value, expectedType) {
    switch (expectedType) {
      case 'string':
        return typeof value === 'string';
      case 'number':
        return typeof value === 'number' && !isNaN(value);
      case 'boolean':
        return typeof value === 'boolean';
      case 'object':
        return typeof value === 'object' && value !== null;
      default:
        return true;
    }
  }

  /**
   * Validate string field
   * @param {string} value - String value
   * @param {Object} rule - Validation rule
   * @param {string} fieldName - Field name
   * @private
   */
  _validateString(value, rule, fieldName) {
    if (rule.minLength && value.length < rule.minLength) {
      throw new Error(`${fieldName} must be at least ${rule.minLength} characters long`);
    }

    if (rule.maxLength && value.length > rule.maxLength) {
      throw new Error(`${fieldName} must be no more than ${rule.maxLength} characters long`);
    }

    if (rule.pattern && !rule.pattern.test(value)) {
      throw new Error(`${fieldName} format is invalid`);
    }
  }

  /**
   * Validate number field
   * @param {number} value - Number value
   * @param {Object} rule - Validation rule
   * @param {string} fieldName - Field name
   * @private
   */
  _validateNumber(value, rule, fieldName) {
    if (rule.min !== undefined && value < rule.min) {
      throw new Error(`${fieldName} must be at least ${rule.min}`);
    }

    if (rule.max !== undefined && value > rule.max) {
      throw new Error(`${fieldName} must be no more than ${rule.max}`);
    }

    if (!Number.isInteger(value) && rule.integer) {
      throw new Error(`${fieldName} must be an integer`);
    }
  }

  /**
   * Validate object field with properties
   * @param {Object} value - Object value
   * @param {Object} rule - Validation rule
   * @param {string} fieldName - Field name
   * @returns {Object} Validated object
   * @private
   */
  _validateObject(value, rule, fieldName) {
    const result = { ...value };

    for (const [propName, propRule] of Object.entries(rule.properties)) {
      try {
        const propResult = this._validateField(
          `${fieldName}.${propName}`,
          value[propName],
          propRule
        );
        result[propName] = propResult.value;
      } catch (error) {
        throw new Error(`${fieldName}.${propName}: ${error.message}`);
      }
    }

    return result;
  }

  /**
   * Validate cross-field dependencies
   * @param {Object} config - Normalized configuration
   * @param {Object} result - Validation result
   * @private
   */
  _validateCrossFields(config, result) {
    // Validate min <= max for pool settings
    if (config.min >= config.max) {
      result.errors.push({
        field: 'min/max',
        message: 'Minimum pool size must be less than maximum pool size',
        value: { min: config.min, max: config.max }
      });
      result.isValid = false;
    }

    // Validate timeout relationships
    if (config.connectionTimeoutMillis >= config.acquireTimeoutMillis) {
      result.warnings.push(
        'Connection timeout should be less than acquire timeout for optimal performance'
      );
    }

    // Validate SSL configuration in production
    if (process.env.NODE_ENV === 'production' && !config.ssl) {
      result.warnings.push(
        'SSL is not enabled in production environment - consider enabling for security'
      );
    }

    // Validate retry configuration
    if (config.retry) {
      const maxRetryTime = config.retry.delay * 
        Math.pow(config.retry.backoffMultiplier, config.retry.attempts - 1);
      
      if (maxRetryTime > config.acquireTimeoutMillis) {
        result.warnings.push(
          'Maximum retry time exceeds acquire timeout - some retries may not complete'
        );
      }
    }
  }

  /**
   * Validate environment-specific configuration
   * @param {Object} config - Configuration to validate
   * @param {string} environment - Environment name (development, staging, production)
   * @returns {Object} Environment-specific validation result
   */
  validateForEnvironment(config, environment = process.env.NODE_ENV) {
    const result = this.validate(config);

    // Environment-specific validations
    switch (environment) {
      case 'production':
        this._validateProductionConfig(result.normalizedConfig, result);
        break;
      case 'development':
        this._validateDevelopmentConfig(result.normalizedConfig, result);
        break;
      case 'test':
        this._validateTestConfig(result.normalizedConfig, result);
        break;
    }

    return result;
  }

  /**
   * Validate production-specific requirements
   * @param {Object} config - Configuration
   * @param {Object} result - Validation result
   * @private
   */
  _validateProductionConfig(config, result) {
    // SSL should be enabled in production
    if (!config.ssl) {
      result.warnings.push('SSL should be enabled in production environment');
    }

    // Pool size should be appropriate for production
    if (config.max < 10) {
      result.warnings.push('Consider increasing maximum pool size for production workload');
    }

    // Query logging should be disabled for performance
    if (config.monitoring.enableQueryLogging) {
      result.warnings.push('Query logging is enabled - may impact performance in production');
    }
  }

  /**
   * Validate development-specific settings
   * @param {Object} config - Configuration
   * @param {Object} result - Validation result
   * @private
   */
  _validateDevelopmentConfig(config, result) {
    // Smaller pool sizes are fine for development
    if (config.max > 10) {
      result.warnings.push('Large pool size may be unnecessary for development');
    }

    // Query logging can be helpful for development
    if (!config.monitoring.enableQueryLogging) {
      result.warnings.push('Consider enabling query logging for development debugging');
    }
  }

  /**
   * Validate test-specific settings
   * @param {Object} config - Configuration
   * @param {Object} result - Validation result
   * @private
   */
  _validateTestConfig(config, result) {
    // Test environment should use minimal resources
    if (config.max > 5) {
      result.warnings.push('Consider reducing pool size for test environment');
    }

    // Fast timeouts for tests
    if (config.connectionTimeoutMillis > 2000) {
      result.warnings.push('Consider shorter timeouts for test environment');
    }
  }

  /**
   * Get validation summary
   * @param {Object} validationResult - Result from validate method
   * @returns {string} Human-readable validation summary
   */
  getValidationSummary(validationResult) {
    const lines = [];
    
    lines.push(`Configuration Validation: ${validationResult.isValid ? 'PASSED' : 'FAILED'}`);
    
    if (validationResult.errors.length > 0) {
      lines.push('\nErrors:');
      validationResult.errors.forEach(error => {
        lines.push(`  - ${error.field}: ${error.message}`);
      });
    }
    
    if (validationResult.warnings.length > 0) {
      lines.push('\nWarnings:');
      validationResult.warnings.forEach(warning => {
        lines.push(`  - ${warning}`);
      });
    }
    
    return lines.join('\n');
  }
}

module.exports = {
  ConfigValidator
};