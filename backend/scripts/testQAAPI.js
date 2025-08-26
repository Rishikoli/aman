#!/usr/bin/env node

/**
 * Test script for Q&A API endpoints
 * This script tests the Q&A API endpoints directly
 */

const axios = require('axios');

const BASE_URL = 'http://localhost:3001/api/v1';

async function testQAAPI() {
  console.log('🧪 Testing Q&A API Endpoints\n');

  try {
    // Test 1: Get suggestions
    console.log('📝 Test 1: GET /qa/suggestions');
    try {
      const response = await axios.get(`${BASE_URL}/qa/suggestions`);
      console.log('✅ Status:', response.status);
      console.log('✅ Suggestions count:', response.data.data.suggestions.length);
      console.log('✅ Sample suggestions:', response.data.data.suggestions.slice(0, 3));
    } catch (error) {
      console.log('❌ Error:', error.response?.data?.error || error.message);
    }
    console.log('');

    // Test 2: Ask a question
    console.log('💬 Test 2: POST /qa/ask');
    try {
      const response = await axios.post(`${BASE_URL}/qa/ask`, {
        question: 'What deals are currently active?'
      });
      console.log('✅ Status:', response.status);
      console.log('✅ Query Type:', response.data.data.queryType);
      console.log('✅ Answer:', response.data.data.answer.substring(0, 100) + '...');
      console.log('✅ Confidence:', response.data.data.confidence);
    } catch (error) {
      console.log('❌ Error:', error.response?.data?.error || error.message);
    }
    console.log('');

    // Test 3: Search
    console.log('🔍 Test 3: GET /qa/search');
    try {
      const response = await axios.get(`${BASE_URL}/qa/search?q=company`);
      console.log('✅ Status:', response.status);
      console.log('✅ Total results:', response.data.data.results.total);
      console.log('✅ Search term:', response.data.data.searchTerm);
    } catch (error) {
      console.log('❌ Error:', error.response?.data?.error || error.message);
    }
    console.log('');

    // Test 4: Get categories
    console.log('📂 Test 4: GET /qa/categories');
    try {
      const response = await axios.get(`${BASE_URL}/qa/categories`);
      console.log('✅ Status:', response.status);
      console.log('✅ Categories count:', response.data.data.categories.length);
      console.log('✅ Sample category:', response.data.data.categories[0].name);
    } catch (error) {
      console.log('❌ Error:', error.response?.data?.error || error.message);
    }
    console.log('');

    // Test 5: Get stats
    console.log('📊 Test 5: GET /qa/stats');
    try {
      const response = await axios.get(`${BASE_URL}/qa/stats`);
      console.log('✅ Status:', response.status);
      console.log('✅ Total deals:', response.data.data.overview.totalDeals);
      console.log('✅ Total companies:', response.data.data.overview.totalCompanies);
      console.log('✅ AI enabled:', response.data.data.capabilities.aiEnabled);
    } catch (error) {
      console.log('❌ Error:', error.response?.data?.error || error.message);
    }
    console.log('');

    // Test 6: Batch processing
    console.log('📦 Test 6: POST /qa/batch');
    try {
      const response = await axios.post(`${BASE_URL}/qa/batch`, {
        questions: [
          { question: 'What deals are active?' },
          { question: 'Show me company information' }
        ]
      });
      console.log('✅ Status:', response.status);
      console.log('✅ Total questions:', response.data.data.summary.total);
      console.log('✅ Successful:', response.data.data.summary.successful);
      console.log('✅ Failed:', response.data.data.summary.failed);
    } catch (error) {
      console.log('❌ Error:', error.response?.data?.error || error.message);
    }
    console.log('');

    // Test 7: Validation errors
    console.log('⚠️  Test 7: Testing validation errors');
    try {
      const response = await axios.post(`${BASE_URL}/qa/ask`, {
        question: 'Hi' // Too short
      });
      console.log('❌ Should have failed but got status:', response.status);
    } catch (error) {
      if (error.response?.status === 400) {
        console.log('✅ Validation error correctly caught:', error.response.data.error);
      } else {
        console.log('❌ Unexpected error:', error.response?.data?.error || error.message);
      }
    }
    console.log('');

    console.log('🎉 Q&A API testing completed!');

  } catch (error) {
    console.error('❌ API testing failed:', error.message);
    process.exit(1);
  }
}

// Test server connectivity
async function testServerConnection() {
  console.log('🔗 Testing server connection...');
  try {
    const response = await axios.get(`${BASE_URL}/`);
    console.log('✅ Server is running');
    console.log('✅ API version:', response.data.version);
    console.log('✅ Available endpoints:', Object.keys(response.data.endpoints).length);
    return true;
  } catch (error) {
    console.log('❌ Server not accessible:', error.message);
    console.log('💡 Make sure the backend server is running on port 3001');
    console.log('💡 Run: npm start or node server.js in the backend directory');
    return false;
  }
}

// Main execution
async function main() {
  const serverRunning = await testServerConnection();
  console.log('');
  
  if (serverRunning) {
    await testQAAPI();
  } else {
    console.log('❌ Cannot test API endpoints - server not running');
    process.exit(1);
  }
}

// Handle script execution
if (require.main === module) {
  main();
}

module.exports = { testQAAPI, testServerConnection };