/**
 * Mock Financial Data Service
 * Generates realistic financial analysis data for M&A scenarios
 */

class MockFinancialDataService {
    static generateRandomValue(min, max) {
        return Math.random() * (max - min) + min;
    }

    static generateFinancialAnalysis(dealId, companyId) {
        return {
            dealId,
            companyId,
            analysisDate: new Date().toISOString(),
            overallScore: this.generateRandomValue(60, 95),
            riskLevel: this.getRandomRiskLevel(),
            recommendation: this.getRandomRecommendation(),
            synergyValue: this.generateRandomValue(500000000, 5000000000),
            confidenceLevel: this.generateRandomValue(0.7, 0.95),
            metadata: {
                analysisVersion: '2.1',
                dataSource: 'integrated',
                processingTime: this.generateRandomValue(45, 120)
            },
            metrics: this.generateMetrics(),
            trendData: this.generateTrendData(),
            anomalies: this.generateAnomalies(),
            forecasts: this.generateForecasts(),
            riskFactors: this.generateRiskFactors()
        };
    }

    static generateMetrics() {
        return [
            {
                name: 'Return on Equity',
                value: this.generateRandomValue(12, 25),
                unit: '%',
                category: 'profitability',
                trend: Math.random() > 0.5 ? 'up' : 'down',
                trendValue: `${this.generateRandomValue(1, 5).toFixed(1)}%`,
                benchmark: 15,
                description: 'Measures how effectively management uses equity to generate profits'
            },
            {
                name: 'Return on Assets',
                value: this.generateRandomValue(8, 18),
                unit: '%',
                category: 'profitability',
                trend: 'up',
                trendValue: '2.3%',
                benchmark: 12,
                description: 'Indicates how profitable a company is relative to its total assets'
            },
            {
                name: 'Current Ratio',
                value: this.generateRandomValue(1.2, 2.8),
                unit: 'x',
                category: 'liquidity',
                trend: 'flat',
                trendValue: '0.1x',
                benchmark: 2.0,
                description: 'Measures ability to pay short-term obligations'
            },
            {
                name: 'Debt-to-Equity',
                value: this.generateRandomValue(0.3, 1.2),
                unit: 'x',
                category: 'leverage',
                trend: 'down',
                trendValue: '-0.2x',
                benchmark: 0.6,
                description: 'Indicates the relative proportion of debt and equity'
            },
            {
                name: 'P/E Ratio',
                value: this.generateRandomValue(15, 35),
                unit: 'x',
                category: 'valuation',
                trend: 'up',
                trendValue: '3.2x',
                benchmark: 22,
                description: 'Price-to-earnings ratio for valuation assessment'
            },
            {
                name: 'Asset Turnover',
                value: this.generateRandomValue(0.8, 1.8),
                unit: 'x',
                category: 'efficiency',
                trend: 'up',
                trendValue: '0.1x',
                benchmark: 1.2,
                description: 'Measures how efficiently assets generate revenue'
            }
        ];
    }

    static generateTrendData(periods = 12) {
        const data = [];
        const baseDate = new Date();
        
        for (let i = periods - 1; i >= 0; i--) {
            const date = new Date(baseDate);
            date.setMonth(date.getMonth() - i);
            
            const revenue = this.generateRandomValue(800000000, 1200000000);
            const netIncome = revenue * this.generateRandomValue(0.1, 0.25);
            const ebitda = revenue * this.generateRandomValue(0.15, 0.35);
            
            data.push({
                period: `Q${Math.floor(i / 3) + 1} ${date.getFullYear()}`,
                date: date.toISOString(),
                revenue,
                netIncome,
                ebitda,
                totalAssets: revenue * this.generateRandomValue(2, 4),
                totalLiabilities: revenue * this.generateRandomValue(1, 2),
                equity: revenue * this.generateRandomValue(0.8, 1.5),
                cashFlow: netIncome * this.generateRandomValue(1.1, 1.4)
            });
        }
        
        return data;
    }

    static generateAnomalies() {
        const anomalies = [];
        
        if (Math.random() > 0.3) {
            anomalies.push({
                type: 'revenue_drop',
                severity: 'high',
                title: 'Significant Revenue Decline in Q3',
                description: 'Revenue dropped 15% compared to previous quarter, indicating potential market challenges or operational issues.',
                impact: -45000000,
                period: 'Q3 2024',
                metric: 'Revenue',
                expectedValue: 950000000,
                actualValue: 807500000,
                variance: -15.0,
                recommendations: [
                    'Investigate market conditions and competitive landscape',
                    'Review sales pipeline and customer retention rates',
                    'Consider strategic initiatives to boost revenue'
                ]
            });
        }

        if (Math.random() > 0.5) {
            anomalies.push({
                type: 'margin_compression',
                severity: 'medium',
                title: 'Gross Margin Compression',
                description: 'Gross margins have decreased by 3% over the last two quarters due to increased input costs.',
                impact: -12000000,
                period: 'Q2-Q3 2024',
                metric: 'Gross Margin',
                expectedValue: 42,
                actualValue: 39,
                variance: -7.1,
                recommendations: [
                    'Implement cost reduction initiatives',
                    'Negotiate better supplier terms',
                    'Consider price adjustments for products'
                ]
            });
        }

        return anomalies;
    }

    static generateForecasts() {
        const forecasts = [];
        const baseDate = new Date();
        
        const scenarios = ['optimistic', 'base', 'pessimistic'];
        
        for (let i = 1; i <= 12; i++) {
            const date = new Date(baseDate);
            date.setMonth(date.getMonth() + i);
            
            scenarios.forEach(scenario => {
                const multiplier = scenario === 'optimistic' ? 1.15 : scenario === 'pessimistic' ? 0.85 : 1.0;
                const baseRevenue = 1000000000 * multiplier;
                
                forecasts.push({
                    period: `Q${Math.floor((i - 1) / 3) + 1} ${date.getFullYear()}`,
                    date: date.toISOString(),
                    metric: 'revenue',
                    forecastValue: baseRevenue * (1 + (i * 0.02)), // 2% growth per quarter
                    confidenceInterval: {
                        lower: baseRevenue * 0.9,
                        upper: baseRevenue * 1.1
                    },
                    confidence: this.generateRandomValue(70, 95),
                    scenario
                });
            });
        }
        
        return forecasts;
    }

    static generateRiskFactors() {
        const riskFactors = [
            {
                category: 'market',
                name: 'Market Volatility Risk',
                description: 'High volatility in target markets could impact revenue projections',
                probability: this.generateRandomValue(60, 80),
                impact: this.generateRandomValue(70, 90),
                riskScore: 0, // Will be calculated
                mitigation: [
                    'Diversify revenue streams across multiple markets',
                    'Implement hedging strategies for currency exposure',
                    'Develop contingency plans for market downturns'
                ],
                status: 'assessed'
            },
            {
                category: 'operational',
                name: 'Integration Complexity',
                description: 'Complex IT systems and cultural differences may hinder integration',
                probability: this.generateRandomValue(70, 85),
                impact: this.generateRandomValue(60, 80),
                riskScore: 0,
                mitigation: [
                    'Establish dedicated integration management office',
                    'Conduct thorough cultural assessment',
                    'Plan phased integration approach'
                ],
                status: 'identified'
            },
            {
                category: 'regulatory',
                name: 'Regulatory Approval Risk',
                description: 'Potential antitrust concerns may delay or block the transaction',
                probability: this.generateRandomValue(30, 50),
                impact: this.generateRandomValue(80, 95),
                riskScore: 0,
                mitigation: [
                    'Engage with regulators early in the process',
                    'Prepare divestiture options if required',
                    'Develop alternative deal structures'
                ],
                status: 'mitigated'
            },
            {
                category: 'financial',
                name: 'Increased Financial Leverage',
                description: 'Deal financing will significantly increase debt levels',
                probability: this.generateRandomValue(80, 95),
                impact: this.generateRandomValue(50, 70),
                riskScore: 0,
                mitigation: [
                    'Optimize capital structure post-transaction',
                    'Accelerate synergy realization',
                    'Consider equity financing alternatives'
                ],
                status: 'accepted'
            }
        ];

        // Calculate risk scores
        riskFactors.forEach(factor => {
            factor.riskScore = (factor.probability * factor.impact) / 100;
        });

        return riskFactors;
    }

    static getRandomRiskLevel() {
        const levels = ['low', 'medium', 'high', 'critical'];
        const weights = [0.1, 0.4, 0.4, 0.1]; // Medium and high are more common
        
        const random = Math.random();
        let cumulative = 0;
        
        for (let i = 0; i < levels.length; i++) {
            cumulative += weights[i];
            if (random <= cumulative) {
                return levels[i];
            }
        }
        
        return 'medium';
    }

    static getRandomRecommendation() {
        const recommendations = ['proceed', 'caution', 'review'];
        const weights = [0.3, 0.5, 0.2]; // Caution is most common
        
        const random = Math.random();
        let cumulative = 0;
        
        for (let i = 0; i < recommendations.length; i++) {
            cumulative += weights[i];
            if (random <= cumulative) {
                return recommendations[i];
            }
        }
        
        return 'caution';
    }
}

module.exports = MockFinancialDataService;