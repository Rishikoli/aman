#!/usr/bin/env node

/**
 * Database Setup Script
 * This script helps create the database and user if they don't exist
 */

const { Client } = require('pg');
const fs = require('fs');
const path = require('path');

async function setupDatabase() {
  console.log('🚀 Setting up PostgreSQL Database...\n');

  // Read environment configuration
  const envPath = path.join(__dirname, '../.env');
  if (!fs.existsSync(envPath)) {
    console.error('❌ .env file not found. Please create it first.');
    process.exit(1);
  }

  // Parse .env file
  const envContent = fs.readFileSync(envPath, 'utf8');
  const envVars = {};
  envContent.split('\n').forEach(line => {
    const [key, value] = line.split('=');
    if (key && value) {
      envVars[key.trim()] = value.trim();
    }
  });

  const dbConfig = {
    host: envVars.DATABASE_HOST || 'localhost',
    port: parseInt(envVars.DATABASE_PORT) || 5432,
    database: envVars.DATABASE_NAME || 'aman_db',
    user: envVars.DATABASE_USER || 'aman_user',
    password: envVars.DATABASE_PASSWORD || 'aman_password'
  };

  console.log('📋 Database Configuration:');
  console.log(`  Host: ${dbConfig.host}`);
  console.log(`  Port: ${dbConfig.port}`);
  console.log(`  Database: ${dbConfig.database}`);
  console.log(`  User: ${dbConfig.user}`);
  console.log(`  Password: ${'*'.repeat(dbConfig.password.length)}\n`);

  try {
    // First, try to connect as postgres superuser to create database and user
    console.log('🔐 Attempting to connect as postgres superuser...');
    
    // Try different common postgres configurations
    const postgresConfigs = [
      { host: dbConfig.host, port: dbConfig.port, database: 'postgres', user: 'postgres', password: 'ritu' },
      { host: dbConfig.host, port: dbConfig.port, database: 'postgres', user: 'postgres', password: 'postgres' },
      { host: dbConfig.host, port: dbConfig.port, database: 'postgres', user: 'postgres', password: '' },
      { host: dbConfig.host, port: dbConfig.port, database: 'postgres', user: 'postgres', password: 'admin' }
    ];

    let postgresClient = null;
    let connectedConfig = null;

    for (const config of postgresConfigs) {
      try {
        console.log(`  Trying postgres user with password: ${config.password ? '*'.repeat(config.password.length) : '(empty)'}`);
        postgresClient = new Client(config);
        await postgresClient.connect();
        connectedConfig = config;
        console.log('✅ Connected as postgres superuser');
        break;
      } catch (error) {
        if (postgresClient) {
          try { await postgresClient.end(); } catch (e) {}
        }
        console.log(`  ❌ Failed: ${error.message}`);
      }
    }

    if (!postgresClient || !connectedConfig) {
      console.log('\n❌ Could not connect as postgres superuser.');
      console.log('🔧 Manual Setup Required:');
      console.log('1. Connect to PostgreSQL as superuser (postgres)');
      console.log(`2. Create database: CREATE DATABASE ${dbConfig.database};`);
      console.log(`3. Create user: CREATE USER ${dbConfig.user} WITH PASSWORD '${dbConfig.password}';`);
      console.log(`4. Grant privileges: GRANT ALL PRIVILEGES ON DATABASE ${dbConfig.database} TO ${dbConfig.user};`);
      console.log(`5. Grant schema privileges: GRANT ALL ON SCHEMA public TO ${dbConfig.user};`);
      process.exit(1);
    }

    // Check if database exists
    console.log(`\n🔍 Checking if database '${dbConfig.database}' exists...`);
    const dbCheckResult = await postgresClient.query(
      'SELECT 1 FROM pg_database WHERE datname = $1',
      [dbConfig.database]
    );

    if (dbCheckResult.rows.length === 0) {
      console.log(`📦 Creating database '${dbConfig.database}'...`);
      await postgresClient.query(`CREATE DATABASE ${dbConfig.database}`);
      console.log('✅ Database created successfully');
    } else {
      console.log('✅ Database already exists');
    }

    // Check if user exists
    console.log(`\n🔍 Checking if user '${dbConfig.user}' exists...`);
    const userCheckResult = await postgresClient.query(
      'SELECT 1 FROM pg_roles WHERE rolname = $1',
      [dbConfig.user]
    );

    if (userCheckResult.rows.length === 0) {
      console.log(`👤 Creating user '${dbConfig.user}'...`);
      await postgresClient.query(
        `CREATE USER ${dbConfig.user} WITH PASSWORD '${dbConfig.password}'`
      );
      console.log('✅ User created successfully');
    } else {
      console.log('✅ User already exists');
      
      // Update password just in case
      console.log('🔄 Updating user password...');
      await postgresClient.query(
        `ALTER USER ${dbConfig.user} WITH PASSWORD '${dbConfig.password}'`
      );
      console.log('✅ Password updated');
    }

    // Grant privileges
    console.log(`\n🔐 Granting privileges to user '${dbConfig.user}'...`);
    await postgresClient.query(
      `GRANT ALL PRIVILEGES ON DATABASE ${dbConfig.database} TO ${dbConfig.user}`
    );
    console.log('✅ Database privileges granted');

    // Close postgres connection
    await postgresClient.end();

    // Now connect to the target database to grant schema privileges
    console.log(`\n🔗 Connecting to database '${dbConfig.database}' to set up schema privileges...`);
    const targetClient = new Client({
      ...connectedConfig,
      database: dbConfig.database
    });
    
    await targetClient.connect();
    
    // Grant schema privileges
    await targetClient.query(`GRANT ALL ON SCHEMA public TO ${dbConfig.user}`);
    await targetClient.query(`GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO ${dbConfig.user}`);
    await targetClient.query(`GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO ${dbConfig.user}`);
    await targetClient.query(`ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO ${dbConfig.user}`);
    await targetClient.query(`ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO ${dbConfig.user}`);
    
    console.log('✅ Schema privileges granted');
    
    await targetClient.end();

    // Test the connection with the target user
    console.log(`\n🧪 Testing connection with user '${dbConfig.user}'...`);
    const testClient = new Client(dbConfig);
    await testClient.connect();
    
    const testResult = await testClient.query('SELECT NOW() as current_time, current_user, current_database()');
    console.log('✅ Connection test successful!');
    console.log(`  Current Time: ${testResult.rows[0].current_time}`);
    console.log(`  Connected User: ${testResult.rows[0].current_user}`);
    console.log(`  Connected Database: ${testResult.rows[0].current_database}`);
    
    await testClient.end();

    // Run schema initialization if schema.sql exists
    const schemaPath = path.join(__dirname, '../database/schema.sql');
    if (fs.existsSync(schemaPath)) {
      console.log('\n📋 Found schema.sql, initializing database schema...');
      const schemaSQL = fs.readFileSync(schemaPath, 'utf8');
      
      const schemaClient = new Client(dbConfig);
      await schemaClient.connect();
      
      try {
        await schemaClient.query(schemaSQL);
        console.log('✅ Database schema initialized successfully');
      } catch (error) {
        console.log(`⚠️  Schema initialization warning: ${error.message}`);
      }
      
      await schemaClient.end();
    }

    console.log('\n🎉 Database Setup Complete!');
    console.log('=====================================');
    console.log('✅ Database created and configured');
    console.log('✅ User created with proper privileges');
    console.log('✅ Connection tested successfully');
    console.log('\nYou can now run your application!');

  } catch (error) {
    console.error('\n❌ Database setup failed:', error.message);
    console.error('\n🔧 Troubleshooting:');
    console.error('1. Make sure PostgreSQL is running');
    console.error('2. Check if you can connect manually with psql');
    console.error('3. Verify postgres superuser credentials');
    console.error('4. Check firewall and network settings');
    process.exit(1);
  }
}

// Run the setup
if (require.main === module) {
  setupDatabase()
    .then(() => {
      console.log('\n✅ Database setup completed successfully');
      process.exit(0);
    })
    .catch((error) => {
      console.error('\n❌ Database setup failed:', error.message);
      process.exit(1);
    });
}

module.exports = { setupDatabase };