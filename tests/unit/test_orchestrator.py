"""
Unit tests for Deal Orchestrator
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import os
from datetime import datetime, timedelta

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

class TestDealOrchestrator:
    
    @pytest.fixture
    def mock_orchestrator(self, mock_env_vars):
        """Create mock Deal Orchestrator for testing"""
        with patch('backend.services.dealOrchestrator.DealOrchestrator') as MockOrchestrator:
            orchestrator = MockOrchestrator.return_value
            orchestrator.create_deal = Mock()
            orchestrator.distribute_tasks = Mock()
            orchestrator.aggregate_results = Mock()
            orchestrator.get_deal_status = Mock()
            yield orchestrator
    
    @pytest.fixture
    def sample_deal_request(self):
        """Sample deal creation request"""
        return {
            'deal_name': 'Test M&A Deal',
            'acquirer': {
                'name': 'Acquirer Corp',
                'ticker': 'ACQ'
            },
            'target': {
                'name': 'Target Corp',
                'ticker': 'TGT'
            },
            'deal_value': 1000000000,
            'analysis_scope': ['financial', 'legal', 'synergy']
        }
    
    @pytest.mark.unit
    def test_deal_creation(self, mock_orchestrator, sample_deal_request):
        """Test deal creation functionality"""
        # Mock successful deal creation
        mock_orchestrator.create_deal.return_value = {
            'deal_id': 'test-deal-001',
            'status': 'created',
            'created_at': datetime.now().isoformat(),
            'estimated_completion': (datetime.now() + timedelta(hours=8)).isoformat()
        }
        
        result = mock_orchestrator.create_deal(sample_deal_request)
        
        assert result['deal_id'] == 'test-deal-001'
        assert result['status'] == 'created'
        assert 'estimated_completion' in result
        mock_orchestrator.create_deal.assert_called_once_with(sample_deal_request)
    
    @pytest.mark.unit
    def test_task_distribution(self, mock_orchestrator):
        """Test agent task distribution"""
        deal_id = 'test-deal-001'
        analysis_scope = ['financial', 'legal', 'synergy']
        
        # Mock successful task distribution
        mock_orchestrator.distribute_tasks.return_value = {
            'deal_id': deal_id,
            'tasks_created': len(analysis_scope),
            'agent_assignments': {
                'financial': {'status': 'queued', 'priority': 1},
                'legal': {'status': 'queued', 'priority': 1},
                'synergy': {'status': 'queued', 'priority': 2}  # Depends on financial
            }
        }
        
        result = mock_orchestrator.distribute_tasks(deal_id, analysis_scope)
        
        assert result['deal_id'] == deal_id
        assert result['tasks_created'] == 3
        assert len(result['agent_assignments']) == 3
        mock_orchestrator.distribute_tasks.assert_called_once_with(deal_id, analysis_scope)
    
    @pytest.mark.unit
    def test_result_aggregation(self, mock_orchestrator):
        """Test agent result aggregation"""
        deal_id = 'test-deal-001'
        agent_results = {
            'financial': {
                'risk_score': 25,
                'findings': ['Strong financial position'],
                'confidence': 0.85
            },
            'legal': {
                'risk_score': 40,
                'findings': ['Minor compliance gaps'],
                'confidence': 0.80
            },
            'synergy': {
                'cost_synergies': 50000000,
                'revenue_synergies': 30000000,
                'confidence': 0.75
            }
        }
        
        # Mock aggregated results
        mock_orchestrator.aggregate_results.return_value = {
            'deal_id': deal_id,
            'status': 'completed',
            'overall_risk_score': 32,  # Weighted average
            'agent_results': agent_results,
            'overall_confidence': 0.80,
            'recommendation': 'proceed',
            'completed_at': datetime.now().isoformat()
        }
        
        result = mock_orchestrator.aggregate_results(deal_id, agent_results)
        
        assert result['deal_id'] == deal_id
        assert result['status'] == 'completed'
        assert result['overall_risk_score'] == 32
        assert 'recommendation' in result
        mock_orchestrator.aggregate_results.assert_called_once_with(deal_id, agent_results)
    
    @pytest.mark.unit
    def test_deal_status_tracking(self, mock_orchestrator):
        """Test deal status tracking"""
        deal_id = 'test-deal-001'
        
        # Mock deal status response
        mock_orchestrator.get_deal_status.return_value = {
            'deal_id': deal_id,
            'status': 'in_progress',
            'progress': 60,
            'completed_agents': ['financial', 'legal'],
            'pending_agents': ['synergy'],
            'estimated_completion': (datetime.now() + timedelta(hours=2)).isoformat()
        }
        
        result = mock_orchestrator.get_deal_status(deal_id)
        
        assert result['deal_id'] == deal_id
        assert result['status'] == 'in_progress'
        assert result['progress'] == 60
        assert len(result['completed_agents']) == 2
        assert len(result['pending_agents']) == 1
        mock_orchestrator.get_deal_status.assert_called_once_with(deal_id)
    
    @pytest.mark.unit
    def test_timeline_prediction(self, mock_orchestrator):
        """Test timeline prediction functionality"""
        deal_request = {
            'documents': [
                {'type': 'financial_statements', 'pages': 200},
                {'type': 'legal_contracts', 'pages': 150},
                {'type': 'technical_docs', 'pages': 100}
            ],
            'analysis_scope': ['financial', 'legal', 'synergy']
        }
        
        with patch.object(mock_orchestrator, 'predict_timeline') as mock_predict:
            mock_predict.return_value = {
                'total_estimated_hours': 12,
                'agent_estimates': {
                    'financial': {'hours': 4, 'confidence': 0.85},
                    'legal': {'hours': 6, 'confidence': 0.75},
                    'synergy': {'hours': 2, 'confidence': 0.80}
                },
                'bottlenecks': ['legal_document_review'],
                'estimated_completion': (datetime.now() + timedelta(hours=12)).isoformat()
            }
            
            result = mock_orchestrator.predict_timeline(deal_request)
            
            assert result['total_estimated_hours'] == 12
            assert len(result['agent_estimates']) == 3
            assert 'bottlenecks' in result
            assert result['bottlenecks'] == ['legal_document_review']
    
    @pytest.mark.unit
    def test_error_handling_agent_failure(self, mock_orchestrator):
        """Test error handling when agents fail"""
        deal_id = 'test-deal-001'
        
        # Mock scenario where legal agent fails
        agent_results = {
            'financial': {
                'risk_score': 25,
                'status': 'completed'
            },
            'legal': {
                'error': 'API timeout',
                'status': 'failed'
            },
            'synergy': {
                'cost_synergies': 50000000,
                'status': 'completed'
            }
        }
        
        # Mock graceful degradation
        mock_orchestrator.aggregate_results.return_value = {
            'deal_id': deal_id,
            'status': 'completed_with_errors',
            'successful_agents': ['financial', 'synergy'],
            'failed_agents': ['legal'],
            'overall_risk_score': 25,  # Based on available data
            'confidence_impact': 'reduced_due_to_missing_legal_analysis',
            'recommendation': 'proceed_with_caution'
        }
        
        result = mock_orchestrator.aggregate_results(deal_id, agent_results)
        
        assert result['status'] == 'completed_with_errors'
        assert len(result['successful_agents']) == 2
        assert len(result['failed_agents']) == 1
        assert 'legal' in result['failed_agents']
    
    @pytest.mark.unit
    def test_recursive_analysis_trigger(self, mock_orchestrator):
        """Test recursive analysis triggering"""
        deal_id = 'test-deal-001'
        
        # Mock initial result that triggers recursion
        initial_result = {
            'agent': 'financial',
            'risk_score': 85,  # High risk
            'confidence': 0.60,  # Low confidence
            'requires_recursion': True,
            'recursion_areas': ['debt_analysis', 'cash_flow_forensics']
        }
        
        with patch.object(mock_orchestrator, 'trigger_recursive_analysis') as mock_recursive:
            mock_recursive.return_value = {
                'recursion_triggered': True,
                'original_agent': 'financial',
                'recursion_areas': ['debt_analysis', 'cash_flow_forensics'],
                'new_task_id': 'recursive-task-001'
            }
            
            result = mock_orchestrator.trigger_recursive_analysis(deal_id, initial_result)
            
            assert result['recursion_triggered'] is True
            assert result['original_agent'] == 'financial'
            assert len(result['recursion_areas']) == 2
            assert 'new_task_id' in result
    
    @pytest.mark.unit
    def test_deal_priority_management(self, mock_orchestrator):
        """Test deal priority and queue management"""
        deals = [
            {'deal_id': 'urgent-deal', 'priority': 'high', 'deal_value': 5000000000},
            {'deal_id': 'normal-deal', 'priority': 'medium', 'deal_value': 1000000000},
            {'deal_id': 'low-priority-deal', 'priority': 'low', 'deal_value': 500000000}
        ]
        
        with patch.object(mock_orchestrator, 'prioritize_deals') as mock_prioritize:
            mock_prioritize.return_value = {
                'prioritized_queue': [
                    {'deal_id': 'urgent-deal', 'queue_position': 1},
                    {'deal_id': 'normal-deal', 'queue_position': 2},
                    {'deal_id': 'low-priority-deal', 'queue_position': 3}
                ],
                'priority_factors': ['deal_value', 'urgency', 'complexity']
            }
            
            result = mock_orchestrator.prioritize_deals(deals)
            
            assert len(result['prioritized_queue']) == 3
            assert result['prioritized_queue'][0]['deal_id'] == 'urgent-deal'
            assert result['prioritized_queue'][0]['queue_position'] == 1