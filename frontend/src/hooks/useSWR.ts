import useSWR, { SWRConfiguration, SWRResponse } from 'swr';
import { api } from '../lib/api';

// Default SWR configuration
const defaultConfig: SWRConfiguration = {
  revalidateOnFocus: false,
  revalidateOnReconnect: true,
  refreshInterval: 0,
  dedupingInterval: 2000,
  errorRetryCount: 3,
  errorRetryInterval: 5000,
};

// Generic fetcher function
const fetcher = async (url: string) => {
  return api.get(url);
};

// Define proper types for API responses
interface Deal {
  id: string;
  name: string;
  status: string;
  [key: string]: unknown;
}

interface Company {
  id: string;
  name: string;
  industry: string;
  [key: string]: unknown;
}

interface Agent {
  id: string;
  name: string;
  status: string;
  [key: string]: unknown;
}

interface Report {
  id: string;
  title: string;
  type: string;
  [key: string]: unknown;
}

interface HealthStatus {
  status: string;
  timestamp: string;
  [key: string]: unknown;
}

interface Config {
  app: Record<string, unknown>;
  ui: Record<string, unknown>;
  [key: string]: unknown;
}

// Custom hooks for different data types
export const useDeals = (config?: SWRConfiguration): SWRResponse<Deal[], Error> => {
  return useSWR('/api/deals', fetcher, { ...defaultConfig, ...config });
};

export const useDeal = (id: string, config?: SWRConfiguration): SWRResponse<Deal, Error> => {
  return useSWR(id ? `/api/deals/${id}` : null, fetcher, { ...defaultConfig, ...config });
};

export const useCompanies = (config?: SWRConfiguration): SWRResponse<Company[], Error> => {
  return useSWR('/api/companies', fetcher, { ...defaultConfig, ...config });
};

export const useCompany = (id: string, config?: SWRConfiguration): SWRResponse<Company, Error> => {
  return useSWR(id ? `/api/companies/${id}` : null, fetcher, { ...defaultConfig, ...config });
};

export const useAgents = (config?: SWRConfiguration): SWRResponse<Agent[], Error> => {
  return useSWR('/api/agents', fetcher, { ...defaultConfig, ...config });
};

export const useAgentStatus = (agentId: string, config?: SWRConfiguration): SWRResponse<Agent, Error> => {
  return useSWR(
    agentId ? `/api/agents/${agentId}/status` : null,
    fetcher,
    { 
      ...defaultConfig, 
      refreshInterval: 5000, // Refresh every 5 seconds for status
      ...config 
    }
  );
};

export const useReports = (config?: SWRConfiguration): SWRResponse<Report[], Error> => {
  return useSWR('/api/reports', fetcher, { ...defaultConfig, ...config });
};

export const useReport = (id: string, config?: SWRConfiguration): SWRResponse<Report, Error> => {
  return useSWR(id ? `/api/reports/${id}` : null, fetcher, { ...defaultConfig, ...config });
};

export const useHealth = (config?: SWRConfiguration): SWRResponse<HealthStatus, Error> => {
  return useSWR('/api/health', fetcher, { 
    ...defaultConfig, 
    refreshInterval: 30000, // Check health every 30 seconds
    ...config 
  });
};

export const useConfig = (config?: SWRConfiguration): SWRResponse<Config, Error> => {
  return useSWR('/api/config', fetcher, { 
    ...defaultConfig,
    revalidateOnMount: true,
    ...config 
  });
};

// Search hook with debouncing
export const useCompanySearch = (query: string, config?: SWRConfiguration): SWRResponse<Company[], Error> => {
  const debouncedQuery = query.length >= 2 ? query : null;
  
  return useSWR(
    debouncedQuery ? `/api/companies/search?q=${encodeURIComponent(debouncedQuery)}` : null,
    fetcher,
    {
      ...defaultConfig,
      dedupingInterval: 1000,
      ...config,
    }
  );
};

// Utility hook for manual data fetching
export const useManualFetch = () => {
  const fetchData = async (url: string) => {
    try {
      return await api.get(url);
    } catch (error) {
      console.error('Manual fetch error:', error);
      throw error;
    }
  };

  return { fetchData };
};

export default useSWR;