const { initializeDatabaseManager, healthCheck, shutdown } = require('../database');

/**
 * Simple database connection checker utility
 */
class ConnectionChecker {
  constructor() {
    this.isConnected = false;
    this.lastCheckTime = null;
    this.lastError = null;
  }

  /**
   * Quick connection check
   * @returns {Promise<boolean>} True if connected, false otherwise
   */
  async isConnectedQuick() {
    try {
      await initializeDatabaseManager();
      const health = await healthCheck();
      
      this.isConnected = health.status === 'healthy';
      this.lastCheckTime = new Date();
      this.lastError = health.error || null;
      
      return this.isConnected;
    } catch (error) {
      this.isConnected = false;
      this.lastCheckTime = new Date();
      this.lastError = error;
      return false;
    }
  }

  /**
   * Detailed connection check with metrics
   * @returns {Promise<Object>} Detailed connection status
   */
  async checkConnectionDetailed() {
    try {
      await initializeDatabaseManager();
      const health = await healthCheck();
      
      this.isConnected = health.status === 'healthy';
      this.lastCheckTime = new Date();
      this.lastError = health.error || null;
      
      return {
        connected: this.isConnected,
        status: health.status,
        timestamp: health.timestamp,
        checks: health.checks,
        metrics: health.metrics,
        error: health.error,
        lastCheckTime: this.lastCheckTime
      };
    } catch (error) {
      this.isConnected = false;
      this.lastCheckTime = new Date();
      this.lastError = error;
      
      return {
        connected: false,
        status: 'error',
        timestamp: new Date().toISOString(),
        error: {
          message: error.message,
          code: error.code || 'UNKNOWN_ERROR'
        },
        lastCheckTime: this.lastCheckTime
      };
    }
  }

  /**
   * Get current connection status without performing new check
   * @returns {Object} Current status
   */
  getCurrentStatus() {
    return {
      connected: this.isConnected,
      lastCheckTime: this.lastCheckTime,
      lastError: this.lastError
    };
  }

  /**
   * Wait for database to become available
   * @param {number} maxAttempts - Maximum number of attempts
   * @param {number} delayMs - Delay between attempts in milliseconds
   * @returns {Promise<boolean>} True if connection established
   */
  async waitForConnection(maxAttempts = 10, delayMs = 2000) {
    for (let attempt = 1; attempt <= maxAttempts; attempt++) {
      console.log(`Attempt ${attempt}/${maxAttempts}: Checking database connection...`);
      
      const isConnected = await this.isConnectedQuick();
      if (isConnected) {
        console.log('✅ Database connection established');
        return true;
      }
      
      if (attempt < maxAttempts) {
        console.log(`❌ Connection failed, retrying in ${delayMs}ms...`);
        await new Promise(resolve => setTimeout(resolve, delayMs));
      }
    }
    
    console.log('❌ Failed to establish database connection after all attempts');
    return false;
  }
}

// Create singleton instance
const connectionChecker = new ConnectionChecker();

module.exports = {
  ConnectionChecker,
  connectionChecker
};