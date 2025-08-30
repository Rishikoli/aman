const express = require('express');
const router = express.Router();

// Mock agent status data (in production, this would come from actual agent services)
let agentStatuses = {
  finance_agent: {
    id: 'finance_agent',
    name: 'Finance Agent',
    status: 'active',
    healthScore: 92,
    cpuUsage: 23,
    memoryUsage: 68,
    lastRun: new Date().toISOString(),
    tasksCompleted: 1247,
    successRate: 94.2,
    avgExecutionTime: 45.3,
    currentTask: null,
    isProcessing: false
  },
  legal_agent: {
    id: 'legal_agent',
    name: 'Legal & Compliance Agent',
    status: 'active',
    healthScore: 96,
    cpuUsage: 18,
    memoryUsage: 45,
    lastRun: new Date().toISOString(),
    tasksCompleted: 892,
    successRate: 97.8,
    avgExecutionTime: 62.1,
    currentTask: null,
    isProcessing: false
  },
  operations_agent: {
    id: 'operations_agent',
    name: 'Global Operations Agent',
    status: 'active',
    healthScore: 88,
    cpuUsage: 31,
    memoryUsage: 72,
    lastRun: new Date().toISOString(),
    tasksCompleted: 634,
    successRate: 91.5,
    avgExecutionTime: 78.9,
    currentTask: null,
    isProcessing: false
  },
  monitoring_agent: {
    id: 'monitoring_agent',
    name: 'System Monitoring Agent',
    status: 'active',
    healthScore: 98,
    cpuUsage: 15,
    memoryUsage: 34,
    lastRun: new Date().toISOString(),
    tasksCompleted: 2156,
    successRate: 99.1,
    avgExecutionTime: 12.4,
    currentTask: null,
    isProcessing: false
  },
  synergy_agent: {
    id: 'synergy_agent',
    name: 'Synergy Analysis Agent',
    status: 'idle',
    healthScore: 85,
    cpuUsage: 8,
    memoryUsage: 52,
    lastRun: new Date(Date.now() - 15 * 60 * 1000).toISOString(),
    tasksCompleted: 423,
    successRate: 89.7,
    avgExecutionTime: 156.2,
    currentTask: null,
    isProcessing: false
  },
  reputation_agent: {
    id: 'reputation_agent',
    name: 'Reputation Analysis Agent',
    status: 'maintenance',
    healthScore: 72,
    cpuUsage: 5,
    memoryUsage: 41,
    lastRun: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
    tasksCompleted: 567,
    successRate: 86.3,
    avgExecutionTime: 89.7,
    currentTask: null,
    isProcessing: false
  },
  audit_agent: {
    id: 'audit_agent',
    name: 'Audit & Compliance Agent',
    status: 'active',
    healthScore: 94,
    cpuUsage: 12,
    memoryUsage: 28,
    lastRun: new Date().toISOString(),
    tasksCompleted: 1089,
    successRate: 95.4,
    avgExecutionTime: 34.6,
    currentTask: null,
    isProcessing: false
  }
};

// Store active tasks
let activeTasks = new Map();

// GET /api/agents - Get all agent statuses
router.get('/', (req, res) => {
  try {
    const agents = Object.values(agentStatuses).map(agent => ({
      ...agent,
      lastRun: getRelativeTime(agent.lastRun)
    }));
    
    res.json({
      success: true,
      agents,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// GET /api/agents/:agentId - Get specific agent status
router.get('/:agentId', (req, res) => {
  try {
    const { agentId } = req.params;
    const agent = agentStatuses[agentId];
    
    if (!agent) {
      return res.status(404).json({
        success: false,
        error: 'Agent not found'
      });
    }
    
    res.json({
      success: true,
      agent: {
        ...agent,
        lastRun: getRelativeTime(agent.lastRun)
      }
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// POST /api/agents/analyze - Send data to all agents for analysis
router.post('/analyze', async (req, res) => {
  try {
    const { companyData, analysisType = 'comprehensive' } = req.body;
    
    if (!companyData) {
      return res.status(400).json({
        success: false,
        error: 'Company data is required'
      });
    }
    
    const taskId = generateTaskId();
    const timestamp = new Date().toISOString();
    
    // Create analysis task
    const analysisTask = {
      taskId,
      companyData,
      analysisType,
      timestamp,
      status: 'initiated',
      results: {},
      agentStatuses: {}
    };
    
    activeTasks.set(taskId, analysisTask);
    
    // Start analysis for each active agent
    const activeAgents = Object.values(agentStatuses).filter(agent => 
      agent.status === 'active' && !agent.isProcessing
    );
    
    const analysisPromises = activeAgents.map(agent => 
      startAgentAnalysis(agent.id, companyData, analysisType, taskId)
    );
    
    // Don't wait for all analyses to complete, return immediately
    Promise.all(analysisPromises).catch(error => {
      console.error('Error in agent analyses:', error);
    });
    
    res.json({
      success: true,
      taskId,
      message: 'Analysis initiated for all active agents',
      activeAgents: activeAgents.length,
      timestamp
    });
    
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// POST /api/agents/:agentId/analyze - Send data to specific agent
router.post('/:agentId/analyze', async (req, res) => {
  try {
    const { agentId } = req.params;
    const { companyData, analysisType = 'comprehensive' } = req.body;
    
    const agent = agentStatuses[agentId];
    if (!agent) {
      return res.status(404).json({
        success: false,
        error: 'Agent not found'
      });
    }
    
    if (agent.status !== 'active') {
      return res.status(400).json({
        success: false,
        error: `Agent is ${agent.status} and cannot process requests`
      });
    }
    
    if (agent.isProcessing) {
      return res.status(409).json({
        success: false,
        error: 'Agent is currently processing another task'
      });
    }
    
    const taskId = generateTaskId();
    const result = await startAgentAnalysis(agentId, companyData, analysisType, taskId);
    
    res.json({
      success: true,
      taskId,
      agentId,
      result,
      timestamp: new Date().toISOString()
    });
    
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// GET /api/agents/tasks/:taskId - Get task status and results
router.get('/tasks/:taskId', (req, res) => {
  try {
    const { taskId } = req.params;
    const task = activeTasks.get(taskId);
    
    if (!task) {
      return res.status(404).json({
        success: false,
        error: 'Task not found'
      });
    }
    
    // Calculate overall progress
    const totalAgents = Object.keys(task.agentStatuses).length;
    const completedAgents = Object.values(task.agentStatuses).filter(
      status => status === 'completed' || status === 'error'
    ).length;
    
    const progress = totalAgents > 0 ? (completedAgents / totalAgents) * 100 : 0;
    const isComplete = completedAgents === totalAgents;
    
    res.json({
      success: true,
      task: {
        ...task,
        progress: Math.round(progress),
        isComplete,
        completedAgents,
        totalAgents
      }
    });
    
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// POST /api/agents/:agentId/control - Control agent (start/stop)
router.post('/:agentId/control', (req, res) => {
  try {
    const { agentId } = req.params;
    const { action } = req.body;
    
    const agent = agentStatuses[agentId];
    if (!agent) {
      return res.status(404).json({
        success: false,
        error: 'Agent not found'
      });
    }
    
    if (!['start', 'stop', 'restart'].includes(action)) {
      return res.status(400).json({
        success: false,
        error: 'Invalid action. Use start, stop, or restart'
      });
    }
    
    // Update agent status based on action
    switch (action) {
      case 'start':
        agent.status = 'active';
        break;
      case 'stop':
        agent.status = 'idle';
        agent.isProcessing = false;
        agent.currentTask = null;
        break;
      case 'restart':
        agent.status = 'active';
        agent.isProcessing = false;
        agent.currentTask = null;
        break;
    }
    
    agent.lastRun = new Date().toISOString();
    
    res.json({
      success: true,
      message: `Agent ${action} successful`,
      agent: {
        ...agent,
        lastRun: getRelativeTime(agent.lastRun)
      }
    });
    
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// Helper function to start agent analysis
async function startAgentAnalysis(agentId, companyData, analysisType, taskId) {
  const agent = agentStatuses[agentId];
  
  // Mark agent as processing
  agent.isProcessing = true;
  agent.currentTask = taskId;
  agent.lastRun = new Date().toISOString();
  
  // Update task status
  const task = activeTasks.get(taskId);
  if (task) {
    task.agentStatuses[agentId] = 'processing';
  }
  
  try {
    // Simulate agent processing time
    const processingTime = agent.avgExecutionTime * 1000 + Math.random() * 5000;
    
    await new Promise(resolve => setTimeout(resolve, processingTime));
    
    // Generate mock analysis result based on agent type
    const result = generateMockAnalysisResult(agentId, companyData, analysisType);
    
    // Update agent stats
    agent.tasksCompleted += 1;
    agent.isProcessing = false;
    agent.currentTask = null;
    agent.lastRun = new Date().toISOString();
    
    // Simulate success rate
    const isSuccess = Math.random() < (agent.successRate / 100);
    
    if (isSuccess) {
      // Update task with results
      if (task) {
        task.results[agentId] = result;
        task.agentStatuses[agentId] = 'completed';
      }
      
      return result;
    } else {
      // Simulate failure
      const error = `Analysis failed for ${agent.name}`;
      if (task) {
        task.results[agentId] = { error };
        task.agentStatuses[agentId] = 'error';
      }
      throw new Error(error);
    }
    
  } catch (error) {
    agent.isProcessing = false;
    agent.currentTask = null;
    
    if (task) {
      task.results[agentId] = { error: error.message };
      task.agentStatuses[agentId] = 'error';
    }
    
    throw error;
  }
}

// Helper function to generate mock analysis results
function generateMockAnalysisResult(agentId, companyData, analysisType) {
  const baseResult = {
    agentId,
    analysisType,
    timestamp: new Date().toISOString(),
    companyName: companyData.name || 'Unknown Company',
    confidence: Math.random() * 0.3 + 0.7 // 70-100% confidence
  };
  
  switch (agentId) {
    case 'finance_agent':
      return {
        ...baseResult,
        financialHealth: {
          score: Math.random() * 40 + 60, // 60-100
          profitability: Math.random() * 30 + 70,
          liquidity: Math.random() * 25 + 75,
          leverage: Math.random() * 50 + 25
        },
        riskFactors: [
          'Market volatility exposure',
          'Currency exchange risk',
          'Interest rate sensitivity'
        ].slice(0, Math.floor(Math.random() * 3) + 1),
        recommendation: 'Proceed with enhanced due diligence'
      };
      
    case 'legal_agent':
      return {
        ...baseResult,
        legalRisk: {
          score: Math.random() * 30 + 20, // 20-50 (lower is better)
          complianceStatus: 'Good',
          litigationRisk: 'Low',
          regulatoryIssues: Math.floor(Math.random() * 3)
        },
        findings: [
          'SEC filings up to date',
          'No major litigation pending',
          'Compliance framework adequate'
        ],
        recommendation: 'Legal structure appears sound'
      };
      
    case 'operations_agent':
      return {
        ...baseResult,
        operationalRisk: {
          score: Math.random() * 40 + 30, // 30-70
          geopoliticalRisk: 'Medium',
          supplyChainRisk: 'Low',
          operationalEfficiency: Math.random() * 20 + 80
        },
        keyMetrics: {
          countriesAnalyzed: Math.floor(Math.random() * 5) + 2,
          supplierRisk: 'Low',
          facilitiesAssessed: Math.floor(Math.random() * 10) + 5
        },
        recommendation: 'Monitor geopolitical developments'
      };
      
    case 'monitoring_agent':
      return {
        ...baseResult,
        systemHealth: {
          score: Math.random() * 10 + 90, // 90-100
          uptime: '99.9%',
          performance: 'Excellent',
          alerts: Math.floor(Math.random() * 3)
        },
        metrics: {
          responseTime: Math.random() * 100 + 50,
          throughput: Math.random() * 1000 + 500,
          errorRate: Math.random() * 0.5
        },
        recommendation: 'System operating optimally'
      };
      
    default:
      return {
        ...baseResult,
        analysis: `${agentId} analysis completed`,
        score: Math.random() * 40 + 60,
        recommendation: 'Analysis completed successfully'
      };
  }
}

// Helper functions
function generateTaskId() {
  return 'task_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
}

function getRelativeTime(timestamp) {
  const now = new Date();
  const time = new Date(timestamp);
  const diffMs = now - time;
  const diffMins = Math.floor(diffMs / 60000);
  
  if (diffMins < 1) return 'Just now';
  if (diffMins < 60) return `${diffMins} minute${diffMins > 1 ? 's' : ''} ago`;
  
  const diffHours = Math.floor(diffMins / 60);
  if (diffHours < 24) return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`;
  
  const diffDays = Math.floor(diffHours / 24);
  return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`;
}

// Simulate real-time updates
setInterval(() => {
  Object.values(agentStatuses).forEach(agent => {
    if (agent.status === 'active' && !agent.isProcessing) {
      // Simulate resource usage fluctuations
      agent.cpuUsage = Math.max(5, Math.min(95, agent.cpuUsage + (Math.random() - 0.5) * 10));
      agent.memoryUsage = Math.max(10, Math.min(90, agent.memoryUsage + (Math.random() - 0.5) * 8));
      
      // Occasionally update health score
      if (Math.random() < 0.1) {
        agent.healthScore = Math.max(60, Math.min(100, agent.healthScore + (Math.random() - 0.5) * 5));
      }
    }
  });
}, 3000);

module.exports = router;