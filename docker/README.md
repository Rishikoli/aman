# AMAN Docker Configuration

This directory contains all Docker-related configuration files for the Autonomous M&A Navigator (AMAN) project.

## Quick Start

### Prerequisites
- Docker Desktop installed and running
- Docker Compose v2.0 or higher

### Development Environment
```bash
# Unix/Linux/macOS
./docker/docker-helper.sh dev

# Windows
docker\docker-helper.bat dev
```

### Production Environment
```bash
# Unix/Linux/macOS
./docker/docker-helper.sh prod

# Windows
docker\docker-helper.bat prod
```

## Services

### Core Services
- **PostgreSQL**: Primary database (port 5432)
- **Redis**: Cache and message queue (port 6379)
- **Backend**: Node.js API service (port 3001)
- **Agents**: Python AI agents service
- **Frontend**: Next.js web application (port 3000)
- **Superset**: Analytics dashboard (port 8088)

### Service URLs
- Frontend: http://localhost:3000
- Backend API: http://localhost:3001
- Superset: http://localhost:8088
- PostgreSQL: localhost:5432
- Redis: localhost:6379

## File Structure

```
docker/
├── README.md                 # This file
├── docker-helper.sh         # Unix helper script
├── docker-helper.bat        # Windows helper script
├── health-check.sh          # Health check utilities
├── validate-setup.sh        # Setup validation script
└── superset/
    └── superset_config.py   # Superset configuration
```

## Configuration Files

### Docker Compose Files
- `docker-compose.yml`: Base configuration
- `docker-compose.dev.yml`: Development overrides
- `docker-compose.prod.yml`: Production overrides

### Dockerfiles
- `backend/Dockerfile`: Production backend image
- `backend/Dockerfile.dev`: Development backend image
- `agents/Dockerfile`: Production agents image
- `agents/Dockerfile.dev`: Development agents image
- `frontend/Dockerfile`: Production frontend image
- `frontend/Dockerfile.dev`: Development frontend image

## Helper Scripts

### docker-helper.sh / docker-helper.bat
Convenient commands for managing the Docker environment:

```bash
./docker/docker-helper.sh [command]

Commands:
  dev       Start development environment
  prod      Start production environment
  stop      Stop all services
  restart   Restart all services
  logs      View logs (optionally specify service name)
  migrate   Run database migrations
  seed      Seed database with sample data
  cleanup   Remove all containers, networks, and volumes
  help      Show help message
```

### validate-setup.sh
Validates that all Docker configurations are properly set up:

```bash
./docker/validate-setup.sh
```

### health-check.sh
Health check utilities for all services:

```bash
./docker/health-check.sh [service] [port]

Services: backend, frontend, agents, postgres, redis, superset, all
```