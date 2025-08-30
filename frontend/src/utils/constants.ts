// Application constants
export const APP_NAME = 'AMAN Dashboard';
export const APP_VERSION = '1.0.0';

// API endpoints
export const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:3001/api';

// Local storage keys
export const STORAGE_KEYS = {
  AUTH_TOKEN: 'aman_auth_token',
  USER_PREFERENCES: 'aman_user_preferences',
  DASHBOARD_FILTERS: 'aman_dashboard_filters',
} as const;

// Route paths
export const ROUTES = {
  HOME: '/',
  DASHBOARD: '/dashboard',
  DEALS: '/deals',
  AGENTS: '/agents',
  ANALYTICS: '/analytics',
  SETTINGS: '/settings',
} as const;

// Chart colors
export const CHART_COLORS = {
  PRIMARY: '#1976d2',
  SECONDARY: '#dc004e',
  SUCCESS: '#4caf50',
  WARNING: '#ff9800',
  ERROR: '#f44336',
  INFO: '#2196f3',
} as const;

// Risk severity levels
export const RISK_LEVELS = {
  LOW: 'low',
  MEDIUM: 'medium',
  HIGH: 'high',
  CRITICAL: 'critical',
} as const;

// Agent status types
export const AGENT_STATUS = {
  IDLE: 'idle',
  RUNNING: 'running',
  COMPLETED: 'completed',
  FAILED: 'failed',
  PAUSED: 'paused',
} as const;