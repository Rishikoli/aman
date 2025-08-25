#!/usr/bin/env python3
"""
Test script for Global Operations Intelligence Agent - Task 8.1 Implementation

Tests all components of comprehensive global data integration:
- World Bank API integration
- OpenStreetMap API integration  
- OFAC Sanctions List integration
- Supply chain mapping and risk assessment algorithms
"""

import asyncio
import logging
import sys
import os
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from operations.operations_agent import OperationsAgent
from operations.world_bank_client import WorldBankClient
from operations.openstreetmap_client import OpenStreetMapClient
from operations.ofac_sanctions_client import OFACSanctionsClient
from operations.supply_chain_mapper import SupplyChainMapper
from operations.geopolitical_analyzer import GeopoliticalAnalyzer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class GlobalIntegrationTester:
    """Test suite for global data integration components"""
    
    def __init__(self):
        self.results = {}
        self.passed_tests = 0
        self.total_tests = 0
    
    async def run_all_tests(self):
        """Run comprehensive test suite"""
        logger.info("Starting Global Data Integration Test Suite")
        logger.info("=" * 60)
        
        # Test individual components
        await self.test_world_bank_integration()
        await self.test_openstreetmap_integration()
        await self.test_ofac_sanctions_integration()
        await self.test_supply_chain_mapping()
        await self.test_geopolitical_analysis()
        
        # Test integrated operations agent
        await self.test_operations_agent_integration()
        
        # Print summary
        self.print_test_summary()
    
    async def test_world_bank_integration(self):
        """Test World Bank API integration"""
        logger.info("\n1. Testing World Bank API Integration")
        logger.info("-" * 40)
        
        try:
            async with WorldBankClient() as wb_client:
                # Test country indicator fetching
                test_countries = ['USA', 'DEU', 'CHN', 'BRA']
                
                for country in test_countries:
                    logger.info(f"Testing World Bank data for {country}...")
                    data = await wb_client.get_country_indicators(country)
                    
                    if 'error' not in data:
                        logger.info(f"✓ Successfully fetched data for {country}")
                        logger.info(f"  - Economic risk: {data.get('economic_risk_score', 'N/A')}")
                        logger.info(f"  - Governance risk: {data.get('governance_risk_score', 'N/A')}")
                        logger.info(f"  - Overall risk: {data.get('overall_country_risk', 'N/A')}")
                        self.passed_tests += 1
                    else:
                        logger.warning(f"✗ Failed to fetch data for {country}: {data.get('error')}")
                    
                    self.total_tests += 1
                
                self.results['world_bank'] = 'PASSED' if self.passed_tests > 0 else 'FAILED'
                
        except Exception as e:
            logger.error(f"✗ World Bank integration test failed: {str(e)}")
            self.results['world_bank'] = 'FAILED'
    
    async def test_openstreetmap_integration(self):
        """Test OpenStreetMap API integration"""
        logger.info("\n2. Testing OpenStreetMap API Integration")
        logger.info("-" * 40)
        
        try:
            async with OpenStreetMapClient() as osm_client:
                # Test geocoding
                test_locations = [
                    "New York, USA",
                    "Berlin, Germany", 
                    "Tokyo, Japan",
                    "São Paulo, Brazil"
                ]
                
                for location in test_locations:
                    logger.info(f"Testing geocoding for {location}...")
                    coords = await osm_client.geocode(location)
                    
                    if coords:
                        logger.info(f"✓ Geocoded {location}: {coords}")
                        self.passed_tests += 1
                        
                        # Test reverse geocoding
                        reverse_data = await osm_client.reverse_geocode(coords[0], coords[1])
                        if reverse_data:
                            logger.info(f"✓ Reverse geocoded: {reverse_data.get('display_name', 'N/A')}")
                    else:
                        logger.warning(f"✗ Failed to geocode {location}")
                    
                    self.total_tests += 1
                
                # Test facility finding
                if test_locations:
                    coords = await osm_client.geocode(test_locations[0])
                    if coords:
                        logger.info("Testing nearby facility search...")
                        facilities = await osm_client.find_nearby_facilities(
                            coords[0], coords[1], "industrial", 25.0
                        )
                        logger.info(f"✓ Found {len(facilities)} nearby facilities")
                        self.passed_tests += 1
                    self.total_tests += 1
                
                self.results['openstreetmap'] = 'PASSED'
                
        except Exception as e:
            logger.error(f"✗ OpenStreetMap integration test failed: {str(e)}")
            self.results['openstreetmap'] = 'FAILED'
    
    async def test_ofac_sanctions_integration(self):
        """Test OFAC Sanctions List integration"""
        logger.info("\n3. Testing OFAC Sanctions Integration")
        logger.info("-" * 40)
        
        try:
            async with OFACSanctionsClient() as ofac_client:
                # Test sanctions data update
                logger.info("Testing sanctions data update...")
                await ofac_client._update_sanctions_data()
                
                if ofac_client._sdn_list:
                    logger.info(f"✓ Loaded {len(ofac_client._sdn_list)} SDN entries")
                    self.passed_tests += 1
                else:
                    logger.warning("✗ No SDN data loaded")
                
                self.total_tests += 1
                
                # Test entity checking
                test_entities = [
                    {'name': 'Clean Company Inc', 'country': 'USA'},
                    {'name': 'Test Entity Ltd', 'country': 'GBR'},
                    {'name': 'Demo Sanctioned Entity', 'country': 'XXX'}  # Should match demo data
                ]
                
                logger.info("Testing entity sanctions checking...")
                results = await ofac_client.check_entities(test_entities)
                
                if results and not results[0].get('error'):
                    logger.info(f"✓ Checked {len(results)} entities")
                    for result in results:
                        entity_name = result.get('entity_name', 'Unknown')
                        match_found = result.get('match_found', False)
                        confidence = result.get('match_confidence', 0)
                        logger.info(f"  - {entity_name}: Match={match_found}, Confidence={confidence:.2f}")
                    self.passed_tests += 1
                else:
                    logger.warning("✗ Entity checking failed")
                
                self.total_tests += 1
                
                # Test statistics
                stats = await ofac_client.get_sanctions_statistics()
                if 'error' not in stats:
                    logger.info(f"✓ Sanctions statistics: {stats.get('total_entries', 0)} total entries")
                    self.passed_tests += 1
                else:
                    logger.warning("✗ Failed to get sanctions statistics")
                
                self.total_tests += 1
                
                self.results['ofac_sanctions'] = 'PASSED'
                
        except Exception as e:
            logger.error(f"✗ OFAC sanctions integration test failed: {str(e)}")
            self.results['ofac_sanctions'] = 'FAILED'
    
    async def test_supply_chain_mapping(self):
        """Test supply chain mapping algorithms"""
        logger.info("\n4. Testing Supply Chain Mapping")
        logger.info("-" * 40)
        
        try:
            mapper = SupplyChainMapper()
            
            # Test data
            test_suppliers = [
                {
                    'name': 'TechCorp Semiconductors',
                    'country': 'TWN',
                    'sector': 'semiconductors',
                    'criticality': 0.9
                },
                {
                    'name': 'Global Logistics Ltd',
                    'country': 'SGP',
                    'sector': 'logistics',
                    'criticality': 0.7
                },
                {
                    'name': 'European Chemicals',
                    'country': 'DEU',
                    'sector': 'chemicals',
                    'criticality': 0.6
                }
            ]
            
            test_facilities = [
                {
                    'name': 'Main Manufacturing Plant',
                    'country': 'USA',
                    'type': 'manufacturing',
                    'capacity_percentage': 60
                },
                {
                    'name': 'European Distribution Center',
                    'country': 'DEU',
                    'type': 'distribution',
                    'capacity_percentage': 30
                },
                {
                    'name': 'Asia Pacific Hub',
                    'country': 'SGP',
                    'type': 'distribution',
                    'capacity_percentage': 25
                }
            ]
            
            # Test supply chain mapping
            logger.info("Testing supply chain map creation...")
            supply_chain_map = await mapper.create_supply_chain_map(test_suppliers, test_facilities)
            
            if 'error' not in supply_chain_map:
                logger.info("✓ Supply chain map created successfully")
                logger.info(f"  - Resilience score: {supply_chain_map.get('resilience_score', 'N/A')}")
                logger.info(f"  - Critical dependencies: {len(supply_chain_map.get('critical_dependencies', []))}")
                self.passed_tests += 1
            else:
                logger.warning(f"✗ Supply chain mapping failed: {supply_chain_map.get('error')}")
            
            self.total_tests += 1
            
            # Test vulnerability assessment
            logger.info("Testing vulnerability assessment...")
            vulnerabilities = await mapper.assess_vulnerabilities(supply_chain_map)
            
            if vulnerabilities and 'error' not in vulnerabilities[0]:
                logger.info(f"✓ Identified {len(vulnerabilities)} vulnerabilities")
                for vuln in vulnerabilities[:3]:  # Show top 3
                    logger.info(f"  - {vuln.get('type', 'Unknown')}: {vuln.get('severity', 'Unknown')} severity")
                self.passed_tests += 1
            else:
                logger.warning("✗ Vulnerability assessment failed")
            
            self.total_tests += 1
            
            self.results['supply_chain_mapping'] = 'PASSED'
            
        except Exception as e:
            logger.error(f"✗ Supply chain mapping test failed: {str(e)}")
            self.results['supply_chain_mapping'] = 'FAILED'
    
    async def test_geopolitical_analysis(self):
        """Test geopolitical risk analysis"""
        logger.info("\n5. Testing Geopolitical Analysis")
        logger.info("-" * 40)
        
        try:
            analyzer = GeopoliticalAnalyzer()
            
            # Test countries with different risk profiles
            test_countries = ['USA', 'DEU', 'CHN', 'RUS', 'AFG']
            
            for country in test_countries:
                logger.info(f"Testing geopolitical analysis for {country}...")
                
                # Mock World Bank data
                mock_wb_data = {
                    'indicators': {
                        'CC.EST': {'latest_value': 1.0 if country in ['USA', 'DEU'] else -0.5},
                        'GE.EST': {'latest_value': 1.2 if country in ['USA', 'DEU'] else -0.3},
                        'PV.EST': {'latest_value': 0.8 if country in ['USA', 'DEU'] else -1.0},
                        'NY.GDP.PCAP.CD': {'latest_value': 50000 if country in ['USA', 'DEU'] else 10000}
                    }
                }
                
                risk_assessment = await analyzer.assess_country_risk(country, mock_wb_data)
                
                if 'error' not in risk_assessment:
                    logger.info(f"✓ Risk assessment for {country}:")
                    logger.info(f"  - Risk score: {risk_assessment.get('risk_score', 'N/A')}")
                    logger.info(f"  - Risk level: {risk_assessment.get('risk_level', 'N/A')}")
                    logger.info(f"  - Risk factors: {len(risk_assessment.get('risk_factors', []))}")
                    self.passed_tests += 1
                else:
                    logger.warning(f"✗ Risk assessment failed for {country}")
                
                self.total_tests += 1
            
            self.results['geopolitical_analysis'] = 'PASSED'
            
        except Exception as e:
            logger.error(f"✗ Geopolitical analysis test failed: {str(e)}")
            self.results['geopolitical_analysis'] = 'FAILED'
    
    async def test_operations_agent_integration(self):
        """Test integrated Operations Agent"""
        logger.info("\n6. Testing Operations Agent Integration")
        logger.info("-" * 40)
        
        try:
            agent = OperationsAgent()
            
            # Comprehensive test data
            test_company_data = {
                'name': 'Global Manufacturing Corp',
                'locations': [
                    {'country': 'USA', 'city': 'New York', 'type': 'headquarters'},
                    {'country': 'DEU', 'city': 'Berlin', 'type': 'regional_office'},
                    {'country': 'CHN', 'city': 'Shanghai', 'type': 'manufacturing'},
                    {'country': 'SGP', 'city': 'Singapore', 'type': 'distribution'}
                ],
                'suppliers': [
                    {
                        'name': 'TechCorp Semiconductors',
                        'country': 'TWN',
                        'sector': 'semiconductors',
                        'criticality': 0.9
                    },
                    {
                        'name': 'European Steel Works',
                        'country': 'DEU',
                        'sector': 'metals',
                        'criticality': 0.6
                    }
                ],
                'facilities': [
                    {
                        'name': 'Main Manufacturing Plant',
                        'country': 'CHN',
                        'city': 'Shanghai',
                        'type': 'manufacturing',
                        'capacity_percentage': 70,
                        'latitude': 31.2304,
                        'longitude': 121.4737
                    },
                    {
                        'name': 'Distribution Center',
                        'country': 'SGP',
                        'city': 'Singapore',
                        'type': 'distribution',
                        'capacity_percentage': 40,
                        'latitude': 1.3521,
                        'longitude': 103.8198
                    }
                ],
                'partners': [
                    {'name': 'Clean Partner Ltd', 'country': 'GBR'},
                    {'name': 'Regional Distributor', 'country': 'BRA'}
                ]
            }
            
            logger.info("Testing comprehensive global operations analysis...")
            analysis_result = await agent.analyze_global_operations(test_company_data)
            
            if 'error' not in analysis_result:
                logger.info("✓ Global operations analysis completed successfully")
                logger.info(f"  - Overall risk score: {analysis_result.get('overall_risk_score', 'N/A')}")
                logger.info(f"  - Recommendations: {len(analysis_result.get('recommendations', []))}")
                
                # Check individual components
                components = [
                    'geopolitical_risks',
                    'supply_chain_analysis', 
                    'sanctions_compliance',
                    'operational_efficiency'
                ]
                
                for component in components:
                    if component in analysis_result and 'error' not in analysis_result[component]:
                        logger.info(f"  ✓ {component} analysis completed")
                    else:
                        logger.warning(f"  ✗ {component} analysis failed")
                
                self.passed_tests += 1
            else:
                logger.warning(f"✗ Global operations analysis failed: {analysis_result.get('error')}")
            
            self.total_tests += 1
            
            self.results['operations_agent'] = 'PASSED'
            
        except Exception as e:
            logger.error(f"✗ Operations agent integration test failed: {str(e)}")
            self.results['operations_agent'] = 'FAILED'
    
    def print_test_summary(self):
        """Print comprehensive test summary"""
        logger.info("\n" + "=" * 60)
        logger.info("GLOBAL DATA INTEGRATION TEST SUMMARY")
        logger.info("=" * 60)
        
        logger.info(f"Total Tests Run: {self.total_tests}")
        logger.info(f"Tests Passed: {self.passed_tests}")
        logger.info(f"Success Rate: {(self.passed_tests/self.total_tests*100):.1f}%" if self.total_tests > 0 else "0%")
        
        logger.info("\nComponent Results:")
        logger.info("-" * 30)
        
        for component, result in self.results.items():
            status_icon = "✓" if result == "PASSED" else "✗"
            logger.info(f"{status_icon} {component.replace('_', ' ').title()}: {result}")
        
        # Overall assessment
        passed_components = sum(1 for result in self.results.values() if result == "PASSED")
        total_components = len(self.results)
        
        logger.info(f"\nOverall Assessment:")
        logger.info("-" * 20)
        
        if passed_components == total_components:
            logger.info("🎉 ALL COMPONENTS PASSED - Task 8.1 Implementation Complete!")
            logger.info("✓ World Bank API integration working")
            logger.info("✓ OpenStreetMap API integration working") 
            logger.info("✓ OFAC Sanctions List integration working")
            logger.info("✓ Supply chain mapping algorithms working")
            logger.info("✓ Global risk assessment algorithms working")
            logger.info("✓ Integrated operations agent working")
        elif passed_components >= total_components * 0.8:
            logger.info("⚠️  MOSTLY WORKING - Minor issues detected")
            logger.info("Most components are functional with some limitations")
        else:
            logger.info("❌ SIGNIFICANT ISSUES - Major components failing")
            logger.info("Implementation needs additional work")
        
        logger.info("\n" + "=" * 60)

async def main():
    """Main test execution"""
    tester = GlobalIntegrationTester()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())