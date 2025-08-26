-- Analytics Views for Superset Integration
-- These views provide pre-aggregated and joined data for better dashboard performance

-- Deal overview with company information
CREATE OR REPLACE VIEW deals_overview AS
SELECT 
    d.id as deal_id,
    d.name as deal_name,
    d.status,
    d.deal_value,
    d.currency,
    d.priority,
    d.created_at as deal_created_at,
    d.estimated_completion_date,
    d.actual_completion_date,
    acquirer.name as acquirer_name,
    acquirer.industry as acquirer_industry,
    acquirer.company_size as acquirer_size,
    target.name as target_name,
    target.industry as target_industry,
    target.company_size as target_size,
    CASE 
        WHEN d.actual_completion_date IS NOT NULL THEN 'Completed'
        WHEN d.estimated_completion_date < CURRENT_DATE THEN 'Overdue'
        WHEN d.estimated_completion_date <= CURRENT_DATE + INTERVAL '30 days' THEN 'Due Soon'
        ELSE 'On Track'
    END as timeline_status
FROM deals d
LEFT JOIN companies acquirer ON d.acquirer_id = acquirer.id
LEFT JOIN companies target ON d.target_id = target.id;

-- Agent performance metrics
CREATE OR REPLACE VIEW agent_performance AS
SELECT 
    ae.agent_type,
    ae.agent_id,
    COUNT(*) as total_executions,
    COUNT(CASE WHEN ae.status = 'completed' THEN 1 END) as successful_executions,
    COUNT(CASE WHEN ae.status = 'failed' THEN 1 END) as failed_executions,
    ROUND(
        COUNT(CASE WHEN ae.status = 'completed' THEN 1 END)::numeric / 
        NULLIF(COUNT(*), 0) * 100, 2
    ) as success_rate,
    AVG(ae.duration_seconds) as avg_duration_seconds,
    MIN(ae.duration_seconds) as min_duration_seconds,
    MAX(ae.duration_seconds) as max_duration_seconds,
    AVG(ae.progress_percentage) as avg_progress,
    DATE_TRUNC('day', ae.start_time) as execution_date
FROM agent_executions ae
WHERE ae.start_time IS NOT NULL
GROUP BY ae.agent_type, ae.agent_id, DATE_TRUNC('day', ae.start_time);

-- Risk assessment summary
CREATE OR REPLACE VIEW risk_assessment_summary AS
SELECT 
    d.id as deal_id,
    d.name as deal_name,
    f.category as risk_category,
    f.severity,
    COUNT(*) as finding_count,
    AVG(f.confidence_score) as avg_confidence,
    STRING_AGG(DISTINCT f.title, '; ') as finding_titles,
    MAX(f.created_at) as latest_finding_date
FROM deals d
LEFT JOIN findings f ON d.id = f.deal_id
GROUP BY d.id, d.name, f.category, f.severity;

-- Financial metrics comparison
CREATE OR REPLACE VIEW financial_metrics_comparison AS
SELECT 
    c.id as company_id,
    c.name as company_name,
    c.industry,
    c.company_size,
    fd.fiscal_year,
    fd.fiscal_quarter,
    fd.revenue,
    fd.net_income,
    fd.total_assets,
    fd.total_liabilities,
    fd.shareholders_equity,
    fd.cash_and_equivalents,
    fd.total_debt,
    fd.operating_cash_flow,
    fd.free_cash_flow,
    fd.gross_margin,
    fd.operating_margin,
    fd.net_margin,
    fd.roe,
    fd.roa,
    fd.debt_to_equity,
    fd.current_ratio,
    fd.quick_ratio,
    -- Calculate year-over-year growth
    LAG(fd.revenue) OVER (PARTITION BY c.id ORDER BY fd.fiscal_year, fd.fiscal_quarter) as prev_revenue,
    CASE 
        WHEN LAG(fd.revenue) OVER (PARTITION BY c.id ORDER BY fd.fiscal_year, fd.fiscal_quarter) > 0 
        THEN ROUND(
            ((fd.revenue - LAG(fd.revenue) OVER (PARTITION BY c.id ORDER BY fd.fiscal_year, fd.fiscal_quarter)) / 
             LAG(fd.revenue) OVER (PARTITION BY c.id ORDER BY fd.fiscal_year, fd.fiscal_quarter)) * 100, 2
        )
        ELSE NULL
    END as revenue_growth_rate
FROM companies c
LEFT JOIN financial_data fd ON c.id = fd.company_id;

-- Deal timeline analysis
CREATE OR REPLACE VIEW deal_timeline_analysis AS
SELECT 
    d.id as deal_id,
    d.name as deal_name,
    d.status,
    te.total_estimated_hours,
    te.estimated_completion_date,
    te.confidence_level,
    d.created_at as deal_start_date,
    EXTRACT(DAYS FROM (te.estimated_completion_date - d.created_at)) as estimated_duration_days,
    CASE 
        WHEN d.actual_completion_date IS NOT NULL 
        THEN EXTRACT(DAYS FROM (d.actual_completion_date - d.created_at))
        ELSE NULL
    END as actual_duration_days,
    -- Calculate agent execution statistics
    COUNT(ae.id) as total_agent_tasks,
    COUNT(CASE WHEN ae.status = 'completed' THEN 1 END) as completed_tasks,
    COUNT(CASE WHEN ae.status = 'running' THEN 1 END) as running_tasks,
    COUNT(CASE WHEN ae.status = 'pending' THEN 1 END) as pending_tasks,
    COUNT(CASE WHEN ae.status = 'failed' THEN 1 END) as failed_tasks,
    ROUND(
        COUNT(CASE WHEN ae.status = 'completed' THEN 1 END)::numeric / 
        NULLIF(COUNT(ae.id), 0) * 100, 2
    ) as completion_percentage
FROM deals d
LEFT JOIN timeline_estimates te ON d.id = te.deal_id
LEFT JOIN agent_executions ae ON d.id = ae.deal_id
GROUP BY d.id, d.name, d.status, te.total_estimated_hours, te.estimated_completion_date, 
         te.confidence_level, d.created_at, d.actual_completion_date;

-- Industry benchmarking view
CREATE OR REPLACE VIEW industry_benchmarks AS
SELECT 
    c.industry,
    COUNT(DISTINCT c.id) as company_count,
    AVG(c.annual_revenue) as avg_annual_revenue,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY c.annual_revenue) as median_annual_revenue,
    AVG(c.employee_count) as avg_employee_count,
    AVG(c.market_cap) as avg_market_cap,
    -- Financial ratios averages
    AVG(fd.gross_margin) as avg_gross_margin,
    AVG(fd.operating_margin) as avg_operating_margin,
    AVG(fd.net_margin) as avg_net_margin,
    AVG(fd.roe) as avg_roe,
    AVG(fd.roa) as avg_roa,
    AVG(fd.debt_to_equity) as avg_debt_to_equity,
    AVG(fd.current_ratio) as avg_current_ratio,
    -- Deal activity
    COUNT(DISTINCT d.id) as total_deals,
    AVG(d.deal_value) as avg_deal_value,
    COUNT(CASE WHEN d.status = 'completed' THEN 1 END) as completed_deals
FROM companies c
LEFT JOIN financial_data fd ON c.id = fd.company_id
LEFT JOIN deals d ON (c.id = d.acquirer_id OR c.id = d.target_id)
WHERE c.industry IS NOT NULL
GROUP BY c.industry;

-- Executive summary metrics
CREATE OR REPLACE VIEW executive_summary AS
SELECT 
    -- Deal metrics
    COUNT(DISTINCT d.id) as total_deals,
    COUNT(CASE WHEN d.status = 'active' THEN 1 END) as active_deals,
    COUNT(CASE WHEN d.status = 'completed' THEN 1 END) as completed_deals,
    SUM(d.deal_value) as total_deal_value,
    AVG(d.deal_value) as avg_deal_value,
    
    -- Risk metrics
    COUNT(DISTINCT f.id) as total_findings,
    COUNT(CASE WHEN f.severity = 'critical' THEN 1 END) as critical_findings,
    COUNT(CASE WHEN f.severity = 'high' THEN 1 END) as high_risk_findings,
    
    -- Agent performance
    COUNT(DISTINCT ae.id) as total_agent_executions,
    COUNT(CASE WHEN ae.status = 'completed' THEN 1 END) as successful_executions,
    ROUND(
        COUNT(CASE WHEN ae.status = 'completed' THEN 1 END)::numeric / 
        NULLIF(COUNT(ae.id), 0) * 100, 2
    ) as overall_success_rate,
    
    -- Timeline metrics
    AVG(te.total_estimated_hours) as avg_estimated_hours,
    COUNT(CASE WHEN te.estimated_completion_date < CURRENT_DATE AND d.status != 'completed' THEN 1 END) as overdue_deals,
    
    -- Data freshness
    MAX(d.updated_at) as last_deal_update,
    MAX(f.created_at) as last_finding_created,
    MAX(ae.end_time) as last_agent_execution
FROM deals d
LEFT JOIN findings f ON d.id = f.deal_id
LEFT JOIN agent_executions ae ON d.id = ae.deal_id
LEFT JOIN timeline_estimates te ON d.id = te.deal_id;

-- Grant permissions to superset user (if different from aman_user)
GRANT SELECT ON ALL TABLES IN SCHEMA public TO aman_user;
GRANT SELECT ON deals_overview TO aman_user;
GRANT SELECT ON agent_performance TO aman_user;
GRANT SELECT ON risk_assessment_summary TO aman_user;
GRANT SELECT ON financial_metrics_comparison TO aman_user;
GRANT SELECT ON deal_timeline_analysis TO aman_user;
GRANT SELECT ON industry_benchmarks TO aman_user;
GRANT SELECT ON executive_summary TO aman_user;