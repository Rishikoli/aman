-- AMAN Database Schema
-- PostgreSQL schema for Autonomous M&A Navigator

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create ENUM types
CREATE TYPE deal_status AS ENUM ('draft', 'active', 'completed', 'cancelled', 'on_hold');
CREATE TYPE company_size AS ENUM ('startup', 'small', 'medium', 'large', 'enterprise');
CREATE TYPE execution_status AS ENUM ('pending', 'queued', 'running', 'completed', 'failed', 'cancelled');
CREATE TYPE risk_category AS ENUM ('financial', 'legal', 'technical', 'operational', 'market', 'reputation');
CREATE TYPE severity_level AS ENUM ('low', 'medium', 'high', 'critical');
CREATE TYPE agent_type AS ENUM ('finance', 'legal', 'synergy', 'reputation', 'operations', 'orchestrator');

-- Companies table
CREATE TABLE companies (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    ticker_symbol VARCHAR(10),
    industry VARCHAR(100),
    sector VARCHAR(100),
    company_size company_size,
    headquarters_location VARCHAR(255),
    founded_year INTEGER,
    employee_count INTEGER,
    annual_revenue DECIMAL(15,2),
    market_cap DECIMAL(15,2),
    description TEXT,
    website_url VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Deals table
CREATE TABLE deals (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    acquirer_id UUID REFERENCES companies(id),
    target_id UUID REFERENCES companies(id),
    deal_value DECIMAL(15,2),
    currency VARCHAR(3) DEFAULT 'USD',
    status deal_status DEFAULT 'draft',
    created_by VARCHAR(255),
    estimated_completion_date DATE,
    actual_completion_date DATE,
    priority INTEGER DEFAULT 5 CHECK (priority >= 1 AND priority <= 10),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Agent executions table
CREATE TABLE agent_executions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    deal_id UUID REFERENCES deals(id) ON DELETE CASCADE,
    agent_type agent_type NOT NULL,
    agent_id VARCHAR(100) NOT NULL,
    status execution_status DEFAULT 'pending',
    queued_at TIMESTAMP WITH TIME ZONE,
    start_time TIMESTAMP WITH TIME ZONE,
    end_time TIMESTAMP WITH TIME ZONE,
    duration_seconds INTEGER,
    recursion_level INTEGER DEFAULT 0,
    parent_execution_id UUID REFERENCES agent_executions(id),
    input_data JSONB DEFAULT '{}',
    output_data JSONB DEFAULT '{}',
    error_message TEXT,
    progress_percentage INTEGER DEFAULT 0 CHECK (progress_percentage >= 0 AND progress_percentage <= 100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Findings table
CREATE TABLE findings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    deal_id UUID REFERENCES deals(id) ON DELETE CASCADE,
    agent_execution_id UUID REFERENCES agent_executions(id) ON DELETE CASCADE,
    category risk_category NOT NULL,
    severity severity_level NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    evidence JSONB DEFAULT '[]',
    recommendations JSONB DEFAULT '[]',
    confidence_score DECIMAL(3,2) CHECK (confidence_score >= 0 AND confidence_score <= 1),
    requires_recursion BOOLEAN DEFAULT FALSE,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Financial data table
CREATE TABLE financial_data (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_id UUID REFERENCES companies(id) ON DELETE CASCADE,
    fiscal_year INTEGER NOT NULL,
    fiscal_quarter INTEGER CHECK (fiscal_quarter >= 1 AND fiscal_quarter <= 4),
    revenue DECIMAL(15,2),
    net_income DECIMAL(15,2),
    total_assets DECIMAL(15,2),
    total_liabilities DECIMAL(15,2),
    shareholders_equity DECIMAL(15,2),
    cash_and_equivalents DECIMAL(15,2),
    total_debt DECIMAL(15,2),
    operating_cash_flow DECIMAL(15,2),
    free_cash_flow DECIMAL(15,2),
    gross_margin DECIMAL(5,4),
    operating_margin DECIMAL(5,4),
    net_margin DECIMAL(5,4),
    roe DECIMAL(5,4),
    roa DECIMAL(5,4),
    debt_to_equity DECIMAL(5,4),
    current_ratio DECIMAL(5,4),
    quick_ratio DECIMAL(5,4),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(company_id, fiscal_year, fiscal_quarter)
);

-- Timeline estimates table
CREATE TABLE timeline_estimates (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    deal_id UUID UNIQUE REFERENCES deals(id) ON DELETE CASCADE,
    total_estimated_hours DECIMAL(8,2) NOT NULL,
    estimated_completion_date TIMESTAMP WITH TIME ZONE,
    complexity_analysis JSONB DEFAULT '{}',
    agent_estimates JSONB DEFAULT '[]',
    execution_phases JSONB DEFAULT '[]',
    external_milestones JSONB DEFAULT '[]',
    bottlenecks JSONB DEFAULT '[]',
    confidence_level INTEGER CHECK (confidence_level >= 0 AND confidence_level <= 100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Timeline events table for tracking deal progress
CREATE TABLE timeline_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    deal_id UUID REFERENCES deals(id) ON DELETE CASCADE,
    event_type VARCHAR(100) NOT NULL,
    event_data JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_deals_status ON deals(status);
CREATE INDEX idx_deals_acquirer ON deals(acquirer_id);
CREATE INDEX idx_deals_target ON deals(target_id);
CREATE INDEX idx_deals_created_at ON deals(created_at);

CREATE INDEX idx_companies_ticker ON companies(ticker_symbol);
CREATE INDEX idx_companies_industry ON companies(industry);
CREATE INDEX idx_companies_size ON companies(company_size);

CREATE INDEX idx_agent_executions_deal ON agent_executions(deal_id);
CREATE INDEX idx_agent_executions_status ON agent_executions(status);
CREATE INDEX idx_agent_executions_agent_type ON agent_executions(agent_type);
CREATE INDEX idx_agent_executions_start_time ON agent_executions(start_time);

CREATE INDEX idx_findings_deal ON findings(deal_id);
CREATE INDEX idx_findings_category ON findings(category);
CREATE INDEX idx_findings_severity ON findings(severity);
CREATE INDEX idx_findings_agent_execution ON findings(agent_execution_id);

CREATE INDEX idx_financial_data_company ON financial_data(company_id);
CREATE INDEX idx_financial_data_year ON financial_data(fiscal_year);

CREATE INDEX idx_timeline_estimates_deal ON timeline_estimates(deal_id);
CREATE INDEX idx_timeline_events_deal ON timeline_events(deal_id);
CREATE INDEX idx_timeline_events_type ON timeline_events(event_type);
CREATE INDEX idx_timeline_events_created_at ON timeline_events(created_at);

-- Update triggers for updated_at columns
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_companies_updated_at BEFORE UPDATE ON companies
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_deals_updated_at BEFORE UPDATE ON deals
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_agent_executions_updated_at BEFORE UPDATE ON agent_executions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_findings_updated_at BEFORE UPDATE ON findings
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_financial_data_updated_at BEFORE UPDATE ON financial_data
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_timeline_estimates_updated_at BEFORE UPDATE ON timeline_estimates
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();