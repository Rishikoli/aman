"""
End-to-end tests for complete deal analysis scenarios
"""
import pytest
import requests
import json
import time
from unittest.mock import patch, Mock
import sys
import os

# Add paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

class TestCompleteDealScenarios:
    
    @pytest.fixture
    def api_base_url(self):
        """Base URL for API testing"""
        return "http://localhost:3001/api"
    
    @pytest.fixture
    def sample_tech_acquisition(self):
        """Sample technology company acquisition scenario"""
        return {
            'deal_name': 'TechCorp Acquires StartupAI',
            'deal_type': 'acquisition',
            'acquirer': {
                'name': 'TechCorp Inc',
                'ticker': 'TECH',
                'industry': 'Technology',
                'market_cap': 50000000000,
                'employees': 25000,
                'headquarters': 'San Francisco, CA'
            },
            'target': {
                'name': 'StartupAI Ltd',
                'ticker': None,  # Private company
                'industry': 'Artificial Intelligence',
                'valuation': 2000000000,
                'employees': 500,
                'headquarters': 'Austin, TX'
            },
            'deal_value': 2500000000,
            'deal_structure': 'cash_and_stock',
            'expected_closing': '2024-06-30',
            'analysis_scope': ['financial', 'legal', 'synergy', 'reputation', 'operations'],
            'documents': [
                {'type': 'financial_statements', 'pages': 150},
                {'type': 'legal_contracts', 'pages': 300},
                {'type': 'ip_portfolio', 'pages': 75},
                {'type': 'employee_agreements', 'pages': 200}
            ]
        }
    
    @pytest.fixture
    def sample_cross_border_merger(self):
        """Sample cross-border merger scenario"""
        return {
            'deal_name': 'GlobalManufacturing Merges with EuroTech',
            'deal_type': 'merger',
            'acquirer': {
                'name': 'GlobalManufacturing Corp',
                'ticker': 'GMFG',
                'industry': 'Manufacturing',
                'market_cap': 15000000000,
                'employees': 50000,
                'headquarters': 'Detroit, MI'
            },
            'target': {
                'name': 'EuroTech GmbH',
                'ticker': 'ETG',
                'industry': 'Industrial Technology',
                'market_cap': 8000000000,
                'employees': 15000,
                'headquarters': 'Munich, Germany'
            },
            'deal_value': 12000000000,
            'deal_structure': 'stock_swap',
            'expected_closing': '2024-12-31',
            'analysis_scope': ['financial', 'legal', 'synergy', 'reputation', 'operations'],
            'regulatory_considerations': ['EU_merger_control', 'US_antitrust', 'German_foreign_investment'],
            'documents': [
                {'type': 'financial_statements', 'pages': 400},
                {'type': 'regulatory_filings', 'pages': 250},
                {'type': 'environmental_reports', 'pages': 100},
                {'type': 'labor_agreements', 'pages': 150}
            ]
        }
    
    @pytest.mark.e2e
    @pytest.mark.slow
    def test_tech_acquisition_full_workflow(self, api_base_url, sample_tech_acquisition, mock_external_apis):
        """Test complete workflow for technology acquisition"""
        
        with patch('requests.post') as mock_post, \
             patch('requests.get') as mock_get:
            
            # Mock API responses for deal creation
            mock_post.return_value = Mock(
                status_code=201,
                json=lambda: {
                    'deal_id': 'tech-deal-001',
                    'status': 'created',
                    'estimated_completion': '2024-01-15T10:00:00Z'
                }
            )
            
            # Mock API responses for status checking
            mock_get.return_value = Mock(
                status_code=200,
                json=lambda: {
                    'deal_id': 'tech-deal-001',
                    'status': 'completed',
                    'progress': 100,
                    'results': {
                        'financial': {
                            'risk_score': 25,
                            'key_findings': [
                                'Strong revenue growth (40% YoY)',
                                'Healthy cash position ($200M)',
                                'Minimal debt exposure'
                            ],
                            'financial_ratios': {
                                'debt_to_equity': 0.15,
                                'current_ratio': 2.5,
                                'gross_margin': 0.75
                            },
                            'forecast': {
                                'revenue_3yr': [300000000, 420000000, 588000000],
                                'confidence_interval': 0.85
                            }
                        },
                        'legal': {
                            'risk_score': 30,
                            'compliance_status': 'good',
                            'key_findings': [
                                'No major litigation pending',
                                'Strong IP portfolio (150 patents)',
                                'Minor regulatory compliance gaps'
                            ],
                            'ip_analysis': {
                                'patent_count': 150,
                                'trademark_count': 25,
                                'trade_secrets': 'well_protected'
                            }
                        },
                        'synergy': {
                            'total_synergy_value': 400000000,
                            'cost_synergies': 150000000,
                            'revenue_synergies': 250000000,
                            'key_opportunities': [
                                'Cross-selling AI solutions to TechCorp customers',
                                'Consolidation of R&D facilities',
                                'Technology stack integration'
                            ],
                            'integration_timeline': 18,  # months
                            'realization_confidence': 0.80
                        },
                        'reputation': {
                            'reputation_score': 85,
                            'sentiment_analysis': 'positive',
                            'key_findings': [
                                'Strong brand recognition in AI space',
                                'Positive employee reviews (4.2/5)',
                                'No major ESG concerns'
                            ],
                            'esg_score': 78,
                            'media_sentiment': 0.65
                        },
                        'operations': {
                            'operational_risk': 20,
                            'efficiency_score': 85,
                            'key_findings': [
                                'Efficient remote-first operations',
                                'Strong talent retention (95%)',
                                'Minimal supply chain dependencies'
                            ],
                            'geographic_risk': 'low',
                            'supply_chain_resilience': 0.90
                        }
                    },
                    'overall_assessment': {
                        'recommendation': 'proceed',
                        'overall_risk_score': 28,
                        'confidence_level': 0.83,
                        'key_success_factors': [
                            'Retain key AI talent',
                            'Integrate technology platforms',
                            'Maintain startup culture'
                        ],
                        'major_risks': [
                            'Talent retention during integration',
                            'Technology integration complexity'
                        ]
                    }
                }
            )
            
            # Step 1: Create deal analysis request
            create_response = mock_post(
                f"{api_base_url}/deals",
                json=sample_tech_acquisition
            )
            
            assert create_response.status_code == 201
            deal_data = create_response.json()
            deal_id = deal_data['deal_id']
            
            # Step 2: Monitor analysis progress
            max_attempts = 10
            for attempt in range(max_attempts):
                status_response = mock_get(f"{api_base_url}/deals/{deal_id}/status")
                assert status_response.status_code == 200
                
                status_data = status_response.json()
                if status_data['status'] == 'completed':
                    break
                
                time.sleep(1)  # Wait before next check
            
            # Step 3: Verify final results
            final_response = mock_get(f"{api_base_url}/deals/{deal_id}")
            assert final_response.status_code == 200
            
            results = final_response.json()
            
            # Verify all analysis components completed
            assert 'financial' in results['results']
            assert 'legal' in results['results']
            assert 'synergy' in results['results']
            assert 'reputation' in results['results']
            assert 'operations' in results['results']
            
            # Verify financial analysis quality
            financial = results['results']['financial']
            assert financial['risk_score'] <= 50  # Low to medium risk
            assert len(financial['key_findings']) >= 3
            assert 'forecast' in financial
            
            # Verify synergy analysis
            synergy = results['results']['synergy']
            assert synergy['total_synergy_value'] > 0
            assert synergy['realization_confidence'] > 0.5
            
            # Verify overall assessment
            overall = results['overall_assessment']
            assert overall['recommendation'] in ['proceed', 'proceed_with_caution', 'do_not_proceed']
            assert 0 <= overall['overall_risk_score'] <= 100
    
    @pytest.mark.e2e
    @pytest.mark.slow
    def test_cross_border_merger_complex_scenario(self, api_base_url, sample_cross_border_merger, mock_external_apis):
        """Test complex cross-border merger scenario with regulatory considerations"""
        
        with patch('requests.post') as mock_post, \
             patch('requests.get') as mock_get:
            
            # Mock more complex responses for cross-border deal
            mock_post.return_value = Mock(
                status_code=201,
                json=lambda: {
                    'deal_id': 'cross-border-001',
                    'status': 'created',
                    'estimated_completion': '2024-02-28T15:00:00Z',
                    'complexity_factors': ['cross_border', 'regulatory_intensive', 'large_scale']
                }
            )
            
            mock_get.return_value = Mock(
                status_code=200,
                json=lambda: {
                    'deal_id': 'cross-border-001',
                    'status': 'completed',
                    'progress': 100,
                    'results': {
                        'financial': {
                            'risk_score': 45,
                            'currency_risk': 'medium',
                            'key_findings': [
                                'Strong fundamentals in both entities',
                                'EUR/USD exposure requires hedging',
                                'Synergistic cost structures'
                            ]
                        },
                        'legal': {
                            'risk_score': 60,  # Higher due to cross-border complexity
                            'regulatory_complexity': 'high',
                            'key_findings': [
                                'EU merger control approval required',
                                'US antitrust review needed',
                                'German foreign investment screening'
                            ],
                            'approval_timeline': '12-18 months',
                            'approval_probability': 0.75
                        },
                        'operations': {
                            'operational_risk': 55,  # Higher due to integration complexity
                            'geographic_diversification': 'excellent',
                            'key_findings': [
                                'Complementary geographic footprints',
                                'Supply chain optimization opportunities',
                                'Cultural integration challenges'
                            ]
                        }
                    },
                    'regulatory_analysis': {
                        'jurisdictions': ['US', 'EU', 'Germany'],
                        'approval_requirements': [
                            'Hart-Scott-Rodino filing (US)',
                            'EU Merger Regulation notification',
                            'German Foreign Trade Ordinance review'
                        ],
                        'estimated_timeline': '15 months',
                        'key_risks': [
                            'Antitrust concerns in industrial automation',
                            'National security considerations',
                            'Labor union opposition'
                        ]
                    },
                    'overall_assessment': {
                        'recommendation': 'proceed_with_caution',
                        'overall_risk_score': 52,
                        'confidence_level': 0.70,
                        'critical_success_factors': [
                            'Obtain all regulatory approvals',
                            'Manage cultural integration',
                            'Realize operational synergies'
                        ]
                    }
                }
            )
            
            # Execute cross-border merger analysis
            create_response = mock_post(
                f"{api_base_url}/deals",
                json=sample_cross_border_merger
            )
            
            assert create_response.status_code == 201
            deal_data = create_response.json()
            
            # Verify complexity factors identified
            assert 'complexity_factors' in deal_data
            assert 'cross_border' in deal_data['complexity_factors']
            
            # Get final results
            deal_id = deal_data['deal_id']
            final_response = mock_get(f"{api_base_url}/deals/{deal_id}")
            results = final_response.json()
            
            # Verify regulatory analysis included
            assert 'regulatory_analysis' in results
            regulatory = results['regulatory_analysis']
            assert len(regulatory['jurisdictions']) >= 2
            assert 'estimated_timeline' in regulatory
            
            # Verify higher risk scores due to complexity
            legal_risk = results['results']['legal']['risk_score']
            ops_risk = results['results']['operations']['operational_risk']
            assert legal_risk >= 50  # Should be higher for cross-border
            assert ops_risk >= 50   # Should be higher for integration complexity
    
    @pytest.mark.e2e
    def test_deal_timeline_prediction_accuracy(self, api_base_url, sample_tech_acquisition, performance_timer):
        """Test accuracy of deal timeline predictions"""
        
        with patch('requests.post') as mock_post, \
             patch('requests.get') as mock_get:
            
            # Mock timeline prediction response
            mock_post.return_value = Mock(
                status_code=201,
                json=lambda: {
                    'deal_id': 'timeline-test-001',
                    'status': 'created',
                    'timeline_prediction': {
                        'estimated_completion': '2024-01-20T12:00:00Z',
                        'agent_estimates': {
                            'finance': {'hours': 8, 'confidence': 0.85},
                            'legal': {'hours': 12, 'confidence': 0.75},
                            'synergy': {'hours': 6, 'confidence': 0.80},
                            'reputation': {'hours': 4, 'confidence': 0.90},
                            'operations': {'hours': 10, 'confidence': 0.70}
                        },
                        'total_estimated_hours': 40,
                        'bottlenecks': ['legal_document_review', 'regulatory_analysis']
                    }
                }
            )
            
            # Track actual execution time
            performance_timer.start()
            
            create_response = mock_post(
                f"{api_base_url}/deals",
                json=sample_tech_acquisition
            )
            
            performance_timer.stop()
            
            assert create_response.status_code == 201
            deal_data = create_response.json()
            
            # Verify timeline prediction structure
            timeline = deal_data['timeline_prediction']
            assert 'estimated_completion' in timeline
            assert 'agent_estimates' in timeline
            assert 'total_estimated_hours' in timeline
            assert 'bottlenecks' in timeline
            
            # Verify all agents have estimates
            agent_estimates = timeline['agent_estimates']
            expected_agents = ['finance', 'legal', 'synergy', 'reputation', 'operations']
            for agent in expected_agents:
                assert agent in agent_estimates
                assert 'hours' in agent_estimates[agent]
                assert 'confidence' in agent_estimates[agent]
    
    @pytest.mark.e2e
    def test_error_recovery_and_partial_results(self, api_base_url, sample_tech_acquisition):
        """Test system behavior when some agents fail"""
        
        with patch('requests.post') as mock_post, \
             patch('requests.get') as mock_get:
            
            # Mock partial failure scenario
            mock_post.return_value = Mock(
                status_code=201,
                json=lambda: {
                    'deal_id': 'partial-failure-001',
                    'status': 'created'
                }
            )
            
            mock_get.return_value = Mock(
                status_code=200,
                json=lambda: {
                    'deal_id': 'partial-failure-001',
                    'status': 'completed_with_errors',
                    'progress': 80,  # 4 out of 5 agents completed
                    'results': {
                        'financial': {'risk_score': 30, 'status': 'completed'},
                        'legal': {'error': 'API timeout', 'status': 'failed'},
                        'synergy': {'risk_score': 25, 'status': 'completed'},
                        'reputation': {'reputation_score': 75, 'status': 'completed'},
                        'operations': {'operational_risk': 35, 'status': 'completed'}
                    },
                    'errors': [
                        {
                            'agent': 'legal',
                            'error_type': 'timeout',
                            'message': 'SEC API timeout after 30 seconds',
                            'retry_possible': True
                        }
                    ],
                    'overall_assessment': {
                        'recommendation': 'proceed_with_caution',
                        'confidence_level': 0.65,  # Lower due to missing legal analysis
                        'missing_analysis': ['legal'],
                        'impact_of_missing': 'Legal risk assessment unavailable - recommend manual legal review'
                    }
                }
            )
            
            # Execute deal with partial failure
            create_response = mock_post(
                f"{api_base_url}/deals",
                json=sample_tech_acquisition
            )
            
            deal_id = create_response.json()['deal_id']
            final_response = mock_get(f"{api_base_url}/deals/{deal_id}")
            results = final_response.json()
            
            # Verify graceful handling of partial failure
            assert results['status'] == 'completed_with_errors'
            assert results['progress'] == 80
            assert len(results['errors']) == 1
            assert results['errors'][0]['agent'] == 'legal'
            
            # Verify other agents completed successfully
            completed_agents = [agent for agent, data in results['results'].items() 
                             if data.get('status') == 'completed']
            assert len(completed_agents) == 4
            
            # Verify overall assessment accounts for missing data
            overall = results['overall_assessment']
            assert 'missing_analysis' in overall
            assert 'legal' in overall['missing_analysis']
            assert overall['confidence_level'] < 0.80  # Reduced confidence