"""
Pytest configuration and shared fixtures for AMAN test suite
"""
import pytest
import os
import sys
import tempfile
import shutil
from unittest.mock import Mock, patch
import asyncio
from datetime import datetime, timedelta

# Add agents directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'agents'))

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

@pytest.fixture
def mock_env_vars():
    """Mock environment variables for testing"""
    env_vars = {
        'DATABASE_URL': 'postgresql://test:test@localhost:5432/test_aman',
        'REDIS_URL': 'redis://localhost:6379/1',
        'GEMINI_API_KEY': 'test_gemini_key',
        'FMP_API_KEY': 'test_fmp_key',
        'NEWS_API_KEY': 'test_news_key',
        'ENVIRONMENT': 'test'
    }
    
    with patch.dict(os.environ, env_vars):
        yield env_vars

@pytest.fixture
def sample_company_data():
    """Sample company data for testing"""
    return {
        'id': 'test-company-1',
        'name': 'Test Corp',
        'ticker': 'TEST',
        'industry': 'Technology',
        'market_cap': 1000000000,
        'employees': 5000,
        'founded': 2010,
        'headquarters': 'San Francisco, CA',
        'financials': {
            'revenue': 500000000,
            'net_income': 50000000,
            'total_assets': 800000000,
            'total_debt': 200000000,
            'cash': 100000000
        }
    }

@pytest.fixture
def sample_deal_data():
    """Sample M&A deal data for testing"""
    return {
        'id': 'test-deal-1',
        'name': 'Test Acquisition',
        'acquirer': 'Acquirer Corp',
        'target': 'Target Corp',
        'deal_value': 2000000000,
        'status': 'in_progress',
        'created_at': datetime.now().isoformat(),
        'estimated_completion': (datetime.now() + timedelta(days=90)).isoformat()
    }

@pytest.fixture
def mock_database():
    """Mock database connection"""
    mock_db = Mock()
    mock_db.execute.return_value = Mock()
    mock_db.fetchone.return_value = None
    mock_db.fetchall.return_value = []
    return mock_db

@pytest.fixture
def mock_redis():
    """Mock Redis connection"""
    mock_redis = Mock()
    mock_redis.get.return_value = None
    mock_redis.set.return_value = True
    mock_redis.delete.return_value = True
    return mock_redis

@pytest.fixture
def mock_gemini_api():
    """Mock Gemini API responses"""
    mock_response = Mock()
    mock_response.text = "This is a mock AI response for testing purposes."
    
    with patch('google.generativeai.GenerativeModel') as mock_model:
        mock_instance = Mock()
        mock_instance.generate_content.return_value = mock_response
        mock_model.return_value = mock_instance
        yield mock_instance

@pytest.fixture
def mock_external_apis():
    """Mock all external API calls"""
    with patch('requests.get') as mock_get, \
         patch('requests.post') as mock_post:
        
        # Mock successful API responses
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'status': 'success', 'data': {}}
        mock_response.text = 'Mock response text'
        
        mock_get.return_value = mock_response
        mock_post.return_value = mock_response
        
        yield {
            'get': mock_get,
            'post': mock_post,
            'response': mock_response
        }

@pytest.fixture
def performance_timer():
    """Timer fixture for performance testing"""
    class Timer:
        def __init__(self):
            self.start_time = None
            self.end_time = None
        
        def start(self):
            self.start_time = datetime.now()
        
        def stop(self):
            self.end_time = datetime.now()
            return self.elapsed_seconds
        
        @property
        def elapsed_seconds(self):
            if self.start_time and self.end_time:
                return (self.end_time - self.start_time).total_seconds()
            return None
    
    return Timer()

# Test data cleanup
@pytest.fixture(autouse=True)
def cleanup_test_data():
    """Automatically cleanup test data after each test"""
    yield
    # Cleanup logic here if needed
    pass