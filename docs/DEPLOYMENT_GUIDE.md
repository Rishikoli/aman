# Production Deployment Guide

## Prerequisites
- Docker and Docker Compose installed
- SSL certificates (for HTTPS)
- Domain name configured
- Required API keys

## Quick Start

1. **Configure Environment**
   ```bash
   cp .env.prod.example .env.prod
   # Edit .env.prod with your production values
   ```

2. **Deploy**
   ```bash
   chmod +x scripts/deploy.sh
   ./scripts/deploy.sh
   ```

## Services
- **Frontend**: Port 3000 (via Nginx 80/443)
- **Backend API**: Port 3001 (internal)
- **Superset**: Port 8088 (via Nginx /superset)
- **Grafana**: Port 3003
- **Prometheus**: Port 9090 (internal)

## Monitoring
- Health checks: `https://your-domain.com/health`
- Metrics: `https://your-domain.com:3003` (Grafana)
- Logs: `docker-compose -f docker-compose.prod.yml logs -f`

## Backup
Database backups are stored in `./backups/` directory.

## Security
- All services run as non-root users
- SSL/TLS encryption enabled
- Rate limiting configured
- Security headers applied