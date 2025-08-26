# AMAN Superset Startup Guide

## Quick Start

To start the Superset analytics dashboard:

### 1. Start the Services
```bash
# Start all services including Superset
docker-compose up -d

# Or start just Superset (requires postgres and redis to be running)
docker-compose up -d superset
```

### 2. Wait for Initialization
Superset takes 2-3 minutes to initialize on first startup. You can monitor the progress:

```bash
# Watch the logs
docker-compose logs -f superset

# Check if Superset is ready
curl http://localhost:8088/health
```

### 3. Access Superset
Once ready, access Superset at:
- **URL:** http://localhost:8088
- **Username:** admin
- **Password:** admin123

### 4. Test the Integration
Run the integration test to verify everything is working:

```bash
# Run the test script
python docker/superset/test_complete_integration.py
```

## Available Dashboards

After successful setup, you'll have access to:

1. **Executive Dashboard**
   - URL: http://localhost:8088/superset/dashboard/aman-executive-dashboard/
   - High-level KPIs and summary metrics

2. **Comprehensive M&A Analysis**
   - URL: http://localhost:8088/superset/dashboard/comprehensive-ma-analysis/
   - Detailed operational analytics

3. **Scenario Modeling Dashboard**
   - URL: http://localhost:8088/superset/dashboard/ma-scenario-modeling/
   - What-if analysis and scenario planning

## Troubleshooting

### Common Issues

1. **Superset won't start:**
   ```bash
   # Check if postgres is running
   docker-compose ps postgres
   
   # Check Superset logs
   docker-compose logs superset
   ```

2. **Port 8088 already in use:**
   ```bash
   # Check what's using the port
   netstat -tulpn | grep 8088
   
   # Stop the conflicting service or change the port in docker-compose.yml
   ```

3. **Database connection issues:**
   ```bash
   # Restart the services in order
   docker-compose down
   docker-compose up -d postgres redis
   # Wait 30 seconds
   docker-compose up -d superset
   ```

### Reset Superset
If you need to reset Superset completely:

```bash
# Stop and remove containers
docker-compose down

# Remove Superset data volume
docker volume rm aman_superset_data

# Start fresh
docker-compose up -d
```

## Next Steps

1. **Explore the dashboards** - Click around and interact with the visualizations
2. **Create custom charts** - Use SQL Lab to create your own visualizations
3. **Set up automated reports** - Configure email reports for stakeholders
4. **Integrate with frontend** - Embed dashboards in the AMAN web interface

## Support

If you encounter issues:
1. Check the logs: `docker-compose logs superset`
2. Run the test script: `python docker/superset/test_complete_integration.py`
3. Review the troubleshooting section in README.md
4. Create an issue in the project repository