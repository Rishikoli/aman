"""
Unit tests for Synergy Agent
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add agents to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'agents'))

from synergy.synergy_discovery_engine import SynergyDiscoveryEngine
from synergy.market_intelligence_service import MarketIntelligenceService

class TestSynergyAgent:
    
    @pytest.fixture
    def synergy_engine(self, mock_env_vars):
        """Create Synergy Discovery Engine for testing"""
        return SynergyDiscoveryEngine()
    
    @pytest.fixture
    def sample_company_profiles(self):
        """Sample company profiles for synergy analysis"""
        return {
            'acquirer': {
                'name': 'Acquirer Corp',
                'industry': 'Technology',
                'employees': 10000,
                'revenue': 1000000000,
                'locations': ['San Francisco', 'New York'],
                'tech_stack': ['Python', 'React', 'AWS'],
                'departments': ['Engineering', 'Sales', 'Marketing', 'HR']
            },
            'target': {
                'name': 'Target Corp',
                'industry': 'Technology',
                'employees': 2000,
                'revenue': 200000000,
                'locations': ['Austin', 'Seattle'],
                'tech_stack': ['Java', 'Angular', 'Azure'],
                'departments': ['Engineering', 'Sales', 'Support', 'HR']
            }
        }
    
    @pytest.mark.unit
    def test_synergy_engine_initialization(self, synergy_engine):
        """Test Synergy Engine initialization"""
        assert synergy_engine is not None
        assert hasattr(synergy_engine, 'analyze_synergies')
    
    @pytest.mark.unit
    def test_cost_synergy_identification(self, synergy_engine, sample_company_profiles):
        """Test cost synergy identification"""
        cost_synergies = synergy_engine.identify_cost_synergies(
            sample_company_profiles['acquirer'],
            sample_company_profiles['target']
        )
        
        assert 'personnel_synergies' in cost_synergies
        assert 'technology_synergies' in cost_synergies
        assert 'facility_synergies' in cost_synergies
        assert 'operational_synergies' in cost_synergies
        
        # Check that synergies have required fields
        for synergy_type in cost_synergies.values():
            if synergy_type:  # If synergies exist
                assert 'estimated_savings' in synergy_type[0]
                assert 'confidence_level' in synergy_type[0]
    
    @pytest.mark.unit
    def test_revenue_synergy_identification(self, synergy_engine, sample_company_profiles):
        """Test revenue synergy identification"""
        revenue_synergies = synergy_engine.identify_revenue_synergies(
            sample_company_profiles['acquirer'],
            sample_company_profiles['target']
        )
        
        assert 'cross_selling' in revenue_synergies
        assert 'market_expansion' in revenue_synergies
        assert 'product_bundling' in revenue_synergies
        
        # Verify revenue synergy calculations
        for synergy in revenue_synergies.values():
            if synergy:
                assert 'potential_revenue' in synergy
                assert 'time_to_realize' in synergy
    
    @pytest.mark.unit
    def test_integration_risk_assessment(self, synergy_engine, sample_company_profiles):
        """Test integration risk assessment"""
        risks = synergy_engine.assess_integration_risks(
            sample_company_profiles['acquirer'],
            sample_company_profiles['target']
        )
        
        assert 'cultural_risks' in risks
        assert 'technical_risks' in risks
        assert 'operational_risks' in risks
        assert 'regulatory_risks' in risks
        
        # Check risk scoring
        for risk_category in risks.values():
            assert 'risk_score' in risk_category
            assert 0 <= risk_category['risk_score'] <= 100
    
    @pytest.mark.unit
    def test_synergy_value_calculation(self, synergy_engine):
        """Test synergy value calculations"""
        synergy_data = {
            'cost_savings': 10000000,  # $10M
            'revenue_upside': 5000000,  # $5M
            'integration_costs': 2000000,  # $2M
            'time_to_realize': 24  # months
        }
        
        npv = synergy_engine.calculate_synergy_npv(synergy_data)
        
        assert 'net_present_value' in npv
        assert 'payback_period' in npv
        assert 'irr' in npv
        assert npv['net_present_value'] > 0
    
    @pytest.mark.unit
    @patch('synergy.synergy_discovery_engine.requests.get')
    def test_market_analysis_integration(self, mock_get, synergy_engine):
        """Test market analysis for synergy validation"""
        # Mock market data response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'market_size': 50000000000,
            'growth_rate': 0.15,
            'competitive_landscape': ['Competitor1', 'Competitor2']
        }
        mock_get.return_value = mock_response
        
        market_analysis = synergy_engine.analyze_market_opportunity('Technology')
        
        assert 'market_size' in market_analysis
        assert 'growth_rate' in market_analysis
        assert market_analysis['market_size'] > 0

class TestMarketIntelligenceService:
    
    @pytest.fixture
    def market_service(self):
        """Create Market Intelligence Service for testing"""
        return MarketIntelligenceService()
    
    @pytest.mark.unit
    @patch('synergy.market_intelligence_service.pytrends.TrendReq')
    def test_google_trends_analysis(self, mock_trends, market_service):
        """Test Google Trends analysis"""
        # Mock trends data
        mock_trends_instance = Mock()
        mock_trends_instance.interest_over_time.return_value = Mock()
        mock_trends.return_value = mock_trends_instance
        
        trends = market_service.analyze_market_trends(['AI', 'Machine Learning'])
        
        assert trends is not None
        mock_trends.assert_called_once()
    
    @pytest.mark.unit
    @patch('synergy.market_intelligence_service.requests.get')
    def test_competitive_analysis(self, mock_get, market_service):
        """Test competitive landscape analysis"""
        # Mock competitive data
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'competitors': [
                {'name': 'Competitor A', 'market_share': 0.25},
                {'name': 'Competitor B', 'market_share': 0.15}
            ]
        }
        mock_get.return_value = mock_response
        
        competitive_analysis = market_service.analyze_competitive_landscape('Technology')
        
        assert 'competitors' in competitive_analysis
        assert len(competitive_analysis['competitors']) > 0
    
    @pytest.mark.unit
    def test_synergy_opportunity_scoring(self, market_service):
        """Test synergy opportunity scoring algorithm"""
        opportunity_data = {
            'market_size': 1000000000,
            'growth_rate': 0.20,
            'competitive_intensity': 0.60,
            'technical_feasibility': 0.80,
            'time_to_market': 12
        }
        
        score = market_service.score_synergy_opportunity(opportunity_data)
        
        assert 0 <= score <= 100
        assert isinstance(score, (int, float))
    
    @pytest.mark.unit
    def test_cross_selling_potential(self, market_service):
        """Test cross-selling potential analysis"""
        customer_data = {
            'acquirer_customers': 100000,
            'target_customers': 20000,
            'overlap_percentage': 0.15,
            'product_compatibility': 0.85
        }
        
        cross_sell_potential = market_service.calculate_cross_selling_potential(customer_data)
        
        assert 'potential_revenue' in cross_sell_potential
        assert 'addressable_customers' in cross_sell_potential
        assert cross_sell_potential['potential_revenue'] > 0
    
    @pytest.mark.unit
    def test_market_expansion_analysis(self, market_service):
        """Test market expansion opportunity analysis"""
        expansion_data = {
            'current_markets': ['US', 'Canada'],
            'target_markets': ['UK', 'Germany', 'France'],
            'market_entry_costs': 5000000,
            'expected_revenue': 50000000
        }
        
        expansion_analysis = market_service.analyze_market_expansion(expansion_data)
        
        assert 'expansion_score' in expansion_analysis
        assert 'roi_projection' in expansion_analysis
        assert 'risk_factors' in expansion_analysis