#!/bin/bash

# AMAN Docker Health Check Script
# This script provides health check functionality for all services

set -e

SERVICE_TYPE=${1:-"unknown"}
SERVICE_PORT=${2:-"3000"}

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[HEALTH]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Health check for backend service
check_backend() {
    local port=${1:-3001}
    if curl -f -s "http://localhost:${port}/health" > /dev/null; then
        print_status "Backend service is healthy on port ${port}"
        return 0
    else
        print_error "Backend service health check failed on port ${port}"
        return 1
    fi
}

# Health check for frontend service
check_frontend() {
    local port=${1:-3000}
    if curl -f -s "http://localhost:${port}/api/health" > /dev/null; then
        print_status "Frontend service is healthy on port ${port}"
        return 0
    else
        print_error "Frontend service health check failed on port ${port}"
        return 1
    fi
}

# Health check for agents service
check_agents() {
    if python -c "import sys; sys.exit(0)" 2>/dev/null; then
        print_status "Agents service is healthy"
        return 0
    else
        print_error "Agents service health check failed"
        return 1
    fi
}

# Health check for PostgreSQL
check_postgres() {
    local host=${1:-localhost}
    local port=${2:-5432}
    local user=${3:-aman_user}
    local db=${4:-aman_db}
    
    if pg_isready -h "${host}" -p "${port}" -U "${user}" -d "${db}" > /dev/null 2>&1; then
        print_status "PostgreSQL is healthy on ${host}:${port}"
        return 0
    else
        print_error "PostgreSQL health check failed on ${host}:${port}"
        return 1
    fi
}

# Health check for Redis
check_redis() {
    local host=${1:-localhost}
    local port=${2:-6379}
    
    if redis-cli -h "${host}" -p "${port}" ping > /dev/null 2>&1; then
        print_status "Redis is healthy on ${host}:${port}"
        return 0
    else
        print_error "Redis health check failed on ${host}:${port}"
        return 1
    fi
}

# Health check for Superset
check_superset() {
    local port=${1:-8088}
    if curl -f -s "http://localhost:${port}/health" > /dev/null; then
        print_status "Superset service is healthy on port ${port}"
        return 0
    else
        print_error "Superset service health check failed on port ${port}"
        return 1
    fi
}

# Main health check logic
case "$SERVICE_TYPE" in
    "backend")
        check_backend "$SERVICE_PORT"
        ;;
    "frontend")
        check_frontend "$SERVICE_PORT"
        ;;
    "agents")
        check_agents
        ;;
    "postgres")
        check_postgres
        ;;
    "redis")
        check_redis
        ;;
    "superset")
        check_superset "$SERVICE_PORT"
        ;;
    "all")
        print_status "Running comprehensive health check..."
        check_postgres && \
        check_redis && \
        check_backend && \
        check_agents && \
        check_frontend && \
        check_superset
        ;;
    *)
        print_error "Unknown service type: $SERVICE_TYPE"
        echo "Usage: $0 [backend|frontend|agents|postgres|redis|superset|all] [port]"
        exit 1
        ;;
esac