#!/usr/bin/env node

/**
 * Schema Push Script
 * This script applies the database schema to the PostgreSQL database
 */

const fs = require('fs');
const path = require('path');
const { initializeDatabaseManager, query, shutdown } = require('../database');

async function pushSchema() {
  console.log('🚀 Pushing Database Schema...\n');

  try {
    // Initialize database manager
    console.log('📡 Initializing database connection...');
    await initializeDatabaseManager();
    console.log('✅ Database connection established\n');

    // Read schema file
    const schemaPath = path.join(__dirname, '../database/schema.sql');
    if (!fs.existsSync(schemaPath)) {
      throw new Error('Schema file not found at: ' + schemaPath);
    }

    console.log('📋 Reading schema file...');
    const schemaSQL = fs.readFileSync(schemaPath, 'utf8');
    console.log(`✅ Schema file loaded (${schemaSQL.length} characters)\n`);

    // Check current database state
    console.log('🔍 Checking current database state...');
    
    try {
      const tablesResult = await query(`
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_type = 'BASE TABLE'
        ORDER BY table_name
      `);
      
      console.log(`📊 Found ${tablesResult.rows.length} existing tables:`);
      tablesResult.rows.forEach(row => {
        console.log(`  - ${row.table_name}`);
      });
      console.log();
    } catch (error) {
      console.log('⚠️  Could not check existing tables:', error.message);
    }

    // Split schema into individual statements
    console.log('🔧 Processing schema statements...');
    const statements = schemaSQL
      .split(';')
      .map(stmt => stmt.trim())
      .filter(stmt => stmt.length > 0 && !stmt.startsWith('--'));

    console.log(`📝 Found ${statements.length} SQL statements to execute\n`);

    // Execute statements one by one
    let successCount = 0;
    let skipCount = 0;
    let errorCount = 0;

    for (let i = 0; i < statements.length; i++) {
      const statement = statements[i];
      const statementNumber = i + 1;
      
      // Skip comments and empty statements
      if (!statement || statement.startsWith('--')) {
        continue;
      }

      // Get statement type for better logging
      const statementType = getStatementType(statement);
      
      try {
        console.log(`[${statementNumber}/${statements.length}] Executing ${statementType}...`);
        
        await query(statement);
        successCount++;
        console.log(`✅ Success: ${statementType}`);
        
      } catch (error) {
        // Check if it's a "already exists" error (which we can skip)
        if (isSkippableError(error.message)) {
          skipCount++;
          console.log(`⏭️  Skipped: ${statementType} (already exists)`);
        } else {
          errorCount++;
          console.log(`❌ Error: ${statementType}`);
          console.log(`   Message: ${error.message}`);
          
          // For critical errors, we might want to stop
          if (isCriticalError(error.message)) {
            throw error;
          }
        }
      }
    }

    // Final verification
    console.log('\n🔍 Verifying schema application...');
    
    const finalTablesResult = await query(`
      SELECT table_name 
      FROM information_schema.tables 
      WHERE table_schema = 'public' 
      AND table_type = 'BASE TABLE'
      ORDER BY table_name
    `);

    const expectedTables = [
      'companies',
      'deals', 
      'agent_executions',
      'findings',
      'financial_data',
      'timeline_estimates',
      'timeline_events'
    ];

    console.log(`📊 Database now has ${finalTablesResult.rows.length} tables:`);
    finalTablesResult.rows.forEach(row => {
      const isExpected = expectedTables.includes(row.table_name);
      console.log(`  ${isExpected ? '✅' : '📋'} ${row.table_name}`);
    });

    // Check for missing expected tables
    const actualTables = finalTablesResult.rows.map(row => row.table_name);
    const missingTables = expectedTables.filter(table => !actualTables.includes(table));
    
    if (missingTables.length > 0) {
      console.log(`\n⚠️  Missing expected tables: ${missingTables.join(', ')}`);
    }

    // Check indexes
    console.log('\n🔍 Checking indexes...');
    const indexesResult = await query(`
      SELECT indexname, tablename 
      FROM pg_indexes 
      WHERE schemaname = 'public' 
      AND indexname NOT LIKE '%_pkey'
      ORDER BY tablename, indexname
    `);

    console.log(`📊 Found ${indexesResult.rows.length} custom indexes:`);
    indexesResult.rows.forEach(row => {
      console.log(`  - ${row.indexname} on ${row.tablename}`);
    });

    // Check ENUM types
    console.log('\n🔍 Checking ENUM types...');
    const enumsResult = await query(`
      SELECT typname 
      FROM pg_type 
      WHERE typtype = 'e'
      ORDER BY typname
    `);

    console.log(`📊 Found ${enumsResult.rows.length} ENUM types:`);
    enumsResult.rows.forEach(row => {
      console.log(`  - ${row.typname}`);
    });

    // Summary
    console.log('\n🎉 Schema Push Complete!');
    console.log('========================');
    console.log(`✅ Successful operations: ${successCount}`);
    console.log(`⏭️  Skipped operations: ${skipCount}`);
    console.log(`❌ Failed operations: ${errorCount}`);
    console.log(`📊 Total tables: ${finalTablesResult.rows.length}`);
    console.log(`📊 Total indexes: ${indexesResult.rows.length}`);
    console.log(`📊 Total ENUM types: ${enumsResult.rows.length}`);

    if (errorCount === 0) {
      console.log('\n🎊 All schema operations completed successfully!');
    } else if (errorCount > 0 && successCount > 0) {
      console.log('\n⚠️  Schema applied with some warnings. Please review the errors above.');
    }

  } catch (error) {
    console.error('\n❌ Schema push failed:', error.message);
    console.error('\n🔧 Troubleshooting:');
    console.error('1. Check database connection');
    console.error('2. Verify user has CREATE privileges');
    console.error('3. Review schema syntax');
    console.error('4. Check for conflicting existing objects');
    throw error;
  } finally {
    // Clean shutdown
    try {
      await shutdown();
      console.log('\n🔄 Database connections closed gracefully');
    } catch (shutdownError) {
      console.warn('⚠️  Warning: Error during shutdown:', shutdownError.message);
    }
  }
}

/**
 * Get the type of SQL statement for better logging
 */
function getStatementType(statement) {
  const upperStatement = statement.toUpperCase().trim();
  
  if (upperStatement.startsWith('CREATE TABLE')) return 'CREATE TABLE';
  if (upperStatement.startsWith('CREATE INDEX')) return 'CREATE INDEX';
  if (upperStatement.startsWith('CREATE TYPE')) return 'CREATE TYPE';
  if (upperStatement.startsWith('CREATE EXTENSION')) return 'CREATE EXTENSION';
  if (upperStatement.startsWith('CREATE TRIGGER')) return 'CREATE TRIGGER';
  if (upperStatement.startsWith('CREATE OR REPLACE FUNCTION')) return 'CREATE FUNCTION';
  if (upperStatement.startsWith('ALTER TABLE')) return 'ALTER TABLE';
  if (upperStatement.startsWith('INSERT INTO')) return 'INSERT DATA';
  if (upperStatement.startsWith('UPDATE')) return 'UPDATE DATA';
  
  return 'SQL STATEMENT';
}

/**
 * Check if an error can be safely skipped (e.g., "already exists")
 */
function isSkippableError(errorMessage) {
  const skippablePatterns = [
    'already exists',
    'relation .* already exists',
    'type .* already exists',
    'extension .* already exists',
    'function .* already exists',
    'trigger .* already exists',
    'index .* already exists'
  ];
  
  return skippablePatterns.some(pattern => 
    new RegExp(pattern, 'i').test(errorMessage)
  );
}

/**
 * Check if an error is critical and should stop execution
 */
function isCriticalError(errorMessage) {
  const criticalPatterns = [
    'permission denied',
    'database .* does not exist',
    'role .* does not exist',
    'syntax error',
    'column .* does not exist',
    'relation .* does not exist'
  ];
  
  return criticalPatterns.some(pattern => 
    new RegExp(pattern, 'i').test(errorMessage)
  );
}

// Run the schema push
if (require.main === module) {
  pushSchema()
    .then(() => {
      console.log('\n✅ Schema push completed successfully');
      process.exit(0);
    })
    .catch((error) => {
      console.error('\n❌ Schema push failed:', error.message);
      process.exit(1);
    });
}

module.exports = { pushSchema };