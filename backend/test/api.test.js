describe('Deal Orchestrator Implementation', () => {
  describe('Models Validation', () => {
    test('Deal model validation should work', () => {
      const Deal = require('../models/Deal');
      
      // Test valid deal data
      const validDeal = {
        name: 'Test Deal',
        acquirer_id: '123e4567-e89b-12d3-a456-426614174000',
        target_id: '123e4567-e89b-12d3-a456-426614174001',
        deal_value: 1000000,
        created_by: 'test@example.com'
      };
      
      const validation = Deal.validate(validDeal);
      expect(validation.isValid).toBe(true);
      expect(validation.errors).toHaveLength(0);
    });

    test('Deal model validation should catch errors', () => {
      const Deal = require('../models/Deal');
      
      // Test invalid deal data
      const invalidDeal = {
        name: '', // Empty name
        acquirer_id: 'invalid-uuid',
        target_id: 'invalid-uuid'
        // Missing required fields
      };
      
      const validation = Deal.validate(invalidDeal);
      expect(validation.isValid).toBe(false);
      expect(validation.errors.length).toBeGreaterThan(0);
    });

    test('Company model validation should work', () => {
      const Company = require('../models/Company');
      
      // Test valid company data
      const validCompany = {
        name: 'Test Company',
        ticker_symbol: 'TEST',
        industry: 'Technology',
        founded_year: 2020,
        employee_count: 100
      };
      
      const validation = Company.validate(validCompany);
      expect(validation.isValid).toBe(true);
      expect(validation.errors).toHaveLength(0);
    });

    test('Company model validation should catch errors', () => {
      const Company = require('../models/Company');
      
      // Test invalid company data
      const invalidCompany = {
        name: '', // Empty name
        ticker_symbol: 'TOOLONG', // Too long
        founded_year: 1700, // Too early
        employee_count: -5 // Negative
      };
      
      const validation = Company.validate(invalidCompany);
      expect(validation.isValid).toBe(false);
      expect(validation.errors.length).toBeGreaterThan(0);
    });

    test('AgentExecution model validation should work', () => {
      const AgentExecution = require('../models/AgentExecution');
      
      // Test valid execution data
      const validExecution = {
        deal_id: '123e4567-e89b-12d3-a456-426614174000',
        agent_type: 'finance',
        agent_id: 'finance-agent-1',
        status: 'pending'
      };
      
      const validation = AgentExecution.validate(validExecution);
      expect(validation.isValid).toBe(true);
      expect(validation.errors).toHaveLength(0);
    });

    test('AgentExecution model validation should catch errors', () => {
      const AgentExecution = require('../models/AgentExecution');
      
      // Test invalid execution data
      const invalidExecution = {
        // Missing required fields
        agent_type: 'invalid_type',
        status: 'invalid_status',
        progress_percentage: 150 // Over 100
      };
      
      const validation = AgentExecution.validate(invalidExecution);
      expect(validation.isValid).toBe(false);
      expect(validation.errors.length).toBeGreaterThan(0);
    });
  });

  describe('Deal Orchestrator Service', () => {
    test('Service should be importable and have required methods', () => {
      const dealOrchestrator = require('../services/dealOrchestrator');
      expect(dealOrchestrator).toBeDefined();
      expect(typeof dealOrchestrator.createDeal).toBe('function');
      expect(typeof dealOrchestrator.getDealStatus).toBe('function');
      expect(typeof dealOrchestrator.createOrchestrationPlan).toBe('function');
      expect(typeof dealOrchestrator.updateDealStatus).toBe('function');
    });

    test('Service should have correct agent types and dependencies', () => {
      const dealOrchestrator = require('../services/dealOrchestrator');
      expect(dealOrchestrator.agentTypes).toContain('finance');
      expect(dealOrchestrator.agentTypes).toContain('legal');
      expect(dealOrchestrator.agentTypes).toContain('synergy');
      expect(dealOrchestrator.agentTypes).toContain('reputation');
      expect(dealOrchestrator.agentTypes).toContain('operations');
      
      // Check dependencies
      expect(dealOrchestrator.agentDependencies.synergy).toContain('finance');
      expect(dealOrchestrator.agentDependencies.operations).toContain('finance');
      expect(dealOrchestrator.agentDependencies.operations).toContain('legal');
    });

    test('Service should calculate estimated durations', () => {
      const dealOrchestrator = require('../services/dealOrchestrator');
      
      const financeEstimate = dealOrchestrator.getAgentEstimatedDuration('finance');
      expect(financeEstimate).toBeGreaterThan(0);
      expect(typeof financeEstimate).toBe('number');
      
      const legalEstimate = dealOrchestrator.getAgentEstimatedDuration('legal');
      expect(legalEstimate).toBeGreaterThan(0);
      expect(typeof legalEstimate).toBe('number');
    });
  });

  describe('Database Schema', () => {
    test('Schema file should exist and be readable', () => {
      const fs = require('fs');
      const path = require('path');
      
      const schemaPath = path.join(__dirname, '../database/schema.sql');
      expect(fs.existsSync(schemaPath)).toBe(true);
      
      const schemaContent = fs.readFileSync(schemaPath, 'utf8');
      expect(schemaContent).toContain('CREATE TABLE deals');
      expect(schemaContent).toContain('CREATE TABLE companies');
      expect(schemaContent).toContain('CREATE TABLE agent_executions');
      expect(schemaContent).toContain('CREATE TABLE findings');
    });
  });

  describe('API Route Structure', () => {
    test('Deal routes should be properly structured', () => {
      const dealsRoutes = require('../api/routes/deals');
      expect(dealsRoutes).toBeDefined();
      expect(typeof dealsRoutes).toBe('function'); // Express router is a function
    });

    test('Company routes should be properly structured', () => {
      const companiesRoutes = require('../api/routes/companies');
      expect(companiesRoutes).toBeDefined();
      expect(typeof companiesRoutes).toBe('function');
    });

    test('Agent routes should be properly structured', () => {
      const agentsRoutes = require('../api/routes/agents');
      expect(agentsRoutes).toBeDefined();
      expect(typeof agentsRoutes).toBe('function');
    });
  });
});