/**
 * Test Script for Intelligent Financial Intelligence System
 * Tests smart company lookup, peer identification, and ML-based risk scoring
 */

const IntelligentFinancialService = require('../services/intelligentFinancialService');

async function testIntelligentFinancialSystem() {
  console.log('='.repeat(80));
  console.log('TESTING INTELLIGENT FINANCIAL INTELLIGENCE SYSTEM');
  console.log('='.repeat(80));

  const service = new IntelligentFinancialService();
  const testResults = {
    timestamp: new Date().toISOString(),
    tests: {},
    summary: {}
  };

  // Test 1: Service Capability Test
  console.log('\n1. TESTING SERVICE CAPABILITIES');
  console.log('-'.repeat(50));
  
  try {
    const capabilityTest = await service.testIntelligentFinancialService();
    testResults.tests.capabilities = capabilityTest;
    
    console.log(`✅ Service Status: ${capabilityTest.overallStatus}`);
    console.log(`📊 Working Capabilities: ${capabilityTest.workingCapabilities}`);
    
    for (const [capability, result] of Object.entries(capabilityTest.capabilities)) {
      const status = result.status === 'working' ? '✅' : '❌';
      console.log(`   ${status} ${capability}: ${result.status}`);
      if (result.error) {
        console.log(`      Error: ${result.error}`);
      }
    }
  } catch (error) {
    console.error('❌ Service capability test failed:', error.message);
    testResults.tests.capabilities = { error: error.message };
  }

  // Test 2: Smart Company Lookup
  console.log('\n2. TESTING SMART COMPANY LOOKUP');
  console.log('-'.repeat(50));
  
  const lookupTests = [
    { identifier: 'AAPL', description: 'Exact ticker match' },
    { identifier: 'Apple', description: 'Company name search' },
    { identifier: 'MSFT', description: 'Another exact ticker' },
    { identifier: 'InvalidCompany123', description: 'Invalid company test' }
  ];

  for (const test of lookupTests) {
    try {
      console.log(`\nTesting: ${test.description} (${test.identifier})`);
      
      const lookupResult = await service.smartCompanyLookup(test.identifier, {
        includeFinancials: false,
        includeRiskScore: false,
        maxResults: 3
      });

      testResults.tests[`lookup_${test.identifier}`] = {
        success: true,
        resultsFound: lookupResult.totalResults,
        confidence: lookupResult.confidence,
        dataSources: lookupResult.dataSources
      };

      console.log(`   ✅ Results found: ${lookupResult.totalResults}`);
      console.log(`   📈 Confidence: ${(lookupResult.confidence * 100).toFixed(1)}%`);
      console.log(`   🔍 Data sources: ${lookupResult.dataSources.join(', ')}`);
      
      if (lookupResult.results.length > 0) {
        const topResult = lookupResult.results[0];
        console.log(`   🏢 Top result: ${topResult.name} (${topResult.symbol})`);
        if (topResult.industry) {
          console.log(`   🏭 Industry: ${topResult.industry}`);
        }
      }

      if (lookupResult.errors && lookupResult.errors.length > 0) {
        console.log(`   ⚠️  Errors: ${lookupResult.errors.length} data source(s) failed`);
      }

    } catch (error) {
      console.error(`   ❌ Lookup failed: ${error.message}`);
      testResults.tests[`lookup_${test.identifier}`] = {
        success: false,
        error: error.message
      };
    }
  }

  // Test 3: Peer Company Identification
  console.log('\n3. TESTING PEER COMPANY IDENTIFICATION');
  console.log('-'.repeat(50));
  
  const peerTests = ['AAPL', 'MSFT'];

  for (const symbol of peerTests) {
    try {
      console.log(`\nIdentifying peers for: ${symbol}`);
      
      const peerResult = await service.identifyPeerCompanies(symbol, {
        maxPeers: 5,
        includeFinancials: false,
        similarityThreshold: 0.6
      });

      testResults.tests[`peers_${symbol}`] = {
        success: true,
        peersFound: peerResult.peersFound,
        totalAnalyzed: peerResult.totalPeersAnalyzed
      };

      console.log(`   ✅ Peers found: ${peerResult.peersFound}`);
      console.log(`   🔍 Companies analyzed: ${peerResult.totalPeersAnalyzed}`);
      console.log(`   🏢 Target: ${peerResult.targetCompany.name} (${peerResult.targetCompany.industry})`);
      
      if (peerResult.peers.length > 0) {
        console.log('   📊 Top peers:');
        peerResult.peers.slice(0, 3).forEach((peer, index) => {
          console.log(`      ${index + 1}. ${peer.name} (${peer.symbol}) - ${(peer.similarityScore * 100).toFixed(1)}% similar`);
        });
      }

      if (peerResult.insights && peerResult.insights.length > 0) {
        console.log('   💡 Insights:');
        peerResult.insights.forEach(insight => {
          console.log(`      • ${insight}`);
        });
      }

    } catch (error) {
      console.error(`   ❌ Peer identification failed: ${error.message}`);
      testResults.tests[`peers_${symbol}`] = {
        success: false,
        error: error.message
      };
    }
  }

  // Test 4: Comprehensive Risk Scoring
  console.log('\n4. TESTING COMPREHENSIVE RISK SCORING');
  console.log('-'.repeat(50));
  
  const riskTests = ['AAPL', 'MSFT'];

  for (const symbol of riskTests) {
    try {
      console.log(`\nCalculating risk score for: ${symbol}`);
      
      const riskResult = await service.buildComprehensiveRiskScore(symbol, {
        includePeerComparison: false, // Skip peer comparison for faster testing
        includeHistoricalTrends: true,
        riskHorizon: '1year'
      });

      testResults.tests[`risk_${symbol}`] = {
        success: true,
        riskLevel: riskResult.riskLevel,
        riskScore: riskResult.overallRiskScore,
        confidence: riskResult.confidence?.level
      };

      console.log(`   ✅ Risk Level: ${riskResult.riskLevel}`);
      console.log(`   📊 Risk Score: ${riskResult.overallRiskScore}/100`);
      console.log(`   🎯 Confidence: ${riskResult.confidence?.level || 'Unknown'}`);
      
      console.log('   📈 Risk Components:');
      for (const [component, data] of Object.entries(riskResult.riskComponents)) {
        console.log(`      • ${component}: ${data.level} (${data.score}/100)`);
      }

      if (riskResult.insights && riskResult.insights.length > 0) {
        console.log('   💡 Key Insights:');
        riskResult.insights.slice(0, 3).forEach(insight => {
          console.log(`      • ${insight}`);
        });
      }

      if (riskResult.recommendations && riskResult.recommendations.length > 0) {
        console.log('   🎯 Recommendations:');
        riskResult.recommendations.slice(0, 2).forEach(rec => {
          console.log(`      • ${rec}`);
        });
      }

    } catch (error) {
      console.error(`   ❌ Risk scoring failed: ${error.message}`);
      testResults.tests[`risk_${symbol}`] = {
        success: false,
        error: error.message
      };
    }
  }

  // Test 5: Combined Intelligence Analysis
  console.log('\n5. TESTING COMBINED INTELLIGENCE ANALYSIS');
  console.log('-'.repeat(50));
  
  try {
    console.log('\nRunning combined analysis for: AAPL');
    
    // This would typically be done through the API endpoint
    const lookupResult = await service.smartCompanyLookup('AAPL', {
      includeFinancials: false,
      includeRiskScore: false,
      maxResults: 1
    });

    if (lookupResult.totalResults > 0) {
      const company = lookupResult.results[0];
      
      const [peerResult, riskResult] = await Promise.allSettled([
        service.identifyPeerCompanies(company.symbol, { maxPeers: 3, includeFinancials: false }),
        service.buildComprehensiveRiskScore(company.symbol, { includePeerComparison: false })
      ]);

      testResults.tests.combinedAnalysis = {
        success: true,
        companyFound: true,
        peersAnalyzed: peerResult.status === 'fulfilled',
        riskScored: riskResult.status === 'fulfilled'
      };

      console.log(`   ✅ Company: ${company.name} (${company.symbol})`);
      console.log(`   📊 Peer Analysis: ${peerResult.status === 'fulfilled' ? 'Success' : 'Failed'}`);
      console.log(`   🎯 Risk Scoring: ${riskResult.status === 'fulfilled' ? 'Success' : 'Failed'}`);
      
      if (peerResult.status === 'fulfilled') {
        console.log(`   👥 Peers Found: ${peerResult.value.peersFound}`);
      }
      
      if (riskResult.status === 'fulfilled') {
        console.log(`   ⚠️  Risk Level: ${riskResult.value.riskLevel} (${riskResult.value.overallRiskScore}/100)`);
      }

    } else {
      testResults.tests.combinedAnalysis = {
        success: false,
        error: 'No company found for combined analysis'
      };
      console.log('   ❌ No company found for combined analysis');
    }

  } catch (error) {
    console.error(`   ❌ Combined analysis failed: ${error.message}`);
    testResults.tests.combinedAnalysis = {
      success: false,
      error: error.message
    };
  }

  // Generate Test Summary
  console.log('\n' + '='.repeat(80));
  console.log('TEST SUMMARY');
  console.log('='.repeat(80));

  const totalTests = Object.keys(testResults.tests).length;
  const successfulTests = Object.values(testResults.tests).filter(test => test.success !== false).length;
  const failedTests = totalTests - successfulTests;

  testResults.summary = {
    totalTests,
    successfulTests,
    failedTests,
    successRate: ((successfulTests / totalTests) * 100).toFixed(1)
  };

  console.log(`📊 Total Tests: ${totalTests}`);
  console.log(`✅ Successful: ${successfulTests}`);
  console.log(`❌ Failed: ${failedTests}`);
  console.log(`📈 Success Rate: ${testResults.summary.successRate}%`);

  if (failedTests > 0) {
    console.log('\n❌ FAILED TESTS:');
    for (const [testName, result] of Object.entries(testResults.tests)) {
      if (result.success === false) {
        console.log(`   • ${testName}: ${result.error}`);
      }
    }
  }

  console.log('\n🎯 INTELLIGENT FINANCIAL INTELLIGENCE SYSTEM TEST COMPLETED');
  console.log('='.repeat(80));

  return testResults;
}

// Run the test if this script is executed directly
if (require.main === module) {
  testIntelligentFinancialSystem()
    .then(results => {
      console.log('\n📋 Test results saved to memory');
      process.exit(results.summary.failedTests > 0 ? 1 : 0);
    })
    .catch(error => {
      console.error('\n💥 Test execution failed:', error);
      process.exit(1);
    });
}

module.exports = { testIntelligentFinancialSystem };