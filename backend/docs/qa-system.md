# Q&A System Documentation

## Overview

The Q&A (Question & Answer) System is a factual query processing system that allows users to ask natural language questions about M&A due diligence data and receive direct answers with supporting data references.

## Features

### Core Capabilities

1. **Natural Language Processing**: Understands questions in natural language
2. **Query Classification**: Automatically categorizes questions by type
3. **Entity Extraction**: Identifies companies, deals, agents, and other entities
4. **Context-Aware**: Provides more relevant answers based on context
5. **AI-Powered Answers**: Uses Gemini AI for intelligent response generation
6. **Fallback Answers**: Works even when AI is unavailable
7. **Search Integration**: Full-text search across all data
8. **Batch Processing**: Handle multiple questions simultaneously

### Query Types

The system supports the following query categories:

- **Deal Information**: Questions about deal status, progress, and details
- **Company Information**: Questions about company profiles and characteristics
- **Financial Data**: Questions about financial metrics and performance
- **Risk Assessment**: Questions about risks, threats, and critical findings
- **Agent Status**: Questions about agent execution and performance
- **Timeline**: Questions about timelines, completion dates, and progress
- **Findings**: Questions about specific findings and issues

## API Endpoints

### POST /api/v1/qa/ask

Ask a factual question about M&A data.

**Request Body:**
```json
{
  "question": "What are the key risks for deal ABC?",
  "context": {
    "deal_id": "uuid",
    "company_id": "uuid"
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "question": "What are the key risks for deal ABC?",
    "answer": "Based on the analysis, the key risks include...",
    "queryType": "risk_assessment",
    "entities": {
      "companies": [],
      "deals": [{"id": "uuid", "name": "ABC"}],
      "agents": []
    },
    "supportingData": {
      "findings": [...],
      "sources": ["findings"]
    },
    "confidence": 0.8,
    "sources": ["findings"],
    "timestamp": "2024-01-01T00:00:00.000Z"
  }
}
```

### GET /api/v1/qa/suggestions

Get suggested questions based on context.

**Query Parameters:**
- `deal_id` (optional): UUID of specific deal
- `company_id` (optional): UUID of specific company

**Response:**
```json
{
  "success": true,
  "data": {
    "suggestions": [
      "What are the key risks for deal [deal_name]?",
      "Show me financial metrics for [company_name]",
      "What is the status of all agents?"
    ],
    "context": {
      "deal_id": "uuid",
      "company_id": "uuid"
    },
    "total": 10
  }
}
```

### GET /api/v1/qa/search

Search across all M&A data.

**Query Parameters:**
- `q` (required): Search term (2-100 characters)
- `category` (optional): 'deals', 'companies', 'findings', 'agents', or 'all'
- `limit` (optional): Result limit (1-100, default: 20)

**Response:**
```json
{
  "success": true,
  "data": {
    "searchTerm": "risk",
    "category": "all",
    "results": {
      "deals": [...],
      "companies": [...],
      "findings": [...],
      "agents": [...],
      "total": 25
    },
    "total": 25
  }
}
```

### POST /api/v1/qa/batch

Process multiple questions in batch.

**Request Body:**
```json
{
  "questions": [
    {
      "question": "What deals are active?",
      "context": {}
    },
    {
      "question": "Show me financial data",
      "context": {"company_id": "uuid"}
    }
  ],
  "context": {
    "deal_id": "uuid"
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "results": [
      {
        "index": 0,
        "question": "What deals are active?",
        "success": true,
        "answer": "...",
        "queryType": "deal_info"
      }
    ],
    "summary": {
      "total": 2,
      "successful": 2,
      "failed": 0
    }
  }
}
```

### GET /api/v1/qa/categories

Get available query categories and descriptions.

**Response:**
```json
{
  "success": true,
  "data": {
    "categories": [
      {
        "type": "deal_info",
        "name": "Deal Information",
        "description": "Questions about deal status, progress, and general information",
        "examples": [
          "What is the status of deal XYZ?",
          "Show me all active deals"
        ]
      }
    ],
    "total": 7
  }
}
```

### GET /api/v1/qa/stats

Get Q&A system statistics.

**Response:**
```json
{
  "success": true,
  "data": {
    "overview": {
      "totalDeals": 10,
      "totalCompanies": 25,
      "totalFindings": 150,
      "totalAgentExecutions": 75
    },
    "dealStatus": {
      "total": 10,
      "active": 5,
      "completed": 3
    },
    "findingsBySeverity": {
      "critical": 5,
      "high": 15,
      "medium": 80,
      "low": 50
    },
    "capabilities": {
      "aiEnabled": true,
      "searchEnabled": true,
      "batchProcessing": true,
      "contextAware": true
    }
  }
}
```

## Usage Examples

### Basic Question
```javascript
const response = await fetch('/api/v1/qa/ask', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    question: 'What deals are currently active?'
  })
});
```

### Context-Aware Question
```javascript
const response = await fetch('/api/v1/qa/ask', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    question: 'What are the risks for this deal?',
    context: {
      deal_id: '123e4567-e89b-12d3-a456-426614174000'
    }
  })
});
```

### Search Data
```javascript
const response = await fetch('/api/v1/qa/search?q=financial%20risk&category=findings');
```

### Get Suggestions
```javascript
const response = await fetch('/api/v1/qa/suggestions?deal_id=123e4567-e89b-12d3-a456-426614174000');
```

## Query Examples by Category

### Deal Information
- "What deals are currently active?"
- "Show me all completed deals this month"
- "What is the status of deal [name]?"
- "Which deals have the highest value?"

### Company Information
- "Tell me about Apple Inc."
- "What companies are in the technology sector?"
- "Show me all companies with revenue over $1B"
- "What is the market cap of Microsoft?"

### Financial Data
- "What is the revenue of Apple?"
- "Show me financial ratios for Tesla"
- "Compare the profitability of these companies"
- "What are the debt levels for this company?"

### Risk Assessment
- "What are the key risks for this deal?"
- "Show me all critical findings"
- "What financial risks were identified?"
- "Which deals have the highest risk scores?"

### Agent Status
- "What is the status of all agents?"
- "Which agents are currently running?"
- "Show me failed agent executions"
- "What agents completed successfully?"

### Timeline
- "When will this deal be completed?"
- "What is the estimated timeline?"
- "Show me the project timeline"
- "Which deals are behind schedule?"

### Findings
- "What issues were found?"
- "Show me legal findings"
- "What problems need attention?"
- "List all high-severity findings"

## Implementation Details

### Query Processing Flow

1. **Input Validation**: Validate question format and context
2. **Query Classification**: Determine the type of question
3. **Entity Extraction**: Identify relevant entities (companies, deals, etc.)
4. **Data Retrieval**: Fetch relevant data from database
5. **Answer Generation**: Generate natural language answer using AI
6. **Response Formatting**: Format response with supporting data

### AI Integration

The system integrates with Google's Gemini AI for:
- Natural language answer generation
- Complex query understanding
- Context-aware responses

When AI is unavailable, the system provides:
- Structured data responses
- Basic answer templates
- Fallback explanations

### Database Integration

The system queries the following tables:
- `deals`: Deal information and status
- `companies`: Company profiles and data
- `financial_data`: Financial metrics and ratios
- `findings`: Risk findings and issues
- `agent_executions`: Agent status and results
- `timeline_estimates`: Timeline and progress data

### Performance Considerations

- Query results are limited to prevent large responses
- Database queries use indexes for optimal performance
- AI responses are cached when possible
- Batch processing is limited to 10 questions maximum

## Error Handling

The system handles various error scenarios:

### Validation Errors
- Invalid question format
- Missing required parameters
- Invalid UUIDs in context

### Processing Errors
- Database connection issues
- AI service unavailability
- Query timeout errors

### Response Format
```json
{
  "success": false,
  "error": "Error type",
  "message": "Detailed error message",
  "timestamp": "2024-01-01T00:00:00.000Z"
}
```

## Testing

### Unit Tests
Run unit tests for the Q&A service:
```bash
npm test -- qa.test.js
```

### Integration Testing
Test the complete Q&A system:
```bash
node scripts/testQASystem.js
```

### Manual Testing
Use the API endpoints directly or through the frontend interface.

## Configuration

### Environment Variables
- `GEMINI_API_KEY`: Google Gemini API key for AI features
- `DATABASE_URL`: PostgreSQL connection string

### Service Configuration
The Q&A service can be configured in `services/qaService.js`:
- Query types and classifications
- Suggested queries templates
- Entity extraction patterns
- Fallback answer templates

## Troubleshooting

### Common Issues

1. **AI Not Available**
   - Check `GEMINI_API_KEY` environment variable
   - Verify API key is valid and has quota
   - System will use fallback answers

2. **No Results Found**
   - Check database connection
   - Verify data exists in relevant tables
   - Try broader search terms

3. **Slow Response Times**
   - Check database performance
   - Review query complexity
   - Consider adding database indexes

4. **Invalid Context**
   - Verify UUID format for deal_id/company_id
   - Check if referenced entities exist
   - Use valid context parameters

### Debug Mode
Enable debug logging by setting:
```bash
DEBUG=qa:* node server.js
```

## Future Enhancements

Planned improvements include:
- Advanced NLP for better entity extraction
- Machine learning for query classification
- Caching for frequently asked questions
- Real-time data updates
- Multi-language support
- Voice query processing