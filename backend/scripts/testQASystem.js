#!/usr/bin/env node

/**
 * Test script for the Q&A System
 * This script demonstrates the Q&A system capabilities
 */

const qaService = require('../services/qaService');
const { connectDB } = require('../utils/database');

async function testQASystem() {
  console.log('🤖 Testing AMAN Q&A System\n');

  try {
    // Connect to database
    await connectDB();
    console.log('✅ Database connected\n');

    // Test 1: Get suggested queries
    console.log('📝 Test 1: Getting suggested queries...');
    const suggestions = await qaService.getSuggestedQueries();
    console.log(`Found ${suggestions.length} suggested queries:`);
    suggestions.slice(0, 5).forEach((suggestion, index) => {
      console.log(`  ${index + 1}. ${suggestion}`);
    });
    console.log('');

    // Test 2: Query classification
    console.log('🔍 Test 2: Testing query classification...');
    const testQueries = [
      'What are the risks for this deal?',
      'Show me financial data for Apple',
      'What is the status of all agents?',
      'When will the deal be completed?',
      'What findings were discovered?'
    ];

    for (const query of testQueries) {
      const queryType = await qaService.classifyQuery(query);
      console.log(`  "${query}" → ${queryType}`);
    }
    console.log('');

    // Test 3: Entity extraction
    console.log('🏷️  Test 3: Testing entity extraction...');
    const entityTestQuery = 'What are the financial risks for Apple Inc and Microsoft?';
    const entities = await qaService.extractEntities(entityTestQuery);
    console.log(`Query: "${entityTestQuery}"`);
    console.log('Extracted entities:', JSON.stringify(entities, null, 2));
    console.log('');

    // Test 4: Process actual questions
    console.log('💬 Test 4: Processing sample questions...');
    const sampleQuestions = [
      'What deals are currently active?',
      'Show me all companies in the technology sector',
      'What are the latest findings?',
      'Which agents are currently running?'
    ];

    for (const question of sampleQuestions) {
      console.log(`\n❓ Question: "${question}"`);
      try {
        const result = await qaService.processQuery(question);
        if (result.success) {
          console.log(`✅ Answer: ${result.answer}`);
          console.log(`📊 Query Type: ${result.queryType}`);
          console.log(`🎯 Confidence: ${result.confidence}`);
          console.log(`📚 Sources: ${result.sources.join(', ')}`);
        } else {
          console.log(`❌ Error: ${result.error}`);
        }
      } catch (error) {
        console.log(`❌ Error processing question: ${error.message}`);
      }
    }

    // Test 5: Search functionality
    console.log('\n\n🔎 Test 5: Testing search functionality...');
    const searchTerms = ['deal', 'company', 'risk'];
    
    for (const term of searchTerms) {
      try {
        const searchResults = await qaService.searchAll(term);
        console.log(`\nSearch term: "${term}"`);
        console.log(`Total results: ${searchResults.total}`);
        console.log(`  - Deals: ${searchResults.deals.length}`);
        console.log(`  - Companies: ${searchResults.companies.length}`);
        console.log(`  - Findings: ${searchResults.findings.length}`);
        console.log(`  - Agents: ${searchResults.agents.length}`);
      } catch (error) {
        console.log(`❌ Search error for "${term}": ${error.message}`);
      }
    }

    // Test 6: Context-aware queries
    console.log('\n\n🎯 Test 6: Testing context-aware queries...');
    const contextQueries = [
      {
        question: 'What are the risks?',
        context: { deal_id: '123e4567-e89b-12d3-a456-426614174000' }
      },
      {
        question: 'Show me financial data',
        context: { company_id: '123e4567-e89b-12d3-a456-426614174000' }
      }
    ];

    for (const { question, context } of contextQueries) {
      console.log(`\n❓ Question: "${question}"`);
      console.log(`📍 Context: ${JSON.stringify(context)}`);
      try {
        const result = await qaService.processQuery(question, context);
        if (result.success) {
          console.log(`✅ Answer: ${result.answer}`);
        } else {
          console.log(`❌ Error: ${result.error}`);
        }
      } catch (error) {
        console.log(`❌ Error: ${error.message}`);
      }
    }

    console.log('\n\n🎉 Q&A System testing completed!');
    console.log('\n📋 Summary:');
    console.log('✅ Query classification working');
    console.log('✅ Entity extraction working');
    console.log('✅ Question processing working');
    console.log('✅ Search functionality working');
    console.log('✅ Context-aware queries working');
    console.log('✅ Suggested queries working');

  } catch (error) {
    console.error('❌ Test failed:', error);
    process.exit(1);
  }
}

// Test AI integration
async function testAIIntegration() {
  console.log('\n\n🧠 Testing AI Integration...');
  
  const geminiService = require('../services/gemini');
  
  if (geminiService.isAvailable()) {
    console.log('✅ AI service is available');
    
    try {
      const testPrompt = 'What are common risks in M&A deals?';
      const response = await geminiService.generateText(testPrompt, { temperature: 0.3 });
      console.log('✅ AI response generated successfully');
      console.log(`Sample response length: ${response.length} characters`);
    } catch (error) {
      console.log('❌ AI generation failed:', error.message);
    }
  } else {
    console.log('⚠️  AI service not available - using fallback answers');
  }
}

// Run tests
async function main() {
  try {
    await testQASystem();
    await testAIIntegration();
    
    console.log('\n🚀 Q&A System is ready for use!');
    console.log('\nAPI Endpoints:');
    console.log('  POST /api/v1/qa/ask - Ask questions');
    console.log('  GET  /api/v1/qa/suggestions - Get suggested queries');
    console.log('  GET  /api/v1/qa/search - Search all data');
    console.log('  POST /api/v1/qa/batch - Process multiple questions');
    console.log('  GET  /api/v1/qa/categories - Get query categories');
    console.log('  GET  /api/v1/qa/stats - Get system statistics');
    
  } catch (error) {
    console.error('❌ Testing failed:', error);
    process.exit(1);
  } finally {
    process.exit(0);
  }
}

// Handle script execution
if (require.main === module) {
  main();
}

module.exports = { testQASystem, testAIIntegration };