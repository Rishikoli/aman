# AMAN Superset Integration

This directory contains the Apache Superset configuration and setup scripts for the Autonomous M&A Navigator (AMAN) advanced analytics platform.

## Overview

Apache Superset provides advanced data visualization and business intelligence capabilities for AMAN, enabling:

- Executive dashboards with M&A-specific metrics
- Interactive data exploration and drill-down capabilities
- Advanced charting and visualization options
- Automated report generation and export
- Real-time data analysis and monitoring

## Files Structure

```
docker/superset/
├── superset_config.py          # Main Superset configuration
├── entrypoint.sh              # Docker entrypoint script
├── init_superset.sh           # Superset initialization script
├── setup_aman_dashboards.py   # Automated dashboard setup
├── test_superset_integration.py # Integration test script
├── requirements.txt           # Python dependencies
├── sql/
│   └── create_analytics_views.sql # Database views for analytics
├── dashboards/
│   └── ma_executive_dashboard.json # Dashboard configuration
└── README.md                  # This file
```

## Quick Start

1. **Start the services:**
   ```bash
   docker-compose up -d superset
   ```

2. **Wait for initialization:**
   The first startup takes 2-3 minutes as Superset initializes its database and creates the admin user.

3. **Access Superset:**
   - URL: http://localhost:8088
   - Username: `admin`
   - Password: `admin123`

4. **Test the integration:**
   ```bash
   python docker/superset/test_superset_integration.py
   ```

## Features

### Pre-configured Analytics Views

The integration automatically creates several database views optimized for analytics:

- **deals_overview**: Complete deal information with company details
- **agent_performance**: Agent execution metrics and success rates
- **risk_assessment_summary**: Risk findings aggregated by category and severity
- **financial_metrics_comparison**: Financial data with growth calculations
- **deal_timeline_analysis**: Timeline tracking and completion metrics
- **industry_benchmarks**: Industry-wide performance comparisons
- **executive_summary**: High-level KPIs and metrics

### Dashboard Components

The AMAN Executive Dashboard includes:

1. **Deal Pipeline Overview**: Status distribution and progress tracking
2. **Deal Value by Industry**: Industry-wise deal value analysis
3. **Risk Assessment Heatmap**: Risk findings by category and severity
4. **Agent Performance Timeline**: Agent execution success rates over time
5. **Financial Metrics Comparison**: Company financial performance comparison
6. **Deal Completion Forecast**: Timeline predictions and bottleneck analysis

### Advanced Features

- **Cross-filtering**: Interactive filtering across dashboard components
- **Drill-down capabilities**: Click through from summary to detailed views
- **Real-time updates**: Automatic data refresh every 5 minutes
- **Export functionality**: Export charts and data to various formats
- **SQL Lab**: Direct SQL query interface for ad-hoc analysis

## Configuration

### Database Connection

Superset is configured to connect to the AMAN PostgreSQL database:
- Host: `postgres` (Docker service name)
- Database: `aman_db`
- User: `aman_user`
- Password: `aman_password`

### Caching

Redis is used for caching to improve performance:
- Cache timeout: 300 seconds (5 minutes)
- Results backend: Redis database 1
- Celery broker: Redis database 0

### Security

- CSRF protection enabled
- CORS configured for frontend integration
- Custom security manager can be implemented if needed

## Manual Setup (if automated setup fails)

1. **Create Database Connection:**
   - Go to Data → Databases
   - Click "+ Database"
   - Select PostgreSQL
   - Enter connection details:
     ```
     Host: postgres
     Port: 5432
     Database: aman_db
     Username: aman_user
     Password: aman_password
     ```

2. **Add Datasets:**
   - Go to Data → Datasets
   - Click "+ Dataset"
   - Select the AMAN database
   - Add tables: `deals_overview`, `agent_performance`, etc.

3. **Create Charts:**
   - Go to Charts
   - Click "+ Chart"
   - Select dataset and visualization type
   - Configure metrics and dimensions

4. **Build Dashboard:**
   - Go to Dashboards
   - Click "+ Dashboard"
   - Add charts and arrange layout
   - Configure filters and interactions

## Troubleshooting

### Common Issues

1. **Superset won't start:**
   - Check if PostgreSQL is running: `docker-compose ps postgres`
   - Check logs: `docker-compose logs superset`
   - Ensure port 8088 is not in use

2. **Database connection fails:**
   - Verify PostgreSQL credentials in `superset_config.py`
   - Check network connectivity between containers
   - Ensure AMAN database exists and is accessible

3. **Charts not loading:**
   - Check dataset permissions
   - Verify SQL queries in SQL Lab
   - Check browser console for JavaScript errors

4. **Performance issues:**
   - Increase cache timeout in configuration
   - Add database indexes for frequently queried columns
   - Consider using database connection pooling

### Logs and Debugging

- **Superset logs:** `docker-compose logs superset`
- **Database logs:** `docker-compose logs postgres`
- **Application logs:** Check `/app/superset_home/superset.log` in container

### Performance Optimization

1. **Database Indexes:**
   The analytics views are optimized with appropriate indexes. Additional indexes may be needed based on usage patterns.

2. **Caching:**
   - Increase cache timeout for stable data
   - Use Redis clustering for high-load scenarios
   - Implement query result caching

3. **Query Optimization:**
   - Use materialized views for complex aggregations
   - Implement data partitioning for large tables
   - Consider read replicas for analytics workloads

## API Integration

Superset provides REST APIs that can be integrated with the AMAN frontend:

- **Charts API:** `/api/v1/chart/`
- **Dashboards API:** `/api/v1/dashboard/`
- **Datasets API:** `/api/v1/dataset/`

Example integration in React:
```javascript
// Embed Superset dashboard in AMAN frontend
const SupersetDashboard = ({ dashboardId }) => {
  return (
    <iframe
      src={`http://localhost:8088/superset/dashboard/${dashboardId}/?standalone=true`}
      width="100%"
      height="600px"
      frameBorder="0"
    />
  );
};
```

## Security Considerations

- Change default admin password in production
- Configure proper authentication (LDAP, OAuth, etc.)
- Implement row-level security if needed
- Use HTTPS in production environments
- Regular security updates and patches

## Backup and Recovery

- **Database backup:** Superset metadata is stored in SQLite by default
- **Configuration backup:** Backup `superset_config.py` and custom files
- **Dashboard export:** Use Superset's export functionality for dashboards

## Support and Resources

- [Apache Superset Documentation](https://superset.apache.org/)
- [Superset GitHub Repository](https://github.com/apache/superset)
- [AMAN Project Documentation](../../README.md)

For AMAN-specific issues, check the main project documentation or create an issue in the project repository.