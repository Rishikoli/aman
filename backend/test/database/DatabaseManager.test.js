const { DatabaseManager, DatabaseError } = require('../../database/DatabaseManager');
const { ConfigValidator } = require('../../database/ConfigValidator');

// Mock pg module
jest.mock('pg', () => {
  const mockClient = {
    query: jest.fn(),
    release: jest.fn(),
    on: jest.fn()
  };

  const mockPool = {
    connect: jest.fn().mockResolvedValue(mockClient),
    query: jest.fn(),
    end: jest.fn().mockResolvedValue(),
    on: jest.fn(),
    totalCount: 5,
    idleCount: 3,
    waitingCount: 0
  };

  return {
    Pool: jest.fn().mockImplementation(() => mockPool),
    __mockPool: mockPool,
    __mockClient: mockClient
  };
});

// Mock env-config
jest.mock('../../utils/env-config', () => ({
  getConfig: jest.fn().mockReturnValue({
    database: {
      host: 'localhost',
      port: 5432,
      name: 'test_db',
      user: 'test_user',
      password: 'test_password'
    },
    logging: {
      level: 'info',
      file: './logs/test.log'
    }
  })
}));

const { Pool } = require('pg');

describe('DatabaseManager', () => {
  let databaseManager;
  let mockPool;
  let mockClient;

  beforeEach(() => {
    jest.clearAllMocks();
    
    // Get fresh mock instances
    const pg = require('pg');
    mockPool = pg.__mockPool;
    mockClient = pg.__mockClient;
    
    // Reset mock implementations
    mockClient.query = jest.fn().mockResolvedValue({ 
      rows: [{ 
        current_time: new Date(), 
        pg_version: 'PostgreSQL 14.0 on x86_64-pc-linux-gnu' 
      }], 
      rowCount: 1 
    });
    mockClient.release = jest.fn().mockImplementation(() => {});
    mockPool.connect = jest.fn().mockResolvedValue(mockClient);
    
    databaseManager = new DatabaseManager();
  });

  afterEach(async () => {
    if (databaseManager && databaseManager.isInitialized) {
      await databaseManager.shutdown();
    }
  });

  describe('Constructor', () => {
    it('should create instance with default configuration', () => {
      expect(databaseManager).toBeInstanceOf(DatabaseManager);
      expect(databaseManager.isInitialized).toBe(false);
      expect(databaseManager.pool).toBeNull();
    });

    it('should create instance with custom configuration', () => {
      const customConfig = {
        host: 'custom-host',
        port: 5433,
        database: 'custom_db',
        user: 'custom_user',
        password: 'custom_password',
        max: 10
      };

      const customManager = new DatabaseManager(customConfig);
      expect(customManager.config.host).toBe('custom-host');
      expect(customManager.config.max).toBe(10);
    });

    it('should throw error for invalid configuration', () => {
      expect(() => {
        new DatabaseManager({ host: '' }); // Invalid empty host
      }).toThrow(DatabaseError);
    });
  });

  describe('Configuration Validation', () => {
    it('should validate required configuration fields', () => {
      expect(() => {
        new DatabaseManager({
          // Missing required fields
          host: 'localhost'
        });
      }).toThrow(DatabaseError);
    });

    it('should validate numeric field ranges', () => {
      expect(() => {
        new DatabaseManager({
          host: 'localhost',
          port: 70000, // Invalid port
          database: 'test',
          user: 'test',
          password: 'test'
        });
      }).toThrow(DatabaseError);
    });

    it('should apply default values for optional fields', () => {
      const config = {
        host: 'localhost',
        port: 5432,
        database: 'test',
        user: 'test',
        password: 'test'
      };

      const manager = new DatabaseManager(config);
      expect(manager.config.max).toBe(20); // Default value
      expect(manager.config.min).toBe(5); // Default value
    });
  });

  describe('Initialization', () => {
    it('should initialize successfully with valid configuration', async () => {
      await databaseManager.initialize();
      
      expect(databaseManager.isInitialized).toBe(true);
      expect(Pool).toHaveBeenCalledWith(expect.objectContaining({
        host: 'localhost',
        port: 5432,
        database: 'test_db'
      }));
      expect(mockPool.connect).toHaveBeenCalled();
      expect(mockClient.query).toHaveBeenCalledWith('SELECT NOW() as current_time, version() as pg_version');
    });

    it('should not initialize twice', async () => {
      await databaseManager.initialize();
      const poolCreateCount = Pool.mock.calls.length;
      
      await databaseManager.initialize();
      expect(Pool.mock.calls.length).toBe(poolCreateCount); // Should not create another pool
    });

    it('should handle initialization failure', async () => {
      mockPool.connect.mockRejectedValueOnce(new Error('Connection failed'));
      
      await expect(databaseManager.initialize()).rejects.toThrow(DatabaseError);
      expect(databaseManager.isInitialized).toBe(false);
    });

    it('should emit initialized event on successful initialization', async () => {
      const initSpy = jest.fn();
      databaseManager.on('initialized', initSpy);
      
      await databaseManager.initialize();
      expect(initSpy).toHaveBeenCalled();
    });
  });

  describe('Connection Management', () => {
    beforeEach(async () => {
      await databaseManager.initialize();
    });

    it('should get connection from pool', async () => {
      const connection = await databaseManager.getConnection();
      
      expect(mockPool.connect).toHaveBeenCalled();
      expect(connection).toBeDefined();
      expect(typeof connection.query).toBe('function');
      expect(typeof connection.release).toBe('function');
    });

    it('should throw error when not initialized', async () => {
      const uninitializedManager = new DatabaseManager();
      
      await expect(uninitializedManager.getConnection()).rejects.toThrow(DatabaseError);
    });

    it('should handle connection timeout', async () => {
      mockPool.connect.mockImplementation(() => 
        new Promise(resolve => setTimeout(resolve, 2000))
      );
      
      await expect(
        databaseManager.getConnection({ timeout: 1000 })
      ).rejects.toThrow(DatabaseError);
    });

    it('should wrap client with enhanced functionality', async () => {
      const connection = await databaseManager.getConnection();
      
      // Test enhanced query method
      await connection.query('SELECT 1');
      expect(mockClient.query).toHaveBeenCalledWith('SELECT 1', []);
      
      // Test enhanced release method
      connection.release();
      expect(mockClient.release).toHaveBeenCalled();
    });
  });

  describe('Query Execution', () => {
    beforeEach(async () => {
      await databaseManager.initialize();
    });

    it('should execute query successfully', async () => {
      const expectedResult = { rows: [{ id: 1 }], rowCount: 1 };
      mockClient.query.mockResolvedValueOnce(expectedResult);
      
      const result = await databaseManager.query('SELECT * FROM users WHERE id = $1', [1]);
      
      expect(result).toEqual(expectedResult);
      expect(mockClient.query).toHaveBeenCalledWith('SELECT * FROM users WHERE id = $1', [1]);
    });

    it('should handle query errors', async () => {
      mockClient.query.mockRejectedValueOnce(new Error('Query failed'));
      
      await expect(
        databaseManager.query('INVALID SQL')
      ).rejects.toThrow(DatabaseError);
    });

    it('should log slow queries', async () => {
      // Mock a slow query
      mockClient.query.mockImplementation(() => 
        new Promise(resolve => 
          setTimeout(() => resolve({ rows: [], rowCount: 0 }), 1500)
        )
      );
      
      const slowQuerySpy = jest.fn();
      databaseManager.on('slowQuery', slowQuerySpy);
      
      await databaseManager.query('SELECT pg_sleep(1.5)');
      expect(slowQuerySpy).toHaveBeenCalled();
    });
  });

  describe('Retry Logic', () => {
    beforeEach(async () => {
      await databaseManager.initialize();
    });

    it('should retry retryable errors', async () => {
      const retryableError = new Error('Connection reset');
      retryableError.code = 'ECONNRESET';
      
      mockClient.query
        .mockRejectedValueOnce(retryableError)
        .mockRejectedValueOnce(retryableError)
        .mockResolvedValueOnce({ rows: [], rowCount: 0 });
      
      const result = await databaseManager.withRetry(async () => {
        const client = await databaseManager.getConnection();
        try {
          return await client.query('SELECT 1');
        } finally {
          client.release();
        }
      });
      
      expect(result).toBeDefined();
      expect(mockClient.query).toHaveBeenCalledTimes(3);
    });

    it('should not retry non-retryable errors', async () => {
      const nonRetryableError = new Error('Syntax error');
      mockClient.query.mockRejectedValueOnce(nonRetryableError);
      
      await expect(
        databaseManager.withRetry(async () => {
          const client = await databaseManager.getConnection();
          try {
            return await client.query('INVALID SQL');
          } finally {
            client.release();
          }
        })
      ).rejects.toThrow(DatabaseError);
      
      expect(mockClient.query).toHaveBeenCalledTimes(1);
    });

    it('should exhaust retry attempts', async () => {
      const retryableError = new Error('Connection timeout');
      retryableError.code = 'ETIMEDOUT';
      
      mockClient.query.mockRejectedValue(retryableError);
      
      await expect(
        databaseManager.withRetry(async () => {
          const client = await databaseManager.getConnection();
          try {
            return await client.query('SELECT 1');
          } finally {
            client.release();
          }
        }, { maxAttempts: 2 })
      ).rejects.toThrow(DatabaseError);
      
      expect(mockClient.query).toHaveBeenCalledTimes(2);
    });
  });

  describe('Transaction Management', () => {
    beforeEach(async () => {
      await databaseManager.initialize();
    });

    it('should execute transaction successfully', async () => {
      mockClient.query
        .mockResolvedValueOnce({ rows: [], rowCount: 0 }) // BEGIN
        .mockResolvedValueOnce({ rows: [{ id: 1 }], rowCount: 1 }) // INSERT
        .mockResolvedValueOnce({ rows: [], rowCount: 0 }); // COMMIT
      
      const result = await databaseManager.withTransaction(async (client) => {
        return await client.query('INSERT INTO users (name) VALUES ($1)', ['John']);
      });
      
      expect(result).toEqual({ rows: [{ id: 1 }], rowCount: 1 });
      expect(mockClient.query).toHaveBeenCalledWith('BEGIN');
      expect(mockClient.query).toHaveBeenCalledWith('COMMIT');
    });

    it('should rollback transaction on error', async () => {
      mockClient.query
        .mockResolvedValueOnce({ rows: [], rowCount: 0 }) // BEGIN
        .mockRejectedValueOnce(new Error('Constraint violation')) // INSERT
        .mockResolvedValueOnce({ rows: [], rowCount: 0 }); // ROLLBACK
      
      await expect(
        databaseManager.withTransaction(async (client) => {
          return await client.query('INSERT INTO users (name) VALUES ($1)', ['']);
        })
      ).rejects.toThrow(DatabaseError);
      
      expect(mockClient.query).toHaveBeenCalledWith('BEGIN');
      expect(mockClient.query).toHaveBeenCalledWith('ROLLBACK');
    });
  });

  describe('Health Check', () => {
    beforeEach(async () => {
      await databaseManager.initialize();
    });

    it('should return healthy status', async () => {
      mockClient.query.mockResolvedValueOnce({
        rows: [{ test: 1, current_time: new Date() }],
        rowCount: 1
      });
      
      const health = await databaseManager.healthCheck();
      
      expect(health.status).toBe('healthy');
      expect(health.checks.connectivity).toBe(true);
      expect(health.checks.queryExecution).toBe(true);
      expect(health.metrics).toBeDefined();
      expect(health.metrics.pool).toBeDefined();
    });

    it('should return unhealthy status on connection failure', async () => {
      mockPool.connect.mockRejectedValueOnce(new Error('Connection failed'));
      
      const health = await databaseManager.healthCheck();
      
      expect(health.status).toBe('unhealthy');
      expect(health.checks.connectivity).toBe(false);
      expect(health.error).toBeDefined();
    });
  });

  describe('Pool Metrics', () => {
    beforeEach(async () => {
      await databaseManager.initialize();
    });

    it('should return pool metrics', () => {
      const metrics = databaseManager.getPoolMetrics();
      
      expect(metrics).toEqual({
        totalCount: 5,
        idleCount: 3,
        waitingCount: 0,
        maxConnections: 20,
        minConnections: 5
      });
    });

    it('should return not initialized status when pool is null', () => {
      const uninitializedManager = new DatabaseManager();
      const metrics = uninitializedManager.getPoolMetrics();
      
      expect(metrics).toEqual({ status: 'not_initialized' });
    });
  });

  describe('Shutdown', () => {
    it('should shutdown gracefully', async () => {
      await databaseManager.initialize();
      
      const shutdownSpy = jest.fn();
      databaseManager.on('shutdown', shutdownSpy);
      
      await databaseManager.shutdown();
      
      expect(mockPool.end).toHaveBeenCalled();
      expect(databaseManager.isInitialized).toBe(false);
      expect(databaseManager.pool).toBeNull();
      expect(shutdownSpy).toHaveBeenCalled();
    });

    it('should handle shutdown when not initialized', async () => {
      await expect(databaseManager.shutdown()).resolves.not.toThrow();
    });

    it('should handle shutdown errors', async () => {
      await databaseManager.initialize();
      mockPool.end.mockRejectedValueOnce(new Error('Shutdown failed'));
      
      await expect(databaseManager.shutdown()).rejects.toThrow(DatabaseError);
    });
  });

  describe('Event Handling', () => {
    beforeEach(async () => {
      await databaseManager.initialize();
    });

    it('should handle pool error events', () => {
      const errorSpy = jest.fn();
      databaseManager.on('poolError', errorSpy);
      
      const error = new Error('Pool error');
      databaseManager._handlePoolError(error);
      
      expect(errorSpy).toHaveBeenCalledWith(error);
    });

    it('should handle client connect events', () => {
      const connectSpy = jest.fn();
      databaseManager.on('clientConnect', connectSpy);
      
      databaseManager._handlePoolConnect(mockClient);
      
      expect(connectSpy).toHaveBeenCalledWith(mockClient);
    });
  });
});

describe('DatabaseError', () => {
  it('should create error with code and message', () => {
    const error = new DatabaseError('TEST_ERROR', 'Test error message');
    
    expect(error.name).toBe('DatabaseError');
    expect(error.code).toBe('TEST_ERROR');
    expect(error.message).toBe('Test error message');
    expect(error.timestamp).toBeDefined();
  });

  it('should include original error', () => {
    const originalError = new Error('Original error');
    const error = new DatabaseError('TEST_ERROR', 'Test error', originalError);
    
    expect(error.originalError).toBe(originalError);
  });

  it('should serialize to JSON', () => {
    const originalError = new Error('Original error');
    originalError.code = 'ORIG_CODE';
    
    const error = new DatabaseError('TEST_ERROR', 'Test error', originalError);
    const json = error.toJSON();
    
    expect(json.name).toBe('DatabaseError');
    expect(json.code).toBe('TEST_ERROR');
    expect(json.message).toBe('Test error');
    expect(json.originalError.message).toBe('Original error');
    expect(json.originalError.code).toBe('ORIG_CODE');
  });
});