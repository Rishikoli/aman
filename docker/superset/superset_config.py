# Superset configuration for AMAN
import os

# Database configuration
SQLALCHEMY_DATABASE_URI = os.getenv(
    'DATABASE_URL',
    'postgresql://aman_user:aman_password@postgres:5432/aman_db'
)

# Redis configuration for caching
REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)
REDIS_CELERY_DB = 0
REDIS_RESULTS_DB = 1

# Cache configuration
CACHE_CONFIG = {
    'CACHE_TYPE': 'redis',
    'CACHE_DEFAULT_TIMEOUT': 300,
    'CACHE_KEY_PREFIX': 'superset_',
    'CACHE_REDIS_HOST': REDIS_HOST,
    'CACHE_REDIS_PORT': REDIS_PORT,
    'CACHE_REDIS_DB': 1,
}

# Celery configuration
class CeleryConfig:
    BROKER_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_CELERY_DB}'
    CELERY_IMPORTS = ('superset.sql_lab',)
    CELERY_RESULT_BACKEND = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_RESULTS_DB}'
    CELERYD_LOG_LEVEL = 'DEBUG'
    CELERYD_PREFETCH_MULTIPLIER = 1
    CELERY_ACKS_LATE = False

CELERY_CONFIG = CeleryConfig

# Security
SECRET_KEY = os.getenv('SUPERSET_SECRET_KEY', 'aman_superset_secret_key')
WTF_CSRF_ENABLED = True

# Feature flags
FEATURE_FLAGS = {
    'ENABLE_TEMPLATE_PROCESSING': True,
    'DASHBOARD_NATIVE_FILTERS': True,
    'DASHBOARD_CROSS_FILTERS': True,
    'GLOBAL_ASYNC_QUERIES': True,
}

# Custom roles and permissions for AMAN
CUSTOM_SECURITY_MANAGER = None

# Email configuration (optional)
SMTP_HOST = os.getenv('SMTP_HOST', 'localhost')
SMTP_STARTTLS = True
SMTP_SSL = False
SMTP_USER = os.getenv('SMTP_USER', '')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')
SMTP_MAIL_FROM = os.getenv('SMTP_MAIL_FROM', 'superset@aman.local')

# Logging
ENABLE_TIME_ROTATE = True
TIME_ROTATE_LOG_LEVEL = 'INFO'
FILENAME = os.path.join(os.path.expanduser('~'), 'superset.log')

# CORS settings for frontend integration
ENABLE_CORS = True
CORS_OPTIONS = {
    'supports_credentials': True,
    'allow_headers': ['*'],
    'resources': ['*'],
    'origins': ['http://localhost:3000', 'http://frontend:3000']
}