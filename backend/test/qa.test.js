const request = require('supertest');
const app = require('../server');
const qaService = require('../services/qaService');

describe('Q&A System Tests', () => {
  
  describe('QA Service', () => {
    test('should classify queries correctly', async () => {
      const riskQuery = await qaService.classifyQuery('What are the risks for this deal?');
      expect(riskQuery).toBe('risk_assessment');

      const financialQuery = await qaService.classifyQuery('Show me the revenue data');
      expect(financialQuery).toBe('financial_data');

      const dealQuery = await qaService.classifyQuery('What is the status of the deal?');
      expect(dealQuery).toBe('deal_info');
    });

    test('should extract entities from questions', async () => {
      const entities = await qaService.extractEntities('What are the risks for Apple Inc?');
      expect(entities).toHaveProperty('companies');
      expect(entities).toHaveProperty('deals');
      expect(entities).toHaveProperty('agents');
    });

    test('should generate suggested queries', async () => {
      const suggestions = await qaService.getSuggestedQueries();
      expect(Array.isArray(suggestions)).toBe(true);
      expect(suggestions.length).toBeGreaterThan(0);
      expect(suggestions.length).toBeLessThanOrEqual(10);
    });

    test('should process simple queries', async () => {
      const result = await qaService.processQuery('What deals are active?');
      expect(result).toHaveProperty('success');
      expect(result).toHaveProperty('question');
      expect(result).toHaveProperty('answer');
      expect(result).toHaveProperty('queryType');
    });
  });

  describe('Q&A API Endpoints', () => {
    test('POST /api/v1/qa/ask - should process a question', async () => {
      const response = await request(app)
        .post('/api/v1/qa/ask')
        .send({
          question: 'What deals are currently active?',
          context: {}
        });

      expect(response.status).toBe(200);
      expect(response.body.success).toBe(true);
      expect(response.body.data).toHaveProperty('question');
      expect(response.body.data).toHaveProperty('answer');
      expect(response.body.data).toHaveProperty('queryType');
    });

    test('POST /api/v1/qa/ask - should validate input', async () => {
      const response = await request(app)
        .post('/api/v1/qa/ask')
        .send({
          question: 'Hi' // Too short
        });

      expect(response.status).toBe(400);
      expect(response.body.success).toBe(false);
      expect(response.body.error).toBe('Validation failed');
    });

    test('GET /api/v1/qa/suggestions - should return suggestions', async () => {
      const response = await request(app)
        .get('/api/v1/qa/suggestions');

      expect(response.status).toBe(200);
      expect(response.body.success).toBe(true);
      expect(response.body.data).toHaveProperty('suggestions');
      expect(Array.isArray(response.body.data.suggestions)).toBe(true);
    });

    test('GET /api/v1/qa/search - should search data', async () => {
      const response = await request(app)
        .get('/api/v1/qa/search')
        .query({ q: 'test' });

      expect(response.status).toBe(200);
      expect(response.body.success).toBe(true);
      expect(response.body.data).toHaveProperty('results');
      expect(response.body.data).toHaveProperty('total');
    });

    test('GET /api/v1/qa/search - should validate search term', async () => {
      const response = await request(app)
        .get('/api/v1/qa/search')
        .query({ q: 'a' }); // Too short

      expect(response.status).toBe(400);
      expect(response.body.success).toBe(false);
    });

    test('POST /api/v1/qa/batch - should process multiple questions', async () => {
      const response = await request(app)
        .post('/api/v1/qa/batch')
        .send({
          questions: [
            { question: 'What deals are active?' },
            { question: 'Show me company information' }
          ]
        });

      expect(response.status).toBe(200);
      expect(response.body.success).toBe(true);
      expect(response.body.data).toHaveProperty('results');
      expect(response.body.data.results).toHaveLength(2);
      expect(response.body.data).toHaveProperty('summary');
    });

    test('GET /api/v1/qa/categories - should return query categories', async () => {
      const response = await request(app)
        .get('/api/v1/qa/categories');

      expect(response.status).toBe(200);
      expect(response.body.success).toBe(true);
      expect(response.body.data).toHaveProperty('categories');
      expect(Array.isArray(response.body.data.categories)).toBe(true);
      expect(response.body.data.categories.length).toBeGreaterThan(0);
    });

    test('GET /api/v1/qa/stats - should return system statistics', async () => {
      const response = await request(app)
        .get('/api/v1/qa/stats');

      expect(response.status).toBe(200);
      expect(response.body.success).toBe(true);
      expect(response.body.data).toHaveProperty('overview');
      expect(response.body.data).toHaveProperty('capabilities');
    });
  });

  describe('Context-Aware Queries', () => {
    test('should handle deal-specific context', async () => {
      // This would require actual test data in the database
      const result = await qaService.processQuery(
        'What are the risks for this deal?',
        { deal_id: '123e4567-e89b-12d3-a456-426614174000' }
      );

      expect(result).toHaveProperty('success');
      expect(result).toHaveProperty('queryType');
    });

    test('should handle company-specific context', async () => {
      const result = await qaService.processQuery(
        'Show me financial data',
        { company_id: '123e4567-e89b-12d3-a456-426614174000' }
      );

      expect(result).toHaveProperty('success');
      expect(result).toHaveProperty('queryType');
    });
  });

  describe('Error Handling', () => {
    test('should handle invalid questions gracefully', async () => {
      const result = await qaService.processQuery('');
      expect(result.success).toBe(false);
      expect(result).toHaveProperty('error');
    });

    test('should handle database errors gracefully', async () => {
      // Mock a database error scenario
      const originalQuery = require('../utils/database').query;
      require('../utils/database').query = jest.fn().mockRejectedValue(new Error('Database error'));

      const result = await qaService.processQuery('What deals are active?');
      expect(result.success).toBe(false);

      // Restore original function
      require('../utils/database').query = originalQuery;
    });
  });

  describe('AI Integration', () => {
    test('should work with AI enabled', async () => {
      const geminiService = require('../services/gemini');
      if (geminiService.isAvailable()) {
        const result = await qaService.processQuery('What are the key risks in M&A deals?');
        expect(result.success).toBe(true);
        expect(result.confidence).toBeGreaterThan(0.5);
      }
    });

    test('should work with AI disabled', async () => {
      const geminiService = require('../services/gemini');
      const originalIsAvailable = geminiService.isAvailable;
      geminiService.isAvailable = jest.fn().mockReturnValue(false);

      const result = await qaService.processQuery('What deals are active?');
      expect(result.success).toBe(true);
      expect(result).toHaveProperty('answer');

      // Restore original function
      geminiService.isAvailable = originalIsAvailable;
    });
  });
});

describe('Integration Tests', () => {
  test('should handle end-to-end Q&A workflow', async () => {
    // 1. Get suggestions
    const suggestionsResponse = await request(app)
      .get('/api/v1/qa/suggestions');
    
    expect(suggestionsResponse.status).toBe(200);
    const suggestions = suggestionsResponse.body.data.suggestions;

    // 2. Ask a question from suggestions
    if (suggestions.length > 0) {
      const questionResponse = await request(app)
        .post('/api/v1/qa/ask')
        .send({
          question: suggestions[0]
        });

      expect(questionResponse.status).toBe(200);
      expect(questionResponse.body.success).toBe(true);
    }

    // 3. Search for related data
    const searchResponse = await request(app)
      .get('/api/v1/qa/search')
      .query({ q: 'deal' });

    expect(searchResponse.status).toBe(200);
    expect(searchResponse.body.success).toBe(true);
  });

  test('should provide consistent results', async () => {
    const question = 'What deals are currently active?';
    
    const response1 = await request(app)
      .post('/api/v1/qa/ask')
      .send({ question });

    const response2 = await request(app)
      .post('/api/v1/qa/ask')
      .send({ question });

    expect(response1.status).toBe(200);
    expect(response2.status).toBe(200);
    expect(response1.body.data.queryType).toBe(response2.body.data.queryType);
  });
});