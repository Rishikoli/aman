"""
Unit tests for Finance Agent
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
import pandas as pd
import numpy as np
import sys
import os

# Add agents to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'agents'))

from finance.finance_agent import FinanceAgent
from finance.financial_analysis_engine import FinancialAnalysisEngine

class TestFinanceAgent:
    
    @pytest.fixture
    def finance_agent(self, mock_env_vars):
        """Create a Finance Agent instance for testing"""
        return FinanceAgent()
    
    @pytest.fixture
    def sample_financial_data(self):
        """Sample financial data for testing"""
        return {
            'revenue': [100000000, 120000000, 140000000],
            'net_income': [10000000, 12000000, 14000000],
            'total_assets': [200000000, 220000000, 240000000],
            'total_debt': [50000000, 55000000, 60000000],
            'cash': [20000000, 25000000, 30000000],
            'years': [2021, 2022, 2023]
        }
    
    @pytest.mark.unit
    def test_finance_agent_initialization(self, finance_agent):
        """Test Finance Agent initialization"""
        assert finance_agent is not None
        assert hasattr(finance_agent, 'analyze')
    
    @pytest.mark.unit
    def test_calculate_financial_ratios(self, finance_agent, sample_financial_data):
        """Test financial ratio calculations"""
        ratios = finance_agent.calculate_ratios(sample_financial_data)
        
        assert 'debt_to_equity' in ratios
        assert 'current_ratio' in ratios
        assert 'roa' in ratios  # Return on Assets
        assert 'roe' in ratios  # Return on Equity
        
        # Verify ratio calculations are reasonable
        assert ratios['debt_to_equity'] > 0
        assert ratios['roa'] > 0
    
    @pytest.mark.unit
    @patch('finance.finance_agent.requests.get')
    def test_fetch_market_data(self, mock_get, finance_agent):
        """Test market data fetching"""
        # Mock API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'symbol': 'TEST',
            'price': 100.50,
            'marketCap': 1000000000,
            'pe': 15.5
        }
        mock_get.return_value = mock_response
        
        market_data = finance_agent.fetch_market_data('TEST')
        
        assert market_data['symbol'] == 'TEST'
        assert market_data['price'] == 100.50
        assert mock_get.called
    
    @pytest.mark.unit
    def test_anomaly_detection(self, finance_agent, sample_financial_data):
        """Test financial anomaly detection"""
        # Create data with an anomaly
        anomaly_data = sample_financial_data.copy()
        anomaly_data['revenue'][2] = 50000000  # Sudden drop
        
        anomalies = finance_agent.detect_anomalies(anomaly_data)
        
        assert len(anomalies) > 0
        assert any('revenue' in anomaly['metric'] for anomaly in anomalies)
    
    @pytest.mark.unit
    def test_financial_forecasting(self, finance_agent, sample_financial_data):
        """Test financial forecasting"""
        forecast = finance_agent.generate_forecast(sample_financial_data, periods=3)
        
        assert 'revenue_forecast' in forecast
        assert 'confidence_intervals' in forecast
        assert len(forecast['revenue_forecast']) == 3
    
    @pytest.mark.unit
    def test_risk_scoring(self, finance_agent, sample_financial_data):
        """Test financial risk scoring"""
        risk_score = finance_agent.calculate_risk_score(sample_financial_data)
        
        assert 0 <= risk_score <= 100
        assert isinstance(risk_score, (int, float))
    
    @pytest.mark.unit
    @patch('finance.finance_agent.FinanceAgent.fetch_market_data')
    def test_peer_comparison(self, mock_fetch, finance_agent, sample_financial_data):
        """Test peer company comparison"""
        # Mock peer data
        mock_fetch.return_value = {
            'pe_ratio': 20.0,
            'debt_to_equity': 0.5,
            'roa': 0.08
        }
        
        comparison = finance_agent.compare_to_peers(sample_financial_data, ['PEER1', 'PEER2'])
        
        assert 'peer_metrics' in comparison
        assert 'relative_performance' in comparison
    
    @pytest.mark.unit
    def test_error_handling_invalid_data(self, finance_agent):
        """Test error handling with invalid financial data"""
        invalid_data = {'invalid': 'data'}
        
        with pytest.raises(ValueError):
            finance_agent.calculate_ratios(invalid_data)
    
    @pytest.mark.unit
    def test_error_handling_api_failure(self, finance_agent):
        """Test error handling when API calls fail"""
        with patch('finance.finance_agent.requests.get') as mock_get:
            mock_get.side_effect = Exception("API Error")
            
            result = finance_agent.fetch_market_data('TEST')
            assert result is None or 'error' in result

class TestFinancialAnalysisEngine:
    
    @pytest.fixture
    def analysis_engine(self):
        """Create Financial Analysis Engine for testing"""
        return FinancialAnalysisEngine()
    
    @pytest.mark.unit
    def test_ml_anomaly_detection(self, analysis_engine):
        """Test ML-based anomaly detection"""
        # Create sample data with anomalies
        data = pd.DataFrame({
            'revenue': [100, 110, 120, 50, 130],  # 50 is an anomaly
            'expenses': [80, 85, 90, 95, 100]
        })
        
        anomalies = analysis_engine.detect_ml_anomalies(data)
        assert len(anomalies) > 0
    
    @pytest.mark.unit
    def test_trend_analysis(self, analysis_engine):
        """Test financial trend analysis"""
        data = pd.DataFrame({
            'year': [2020, 2021, 2022, 2023],
            'revenue': [100, 120, 140, 160]
        })
        
        trends = analysis_engine.analyze_trends(data)
        assert 'growth_rate' in trends
        assert trends['growth_rate'] > 0  # Positive growth
    
    @pytest.mark.unit
    def test_confidence_intervals(self, analysis_engine):
        """Test confidence interval calculations"""
        data = np.array([100, 110, 120, 130, 140])
        
        intervals = analysis_engine.calculate_confidence_intervals(data)
        assert 'lower_bound' in intervals
        assert 'upper_bound' in intervals
        assert intervals['lower_bound'] < intervals['upper_bound']