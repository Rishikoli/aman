-- Scenario Modeling Views for Advanced Analytics
-- These views support what-if analysis and scenario modeling capabilities

-- Scenario analysis base view
CREATE OR REPLACE VIEW scenario_analysis_view AS
WITH scenario_parameters AS (
    SELECT 
        'Base Case' as scenario_name,
        1.0 as synergy_multiplier,
        1.0 as risk_multiplier,
        0.1 as discount_rate,
        CURRENT_DATE as scenario_date
    UNION ALL
    SELECT 
        'Optimistic' as scenario_name,
        1.2 as synergy_multiplier,
        0.8 as risk_multiplier,
        0.08 as discount_rate,
        CURRENT_DATE as scenario_date
    UNION ALL
    SELECT 
        'Pessimistic' as scenario_name,
        0.8 as synergy_multiplier,
        1.3 as risk_multiplier,
        0.12 as discount_rate,
        CURRENT_DATE as scenario_date
    UNION ALL
    SELECT 
        'Conservative' as scenario_name,
        0.9 as synergy_multiplier,
        1.1 as risk_multiplier,
        0.11 as discount_rate,
        CURRENT_DATE as scenario_date
)
SELECT 
    d.id as deal_id,
    d.name as deal_name,
    sp.scenario_name,
    sp.synergy_multiplier,
    sp.risk_multiplier,
    sp.discount_rate,
    sp.scenario_date,
    d.deal_value,
    d.deal_value * sp.synergy_multiplier as projected_deal_value,
    d.deal_value * sp.synergy_multiplier * (1 - (sp.risk_multiplier - 1) * 0.1) as risk_adjusted_value,
    -- Calculate NPV with scenario-specific discount rate
    d.deal_value * sp.synergy_multiplier / POWER(1 + sp.discount_rate, 3) as projected_npv
FROM deals d
CROSS JOIN scenario_parameters sp
WHERE d.deal_value IS NOT NULL;

-- Synergy breakdown view for waterfall charts
CREATE OR REPLACE VIEW synergy_breakdown_view AS
SELECT 
    d.id as deal_id,
    d.name as deal_name,
    'Cost Synergies' as synergy_type,
    COALESCE(d.deal_value * 0.15, 0) as estimated_value,
    'Personnel and operational cost reductions' as description
FROM deals d
WHERE d.deal_value IS NOT NULL
UNION ALL
SELECT 
    d.id as deal_id,
    d.name as deal_name,
    'Revenue Synergies' as synergy_type,
    COALESCE(d.deal_value * 0.08, 0) as estimated_value,
    'Cross-selling and market expansion opportunities' as description
FROM deals d
WHERE d.deal_value IS NOT NULL
UNION ALL
SELECT 
    d.id as deal_id,
    d.name as deal_name,
    'Tax Synergies' as synergy_type,
    COALESCE(d.deal_value * 0.03, 0) as estimated_value,
    'Tax optimization and structure benefits' as description
FROM deals d
WHERE d.deal_value IS NOT NULL
UNION ALL
SELECT 
    d.id as deal_id,
    d.name as deal_name,
    'Financial Synergies' as synergy_type,
    COALESCE(d.deal_value * 0.05, 0) as estimated_value,
    'Lower cost of capital and improved financing' as description
FROM deals d
WHERE d.deal_value IS NOT NULL;

-- Risk-adjusted metrics for bubble charts
CREATE OR REPLACE VIEW risk_adjusted_metrics AS
SELECT 
    d.id as deal_id,
    d.name as deal_name,
    d.deal_value,
    -- Calculate probability of success based on risk findings
    CASE 
        WHEN risk_stats.critical_count > 5 THEN 0.3
        WHEN risk_stats.critical_count > 2 THEN 0.5
        WHEN risk_stats.high_count > 10 THEN 0.6
        WHEN risk_stats.high_count > 5 THEN 0.7
        ELSE 0.8
    END as probability_of_success,
    -- Risk-adjusted NPV
    d.deal_value * 0.2 * 
    CASE 
        WHEN risk_stats.critical_count > 5 THEN 0.3
        WHEN risk_stats.critical_count > 2 THEN 0.5
        WHEN risk_stats.high_count > 10 THEN 0.6
        WHEN risk_stats.high_count > 5 THEN 0.7
        ELSE 0.8
    END as risk_adjusted_npv,
    risk_stats.total_findings,
    risk_stats.critical_count,
    risk_stats.high_count
FROM deals d
LEFT JOIN (
    SELECT 
        deal_id,
        COUNT(*) as total_findings,
        COUNT(CASE WHEN severity = 'critical' THEN 1 END) as critical_count,
        COUNT(CASE WHEN severity = 'high' THEN 1 END) as high_count
    FROM findings
    GROUP BY deal_id
) risk_stats ON d.id = risk_stats.deal_id
WHERE d.deal_value IS NOT NULL;

-- Monte Carlo simulation results (simulated data for demonstration)
CREATE OR REPLACE VIEW monte_carlo_results AS
WITH RECURSIVE simulation_data AS (
    SELECT 
        1 as simulation_id,
        d.id as deal_id,
        d.name as deal_name,
        d.deal_value * (0.8 + RANDOM() * 0.4) as simulated_outcome
    FROM deals d
    WHERE d.deal_value IS NOT NULL
    UNION ALL
    SELECT 
        simulation_id + 1,
        deal_id,
        deal_name,
        (SELECT deal_value FROM deals WHERE id = simulation_data.deal_id) * (0.8 + RANDOM() * 0.4)
    FROM simulation_data
    WHERE simulation_id < 1000
)
SELECT * FROM simulation_data;

-- Scenario comparison matrix
CREATE OR REPLACE VIEW scenario_comparison AS
WITH scenario_metrics AS (
    SELECT 
        scenario_name,
        'Deal Value' as metric_name,
        AVG(projected_deal_value) as metric_value
    FROM scenario_analysis_view
    GROUP BY scenario_name
    UNION ALL
    SELECT 
        scenario_name,
        'Risk-Adjusted Value' as metric_name,
        AVG(risk_adjusted_value) as metric_value
    FROM scenario_analysis_view
    GROUP BY scenario_name
    UNION ALL
    SELECT 
        scenario_name,
        'NPV' as metric_name,
        AVG(projected_npv) as metric_value
    FROM scenario_analysis_view
    GROUP BY scenario_name
),
normalized_metrics AS (
    SELECT 
        scenario_name,
        metric_name,
        metric_value,
        (metric_value - MIN(metric_value) OVER (PARTITION BY metric_name)) / 
        NULLIF(MAX(metric_value) OVER (PARTITION BY metric_name) - MIN(metric_value) OVER (PARTITION BY metric_name), 0) as normalized_value
    FROM scenario_metrics
)
SELECT * FROM normalized_metrics;

-- Break-even analysis view
CREATE OR REPLACE VIEW breakeven_analysis AS
WITH RECURSIVE cash_flow_projections AS (
    SELECT 
        d.id as deal_id,
        d.name as deal_name,
        CURRENT_DATE as projection_date,
        0 as period_number,
        -d.deal_value as period_cash_flow,
        -d.deal_value as cumulative_cash_flow
    FROM deals d
    WHERE d.deal_value IS NOT NULL
    UNION ALL
    SELECT 
        deal_id,
        deal_name,
        projection_date + INTERVAL '3 months',
        period_number + 1,
        (SELECT deal_value FROM deals WHERE id = cfp.deal_id) * 0.05 as period_cash_flow,
        cumulative_cash_flow + (SELECT deal_value FROM deals WHERE id = cfp.deal_id) * 0.05
    FROM cash_flow_projections cfp
    WHERE period_number < 20  -- 5 years of quarterly projections
)
SELECT * FROM cash_flow_projections;

-- Sensitivity analysis view
CREATE OR REPLACE VIEW sensitivity_analysis AS
SELECT 
    d.id as deal_id,
    d.name as deal_name,
    'Synergy Realization Rate' as variable_name,
    d.deal_value * 0.1 as impact_on_npv,
    'Impact of 10% change in synergy realization' as description
FROM deals d
WHERE d.deal_value IS NOT NULL
UNION ALL
SELECT 
    d.id as deal_id,
    d.name as deal_name,
    'Integration Costs' as variable_name,
    -d.deal_value * 0.05 as impact_on_npv,
    'Impact of 10% change in integration costs' as description
FROM deals d
WHERE d.deal_value IS NOT NULL
UNION ALL
SELECT 
    d.id as deal_id,
    d.name as deal_name,
    'Market Growth Rate' as variable_name,
    d.deal_value * 0.08 as impact_on_npv,
    'Impact of 1% change in market growth rate' as description
FROM deals d
WHERE d.deal_value IS NOT NULL
UNION ALL
SELECT 
    d.id as deal_id,
    d.name as deal_name,
    'Discount Rate' as variable_name,
    -d.deal_value * 0.12 as impact_on_npv,
    'Impact of 1% change in discount rate' as description
FROM deals d
WHERE d.deal_value IS NOT NULL
UNION ALL
SELECT 
    d.id as deal_id,
    d.name as deal_name,
    'Customer Retention' as variable_name,
    d.deal_value * 0.06 as impact_on_npv,
    'Impact of 5% change in customer retention' as description
FROM deals d
WHERE d.deal_value IS NOT NULL;

-- Probability distributions view
CREATE OR REPLACE VIEW probability_distributions AS
WITH outcome_ranges AS (
    SELECT 
        generate_series(0, 200, 5) as outcome_value
),
probability_calcs AS (
    SELECT 
        outcome_value,
        'Optimistic' as outcome_type,
        EXP(-0.5 * POWER((outcome_value - 120) / 20.0, 2)) / (20.0 * SQRT(2 * PI())) as probability_density
    FROM outcome_ranges
    UNION ALL
    SELECT 
        outcome_value,
        'Base Case' as outcome_type,
        EXP(-0.5 * POWER((outcome_value - 100) / 15.0, 2)) / (15.0 * SQRT(2 * PI())) as probability_density
    FROM outcome_ranges
    UNION ALL
    SELECT 
        outcome_value,
        'Pessimistic' as outcome_type,
        EXP(-0.5 * POWER((outcome_value - 80) / 25.0, 2)) / (25.0 * SQRT(2 * PI())) as probability_density
    FROM outcome_ranges
)
SELECT * FROM probability_calcs;

-- Decision tree nodes view
CREATE OR REPLACE VIEW decision_tree_nodes AS
SELECT 
    d.id as deal_id,
    d.name as deal_name,
    'Proceed → Success' as decision_path,
    'High Return' as outcome,
    d.deal_value * 0.3 as expected_value,
    0.6 as probability
FROM deals d
WHERE d.deal_value IS NOT NULL
UNION ALL
SELECT 
    d.id as deal_id,
    d.name as deal_name,
    'Proceed → Partial Success' as decision_path,
    'Moderate Return' as outcome,
    d.deal_value * 0.1 as expected_value,
    0.3 as probability
FROM deals d
WHERE d.deal_value IS NOT NULL
UNION ALL
SELECT 
    d.id as deal_id,
    d.name as deal_name,
    'Proceed → Failure' as decision_path,
    'Loss' as outcome,
    -d.deal_value * 0.2 as expected_value,
    0.1 as probability
FROM deals d
WHERE d.deal_value IS NOT NULL
UNION ALL
SELECT 
    d.id as deal_id,
    d.name as deal_name,
    'Do Not Proceed' as decision_path,
    'No Change' as outcome,
    0 as expected_value,
    1.0 as probability
FROM deals d
WHERE d.deal_value IS NOT NULL;

-- Real options analysis view
CREATE OR REPLACE VIEW real_options_analysis AS
WITH option_data AS (
    SELECT 
        d.id as deal_id,
        d.name as deal_name,
        CURRENT_DATE + (generate_series(0, 36) * INTERVAL '1 month') as valuation_date,
        'Expansion Option' as option_type,
        d.deal_value * 0.15 * EXP(-0.1 * generate_series(0, 36) / 12.0) as option_value,
        0.3 + 0.1 * SIN(generate_series(0, 36) * PI() / 6) as volatility
    FROM deals d
    WHERE d.deal_value IS NOT NULL
    UNION ALL
    SELECT 
        d.id as deal_id,
        d.name as deal_name,
        CURRENT_DATE + (generate_series(0, 36) * INTERVAL '1 month') as valuation_date,
        'Abandonment Option' as option_type,
        d.deal_value * 0.05 * (1 + 0.02 * generate_series(0, 36)) as option_value,
        0.2 + 0.05 * COS(generate_series(0, 36) * PI() / 4) as volatility
    FROM deals d
    WHERE d.deal_value IS NOT NULL
)
SELECT * FROM option_data;

-- Grant permissions
GRANT SELECT ON scenario_analysis_view TO aman_user;
GRANT SELECT ON synergy_breakdown_view TO aman_user;
GRANT SELECT ON risk_adjusted_metrics TO aman_user;
GRANT SELECT ON monte_carlo_results TO aman_user;
GRANT SELECT ON scenario_comparison TO aman_user;
GRANT SELECT ON breakeven_analysis TO aman_user;
GRANT SELECT ON sensitivity_analysis TO aman_user;
GRANT SELECT ON probability_distributions TO aman_user;
GRANT SELECT ON decision_tree_nodes TO aman_user;
GRANT SELECT ON real_options_analysis TO aman_user;