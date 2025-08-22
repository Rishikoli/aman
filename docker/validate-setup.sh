#!/bin/bash

# AMAN Docker Setup Validation Script
# This script validates that all Docker configurations are properly set up

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Counters
PASSED=0
FAILED=0
WARNINGS=0

# Function to print colored output
print_header() {
    echo -e "${BLUE}=== $1 ===${NC}"
}

print_pass() {
    echo -e "${GREEN}✓${NC} $1"
    ((PASSED++))
}

print_fail() {
    echo -e "${RED}✗${NC} $1"
    ((FAILED++))
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
    ((WARNINGS++))
}

# Function to check if file exists
check_file() {
    local file=$1
    local description=$2
    
    if [ -f "$file" ]; then
        print_pass "$description exists: $file"
        return 0
    else
        print_fail "$description missing: $file"
        return 1
    fi
}

# Function to check if directory exists
check_directory() {
    local dir=$1
    local description=$2
    
    if [ -d "$dir" ]; then
        print_pass "$description exists: $dir"
        return 0
    else
        print_fail "$description missing: $dir"
        return 1
    fi
}

# Function to validate Docker Compose file
validate_compose_file() {
    local file=$1
    local description=$2
    
    if [ -f "$file" ]; then
        if docker-compose -f "$file" config > /dev/null 2>&1; then
            print_pass "$description is valid: $file"
            return 0
        else
            print_fail "$description has syntax errors: $file"
            return 1
        fi
    else
        print_fail "$description missing: $file"
        return 1
    fi
}

# Function to check Docker daemon
check_docker_daemon() {
    if docker info > /dev/null 2>&1; then
        print_pass "Docker daemon is running"
        return 0
    else
        print_fail "Docker daemon is not running"
        return 1
    fi
}

# Function to check Docker Compose
check_docker_compose() {
    if command -v docker-compose > /dev/null 2>&1; then
        local version=$(docker-compose --version | cut -d' ' -f3 | cut -d',' -f1)
        print_pass "Docker Compose is installed (version: $version)"
        return 0
    else
        print_fail "Docker Compose is not installed"
        return 1
    fi
}

# Main validation
print_header "AMAN Docker Setup Validation"
echo

print_header "Docker Environment"
check_docker_daemon
check_docker_compose
echo

print_header "Docker Compose Files"
validate_compose_file "docker-compose.yml" "Main Docker Compose file"
validate_compose_file "docker-compose.dev.yml" "Development Docker Compose file"
validate_compose_file "docker-compose.prod.yml" "Production Docker Compose file"
echo

print_header "Dockerfiles"
check_file "backend/Dockerfile" "Backend production Dockerfile"
check_file "backend/Dockerfile.dev" "Backend development Dockerfile"
check_file "agents/Dockerfile" "Agents production Dockerfile"
check_file "agents/Dockerfile.dev" "Agents development Dockerfile"
check_file "frontend/Dockerfile" "Frontend production Dockerfile"
check_file "frontend/Dockerfile.dev" "Frontend development Dockerfile"
echo

print_header "Docker Ignore Files"
check_file ".dockerignore" "Root .dockerignore"
check_file "backend/.dockerignore" "Backend .dockerignore"
check_file "agents/.dockerignore" "Agents .dockerignore"
check_file "frontend/.dockerignore" "Frontend .dockerignore"
echo

print_header "Configuration Files"
check_file "database/init/01-init.sql" "Database initialization script"
check_file "docker/superset/superset_config.py" "Superset configuration"
check_file "docker/docker-helper.sh" "Docker helper script (Unix)"
check_file "docker/docker-helper.bat" "Docker helper script (Windows)"
check_file "docker/health-check.sh" "Health check script"
echo

print_header "Required Directories"
check_directory "backend" "Backend directory"
check_directory "agents" "Agents directory"
check_directory "frontend" "Frontend directory"
check_directory "database/init" "Database initialization directory"
check_directory "docker/superset" "Superset configuration directory"
echo

print_header "Environment Files"
if check_file "backend/.env.example" "Backend environment example"; then
    if [ ! -f "backend/.env" ]; then
        print_warning "Backend .env file not found. Copy from .env.example and configure."
    else
        print_pass "Backend .env file exists"
    fi
fi

if check_file "agents/.env.example" "Agents environment example"; then
    if [ ! -f "agents/.env" ]; then
        print_warning "Agents .env file not found. Copy from .env.example and configure."
    else
        print_pass "Agents .env file exists"
    fi
fi

if check_file "frontend/.env.local" "Frontend environment file"; then
    print_pass "Frontend environment file exists"
fi
echo

print_header "Package Files"
check_file "backend/package.json" "Backend package.json"
check_file "agents/requirements.txt" "Agents requirements.txt"
check_file "frontend/package.json" "Frontend package.json"
echo

# Summary
print_header "Validation Summary"
echo -e "Passed: ${GREEN}$PASSED${NC}"
echo -e "Failed: ${RED}$FAILED${NC}"
echo -e "Warnings: ${YELLOW}$WARNINGS${NC}"
echo

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ Docker setup validation completed successfully!${NC}"
    echo -e "${GREEN}You can now run: ./docker/docker-helper.sh dev${NC}"
    exit 0
else
    echo -e "${RED}✗ Docker setup validation failed with $FAILED errors.${NC}"
    echo -e "${YELLOW}Please fix the issues above before proceeding.${NC}"
    exit 1
fi