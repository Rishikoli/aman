"""
Unit tests for Operations Agent
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add agents to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'agents'))

from operations.operations_agent import OperationsAgent
from operations.supply_chain_mapper import SupplyChainMapper
from operations.geopolitical_analyzer import GeopoliticalAnalyzer

class TestOperationsAgent:
    
    @pytest.fixture
    def operations_agent(self, mock_env_vars):
        """Create an Operations Agent instance for testing"""
        return OperationsAgent()
    
    @pytest.fixture
    def sample_company_operations(self):
        """Sample company operations data for testing"""
        return {
            'company_name': 'Global Manufacturing Corp',
            'facilities': [
                {
                    'location': 'Detroit, MI, USA',
                    'type': 'manufacturing',
                    'employees': 2000,
                    'capacity': 100000,
                    'coordinates': {'lat': 42.3314, 'lon': -83.0458}
                },
                {
                    'location': 'Shanghai, China',
                    'type': 'manufacturing',
                    'employees': 3000,
                    'capacity': 150000,
                    'coordinates': {'lat': 31.2304, 'lon': 121.4737}
                },
                {
                    'location': 'Munich, Germany',
                    'type': 'r_and_d',
                    'employees': 500,
                    'capacity': None,
                    'coordinates': {'lat': 48.1351, 'lon': 11.5820}
                }
            ],
            'supply_chain': {
                'suppliers': [
                    {'name': 'Steel Corp', 'location': 'Pittsburgh, PA', 'criticality': 'high'},
                    {'name': 'Electronics Ltd', 'location': 'Shenzhen, China', 'criticality': 'medium'},
                    {'name': 'Logistics Inc', 'location': 'Rotterdam, Netherlands', 'criticality': 'high'}
                ],
                'distribution_centers': [
                    {'location': 'Chicago, IL', 'coverage': 'North America'},
                    {'location': 'Hamburg, Germany', 'coverage': 'Europe'},
                    {'location': 'Singapore', 'coverage': 'Asia Pacific'}
                ]
            }
        }
    
    @pytest.mark.unit
    def test_operations_agent_initialization(self, operations_agent):
        """Test Operations Agent initialization"""
        assert operations_agent is not None
        assert hasattr(operations_agent, 'analyze_operations')
    
    @pytest.mark.unit
    def test_supply_chain_risk_assessment(self, operations_agent, sample_company_operations):
        """Test supply chain risk assessment"""
        risk_assessment = operations_agent.assess_supply_chain_risks(sample_company_operations)
        
        assert 'overall_risk_score' in risk_assessment
        assert 'geographic_risks' in risk_assessment
        assert 'supplier_risks' in risk_assessment
        assert 'concentration_risks' in risk_assessment
        assert 0 <= risk_assessment['overall_risk_score'] <= 100
        
        # Verify geographic risk analysis
        assert len(risk_assessment['geographic_risks']) > 0
        for risk in risk_assessment['geographic_risks']:
            assert 'region' in risk
            assert 'risk_level' in risk
            assert 'risk_factors' in risk
    
    @pytest.mark.unit
    @patch('operations.operations_agent.requests.get')
    def test_geopolitical_risk_analysis(self, mock_get, operations_agent):
        """Test geopolitical risk analysis"""
        # Mock World Bank API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {
                'country': {'value': 'China'},
                'date': '2023',
                'value': 65.5  # Political stability score
            },
            {
                'country': {'value': 'Germany'},
                'date': '2023',
                'value': 85.2
            }
        ]
        mock_get.return_value = mock_response
        
        countries = ['China', 'Germany', 'United States']
        geopolitical_risks = operations_agent.analyze_geopolitical_risks(countries)
        
        assert 'country_risks' in geopolitical_risks
        assert 'overall_exposure' in geopolitical_risks
        assert 'risk_mitigation_strategies' in geopolitical_risks
        
        # Verify country-specific risks
        for country in countries:
            if country in [item['country']['value'] for item in mock_response.json.return_value]:
                assert any(risk['country'] == country for risk in geopolitical_risks['country_risks'])
    
    @pytest.mark.unit
    def test_operational_efficiency_scoring(self, operations_agent, sample_company_operations):
        """Test operational efficiency scoring"""
        efficiency_metrics = {
            'capacity_utilization': 0.85,
            'employee_productivity': 120000,  # Revenue per employee
            'facility_efficiency': 0.78,
            'supply_chain_efficiency': 0.82,
            'technology_adoption': 0.75
        }
        
        efficiency_score = operations_agent.calculate_efficiency_score(
            sample_company_operations, 
            efficiency_metrics
        )
        
        assert 'overall_efficiency_score' in efficiency_score
        assert 'efficiency_breakdown' in efficiency_score
        assert 'improvement_opportunities' in efficiency_score
        assert 0 <= efficiency_score['overall_efficiency_score'] <= 100
        
        # Verify breakdown includes all key metrics
        breakdown = efficiency_score['efficiency_breakdown']
        assert 'capacity_utilization' in breakdown
        assert 'employee_productivity' in breakdown
        assert 'supply_chain_efficiency' in breakdown
    
    @pytest.mark.unit
    def test_logistics_optimization_analysis(self, operations_agent, sample_company_operations):
        """Test logistics optimization analysis"""
        logistics_analysis = operations_agent.analyze_logistics_optimization(sample_company_operations)
        
        assert 'current_logistics_cost' in logistics_analysis
        assert 'optimization_opportunities' in logistics_analysis
        assert 'potential_savings' in logistics_analysis
        assert 'implementation_complexity' in logistics_analysis
        
        # Verify optimization opportunities
        opportunities = logistics_analysis['optimization_opportunities']
        assert len(opportunities) > 0
        for opportunity in opportunities:
            assert 'type' in opportunity
            assert 'description' in opportunity
            assert 'estimated_savings' in opportunity
    
    @pytest.mark.unit
    def test_regulatory_compliance_assessment(self, operations_agent, sample_company_operations):
        """Test regulatory compliance assessment"""
        compliance_assessment = operations_agent.assess_regulatory_compliance(sample_company_operations)
        
        assert 'compliance_score' in compliance_assessment
        assert 'jurisdiction_analysis' in compliance_assessment
        assert 'compliance_gaps' in compliance_assessment
        assert 'regulatory_risks' in compliance_assessment
        
        # Verify jurisdiction-specific analysis
        jurisdictions = compliance_assessment['jurisdiction_analysis']
        expected_jurisdictions = ['United States', 'China', 'Germany']
        
        for jurisdiction in expected_jurisdictions:
            jurisdiction_found = any(
                j['jurisdiction'] == jurisdiction for j in jurisdictions
            )
            assert jurisdiction_found, f"Missing analysis for {jurisdiction}"
    
    @pytest.mark.unit
    def test_business_continuity_planning(self, operations_agent, sample_company_operations):
        """Test business continuity planning analysis"""
        continuity_plan = operations_agent.analyze_business_continuity(sample_company_operations)
        
        assert 'continuity_score' in continuity_plan
        assert 'critical_dependencies' in continuity_plan
        assert 'risk_scenarios' in continuity_plan
        assert 'mitigation_strategies' in continuity_plan
        
        # Verify risk scenarios
        scenarios = continuity_plan['risk_scenarios']
        expected_scenario_types = ['natural_disaster', 'geopolitical', 'supply_chain', 'cyber']
        
        for scenario in scenarios:
            assert 'type' in scenario
            assert 'probability' in scenario
            assert 'impact' in scenario
            assert scenario['type'] in expected_scenario_types

class TestSupplyChainMapper:
    
    @pytest.fixture
    def supply_chain_mapper(self):
        """Create Supply Chain Mapper for testing"""
        return SupplyChainMapper()
    
    @pytest.mark.unit
    def test_supply_chain_mapping(self, supply_chain_mapper):
        """Test supply chain network mapping"""
        supply_chain_data = {
            'suppliers': [
                {'name': 'Supplier A', 'location': 'China', 'tier': 1, 'criticality': 'high'},
                {'name': 'Supplier B', 'location': 'Germany', 'tier': 1, 'criticality': 'medium'},
                {'name': 'Supplier C', 'location': 'Mexico', 'tier': 2, 'criticality': 'low'}
            ],
            'manufacturing': [
                {'location': 'United States', 'capacity': 100000},
                {'location': 'India', 'capacity': 75000}
            ],
            'distribution': [
                {'location': 'United States', 'coverage': ['North America']},
                {'location': 'Netherlands', 'coverage': ['Europe', 'Africa']}
            ]
        }
        
        supply_chain_map = supply_chain_mapper.map_supply_chain(supply_chain_data)
        
        assert 'network_topology' in supply_chain_map
        assert 'critical_paths' in supply_chain_map
        assert 'bottlenecks' in supply_chain_map
        assert 'redundancy_analysis' in supply_chain_map
        
        # Verify network topology
        topology = supply_chain_map['network_topology']
        assert 'nodes' in topology
        assert 'connections' in topology
        assert len(topology['nodes']) > 0
    
    @pytest.mark.unit
    def test_supplier_risk_scoring(self, supply_chain_mapper):
        """Test supplier risk scoring"""
        suppliers = [
            {
                'name': 'High Risk Supplier',
                'location': 'High Risk Country',
                'financial_health': 'poor',
                'dependency_level': 'critical',
                'alternative_sources': 0
            },
            {
                'name': 'Low Risk Supplier',
                'location': 'Stable Country',
                'financial_health': 'excellent',
                'dependency_level': 'moderate',
                'alternative_sources': 3
            }
        ]
        
        risk_scores = supply_chain_mapper.score_supplier_risks(suppliers)
        
        assert len(risk_scores) == len(suppliers)
        
        # High risk supplier should have higher risk score
        high_risk_score = next(s['risk_score'] for s in risk_scores if s['name'] == 'High Risk Supplier')
        low_risk_score = next(s['risk_score'] for s in risk_scores if s['name'] == 'Low Risk Supplier')
        
        assert high_risk_score > low_risk_score
        assert 0 <= high_risk_score <= 100
        assert 0 <= low_risk_score <= 100
    
    @pytest.mark.unit
    def test_transportation_route_analysis(self, supply_chain_mapper):
        """Test transportation route analysis"""
        routes = [
            {
                'origin': 'Shanghai, China',
                'destination': 'Los Angeles, USA',
                'mode': 'ocean_freight',
                'distance_km': 11000,
                'transit_time_days': 14,
                'cost_per_unit': 50
            },
            {
                'origin': 'Munich, Germany',
                'destination': 'New York, USA',
                'mode': 'air_freight',
                'distance_km': 6400,
                'transit_time_days': 2,
                'cost_per_unit': 200
            }
        ]
        
        route_analysis = supply_chain_mapper.analyze_transportation_routes(routes)
        
        assert 'route_efficiency' in route_analysis
        assert 'cost_optimization' in route_analysis
        assert 'risk_assessment' in route_analysis
        
        # Verify route-specific analysis
        for route in routes:
            route_key = f"{route['origin']}_to_{route['destination']}"
            assert any(route_key in str(analysis) for analysis in route_analysis.values())

class TestGeopoliticalAnalyzer:
    
    @pytest.fixture
    def geopolitical_analyzer(self):
        """Create Geopolitical Analyzer for testing"""
        return GeopoliticalAnalyzer()
    
    @pytest.mark.unit
    @patch('operations.geopolitical_analyzer.requests.get')
    def test_country_risk_assessment(self, mock_get, geopolitical_analyzer):
        """Test country-specific risk assessment"""
        # Mock World Bank governance indicators
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {
                'country': {'value': 'China'},
                'indicator': {'value': 'Political Stability'},
                'date': '2023',
                'value': 65.5
            }
        ]
        mock_get.return_value = mock_response
        
        country_risk = geopolitical_analyzer.assess_country_risk('China')
        
        assert 'overall_risk_score' in country_risk
        assert 'political_stability' in country_risk
        assert 'economic_indicators' in country_risk
        assert 'regulatory_environment' in country_risk
        assert 0 <= country_risk['overall_risk_score'] <= 100
    
    @pytest.mark.unit
    def test_sanctions_screening(self, geopolitical_analyzer):
        """Test sanctions list screening"""
        entities_to_screen = [
            'Legitimate Business Corp',
            'Sanctioned Entity Ltd',
            'Normal Company Inc'
        ]
        
        with patch.object(geopolitical_analyzer, 'check_sanctions_list') as mock_sanctions:
            mock_sanctions.return_value = {
                'Legitimate Business Corp': {'sanctioned': False, 'risk_level': 'low'},
                'Sanctioned Entity Ltd': {'sanctioned': True, 'risk_level': 'high'},
                'Normal Company Inc': {'sanctioned': False, 'risk_level': 'low'}
            }
            
            sanctions_results = geopolitical_analyzer.screen_sanctions(entities_to_screen)
            
            assert 'screening_results' in sanctions_results
            assert 'high_risk_entities' in sanctions_results
            assert 'compliance_status' in sanctions_results
            
            # Verify high-risk entities identified
            high_risk = sanctions_results['high_risk_entities']
            assert 'Sanctioned Entity Ltd' in [entity['name'] for entity in high_risk]
    
    @pytest.mark.unit
    def test_trade_war_impact_analysis(self, geopolitical_analyzer):
        """Test trade war impact analysis"""
        trade_relationships = [
            {'country_a': 'United States', 'country_b': 'China', 'trade_volume': 500000000000},
            {'country_a': 'United States', 'country_b': 'Germany', 'trade_volume': 200000000000}
        ]
        
        trade_war_analysis = geopolitical_analyzer.analyze_trade_war_impact(trade_relationships)
        
        assert 'impact_assessment' in trade_war_analysis
        assert 'affected_trade_routes' in trade_war_analysis
        assert 'mitigation_strategies' in trade_war_analysis
        
        # Verify impact scoring
        for relationship in trade_relationships:
            relationship_key = f"{relationship['country_a']}_{relationship['country_b']}"
            assert any(relationship_key in str(assessment) for assessment in trade_war_analysis.values())
    
    @pytest.mark.unit
    def test_regulatory_change_monitoring(self, geopolitical_analyzer):
        """Test regulatory change monitoring"""
        jurisdictions = ['United States', 'European Union', 'China']
        
        with patch.object(geopolitical_analyzer, 'fetch_regulatory_updates') as mock_updates:
            mock_updates.return_value = {
                'United States': [
                    {'regulation': 'Export Control Reform', 'impact': 'high', 'effective_date': '2024-01-01'}
                ],
                'European Union': [
                    {'regulation': 'GDPR Update', 'impact': 'medium', 'effective_date': '2024-03-01'}
                ],
                'China': [
                    {'regulation': 'Data Security Law Amendment', 'impact': 'high', 'effective_date': '2024-02-01'}
                ]
            }
            
            regulatory_monitoring = geopolitical_analyzer.monitor_regulatory_changes(jurisdictions)
            
            assert 'regulatory_updates' in regulatory_monitoring
            assert 'impact_assessment' in regulatory_monitoring
            assert 'compliance_timeline' in regulatory_monitoring
            
            # Verify all jurisdictions covered
            for jurisdiction in jurisdictions:
                assert jurisdiction in regulatory_monitoring['regulatory_updates']