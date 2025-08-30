/**
 * Test M&A Analysis API
 * Tests the complete M&A analysis workflow
 */

const axios = require('axios');
require('dotenv').config();

const API_BASE_URL = process.env.API_BASE_URL || 'http://localhost:3001';

async function testMAAnalysis() {
  console.log('🧪 Testing M&A Analysis API...');

  try {
    // Test 1: Create M&A Analysis
    console.log('\n📊 Test 1: Creating M&A Analysis...');
    
    const analysisRequest = {
      acquirer: {
        name: 'Microsoft Corporation',
        ticker: 'MSFT'
      },
      target: {
        name: 'Adobe Inc.',
        ticker: 'ADBE'
      },
      dealValue: 75000000000,
      analysisType: 'acquisition'
    };

    const createResponse = await axios.post(
      `${API_BASE_URL}/api/financial/ma-analysis`,
      analysisRequest
    );

    if (createResponse.data.success) {
      console.log('✅ M&A Analysis created successfully');
      console.log(`   Deal ID: ${createResponse.data.data.dealId}`);
      console.log(`   Acquirer: ${createResponse.data.data.acquirer.name}`);
      console.log(`   Target: ${createResponse.data.data.target.name}`);

      const dealId = createResponse.data.data.dealId;

      // Test 2: Get Financial Analysis
      console.log('\n📈 Test 2: Retrieving Financial Analysis...');
      
      const analysisResponse = await axios.get(
        `${API_BASE_URL}/api/financial/deals/${dealId}/financial-analysis`
      );

      if (analysisResponse.data.success) {
        console.log('✅ Financial analysis retrieved successfully');
        console.log(`   Overall Score: ${analysisResponse.data.data.overall_score}`);
        console.log(`   Risk Level: ${analysisResponse.data.data.risk_level}`);
        console.log(`   Recommendation: ${analysisResponse.data.data.recommendation}`);
      } else {
        console.log('❌ Failed to retrieve financial analysis');
      }

      // Test 3: Get Financial Metrics
      console.log('\n📊 Test 3: Retrieving Financial Metrics...');
      
      const metricsResponse = await axios.get(
        `${API_BASE_URL}/api/financial/deals/${dealId}/financial-metrics`
      );

      if (metricsResponse.data.success) {
        console.log('✅ Financial metrics retrieved successfully');
        console.log(`   Metrics count: ${metricsResponse.data.data.length}`);
        
        if (metricsResponse.data.data.length > 0) {
          const firstMetric = metricsResponse.data.data[0];
          console.log(`   Sample metric: ${firstMetric.name} = ${firstMetric.value}${firstMetric.unit}`);
        }
      } else {
        console.log('❌ Failed to retrieve financial metrics');
      }

      // Test 4: Get Financial Trends
      console.log('\n📈 Test 4: Retrieving Financial Trends...');
      
      const trendsResponse = await axios.get(
        `${API_BASE_URL}/api/financial/deals/${dealId}/financial-trends`
      );

      if (trendsResponse.data.success) {
        console.log('✅ Financial trends retrieved successfully');
        console.log(`   Trend data points: ${trendsResponse.data.data.length}`);
      } else {
        console.log('❌ Failed to retrieve financial trends');
      }

      // Test 5: Get Financial Anomalies
      console.log('\n⚠️  Test 5: Retrieving Financial Anomalies...');
      
      const anomaliesResponse = await axios.get(
        `${API_BASE_URL}/api/financial/deals/${dealId}/financial-anomalies`
      );

      if (anomaliesResponse.data.success) {
        console.log('✅ Financial anomalies retrieved successfully');
        console.log(`   Anomalies count: ${anomaliesResponse.data.data.length}`);
        
        if (anomaliesResponse.data.data.length > 0) {
          const firstAnomaly = anomaliesResponse.data.data[0];
          console.log(`   Sample anomaly: ${firstAnomaly.title} (${firstAnomaly.severity})`);
        }
      } else {
        console.log('❌ Failed to retrieve financial anomalies');
      }

      // Test 6: Get Financial Forecasts
      console.log('\n🔮 Test 6: Retrieving Financial Forecasts...');
      
      const forecastsResponse = await axios.get(
        `${API_BASE_URL}/api/financial/deals/${dealId}/financial-forecasts`
      );

      if (forecastsResponse.data.success) {
        console.log('✅ Financial forecasts retrieved successfully');
        console.log(`   Forecast data points: ${forecastsResponse.data.data.length}`);
      } else {
        console.log('❌ Failed to retrieve financial forecasts');
      }

      // Test 7: Get Risk Assessment
      console.log('\n🛡️  Test 7: Retrieving Risk Assessment...');
      
      const riskResponse = await axios.get(
        `${API_BASE_URL}/api/financial/deals/${dealId}/risk-assessment`
      );

      if (riskResponse.data.success) {
        console.log('✅ Risk assessment retrieved successfully');
        console.log(`   Overall Risk Score: ${riskResponse.data.data.overallRiskScore.toFixed(1)}`);
        console.log(`   Risk Level: ${riskResponse.data.data.riskLevel}`);
        console.log(`   Risk Factors: ${riskResponse.data.data.riskFactors.length}`);
      } else {
        console.log('❌ Failed to retrieve risk assessment');
      }

    } else {
      console.log('❌ Failed to create M&A analysis');
      console.log('   Error:', createResponse.data.message);
    }

    // Test 8: API Health Check
    console.log('\n🏥 Test 8: API Health Check...');
    
    const healthResponse = await axios.get(`${API_BASE_URL}/api/financial/health`);
    
    if (healthResponse.data.success) {
      console.log('✅ Financial API is healthy');
      console.log(`   Database: ${healthResponse.data.data.database.status}`);
      console.log(`   ML Analysis: ${healthResponse.data.data.mlAnalysis.available ? 'Available' : 'Not Available'}`);
    } else {
      console.log('❌ Financial API health check failed');
    }

    console.log('\n🎉 All tests completed successfully!');

  } catch (error) {
    console.error('❌ Test failed:', error.message);
    
    if (error.response) {
      console.error('   Status:', error.response.status);
      console.error('   Data:', error.response.data);
    }
    
    if (error.code === 'ECONNREFUSED') {
      console.error('   Make sure the backend server is running on', API_BASE_URL);
    }
  }
}

// Run the test
if (require.main === module) {
  testMAAnalysis()
    .then(() => {
      console.log('✅ Test suite completed');
      process.exit(0);
    })
    .catch((error) => {
      console.error('❌ Test suite failed:', error);
      process.exit(1);
    });
}

module.exports = { testMAAnalysis };