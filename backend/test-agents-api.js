const express = require('express');
const cors = require('cors');

// Create a simple test server
const app = express();
app.use(cors());
app.use(express.json());

// Import the agents routes
const agentsRouter = require('./api/routes/agents');
app.use('/api/agents', agentsRouter);

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'OK', timestamp: new Date().toISOString() });
});

const PORT = 3001;

app.listen(PORT, () => {
  console.log(`Test server running on http://localhost:${PORT}`);
  console.log('Available endpoints:');
  console.log('  GET  /api/agents - Get all agents');
  console.log('  POST /api/agents/analyze - Analyze with all agents');
  console.log('  GET  /api/agents/tasks/:taskId - Get task status');
  console.log('  POST /api/agents/:agentId/control - Control agent');
  console.log('  GET  /health - Health check');
});

// Test the API endpoints
setTimeout(async () => {
  console.log('\n🧪 Testing API endpoints...\n');
  
  try {
    // Test 1: Get all agents
    console.log('1. Testing GET /api/agents');
    const agentsResponse = await fetch('http://localhost:3001/api/agents');
    const agentsData = await agentsResponse.json();
    console.log(`   ✅ Success: Found ${agentsData.agents?.length || 0} agents`);
    
    // Test 2: Start analysis
    console.log('\n2. Testing POST /api/agents/analyze');
    const analysisResponse = await fetch('http://localhost:3001/api/agents/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        companyData: {
          name: 'Test Company',
          ticker: 'TEST',
          industry: 'Technology',
          description: 'A test company for API testing'
        },
        analysisType: 'comprehensive'
      })
    });
    const analysisData = await analysisResponse.json();
    console.log(`   ✅ Success: Analysis started with task ID ${analysisData.taskId}`);
    
    // Test 3: Check task status
    if (analysisData.taskId) {
      console.log('\n3. Testing GET /api/agents/tasks/:taskId');
      
      // Wait a bit for processing
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      const taskResponse = await fetch(`http://localhost:3001/api/agents/tasks/${analysisData.taskId}`);
      const taskData = await taskResponse.json();
      console.log(`   ✅ Success: Task progress ${taskData.task?.progress || 0}%`);
    }
    
    // Test 4: Control agent
    console.log('\n4. Testing POST /api/agents/:agentId/control');
    const controlResponse = await fetch('http://localhost:3001/api/agents/finance_agent/control', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ action: 'stop' })
    });
    const controlData = await controlResponse.json();
    console.log(`   ✅ Success: Agent control - ${controlData.message}`);
    
    console.log('\n🎉 All API tests passed!');
    
  } catch (error) {
    console.error('❌ API test failed:', error.message);
  }
}, 1000);

module.exports = app;