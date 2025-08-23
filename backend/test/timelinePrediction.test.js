const timelinePrediction = require('../services/timelinePrediction');

describe('Timeline Prediction Service', () => {
  describe('Document Complexity Analysis', () => {
    test('should analyze low complexity documents', () => {
      const documentData = {
        document_count: 10,
        total_pages: 50,
        total_size_mb: 25,
        document_types: {
          'financial_statements': 3,
          'hr_data': 7
        },
        file_formats: {
          'csv': 5,
          'txt': 5
        },
        data_quality: 'good'
      };

      const analysis = timelinePrediction.analyzeDocumentComplexity(documentData);

      expect(analysis.overall_complexity).toBe('low');
      expect(analysis.estimated_multiplier).toBe(0.7);
      expect(analysis.factors.document_volume).toBe('low');
      expect(analysis.factors.page_volume).toBe('low');
      expect(analysis.factors.file_size).toBe('low');
    });

    test('should analyze high complexity documents', () => {
      const documentData = {
        document_count: 150,
        total_pages: 1500,
        total_size_mb: 800,
        document_types: {
          'legal_contracts': 50,
          'technical_docs': 100
        },
        file_formats: {
          'pdf': 100,
          'docx': 50
        },
        languages: ['en', 'es', 'fr'],
        data_quality: 'poor'
      };

      const analysis = timelinePrediction.analyzeDocumentComplexity(documentData);

      expect(analysis.overall_complexity).toBe('very_high');
      expect(analysis.estimated_multiplier).toBe(2.2);
      expect(analysis.factors.document_volume).toBe('high');
      expect(analysis.factors.page_volume).toBe('high');
      expect(analysis.factors.file_size).toBe('high');
      expect(analysis.factors.language_diversity).toBe('high');
      expect(analysis.factors.data_quality).toBe('poor');
    });

    test('should handle missing document data gracefully', () => {
      const documentData = {};

      const analysis = timelinePrediction.analyzeDocumentComplexity(documentData);

      expect(analysis.overall_complexity).toBe('low');
      expect(analysis.estimated_multiplier).toBe(0.7);
      expect(typeof analysis.complexity_score).toBe('number');
    });
  });

  describe('Agent Estimates Calculation', () => {
    test('should calculate agent estimates with complexity multipliers', () => {
      const executions = [
        { agent_type: 'finance', status: 'pending' },
        { agent_type: 'legal', status: 'pending' },
        { agent_type: 'synergy', status: 'pending' }
      ];

      const complexityAnalysis = {
        estimated_multiplier: 1.5,
        factors: {
          document_types: 'high',
          data_quality: 'poor'
        }
      };

      const estimates = timelinePrediction.calculateAgentEstimates(executions, complexityAnalysis);

      expect(estimates).toHaveLength(5); // All agent types
      
      const financeEstimate = estimates.find(e => e.agent_type === 'finance');
      expect(financeEstimate.base_duration_hours).toBe(2.5);
      expect(financeEstimate.complexity_multiplier).toBe(1.5);
      expect(financeEstimate.agent_specific_multiplier).toBe(1.4); // Poor data quality affects finance
      expect(financeEstimate.estimated_hours).toBeGreaterThan(2.5);

      const legalEstimate = estimates.find(e => e.agent_type === 'legal');
      expect(legalEstimate.agent_specific_multiplier).toBe(1.3); // High document types affects legal
    });
  });

  describe('Execution Phases', () => {
    test('should build execution phases considering dependencies', () => {
      const agentEstimates = [
        { agent_type: 'finance', estimated_hours: 3.0, dependencies: [] },
        { agent_type: 'legal', estimated_hours: 4.0, dependencies: [] },
        { agent_type: 'synergy', estimated_hours: 2.0, dependencies: ['finance'] },
        { agent_type: 'operations', estimated_hours: 3.5, dependencies: ['finance', 'legal'] }
      ];

      const phases = timelinePrediction.buildExecutionPhases(agentEstimates);

      expect(phases).toHaveLength(2);
      
      // Phase 1: Independent agents
      expect(phases[0].phase).toBe(1);
      expect(phases[0].agents).toHaveLength(3); // finance, legal, reputation
      expect(phases[0].can_run_parallel).toBe(true);
      expect(phases[0].estimated_duration_hours).toBe(4.0); // Max of parallel agents

      // Phase 2: Dependent agents
      expect(phases[1].phase).toBe(2);
      expect(phases[1].agents).toHaveLength(2); // synergy, operations
    });
  });

  describe('Bottleneck Identification', () => {
    test('should identify long-running agent bottlenecks', () => {
      const agentEstimates = [
        { agent_type: 'finance', estimated_hours: 2.0, dependencies: [] },
        { agent_type: 'legal', estimated_hours: 6.0, dependencies: [] }, // Bottleneck
        { agent_type: 'reputation', estimated_hours: 1.0, dependencies: [] }
      ];

      const executionPhases = [
        {
          phase: 1,
          agents: agentEstimates,
          can_run_parallel: true,
          estimated_duration_hours: 6.0
        }
      ];

      const bottlenecks = timelinePrediction.identifyTimelineBottlenecks(agentEstimates, executionPhases);

      expect(bottlenecks).toHaveLength(1);
      expect(bottlenecks[0].type).toBe('long_running_agent');
      expect(bottlenecks[0].agent_type).toBe('legal');
      expect(bottlenecks[0].severity).toBe('high');
    });

    test('should identify dependency bottlenecks', () => {
      const agentEstimates = [
        { agent_type: 'finance', estimated_hours: 2.0, dependencies: [] },
        { agent_type: 'legal', estimated_hours: 3.0, dependencies: [] },
        { agent_type: 'operations', estimated_hours: 1.0, dependencies: ['finance', 'legal'] } // Heavy dependency
      ];

      const executionPhases = [];

      const bottlenecks = timelinePrediction.identifyTimelineBottlenecks(agentEstimates, executionPhases);

      const dependencyBottleneck = bottlenecks.find(b => b.type === 'dependency_bottleneck');
      expect(dependencyBottleneck).toBeDefined();
      expect(dependencyBottleneck.agent_type).toBe('operations');
      expect(dependencyBottleneck.dependencies).toEqual(['finance', 'legal']);
    });
  });

  describe('Confidence Level Calculation', () => {
    test('should calculate confidence based on complexity and historical data', () => {
      const complexityAnalysis = {
        overall_complexity: 'medium',
        factors: {
          data_quality: 'good'
        }
      };

      const executions = [
        {
          agent_type: 'finance',
          status: 'completed',
          duration_seconds: 9000 // 2.5 hours
        }
      ];

      const confidence = timelinePrediction.calculateConfidenceLevel(complexityAnalysis, executions);

      expect(confidence).toBeGreaterThan(50);
      expect(confidence).toBeLessThanOrEqual(95);
    });

    test('should reduce confidence for very high complexity', () => {
      const complexityAnalysis = {
        overall_complexity: 'very_high',
        factors: {
          data_quality: 'poor'
        }
      };

      const executions = [];

      const confidence = timelinePrediction.calculateConfidenceLevel(complexityAnalysis, executions);

      expect(confidence).toBeLessThan(60); // Should be significantly reduced
    });
  });

  describe('Completion Date Calculation', () => {
    test('should calculate completion date considering working days', () => {
      const totalHours = 16; // 2 working days
      const completionDate = timelinePrediction.calculateCompletionDate(totalHours);

      expect(completionDate).toBeInstanceOf(Date);
      expect(completionDate.getTime()).toBeGreaterThan(new Date().getTime());
    });
  });

  describe('Overall Progress Calculation', () => {
    test('should calculate overall progress correctly', () => {
      const agentEstimates = [
        { status: 'completed' },
        { status: 'running', progress_percentage: 50 },
        { status: 'pending' },
        { status: 'completed' }
      ];

      const progress = timelinePrediction.calculateOverallProgress(agentEstimates);

      expect(progress).toBe(63); // (100 + 50 + 0 + 100) / 4 = 62.5, rounded to 63
    });

    test('should handle empty agent estimates', () => {
      const progress = timelinePrediction.calculateOverallProgress([]);
      expect(progress).toBe(0);
    });
  });
});