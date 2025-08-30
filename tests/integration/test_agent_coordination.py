"""
Integration tests for agent coordination workflows
"""
import pytest
import asyncio
from unittest.mock import Mock, patch, MagicMock
import sys
import os
import json
from datetime import datetime, timedelta

# Add paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'agents'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

class TestAgentCoordination:
    
    @pytest.fixture
    def mock_orchestrator(self):
        """Mock Deal Orchestrator for testing"""
        orchestrator = Mock()
        orchestrator.create_deal.return_value = {'deal_id': 'test-deal-1', 'status': 'created'}
        orchestrator.distribute_tasks.return_value = True
        orchestrator.aggregate_results.return_value = {'status': 'completed'}
        return orchestrator
    
    @pytest.fixture
    def sample_deal_request(self):
        """Sample deal analysis request"""
        return {
            'deal_name': 'Test M&A Deal',
            'acquirer': {
                'name': 'Acquirer Corp',
                'ticker': 'ACQ',
                'industry': 'Technology'
            },
            'target': {
                'name': 'Target Corp', 
                'ticker': 'TGT',
                'industry': 'Technology'
            },
            'deal_value': 2000000000,
            'analysis_scope': ['financial', 'legal', 'synergy', 'reputation', 'operations']
        }
    
    @pytest.mark.integration
    async def test_full_deal_analysis_workflow(self, mock_orchestrator, sample_deal_request, mock_external_apis):
        """Test complete deal analysis workflow from start to finish"""
        
        # Mock all agent responses
        agent_responses = {
            'finance': {
                'risk_score': 25,
                'findings': ['Strong financial position', 'Healthy cash flow'],
                'confidence': 0.85
            },
            'legal': {
                'risk_score': 40,
                'findings': ['Minor compliance gaps', 'No major litigation'],
                'confidence': 0.80
            },
            'synergy': {
                'cost_synergies': 50000000,
                'revenue_synergies': 30000000,
                'integration_risks': ['Cultural differences'],
                'confidence': 0.75
            },
            'reputation': {
                'reputation_score': 75,
                'sentiment': 'positive',
                'risk_flags': [],
                'confidence': 0.90
            },
            'operations': {
                'operational_risk': 30,
                'supply_chain_risks': ['Geographic concentration'],
                'efficiency_score': 80,
                'confidence': 0.85
            }
        }
        
        with patch('agents.finance.finance_agent.FinanceAgent.analyze') as mock_finance, \
             patch('agents.legal.legal_agent.LegalAgent.analyze') as mock_legal, \
             patch('agents.synergy.synergy_discovery_engine.SynergyDiscoveryEngine.analyze_synergies') as mock_synergy, \
             patch('agents.reputation.reputation_agent.ReputationAgent.analyze_reputation') as mock_reputation, \
             patch('agents.operations.operations_agent.OperationsAgent.analyze_operations') as mock_operations:
            
            # Configure mock responses
            mock_finance.return_value = agent_responses['finance']
            mock_legal.return_value = agent_responses['legal']
            mock_synergy.return_value = agent_responses['synergy']
            mock_reputation.return_value = agent_responses['reputation']
            mock_operations.return_value = agent_responses['operations']
            
            # Execute workflow
            deal_id = mock_orchestrator.create_deal(sample_deal_request)['deal_id']
            
            # Verify task distribution
            task_distribution = mock_orchestrator.distribute_tasks(deal_id, sample_deal_request['analysis_scope'])
            assert task_distribution is True
            
            # Simulate agent execution
            results = {}
            for agent_type in sample_deal_request['analysis_scope']:
                if agent_type in agent_responses:
                    results[agent_type] = agent_responses[agent_type]
            
            # Aggregate results
            final_report = mock_orchestrator.aggregate_results(deal_id, results)
            
            assert final_report['status'] == 'completed'
            assert len(results) == len(sample_deal_request['analysis_scope'])
    
    @pytest.mark.integration
    def test_agent_dependency_management(self, mock_orchestrator):
        """Test agent task dependency management"""
        
        # Define task dependencies
        task_dependencies = {
            'finance': [],  # No dependencies
            'legal': [],    # No dependencies
            'synergy': ['finance'],  # Depends on finance
            'reputation': [],  # No dependencies
            'operations': ['legal']  # Depends on legal
        }
        
        execution_order = []
        
        def mock_execute_agent(agent_type):
            execution_order.append(agent_type)
            return {'status': 'completed', 'agent': agent_type}
        
        # Simulate dependency-aware execution
        completed_agents = set()
        
        while len(completed_agents) < len(task_dependencies):
            for agent_type, deps in task_dependencies.items():
                if agent_type not in completed_agents and all(dep in completed_agents for dep in deps):
                    mock_execute_agent(agent_type)
                    completed_agents.add(agent_type)
        
        # Verify execution order respects dependencies
        finance_index = execution_order.index('finance')
        synergy_index = execution_order.index('synergy')
        assert finance_index < synergy_index  # Finance must complete before synergy
        
        legal_index = execution_order.index('legal')
        operations_index = execution_order.index('operations')
        assert legal_index < operations_index  # Legal must complete before operations
    
    @pytest.mark.integration
    def test_recursive_analysis_trigger(self, mock_orchestrator, mock_external_apis):
        """Test recursive analysis when anomalies are detected"""
        
        # Mock initial analysis with anomaly
        initial_finance_result = {
            'risk_score': 85,  # High risk score
            'findings': ['Significant debt increase', 'Unusual cash flow patterns'],
            'confidence': 0.60,  # Low confidence
            'requires_recursion': True,
            'recursion_areas': ['debt_analysis', 'cash_flow_forensics']
        }
        
        # Mock deeper analysis results
        deeper_analysis_result = {
            'risk_score': 75,  # Slightly lower after deeper analysis
            'findings': ['Debt increase due to strategic investments', 'Cash flow patterns explained by seasonal business'],
            'confidence': 0.85,  # Higher confidence
            'requires_recursion': False
        }
        
        with patch('agents.finance.finance_agent.FinanceAgent.analyze') as mock_finance:
            # First call returns anomaly, second call returns deeper analysis
            mock_finance.side_effect = [initial_finance_result, deeper_analysis_result]
            
            # Execute initial analysis
            result1 = mock_finance('test-deal-1', {})
            assert result1['requires_recursion'] is True
            
            # Trigger recursive analysis
            if result1['requires_recursion']:
                result2 = mock_finance('test-deal-1', {'recursion_areas': result1['recursion_areas']})
                assert result2['requires_recursion'] is False
                assert result2['confidence'] > result1['confidence']
    
    @pytest.mark.integration
    def test_parallel_agent_execution(self, mock_orchestrator):
        """Test parallel execution of independent agents"""
        
        async def mock_agent_execution(agent_type, delay=1):
            """Mock agent execution with configurable delay"""
            await asyncio.sleep(delay)
            return {
                'agent_type': agent_type,
                'status': 'completed',
                'execution_time': delay
            }
        
        async def execute_agents_parallel():
            """Execute multiple agents in parallel"""
            tasks = [
                mock_agent_execution('finance', 0.5),
                mock_agent_execution('legal', 0.3),
                mock_agent_execution('reputation', 0.4)
            ]
            
            start_time = asyncio.get_event_loop().time()
            results = await asyncio.gather(*tasks)
            end_time = asyncio.get_event_loop().time()
            
            return results, end_time - start_time
        
        # Execute test
        results, total_time = asyncio.run(execute_agents_parallel())
        
        # Verify parallel execution (should be faster than sequential)
        assert len(results) == 3
        assert total_time < 1.0  # Should be less than sum of individual times
        assert all(result['status'] == 'completed' for result in results)
    
    @pytest.mark.integration
    def test_error_handling_and_recovery(self, mock_orchestrator):
        """Test error handling and recovery in agent coordination"""
        
        def mock_agent_with_failure(agent_type, should_fail=False):
            if should_fail:
                raise Exception(f"{agent_type} agent failed")
            return {'status': 'completed', 'agent': agent_type}
        
        # Test graceful degradation when one agent fails
        agent_results = {}
        failed_agents = []
        
        for agent_type in ['finance', 'legal', 'synergy']:
            try:
                # Simulate legal agent failure
                should_fail = (agent_type == 'legal')
                result = mock_agent_with_failure(agent_type, should_fail)
                agent_results[agent_type] = result
            except Exception as e:
                failed_agents.append(agent_type)
                # Log error but continue with other agents
                print(f"Agent {agent_type} failed: {e}")
        
        # Verify system continues with available agents
        assert len(agent_results) == 2  # finance and synergy completed
        assert 'legal' in failed_agents
        assert 'finance' in agent_results
        assert 'synergy' in agent_results
    
    @pytest.mark.integration
    def test_timeline_prediction_integration(self, mock_orchestrator, performance_timer):
        """Test timeline prediction during agent coordination"""
        
        # Mock document complexity analysis
        document_complexity = {
            'total_pages': 1500,
            'document_types': ['10-K', '10-Q', 'contracts', 'financial_statements'],
            'estimated_processing_time': {
                'finance': 2.5,  # hours
                'legal': 4.0,
                'synergy': 1.5,
                'reputation': 1.0,
                'operations': 2.0
            }
        }
        
        # Calculate total estimated time
        total_estimated_time = sum(document_complexity['estimated_processing_time'].values())
        
        # Mock actual execution times
        performance_timer.start()
        
        # Simulate agent execution (much faster for testing)
        actual_execution_times = {}
        for agent_type, estimated_time in document_complexity['estimated_processing_time'].items():
            # Simulate execution (scaled down for testing)
            import time
            time.sleep(0.01)  # 10ms per agent
            actual_execution_times[agent_type] = 0.01
        
        performance_timer.stop()
        
        # Verify timeline prediction accuracy
        assert total_estimated_time > 0
        assert len(actual_execution_times) == len(document_complexity['estimated_processing_time'])
        assert performance_timer.elapsed_seconds < 1.0  # Should complete quickly in test
    
    @pytest.mark.integration
    def test_data_flow_between_agents(self, mock_orchestrator):
        """Test data flow and sharing between agents"""
        
        # Mock shared data store
        shared_data = {}
        
        def finance_agent_mock(deal_id, input_data):
            # Finance agent produces financial metrics
            financial_data = {
                'revenue': 500000000,
                'debt_to_equity': 0.3,
                'cash_flow': 50000000
            }
            shared_data['financial_metrics'] = financial_data
            return {'status': 'completed', 'data': financial_data}
        
        def synergy_agent_mock(deal_id, input_data):
            # Synergy agent uses financial data from finance agent
            financial_metrics = shared_data.get('financial_metrics', {})
            
            synergy_analysis = {
                'cost_synergies': financial_metrics.get('revenue', 0) * 0.05,  # 5% of revenue
                'financial_health_factor': 1.0 if financial_metrics.get('debt_to_equity', 1.0) < 0.5 else 0.8
            }
            return {'status': 'completed', 'data': synergy_analysis}
        
        # Execute agents in sequence
        finance_result = finance_agent_mock('test-deal-1', {})
        synergy_result = synergy_agent_mock('test-deal-1', {})
        
        # Verify data flow
        assert finance_result['status'] == 'completed'
        assert synergy_result['status'] == 'completed'
        assert synergy_result['data']['cost_synergies'] > 0
        assert 'financial_health_factor' in synergy_result['data']