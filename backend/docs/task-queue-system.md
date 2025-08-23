# Task Queue System Documentation

## Overview

The Task Queue System is a Redis-based message queue implementation using Bull Queue that manages the distribution and execution of agent tasks for M&A due diligence analysis. It provides task scheduling, dependency management, progress monitoring, and failure recovery.

## Architecture

### Components

1. **TaskQueueService** (`services/taskQueue.js`)
   - Main service managing all queue operations
   - Handles task distribution, dependency checking, and progress tracking
   - Manages Redis connections and Bull queues

2. **Queue Types**
   - **Orchestration Queue**: Manages high-level task distribution and dependency checking
   - **Agent Queues**: Separate queues for each agent type (finance, legal, synergy, reputation, operations)
   - **Timeline Queue**: Handles timeline updates and progress tracking

3. **API Routes** (`api/routes/taskQueue.js`)
   - RESTful endpoints for queue management and monitoring
   - Health checks and statistics endpoints

## Key Features

### Task Distribution
- Automatically distributes tasks based on agent dependencies
- Independent agents (finance, legal, reputation) start immediately
- Dependent agents (synergy, operations) wait for their dependencies

### Dependency Management
- **Finance Agent**: No dependencies
- **Legal Agent**: No dependencies  
- **Reputation Agent**: No dependencies
- **Synergy Agent**: Depends on Finance Agent
- **Operations Agent**: Depends on Finance and Legal Agents

### Progress Monitoring
- Real-time progress tracking for each agent execution
- Timeline updates with bottleneck identification
- Queue statistics and health monitoring

### Failure Recovery
- Automatic retry logic with exponential backoff
- Failed job retry capabilities
- Graceful error handling and logging

## API Endpoints

### Queue Statistics
```
GET /api/v1/task-queue/stats
```
Returns statistics for all queues including waiting, active, completed, and failed job counts.

### Task Distribution
```
POST /api/v1/task-queue/distribute/:dealId
```
Initiates task distribution for a specific deal.

### Retry Failed Jobs
```
POST /api/v1/task-queue/retry/:dealId
```
Retries all failed jobs for a specific deal.

### Cancel Jobs
```
DELETE /api/v1/task-queue/cancel/:dealId
```
Cancels all pending and active jobs for a specific deal.

### Execution Status
```
GET /api/v1/task-queue/executions/:dealId
```
Returns detailed execution status for all agents in a deal.

### Active Executions
```
GET /api/v1/task-queue/active-executions
```
Returns all currently active executions across all deals.

### Health Check
```
GET /api/v1/task-queue/health
```
Checks the health status of the task queue system.

### Cleanup
```
POST /api/v1/task-queue/cleanup
```
Cleans up old completed and failed jobs.

## Database Schema Updates

### New Tables

#### timeline_events
```sql
CREATE TABLE timeline_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    deal_id UUID REFERENCES deals(id) ON DELETE CASCADE,
    event_type VARCHAR(100) NOT NULL,
    event_data JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### Updated Tables

#### agent_executions
- Added `queued_at` field to track when jobs are queued
- Added 'queued' status to execution_status enum

## Configuration

### Environment Variables
```bash
# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=your_redis_password
REDIS_DB=0
```

### Queue Configuration
- **Default Job Options**: 
  - Remove completed jobs after 10 jobs
  - Remove failed jobs after 5 jobs
  - 2-3 retry attempts with exponential backoff
  - Priority-based processing

## Usage Examples

### Starting Task Distribution
```javascript
const taskQueue = require('./services/taskQueue');

// Distribute tasks for a deal
const result = await taskQueue.distributeTasks('deal-123');
console.log('Distribution result:', result);
```

### Monitoring Progress
```javascript
// Get queue statistics
const stats = await taskQueue.getQueueStats();
console.log('Queue stats:', stats);

// Get execution status for a deal
const executions = await AgentExecution.findByDealId('deal-123');
console.log('Executions:', executions);
```

### Handling Failures
```javascript
// Retry failed jobs
const retryResult = await taskQueue.retryFailedJobs('deal-123');
console.log('Retry result:', retryResult);

// Cancel all jobs for a deal
const cancelResult = await taskQueue.cancelDealJobs('deal-123');
console.log('Cancel result:', cancelResult);
```

## Integration with Deal Orchestrator

The Task Queue System is integrated with the Deal Orchestrator Service:

1. When a deal is created, the orchestrator creates agent execution records
2. The orchestrator calls `taskQueue.distributeTasks()` to start processing
3. Independent agents are queued immediately
4. Dependent agents are queued when their dependencies complete
5. Progress is tracked and timelines are updated in real-time

## Error Handling

### Retry Logic
- Jobs automatically retry with exponential backoff
- Maximum retry attempts configurable per queue
- Failed jobs can be manually retried via API

### Graceful Degradation
- System continues operating if some agents fail
- Failed agents don't block independent agents
- Comprehensive error logging and monitoring

### Recovery Procedures
1. Check queue health via `/health` endpoint
2. Review failed jobs and error messages
3. Retry failed jobs or restart specific agents
4. Monitor progress and adjust as needed

## Performance Considerations

### Scalability
- Horizontal scaling via multiple worker processes
- Redis clustering support for high availability
- Queue-specific concurrency limits

### Monitoring
- Real-time queue statistics
- Performance metrics tracking
- Bottleneck identification and alerting

### Optimization
- Job cleanup to prevent memory bloat
- Priority-based job processing
- Efficient dependency checking algorithms

## Testing

The system includes comprehensive unit tests covering:
- API endpoint functionality
- Error handling scenarios
- Queue statistics and monitoring
- Task distribution logic
- Health check operations

Run tests with:
```bash
npm test -- taskQueue.test.js
```

## Future Enhancements

1. **Advanced Scheduling**: Cron-based recurring jobs
2. **Load Balancing**: Intelligent agent workload distribution
3. **Metrics Dashboard**: Real-time monitoring interface
4. **Auto-scaling**: Dynamic worker scaling based on queue depth
5. **Dead Letter Queues**: Enhanced failure handling
6. **Job Prioritization**: Dynamic priority adjustment based on business rules