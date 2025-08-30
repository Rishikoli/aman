const { Pool } = require('pg');
const logger = require('../utils/logger');

class FinancialAnalysis {
    constructor(pool) {
        this.pool = pool;
    }

    // Create a new financial analysis record
    async createAnalysis(dealId, companyId, analysisData) {
        const client = await this.pool.connect();
        try {
            await client.query('BEGIN');

            // Insert main analysis record
            const analysisQuery = `
                INSERT INTO financial_analyses (
                    id, deal_id, company_id, analysis_date, 
                    overall_score, risk_level, recommendation,
                    synergy_value, confidence_level, metadata
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
                RETURNING *
            `;

            const analysisId = require('uuid').v4();
            const analysisResult = await client.query(analysisQuery, [
                analysisId,
                dealId,
                companyId,
                new Date(),
                analysisData.overallScore || 0,
                analysisData.riskLevel || 'medium',
                analysisData.recommendation || 'review',
                analysisData.synergyValue || 0,
                analysisData.confidenceLevel || 0.5,
                JSON.stringify(analysisData.metadata || {})
            ]);

            // Insert financial metrics
            if (analysisData.metrics && analysisData.metrics.length > 0) {
                for (const metric of analysisData.metrics) {
                    await this.insertMetric(client, analysisId, metric);
                }
            }

            // Insert trend data
            if (analysisData.trendData && analysisData.trendData.length > 0) {
                for (const trend of analysisData.trendData) {
                    await this.insertTrendData(client, analysisId, trend);
                }
            }

            // Insert anomalies
            if (analysisData.anomalies && analysisData.anomalies.length > 0) {
                for (const anomaly of analysisData.anomalies) {
                    await this.insertAnomaly(client, analysisId, anomaly);
                }
            }

            // Insert forecasts
            if (analysisData.forecasts && analysisData.forecasts.length > 0) {
                for (const forecast of analysisData.forecasts) {
                    await this.insertForecast(client, analysisId, forecast);
                }
            }

            // Insert risk factors
            if (analysisData.riskFactors && analysisData.riskFactors.length > 0) {
                for (const risk of analysisData.riskFactors) {
                    await this.insertRiskFactor(client, analysisId, risk);
                }
            }

            await client.query('COMMIT');
            return analysisResult.rows[0];

        } catch (error) {
            await client.query('ROLLBACK');
            logger.error('Error creating financial analysis:', error);
            throw error;
        } finally {
            client.release();
        }
    }

    // Get financial analysis by deal ID
    async getAnalysisByDealId(dealId) {
        try {
            const query = `
                SELECT fa.*, 
                       d.name as deal_name,
                       c.name as company_name,
                       c.ticker_symbol
                FROM financial_analyses fa
                LEFT JOIN deals d ON fa.deal_id = d.id
                LEFT JOIN companies c ON fa.company_id = c.id
                WHERE fa.deal_id = $1
                ORDER BY fa.created_at DESC
                LIMIT 1
            `;

            const result = await this.pool.query(query, [dealId]);
            
            if (result.rows.length === 0) {
                return null;
            }

            const analysis = result.rows[0];
            
            // Get related data
            analysis.metrics = await this.getMetricsByAnalysisId(analysis.id);
            analysis.trendData = await this.getTrendDataByAnalysisId(analysis.id);
            analysis.anomalies = await this.getAnomaliesByAnalysisId(analysis.id);
            analysis.forecasts = await this.getForecastsByAnalysisId(analysis.id);
            analysis.riskFactors = await this.getRiskFactorsByAnalysisId(analysis.id);

            return analysis;

        } catch (error) {
            logger.error('Error getting financial analysis:', error);
            throw error;
        }
    }

    // Get financial metrics by analysis ID
    async getMetricsByAnalysisId(analysisId) {
        try {
            const query = `
                SELECT * FROM financial_metrics 
                WHERE analysis_id = $1 
                ORDER BY category, name
            `;
            const result = await this.pool.query(query, [analysisId]);
            return result.rows;
        } catch (error) {
            logger.error('Error getting financial metrics:', error);
            throw error;
        }
    }

    // Get trend data by analysis ID
    async getTrendDataByAnalysisId(analysisId) {
        try {
            const query = `
                SELECT * FROM financial_trends 
                WHERE analysis_id = $1 
                ORDER BY period_date
            `;
            const result = await this.pool.query(query, [analysisId]);
            return result.rows;
        } catch (error) {
            logger.error('Error getting trend data:', error);
            throw error;
        }
    }

    // Get anomalies by analysis ID
    async getAnomaliesByAnalysisId(analysisId) {
        try {
            const query = `
                SELECT * FROM financial_anomalies 
                WHERE analysis_id = $1 
                ORDER BY severity DESC, impact DESC
            `;
            const result = await this.pool.query(query, [analysisId]);
            return result.rows;
        } catch (error) {
            logger.error('Error getting anomalies:', error);
            throw error;
        }
    }

    // Get forecasts by analysis ID
    async getForecastsByAnalysisId(analysisId) {
        try {
            const query = `
                SELECT * FROM financial_forecasts 
                WHERE analysis_id = $1 
                ORDER BY period_date, scenario
            `;
            const result = await this.pool.query(query, [analysisId]);
            return result.rows;
        } catch (error) {
            logger.error('Error getting forecasts:', error);
            throw error;
        }
    }

    // Get risk factors by analysis ID
    async getRiskFactorsByAnalysisId(analysisId) {
        try {
            const query = `
                SELECT * FROM risk_factors 
                WHERE analysis_id = $1 
                ORDER BY risk_score DESC
            `;
            const result = await this.pool.query(query, [analysisId]);
            return result.rows;
        } catch (error) {
            logger.error('Error getting risk factors:', error);
            throw error;
        }
    }

    // Helper methods for inserting related data
    async insertMetric(client, analysisId, metric) {
        const query = `
            INSERT INTO financial_metrics (
                id, analysis_id, name, value, unit, category,
                trend, trend_value, benchmark, description
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
        `;

        await client.query(query, [
            require('uuid').v4(),
            analysisId,
            metric.name,
            metric.value,
            metric.unit,
            metric.category,
            metric.trend,
            metric.trendValue,
            metric.benchmark,
            metric.description
        ]);
    }

    async insertTrendData(client, analysisId, trend) {
        const query = `
            INSERT INTO financial_trends (
                id, analysis_id, period, period_date, revenue,
                net_income, ebitda, total_assets, total_liabilities,
                equity, cash_flow
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
        `;

        await client.query(query, [
            require('uuid').v4(),
            analysisId,
            trend.period,
            new Date(trend.date),
            trend.revenue,
            trend.netIncome,
            trend.ebitda,
            trend.totalAssets,
            trend.totalLiabilities,
            trend.equity,
            trend.cashFlow
        ]);
    }

    async insertAnomaly(client, analysisId, anomaly) {
        const query = `
            INSERT INTO financial_anomalies (
                id, analysis_id, type, severity, title, description,
                impact, period, metric, expected_value, actual_value,
                variance, recommendations
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13)
        `;

        await client.query(query, [
            require('uuid').v4(),
            analysisId,
            anomaly.type,
            anomaly.severity,
            anomaly.title,
            anomaly.description,
            anomaly.impact,
            anomaly.period,
            anomaly.metric,
            anomaly.expectedValue,
            anomaly.actualValue,
            anomaly.variance,
            JSON.stringify(anomaly.recommendations || [])
        ]);
    }

    async insertForecast(client, analysisId, forecast) {
        const query = `
            INSERT INTO financial_forecasts (
                id, analysis_id, period, period_date, metric,
                forecast_value, confidence_lower, confidence_upper,
                confidence_level, scenario
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
        `;

        await client.query(query, [
            require('uuid').v4(),
            analysisId,
            forecast.period,
            new Date(forecast.date),
            forecast.metric,
            forecast.forecastValue,
            forecast.confidenceInterval.lower,
            forecast.confidenceInterval.upper,
            forecast.confidence,
            forecast.scenario
        ]);
    }

    async insertRiskFactor(client, analysisId, risk) {
        const query = `
            INSERT INTO risk_factors (
                id, analysis_id, category, name, description,
                probability, impact, risk_score, mitigation,
                status
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
        `;

        await client.query(query, [
            require('uuid').v4(),
            analysisId,
            risk.category,
            risk.name,
            risk.description,
            risk.probability,
            risk.impact,
            risk.riskScore,
            JSON.stringify(risk.mitigation || []),
            risk.status
        ]);
    }
}

module.exports = FinancialAnalysis;