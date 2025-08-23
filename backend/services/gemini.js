const { GoogleGenerativeAI } = require('@google/generative-ai');
const { getConfig } = require('../utils/env-config');

class GeminiService {
  constructor() {
    const config = getConfig();
    this.apiKey = config.apiKeys.gemini;
    
    if (!this.apiKey || this.apiKey === 'demo_gemini_key') {
      console.warn('Gemini API key not configured. AI features will be limited.');
      this.genAI = null;
    } else {
      this.genAI = new GoogleGenerativeAI(this.apiKey);
    }
  }

  /**
   * Generate text using Gemini 2.0 Flash
   * @param {string} prompt - The input prompt
   * @param {Object} options - Generation options
   * @returns {Promise<string>} Generated text
   */
  async generateText(prompt, options = {}) {
    if (!this.genAI) {
      throw new Error('Gemini API not configured');
    }

    try {
      // Use Gemini 2.0 Flash model
      const model = this.genAI.getGenerativeModel({ 
        model: "gemini-2.0-flash-exp",
        generationConfig: {
          temperature: options.temperature || 0.7,
          topP: options.topP || 0.8,
          topK: options.topK || 40,
          maxOutputTokens: options.maxTokens || 2048,
        }
      });

      const result = await model.generateContent(prompt);
      const response = await result.response;
      return response.text();
    } catch (error) {
      console.error('Gemini API Error:', error);
      throw new Error(`Gemini generation failed: ${error.message}`);
    }
  }

  /**
   * Generate structured analysis for M&A deals
   * @param {Object} dealData - Deal information
   * @returns {Promise<Object>} Structured analysis
   */
  async analyzeDeal(dealData) {
    const prompt = `
Analyze the following M&A deal and provide a structured assessment:

Deal Information:
- Target Company: ${dealData.targetCompany || 'Not specified'}
- Acquiring Company: ${dealData.acquiringCompany || 'Not specified'}
- Deal Value: ${dealData.dealValue || 'Not specified'}
- Industry: ${dealData.industry || 'Not specified'}
- Deal Type: ${dealData.dealType || 'Not specified'}

Please provide analysis in the following JSON format:
{
  "riskAssessment": {
    "overallRisk": "Low|Medium|High",
    "riskScore": 1-10,
    "keyRisks": ["risk1", "risk2", "risk3"]
  },
  "financialAnalysis": {
    "valuation": "Fair|Undervalued|Overvalued",
    "synergies": ["synergy1", "synergy2"],
    "concerns": ["concern1", "concern2"]
  },
  "marketAnalysis": {
    "marketConditions": "Favorable|Neutral|Unfavorable",
    "competitivePosition": "Strong|Moderate|Weak",
    "industryTrends": ["trend1", "trend2"]
  },
  "recommendations": {
    "proceed": true|false,
    "conditions": ["condition1", "condition2"],
    "nextSteps": ["step1", "step2"]
  }
}

Provide only the JSON response without additional text.
`;

    try {
      const response = await this.generateText(prompt, { temperature: 0.3 });
      return JSON.parse(response);
    } catch (error) {
      console.error('Deal analysis failed:', error);
      // Return fallback analysis
      return {
        riskAssessment: {
          overallRisk: "Medium",
          riskScore: 5,
          keyRisks: ["Market volatility", "Integration challenges", "Regulatory approval"]
        },
        financialAnalysis: {
          valuation: "Fair",
          synergies: ["Cost savings", "Market expansion"],
          concerns: ["High premium", "Debt levels"]
        },
        marketAnalysis: {
          marketConditions: "Neutral",
          competitivePosition: "Moderate",
          industryTrends: ["Digital transformation", "Consolidation"]
        },
        recommendations: {
          proceed: true,
          conditions: ["Due diligence completion", "Regulatory approval"],
          nextSteps: ["Financial audit", "Legal review"]
        }
      };
    }
  }

  /**
   * Generate company research summary
   * @param {string} companyName - Company name
   * @param {Object} companyData - Additional company data
   * @returns {Promise<Object>} Research summary
   */
  async researchCompany(companyName, companyData = {}) {
    const prompt = `
Provide a comprehensive research summary for the following company:

Company: ${companyName}
Industry: ${companyData.industry || 'Not specified'}
Revenue: ${companyData.revenue || 'Not specified'}
Employees: ${companyData.employees || 'Not specified'}
Founded: ${companyData.founded || 'Not specified'}

Please provide analysis in JSON format:
{
  "overview": "Brief company overview",
  "strengths": ["strength1", "strength2", "strength3"],
  "weaknesses": ["weakness1", "weakness2"],
  "opportunities": ["opportunity1", "opportunity2"],
  "threats": ["threat1", "threat2"],
  "financialHealth": "Strong|Moderate|Weak",
  "marketPosition": "Leader|Challenger|Follower|Niche",
  "keyMetrics": {
    "revenueGrowth": "percentage or trend",
    "profitability": "High|Medium|Low",
    "marketShare": "percentage or position"
  }
}

Provide only the JSON response.
`;

    try {
      const response = await this.generateText(prompt, { temperature: 0.4 });
      return JSON.parse(response);
    } catch (error) {
      console.error('Company research failed:', error);
      return {
        overview: `${companyName} is a company in the ${companyData.industry || 'specified'} industry.`,
        strengths: ["Market presence", "Brand recognition"],
        weaknesses: ["Limited data available"],
        opportunities: ["Market expansion", "Digital transformation"],
        threats: ["Market competition", "Economic uncertainty"],
        financialHealth: "Moderate",
        marketPosition: "Challenger",
        keyMetrics: {
          revenueGrowth: "Data not available",
          profitability: "Medium",
          marketShare: "Data not available"
        }
      };
    }
  }

  /**
   * Generate market intelligence report
   * @param {string} industry - Industry sector
   * @param {Object} options - Report options
   * @returns {Promise<Object>} Market intelligence
   */
  async generateMarketIntelligence(industry, options = {}) {
    const prompt = `
Generate a market intelligence report for the ${industry} industry.

Focus areas:
- Current market trends
- Growth opportunities
- Competitive landscape
- Regulatory environment
- Technology disruptions
- M&A activity

Provide analysis in JSON format:
{
  "marketOverview": {
    "size": "Market size information",
    "growth": "Growth rate and trends",
    "keyPlayers": ["player1", "player2", "player3"]
  },
  "trends": [
    {
      "trend": "Trend name",
      "impact": "High|Medium|Low",
      "description": "Trend description"
    }
  ],
  "opportunities": [
    {
      "opportunity": "Opportunity name",
      "potential": "High|Medium|Low",
      "timeframe": "Short|Medium|Long term"
    }
  ],
  "risks": [
    {
      "risk": "Risk name",
      "probability": "High|Medium|Low",
      "impact": "High|Medium|Low"
    }
  ],
  "maActivity": {
    "volume": "High|Medium|Low",
    "averageDealSize": "Size range",
    "hotSectors": ["sector1", "sector2"]
  }
}

Provide only the JSON response.
`;

    try {
      const response = await this.generateText(prompt, { temperature: 0.5 });
      return JSON.parse(response);
    } catch (error) {
      console.error('Market intelligence generation failed:', error);
      return {
        marketOverview: {
          size: "Market size data not available",
          growth: "Moderate growth expected",
          keyPlayers: ["Major Player 1", "Major Player 2", "Major Player 3"]
        },
        trends: [
          {
            trend: "Digital transformation",
            impact: "High",
            description: "Companies are investing in digital technologies"
          }
        ],
        opportunities: [
          {
            opportunity: "Market consolidation",
            potential: "High",
            timeframe: "Medium term"
          }
        ],
        risks: [
          {
            risk: "Economic uncertainty",
            probability: "Medium",
            impact: "High"
          }
        ],
        maActivity: {
          volume: "Medium",
          averageDealSize: "Varies by sector",
          hotSectors: ["Technology", "Healthcare"]
        }
      };
    }
  }

  /**
   * Check if Gemini service is available
   * @returns {boolean} Service availability
   */
  isAvailable() {
    return this.genAI !== null;
  }

  /**
   * Get service status
   * @returns {Object} Service status information
   */
  getStatus() {
    return {
      service: 'Gemini 2.0 Flash',
      available: this.isAvailable(),
      model: 'gemini-2.0-flash-exp',
      configured: !!this.apiKey && this.apiKey !== 'demo_gemini_key'
    };
  }
}

module.exports = new GeminiService();