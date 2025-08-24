"""
Environment configuration and validation for Python agents
"""
import os
import logging
from typing import Dict, List, Tuple
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Required environment variables
REQUIRED_ENV_VARS = [
    'DATABASE_URL'
]

# Optional environment variables
OPTIONAL_ENV_VARS = [
    'FMP_API_KEY',

    'NEWS_API_KEY',
    'TWITTER_BEARER_TOKEN',
    'USPTO_API_KEY',
    'OPENCORPORATES_API_KEY',
    'GEMINI_API_KEY',
    'PYTHONPATH',
    'LOG_LEVEL',
    'AGENT_TIMEOUT',
    'MAX_CONCURRENT_TASKS',
    'RETRY_ATTEMPTS',
    'TEMP_DIR',
    'PROCESSING_DIR'
]

def validate_environment() -> Tuple[bool, List[str], List[str]]:
    """
    Validates that all required environment variables are present
    
    Returns:
        Tuple[bool, List[str], List[str]]: (success, missing_vars, warning_vars)
    """
    missing = []
    warnings = []
    
    # Check required variables
    for var_name in REQUIRED_ENV_VARS:
        if not os.getenv(var_name):
            missing.append(var_name)
    
    # Check optional variables and warn if missing
    for var_name in OPTIONAL_ENV_VARS:
        if not os.getenv(var_name):
            warnings.append(var_name)
    
    return len(missing) == 0, missing, warnings

def get_config() -> Dict:
    """
    Gets environment configuration with defaults
    
    Returns:
        Dict: Environment configuration object
        
    Raises:
        SystemExit: If required environment variables are missing
    """
    success, missing, warnings = validate_environment()
    
    if not success:
        logging.error(f"Missing required environment variables: {missing}")
        raise SystemExit(1)
    
    if warnings:
        logging.warning(f"Optional environment variables not set: {warnings}")
    
    return {
        # Database
        'database': {
            'url': os.getenv('DATABASE_URL')
        },
        
        # Redis Configuration
        'redis': {
            'url': os.getenv('REDIS_URL', 'redis://localhost:6379/0'),
            'decode_responses': True,
            'socket_timeout': 5,
            'socket_connect_timeout': 5,
            'retry_on_timeout': True
        },
        
        # API Keys
        'api_keys': {
            'fmp': os.getenv('FMP_API_KEY'),
        
            'news': os.getenv('NEWS_API_KEY'),
            'twitter': os.getenv('TWITTER_BEARER_TOKEN'),
            'uspto': os.getenv('USPTO_API_KEY'),
            'opencorporates': os.getenv('OPENCORPORATES_API_KEY'),
            'gemini': os.getenv('GEMINI_API_KEY')
        },
        
        # Python Environment
        'python': {
            'path': os.getenv('PYTHONPATH', '.'),
            'log_level': os.getenv('LOG_LEVEL', 'INFO')
        },
        
        # Agent Configuration
        'agent': {
            'timeout': int(os.getenv('AGENT_TIMEOUT', '300')),
            'max_concurrent_tasks': int(os.getenv('MAX_CONCURRENT_TASKS', '5')),
            'retry_attempts': int(os.getenv('RETRY_ATTEMPTS', '3'))
        },
        
        # File Processing
        'files': {
            'temp_dir': os.getenv('TEMP_DIR', './temp'),
            'processing_dir': os.getenv('PROCESSING_DIR', './processing')
        }
    }

# Initialize configuration
try:
    CONFIG = get_config()
    logging.basicConfig(level=getattr(logging, CONFIG['python']['log_level']))
except SystemExit:
    # Re-raise to exit the application
    raise
except Exception as e:
    logging.error(f"Failed to load configuration: {e}")
    raise SystemExit(1)