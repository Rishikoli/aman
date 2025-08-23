#!/usr/bin/env node

/**
 * Database Connection Test Script
 * This script tests the database connection using the enhanced DatabaseManager
 */

const { initializeDatabaseManager, healthCheck } = require('../database');

async function testDatabaseConnection() {
  console.log('🔍 Testing Database Connection...\n');
  
  try {
    // Initialize the database manager
    console.log('📡 Initializing database manager...');
    const dbManager = await initializeDatabaseManager();
    console.log('✅ Database manager initialized successfully\n');
    
    // Perform health check
    console.log('🏥 Performing health check...');
    const health = await healthCheck();
    
    // Display results
    console.log('📊 Health Check Results:');
    console.log('========================');
    console.log(`Status: ${health.status === 'healthy' ? '✅ HEALTHY' : '❌ UNHEALTHY'}`);
    console.log(`Timestamp: ${health.timestamp}`);
    
    if (health.checks) {
      console.log('\n🔍 Connection Checks:');
      console.log(`  Connectivity: ${health.checks.connectivity ? '✅ PASS' : '❌ FAIL'}`);
      console.log(`  Query Execution: ${health.checks.queryExecution ? '✅ PASS' : '❌ FAIL'}`);
    }
    
    if (health.metrics) {
      console.log('\n📈 Performance Metrics:');
      console.log(`  Connection Time: ${health.metrics.connectionTime}ms`);
      console.log(`  Query Time: ${health.metrics.queryTime}ms`);
      console.log(`  Total Time: ${health.metrics.totalTime}ms`);
      
      if (health.metrics.pool) {
        console.log('\n🏊 Connection Pool Status:');
        console.log(`  Total Connections: ${health.metrics.pool.totalCount}`);
        console.log(`  Idle Connections: ${health.metrics.pool.idleCount}`);
        console.log(`  Waiting Connections: ${health.metrics.pool.waitingCount}`);
        console.log(`  Max Connections: ${health.metrics.pool.maxConnections}`);
        console.log(`  Min Connections: ${health.metrics.pool.minConnections}`);
      }
    }
    
    if (health.error) {
      console.log('\n❌ Error Details:');
      console.log(`  Message: ${health.error.message}`);
      console.log(`  Code: ${health.error.code}`);
    }
    
    // Test a simple query
    console.log('\n🔍 Testing simple query...');
    const { query } = require('../database');
    const result = await query('SELECT NOW() as current_time, version() as db_version');
    
    if (result.rows && result.rows.length > 0) {
      console.log('✅ Query executed successfully');
      console.log(`  Current Time: ${result.rows[0].current_time}`);
      console.log(`  Database Version: ${result.rows[0].db_version.split(' ')[0]}`);
    }
    
    // Final status
    console.log('\n🎉 Database Connection Test Results:');
    console.log('=====================================');
    if (health.status === 'healthy') {
      console.log('✅ DATABASE IS CONNECTED AND WORKING PROPERLY');
      console.log('✅ All systems operational');
    } else {
      console.log('❌ DATABASE CONNECTION HAS ISSUES');
      console.log('❌ Please check configuration and database server');
    }
    
  } catch (error) {
    console.log('\n❌ Database Connection Test Failed:');
    console.log('===================================');
    console.error(`Error: ${error.message}`);
    
    if (error.code) {
      console.error(`Code: ${error.code}`);
    }
    
    // Common troubleshooting tips
    console.log('\n🔧 Troubleshooting Tips:');
    console.log('1. Check if PostgreSQL server is running');
    console.log('2. Verify database credentials in .env file');
    console.log('3. Ensure database exists and is accessible');
    console.log('4. Check network connectivity to database host');
    console.log('5. Verify firewall settings allow database connections');
    
    process.exit(1);
  } finally {
    // Clean shutdown
    try {
      const { shutdown } = require('../database');
      await shutdown();
      console.log('\n🔄 Database connections closed gracefully');
    } catch (shutdownError) {
      console.warn('⚠️  Warning: Error during shutdown:', shutdownError.message);
    }
  }
}

// Run the test
if (require.main === module) {
  testDatabaseConnection()
    .then(() => {
      console.log('\n✅ Database connection test completed successfully');
      process.exit(0);
    })
    .catch((error) => {
      console.error('\n❌ Database connection test failed:', error.message);
      process.exit(1);
    });
}

module.exports = { testDatabaseConnection };