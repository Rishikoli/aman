# Comprehensive Test Suite for Autonomous M&A Navigator

This directory contains the comprehensive test suite for the AMAN system, covering:

## Test Structure

### 1. Unit Tests (`unit/`)
- Individual agent function tests
- API endpoint tests
- Service layer tests
- Utility function tests

### 2. Integration Tests (`integration/`)
- Agent coordination workflows
- Database integration tests
- External API integration tests
- Message queue integration tests

### 3. End-to-End Tests (`e2e/`)
- Complete deal analysis scenarios
- Full workflow tests
- User journey tests

### 4. Performance Tests (`performance/`)
- Concurrent deal processing tests
- Load testing
- Stress testing
- Memory and CPU usage tests

### 5. Test Data (`data/`)
- Mock datasets
- Sample company profiles
- Demo scenarios

## Running Tests

### Backend Tests (Node.js)
```bash
cd backend
npm test                    # Run all tests
npm run test:watch         # Watch mode
npm run test:unit          # Unit tests only
npm run test:integration   # Integration tests only
npm run test:e2e          # End-to-end tests only
npm run test:performance  # Performance tests only
```

### Agent Tests (Python)
```bash
cd agents
python -m pytest tests/                    # Run all tests
python -m pytest tests/unit/              # Unit tests only
python -m pytest tests/integration/       # Integration tests only
python -m pytest tests/e2e/              # End-to-end tests only
python -m pytest tests/performance/      # Performance tests only
```

### Frontend Tests (Next.js)
```bash
cd frontend
npm test                    # Run all tests
npm run test:watch         # Watch mode
npm run test:e2e          # End-to-end tests only
```

## Test Coverage Requirements

- **Unit Tests**: 80% code coverage minimum
- **Integration Tests**: All critical workflows covered
- **End-to-End Tests**: All user scenarios covered
- **Performance Tests**: All concurrent processing scenarios tested

## Test Data Management

All test data is synthetic and does not contain real company information or sensitive data.