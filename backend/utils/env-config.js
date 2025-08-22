const dotenv = require('dotenv');
const path = require('path');

// Load environment variables
dotenv.config({ path: path.join(__dirname, '../.env') });

// Environment validation schema
const requiredEnvVars = [
  'DATABASE_URL',
  'DATABASE_HOST',
  'DATABASE_PORT',
  'DATABASE_NAME',
  'DATABASE_USER',
  'DATABASE_PASSWORD',
  'REDIS_URL',
  'PORT',
  'NODE_ENV',
  'JWT_SECRET'
];

const optionalEnvVars = [
  'FMP_API_KEY',
  'OPENAI_API_KEY',
  'NEWS_API_KEY',
  'TWITTER_BEARER_TOKEN',
  'UPLOAD_DIR',
  'MAX_FILE_SIZE',
  'RATE_LIMIT_WINDOW_MS',
  'RATE_LIMIT_MAX_REQUESTS',
  'LOG_LEVEL',
  'LOG_FILE',
  'SUPERSET_URL',
  'SUPERSET_USERNAME',
  'SUPERSET_PASSWORD'
];

/**
 * Validates that all required environment variables are present
 * @returns {Object} Validation result with success status and missing variables
 */
function validateEnvironment() {
  const missing = [];
  const warnings = [];

  // Check required variables
  requiredEnvVars.forEach(varName => {
    if (!process.env[varName]) {
      missing.push(varName);
    }
  });

  // Check optional variables and warn if missing
  optionalEnvVars.forEach(varName => {
    if (!process.env[varName]) {
      warnings.push(varName);
    }
  });

  return {
    success: missing.length === 0,
    missing,
    warnings
  };
}

/**
 * Validates environment variables and exits if required ones are missing
 */
function validateEnv() {
  const validation = validateEnvironment();
  
  if (!validation.success) {
    console.error('Missing required environment variables:', validation.missing);
    console.error('Please check your .env file and ensure all required variables are set.');
    process.exit(1);
  }

  if (validation.warnings.length > 0) {
    console.warn('Optional environment variables not set:', validation.warnings);
    console.warn('Some features may not work without these variables.');
  }

  console.log('Environment validation passed');
}

/**
 * Gets environment configuration with defaults
 * @returns {Object} Environment configuration object
 */
function getConfig() {
  const validation = validateEnvironment();
  
  if (!validation.success) {
    console.error('Missing required environment variables:', validation.missing);
    process.exit(1);
  }

  if (validation.warnings.length > 0) {
    console.warn('Optional environment variables not set:', validation.warnings);
  }

  return {
    // Database
    database: {
      url: process.env.DATABASE_URL,
      host: process.env.DATABASE_HOST,
      port: parseInt(process.env.DATABASE_PORT, 10),
      name: process.env.DATABASE_NAME,
      user: process.env.DATABASE_USER,
      password: process.env.DATABASE_PASSWORD
    },
    
    // Redis
    redis: {
      url: process.env.REDIS_URL,
      host: process.env.REDIS_HOST || 'localhost',
      port: parseInt(process.env.REDIS_PORT, 10) || 6379
    },
    
    // Server
    server: {
      port: parseInt(process.env.PORT, 10),
      nodeEnv: process.env.NODE_ENV,
      jwtSecret: process.env.JWT_SECRET,
      apiBaseUrl: process.env.API_BASE_URL || `http://localhost:${process.env.PORT}`
    },
    
    // API Keys
    apiKeys: {
      fmp: process.env.FMP_API_KEY,
      openai: process.env.OPENAI_API_KEY,
      news: process.env.NEWS_API_KEY,
      twitter: process.env.TWITTER_BEARER_TOKEN
    },
    
    // File Storage
    storage: {
      uploadDir: process.env.UPLOAD_DIR || './uploads',
      maxFileSize: process.env.MAX_FILE_SIZE || '50MB'
    },
    
    // Rate Limiting
    rateLimit: {
      windowMs: parseInt(process.env.RATE_LIMIT_WINDOW_MS, 10) || 900000,
      maxRequests: parseInt(process.env.RATE_LIMIT_MAX_REQUESTS, 10) || 100
    },
    
    // Logging
    logging: {
      level: process.env.LOG_LEVEL || 'info',
      file: process.env.LOG_FILE || './logs/app.log'
    },
    
    // External Services
    external: {
      superset: {
        url: process.env.SUPERSET_URL,
        username: process.env.SUPERSET_USERNAME,
        password: process.env.SUPERSET_PASSWORD
      }
    }
  };
}

module.exports = {
  validateEnvironment,
  validateEnv,
  getConfig
};