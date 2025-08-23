import { useState, useCallback } from 'react';
import { endpoints } from '../lib/api';

interface GeminiStatus {
  service: string;
  available: boolean;
  model: string;
  configured: boolean;
}

interface DealAnalysis {
  riskAssessment: {
    overallRisk: 'Low' | 'Medium' | 'High';
    riskScore: number;
    keyRisks: string[];
  };
  financialAnalysis: {
    valuation: 'Fair' | 'Undervalued' | 'Overvalued';
    synergies: string[];
    concerns: string[];
  };
  marketAnalysis: {
    marketConditions: 'Favorable' | 'Neutral' | 'Unfavorable';
    competitivePosition: 'Strong' | 'Moderate' | 'Weak';
    industryTrends: string[];
  };
  recommendations: {
    proceed: boolean;
    conditions: string[];
    nextSteps: string[];
  };
}

interface CompanyResearch {
  overview: string;
  strengths: string[];
  weaknesses: string[];
  opportunities: string[];
  threats: string[];
  financialHealth: 'Strong' | 'Moderate' | 'Weak';
  marketPosition: 'Leader' | 'Challenger' | 'Follower' | 'Niche';
  keyMetrics: {
    revenueGrowth: string;
    profitability: 'High' | 'Medium' | 'Low';
    marketShare: string;
  };
}

interface MarketIntelligence {
  marketOverview: {
    size: string;
    growth: string;
    keyPlayers: string[];
  };
  trends: Array<{
    trend: string;
    impact: 'High' | 'Medium' | 'Low';
    description: string;
  }>;
  opportunities: Array<{
    opportunity: string;
    potential: 'High' | 'Medium' | 'Low';
    timeframe: 'Short' | 'Medium' | 'Long term';
  }>;
  risks: Array<{
    risk: string;
    probability: 'High' | 'Medium' | 'Low';
    impact: 'High' | 'Medium' | 'Low';
  }>;
  maActivity: {
    volume: 'High' | 'Medium' | 'Low';
    averageDealSize: string;
    hotSectors: string[];
  };
}

export const useGemini = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [status, setStatus] = useState<GeminiStatus | null>(null);

  // Get AI service status
  const getStatus = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await endpoints.ai.status();
      setStatus(response);
      return response;
    } catch (err: any) {
      const errorMessage = err.response?.data?.error || err.message || 'Failed to get AI status';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  }, []);

  // Analyze M&A deal
  const analyzeDeal = useCallback(async (dealData: {
    targetCompany?: string;
    acquiringCompany?: string;
    dealValue?: string;
    industry?: string;
    dealType?: string;
  }): Promise<DealAnalysis> => {
    try {
      setLoading(true);
      setError(null);
      const response = await endpoints.ai.analyzeDeal(dealData);
      return response;
    } catch (err: any) {
      const errorMessage = err.response?.data?.error || err.message || 'Failed to analyze deal';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  }, []);

  // Research company
  const researchCompany = useCallback(async (
    companyName: string,
    companyData?: {
      industry?: string;
      revenue?: string;
      employees?: string;
      founded?: string;
    }
  ): Promise<CompanyResearch> => {
    try {
      setLoading(true);
      setError(null);
      const response = await endpoints.ai.researchCompany(companyName, companyData);
      return response;
    } catch (err: any) {
      const errorMessage = err.response?.data?.error || err.message || 'Failed to research company';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  }, []);

  // Generate market intelligence
  const generateMarketIntelligence = useCallback(async (
    industry: string,
    focusAreas?: string[]
  ): Promise<MarketIntelligence> => {
    try {
      setLoading(true);
      setError(null);
      const response = await endpoints.ai.marketIntelligence(industry, focusAreas);
      return response;
    } catch (err: any) {
      const errorMessage = err.response?.data?.error || err.message || 'Failed to generate market intelligence';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  }, []);

  // Generate text
  const generateText = useCallback(async (
    prompt: string,
    options?: { temperature?: number; maxTokens?: number }
  ): Promise<string> => {
    try {
      setLoading(true);
      setError(null);
      const response = await endpoints.ai.generateText(prompt, options);
      return response.text;
    } catch (err: any) {
      const errorMessage = err.response?.data?.error || err.message || 'Failed to generate text';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    // State
    loading,
    error,
    status,
    
    // Methods
    getStatus,
    analyzeDeal,
    researchCompany,
    generateMarketIntelligence,
    generateText,
    
    // Utilities
    clearError: () => setError(null),
    isAvailable: status?.available && status?.configured,
  };
};

export default useGemini;