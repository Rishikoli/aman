"""
Test suite for market intelligence functionality.
Tests Google Trends, BuiltWith, and competitive intelligence components.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os
from datetime import datetime

# Add the agents directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from synergy.google_trends_client import GoogleTrendsClient
from synergy.builtwith_client import BuiltWithClient
from synergy.competitive_intelligence import CompetitiveIntelligenceAnalyzer
from synergy.market_intelligence_service import MarketIntelligenceService

class TestGoogleTrendsClient(unittest.TestCase):
    """Test cases for Google Trends client."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.client = GoogleTrendsClient()
    
    @patch('synergy.google_trends_client.TrendReq')
    def test_get_market_interest_success(self, mock_trend_req):
        """Test successful market interest retrieval."""
        # Mock the pytrends response
        mock_pytrends = Mock()
        mock_trend_req.return_value = mock_pytrends
        
        # Mock interest over time data
        import pandas as pd
        mock_data = pd.DataFrame({
            'test_keyword': [50, 60, 70, 80, 90],
            'isPartial': [False, False, False, False, True]
        })
        mock_pytrends.interest_over_time.return_value = mock_data
        mock_pytrends.related_queries.return_value = {}
        mock_pytrends.interest_by_region.return_value = pd.DataFrame()
        
        # Test the method
        result = self.client.get_market_interest(['test_keyword'])
        
        # Assertions
        self.assertIn('keywords', result)
        self.assertIn('trend_analysis', result)
        self.assertEqual(result['keywords'], ['test_keyword'])
    
    def test_validate_revenue_synergies(self):
        """Test revenue synergy validation."""
        with patch.object(self.client, 'get_market_interest') as mock_get_interest:
            # Mock return data
            mock_get_interest.return_value = {
                'trend_analysis': {
                    'synergy_keyword': {
                        'current_interest': 75,
                        'market_momentum': 'strong_positive'
                    }
                }
            }
            
            result = self.client.validate_revenue_synergies(
                ['synergy_keyword'], ['company1', 'company2']
            )
            
            self.assertIn('synergy_score', result)
            self.assertIn('recommendations', result)

class TestBuiltWithClient(unittest.TestCase):
    """Test cases for BuiltWith client."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.client = BuiltWithClient()
    
    @patch('synergy.builtwith_client.builtwith.parse')
    def test_get_tech_stack_success(self, mock_parse):
        """Test successful tech stack retrieval."""
        # Mock builtwith response
        mock_parse.return_value = {
            'web-servers': ['nginx', 'apache'],
            'programming-languages-and-frameworks': ['python', 'javascript'],
            'databases': ['postgresql']
        }
        
        result = self.client.get_tech_stack('example.com')
        
        # Assertions
        self.assertIn('domain', result)
        self.assertIn('technologies', result)
        self.assertIn('analysis', result)
        self.assertEqual(result['domain'], 'example.com')
    
    @patch('synergy.builtwith_client.builtwith.parse')
    def test_compare_tech_stacks(self, mock_parse):
        """Test tech stack comparison."""
        # Mock builtwith responses
        mock_parse.side_effect = [
            {'web-servers': ['nginx'], 'databases': ['postgresql']},
            {'web-servers': ['apache'], 'databases': ['mysql']}
        ]
        
        result = self.client.compare_tech_stacks('domain1.com', 'domain2.com')
        
        # Assertions
        self.assertIn('comparison', result)
        self.assertIn('synergy_opportunities', result)

class TestCompetitiveIntelligenceAnalyzer(unittest.TestCase):
    """Test cases for competitive intelligence analyzer."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = CompetitiveIntelligenceAnalyzer()
    
    @patch('synergy.competitive_intelligence.GoogleTrendsClient')
    @patch('synergy.competitive_intelligence.BuiltWithClient')
    def test_analyze_competitive_position(self, mock_builtwith, mock_trends):
        """Test competitive position analysis."""
        # Mock clients
        mock_trends_instance = Mock()
        mock_builtwith_instance = Mock()
        mock_trends.return_value = mock_trends_instance
        mock_builtwith.return_value = mock_builtwith_instance
        
        # Mock responses
        mock_trends_instance.get_market_interest.return_value = {
            'trend_analysis': {
                'company1': {'current_interest': 60, 'market_momentum': 'moderate_positive'}
            }
        }
        
        mock_builtwith_instance.compare_tech_stacks.return_value = {
            'stack1': {'analysis': {'modernization_level': 'modern', 'tech_complexity': 'medium'}},
            'stack2': {'analysis': {'modernization_level': 'legacy', 'tech_complexity': 'high'}},
            'comparison': {'overlap_percentage': 45, 'integration_complexity': 'medium'}
        }
        
        # Test data
        company1 = {'name': 'Company A', 'domain': 'companya.com', 'keywords': ['keyword1']}
        company2 = {'name': 'Company B', 'domain': 'companyb.com', 'keywords': ['keyword2']}
        industry_keywords = ['industry', 'market']
        
        result = self.analyzer.analyze_competitive_position(company1, company2, industry_keywords)
        
        # Assertions
        self.assertIn('market_positioning', result)
        self.assertIn('technology_positioning', result)
        self.assertIn('competitive_advantages', result)
        self.assertIn('synergy_opportunities', result)

class TestMarketIntelligenceService(unittest.TestCase):
    """Test cases for market intelligence service."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.service = MarketIntelligenceService()
    
    @patch('synergy.market_intelligence_service.GoogleTrendsClient')
    @patch('synergy.market_intelligence_service.BuiltWithClient')
    @patch('synergy.market_intelligence_service.CompetitiveIntelligenceAnalyzer')
    def test_analyze_market_synergies(self, mock_analyzer, mock_builtwith, mock_trends):
        """Test comprehensive market synergy analysis."""
        # Mock all components
        mock_trends_instance = Mock()
        mock_builtwith_instance = Mock()
        mock_analyzer_instance = Mock()
        
        mock_trends.return_value = mock_trends_instance
        mock_builtwith.return_value = mock_builtwith_instance
        mock_analyzer.return_value = mock_analyzer_instance
        
        # Mock responses
        mock_trends_instance.get_market_interest.return_value = {
            'trend_analysis': {'keyword': {'current_interest': 70}},
            'regional_interest': {'US': 80, 'UK': 60}
        }
        
        mock_analyzer_instance.analyze_competitive_position.return_value = {
            'market_positioning': {'market_comparison': {'market_leader': 'balanced'}},
            'technology_positioning': {'tech_stack_comparison': {'comparison': {'overlap_percentage': 55}}}
        }
        
        mock_builtwith_instance.compare_tech_stacks.return_value = {
            'synergy_opportunities': [{'description': 'Test synergy', 'potential_savings': 'high'}]
        }
        
        # Test data
        deal_data = {
            'deal_id': 'test_deal_001',
            'deal_name': 'Test M&A Deal',
            'acquirer': {
                'name': 'Acquirer Corp',
                'domain': 'acquirer.com',
                'keywords': ['acquirer', 'business']
            },
            'target': {
                'name': 'Target Inc',
                'domain': 'target.com',
                'keywords': ['target', 'startup']
            },
            'industry': {
                'keywords': ['technology', 'software', 'saas']
            },
            'synergy_focus': ['integration', 'cross-selling', 'cost-reduction']
        }
        
        result = self.service.analyze_market_synergies(deal_data)
        
        # Assertions
        self.assertIn('deal_id', result)
        self.assertIn('market_trends', result)
        self.assertIn('competitive_positioning', result)
        self.assertIn('synergy_validation', result)
        self.assertIn('recommendations', result)
        self.assertIn('risk_assessment', result)
        self.assertEqual(result['deal_id'], 'test_deal_001')
    
    def test_assess_overall_momentum(self):
        """Test overall market momentum assessment."""
        # Test data with mixed momentum signals
        trends_analysis = {
            'acquirer_trends': {
                'trend_analysis': {
                    'keyword1': {'market_momentum': 'strong_positive'},
                    'keyword2': {'market_momentum': 'moderate_positive'}
                }
            },
            'target_trends': {
                'trend_analysis': {
                    'keyword3': {'market_momentum': 'stable'},
                    'keyword4': {'market_momentum': 'moderate_negative'}
                }
            }
        }
        
        momentum = self.service._assess_overall_momentum(trends_analysis)
        
        # Should be moderate_positive (2 positive out of 4 total = 50%)
        self.assertEqual(momentum, 'moderate_positive')

class TestIntegration(unittest.TestCase):
    """Integration tests for the complete market intelligence system."""
    
    def setUp(self):
        """Set up integration test fixtures."""
        self.service = MarketIntelligenceService()
    
    def test_end_to_end_analysis_with_mocks(self):
        """Test end-to-end analysis with mocked external services."""
        with patch.multiple(
            'synergy.google_trends_client.TrendReq',
            'synergy.builtwith_client.builtwith.parse'
        ) as mocks:
            
            # Mock Google Trends
            mock_pytrends = Mock()
            mocks['TrendReq'].return_value = mock_pytrends
            
            import pandas as pd
            mock_pytrends.interest_over_time.return_value = pd.DataFrame({
                'test': [50, 60, 70],
                'isPartial': [False, False, True]
            })
            mock_pytrends.related_queries.return_value = {}
            mock_pytrends.interest_by_region.return_value = pd.DataFrame({'US': [80]})
            
            # Mock BuiltWith
            mocks['builtwith.parse'].return_value = {
                'web-servers': ['nginx'],
                'programming-languages-and-frameworks': ['python']
            }
            
            # Test data
            deal_data = {
                'deal_id': 'integration_test',
                'acquirer': {'name': 'Test Corp', 'domain': 'test.com'},
                'target': {'name': 'Target Corp', 'domain': 'target.com'},
                'industry': {'keywords': ['tech']},
                'synergy_focus': ['integration']
            }
            
            # This should not raise an exception
            result = self.service.analyze_market_synergies(deal_data)
            
            # Basic validation
            self.assertIsInstance(result, dict)
            self.assertIn('deal_id', result)

if __name__ == '__main__':
    # Configure logging for tests
    import logging
    logging.basicConfig(level=logging.INFO)
    
    # Run tests
    unittest.main(verbosity=2)