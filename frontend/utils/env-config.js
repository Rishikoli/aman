/**
 * Frontend environment configuration and validation
 * Only NEXT_PUBLIC_ prefixed variables are available in the browser
 */

// Required environment variables for frontend
const requiredEnvVars = [
  'NEXT_PUBLIC_API_BASE_URL',
  'NEXT_PUBLIC_APP_NAME'
];

// Optional environment variables
const optionalEnvVars = [
  'NEXT_PUBLIC_APP_VERSION',
  'NEXT_PUBLIC_SUPERSET_URL',
  'NEXT_PUBLIC_ENABLE_DEBUG',
  'NEXT_PUBLIC_LOG_LEVEL',
  'NEXT_PUBLIC_CHART_THEME',
  'NEXT_PUBLIC_DEFAULT_CURRENCY',
  'NEXT_PUBLIC_MAX_FILE_SIZE',
  'NEXT_PUBLIC_ALLOWED_FILE_TYPES',
  'NEXT_PUBLIC_ENABLE_ANALYTICS',
  'NEXT_PUBLIC_ENABLE_NOTIFICATIONS'
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
 * Gets frontend environment configuration with defaults
 * @returns {Object} Environment configuration object
 */
function getConfig() {
  const validation = validateEnvironment();
  
  if (!validation.success) {
    console.error('Missing required environment variables:', validation.missing);
    throw new Error(`Missing required environment variables: ${validation.missing.join(', ')}`);
  }

  if (validation.warnings.length > 0 && process.env.NEXT_PUBLIC_ENABLE_DEBUG === 'true') {
    console.warn('Optional environment variables not set:', validation.warnings);
  }

  return {
    // App Configuration
    app: {
      name: process.env.NEXT_PUBLIC_APP_NAME,
      version: process.env.NEXT_PUBLIC_APP_VERSION || '1.0.0',
      apiBaseUrl: process.env.NEXT_PUBLIC_API_BASE_URL
    },
    
    // External Services
    external: {
      supersetUrl: process.env.NEXT_PUBLIC_SUPERSET_URL
    },
    
    // Development Settings
    development: {
      enableDebug: process.env.NEXT_PUBLIC_ENABLE_DEBUG === 'true',
      logLevel: process.env.NEXT_PUBLIC_LOG_LEVEL || 'info'
    },
    
    // UI Configuration
    ui: {
      chartTheme: process.env.NEXT_PUBLIC_CHART_THEME || 'light',
      defaultCurrency: process.env.NEXT_PUBLIC_DEFAULT_CURRENCY || 'USD'
    },
    
    // File Upload Settings
    upload: {
      maxFileSize: process.env.NEXT_PUBLIC_MAX_FILE_SIZE || '50MB',
      allowedFileTypes: process.env.NEXT_PUBLIC_ALLOWED_FILE_TYPES?.split(',') || ['.pdf', '.docx', '.xlsx', '.csv']
    },
    
    // Feature Flags
    features: {
      enableAnalytics: process.env.NEXT_PUBLIC_ENABLE_ANALYTICS === 'true',
      enableNotifications: process.env.NEXT_PUBLIC_ENABLE_NOTIFICATIONS === 'true'
    }
  };
}

/**
 * Hook for React components to access environment config
 * @returns {Object} Environment configuration
 */
export function useEnvConfig() {
  return getConfig();
}

export {
  validateEnvironment,
  getConfig
};