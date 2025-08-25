"""
Supply Chain Mapper

Maps and analyzes supply chain networks for risk assessment
"""

import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from collections import defaultdict, Counter

logger = logging.getLogger(__name__)

class SupplyChainMapper:
    """
    Mapper and analyzer for supply chain networks and vulnerabilities
    """
    
    def __init__(self):
        # Critical supply chain sectors
        self.critical_sectors = {
            'semiconductors': {'criticality': 0.9, 'concentration_risk': 0.8},
            'rare_earth_metals': {'criticality': 0.85, 'concentration_risk': 0.9},
            'pharmaceuticals': {'criticality': 0.8, 'concentration_risk': 0.6},
            'energy': {'criticality': 0.9, 'concentration_risk': 0.7},
            'food': {'criticality': 0.7, 'concentration_risk': 0.5},
            'automotive': {'criticality': 0.6, 'concentration_risk': 0.6},
            'textiles': {'criticality': 0.3, 'concentration_risk': 0.4},
            'electronics': {'criticality': 0.7, 'concentration_risk': 0.7},
            'chemicals': {'criticality': 0.75, 'concentration_risk': 0.6},
            'logistics': {'criticality': 0.8, 'concentration_risk': 0.5}
        }
        
        # Geographic risk factors
        self.geographic_risks = {
            'single_country_dependency': 0.8,
            'high_risk_region': 0.7,
            'transportation_bottlenecks': 0.6,
            'natural_disaster_zones': 0.5
        }
    
    async def create_supply_chain_map(self, suppliers: List[Dict[str, Any]], 
                                    facilities: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create comprehensive supply chain map and analysis
        """
        try:
            logger.info(f"Creating supply chain map for {len(suppliers)} suppliers and {len(facilities)} facilities")
            
            # Analyze supplier network
            supplier_analysis = self._analyze_supplier_network(suppliers)
            
            # Analyze facility distribution
            facility_analysis = self._analyze_facility_distribution(facilities)
            
            # Calculate geographic distribution
            geographic_analysis = self._analyze_geographic_distribution(suppliers + facilities)
            
            # Identify critical dependencies
            critical_dependencies = self._identify_critical_dependencies(suppliers, facilities)
            
            # Calculate resilience score
            resilience_score = self._calculate_resilience_score(
                supplier_analysis, facility_analysis, geographic_analysis
            )
            
            return {
                'supplier_network': supplier_analysis,
                'facility_distribution': facility_analysis,
                'geographic_distribution': geographic_analysis,
                'critical_dependencies': critical_dependencies,
                'resilience_score': resilience_score,
                'risk_assessment': self._assess_supply_chain_risks(
                    supplier_analysis, facility_analysis, geographic_analysis
                ),
                'analysis_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error creating supply chain map: {str(e)}")
            return {'error': str(e)}
    
    async def assess_vulnerabilities(self, supply_chain_map: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Assess supply chain vulnerabilities from the supply chain map
        """
        try:
            vulnerabilities = []
            
            # Check for single points of failure
            spof_vulnerabilities = self._identify_single_points_of_failure(supply_chain_map)
            vulnerabilities.extend(spof_vulnerabilities)
            
            # Check for geographic concentration risks
            geo_vulnerabilities = self._identify_geographic_vulnerabilities(supply_chain_map)
            vulnerabilities.extend(geo_vulnerabilities)
            
            # Check for sector concentration risks
            sector_vulnerabilities = self._identify_sector_vulnerabilities(supply_chain_map)
            vulnerabilities.extend(sector_vulnerabilities)
            
            # Sort by severity
            vulnerabilities.sort(key=lambda x: x.get('severity_score', 0), reverse=True)
            
            return vulnerabilities
            
        except Exception as e:
            logger.error(f"Error assessing vulnerabilities: {str(e)}")
            return [{'error': str(e)}]
    
    def _analyze_supplier_network(self, suppliers: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze supplier network structure and risks"""
        try:
            if not suppliers:
                return {'total_suppliers': 0, 'analysis': 'No suppliers provided'}
            
            # Categorize suppliers by sector
            sectors = defaultdict(list)
            countries = defaultdict(list)
            criticality_scores = []
            
            for supplier in suppliers:
                sector = supplier.get('sector', 'unknown')
                country = supplier.get('country', 'unknown')
                criticality = supplier.get('criticality', 0.5)
                
                sectors[sector].append(supplier)
                countries[country].append(supplier)
                criticality_scores.append(criticality)
            
            # Calculate concentration metrics
            sector_concentration = self._calculate_concentration_index(
                [len(suppliers) for suppliers in sectors.values()]
            )
            
            country_concentration = self._calculate_concentration_index(
                [len(suppliers) for suppliers in countries.values()]
            )
            
            avg_criticality = sum(criticality_scores) / len(criticality_scores) if criticality_scores else 0.5
            
            return {
                'total_suppliers': len(suppliers),
                'sectors': dict(sectors),
                'countries': dict(countries),
                'sector_concentration': sector_concentration,
                'country_concentration': country_concentration,
                'average_criticality': avg_criticality,
                'concentration_risk': max(sector_concentration, country_concentration)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing supplier network: {str(e)}")
            return {'error': str(e)}
    
    def _analyze_facility_distribution(self, facilities: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze facility distribution and operational footprint"""
        try:
            if not facilities:
                return {'total_facilities': 0, 'analysis': 'No facilities provided'}
            
            # Categorize facilities
            facility_types = defaultdict(list)
            countries = defaultdict(list)
            
            for facility in facilities:
                facility_type = facility.get('type', 'unknown')
                country = facility.get('country', 'unknown')
                
                facility_types[facility_type].append(facility)
                countries[country].append(facility)
            
            return {
                'total_facilities': len(facilities),
                'facility_types': {ftype: len(facilities) for ftype, facilities in facility_types.items()},
                'country_distribution': {country: len(facilities) for country, facilities in countries.items()},
                'geographic_spread': len(countries),
                'operational_redundancy': self._calculate_operational_redundancy(facility_types)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing facility distribution: {str(e)}")
            return {'error': str(e)}
    
    def _analyze_geographic_distribution(self, entities: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze geographic distribution of supply chain entities"""
        try:
            if not entities:
                return {'analysis': 'No entities provided'}
            
            countries = Counter()
            risk_countries = []
            
            for entity in entities:
                country = entity.get('country')
                
                if country:
                    countries[country] += 1
                    
                    # Check if country is high-risk
                    if self._is_high_risk_country(country):
                        risk_countries.append(country)
            
            # Calculate geographic concentration
            total_entities = len(entities)
            country_concentration = self._calculate_herfindahl_index(
                [count / total_entities for count in countries.values()]
            ) if total_entities > 0 else 0
            
            return {
                'countries': dict(countries),
                'country_concentration': country_concentration,
                'high_risk_countries': list(set(risk_countries)),
                'geographic_diversification': 1.0 - country_concentration,
                'total_countries': len(countries)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing geographic distribution: {str(e)}")
            return {'error': str(e)}
    
    def _identify_critical_dependencies(self, suppliers: List[Dict[str, Any]], 
                                      facilities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identify critical dependencies in the supply chain"""
        try:
            critical_deps = []
            
            # Analyze supplier criticality
            for supplier in suppliers:
                criticality = supplier.get('criticality', 0.5)
                sector = supplier.get('sector', 'unknown')
                
                # Check if supplier is in critical sector
                sector_info = self.critical_sectors.get(sector, {'criticality': 0.5})
                
                if criticality > 0.7 or sector_info['criticality'] > 0.8:
                    critical_deps.append({
                        'type': 'supplier',
                        'entity': supplier,
                        'criticality_score': max(criticality, sector_info['criticality']),
                        'risk_factors': self._identify_dependency_risks(supplier),
                        'severity': 'high' if criticality > 0.8 else 'medium'
                    })
            
            # Analyze facility criticality
            for facility in facilities:
                capacity = facility.get('capacity_percentage', 0)
                
                if capacity > 50:
                    critical_deps.append({
                        'type': 'facility',
                        'entity': facility,
                        'criticality_score': capacity / 100.0,
                        'risk_factors': self._identify_dependency_risks(facility),
                        'severity': 'high' if capacity > 70 else 'medium'
                    })
            
            return critical_deps
            
        except Exception as e:
            logger.error(f"Error identifying critical dependencies: {str(e)}")
            return []
    
    def _calculate_resilience_score(self, supplier_analysis: Dict[str, Any], 
                                  facility_analysis: Dict[str, Any],
                                  geographic_analysis: Dict[str, Any]) -> float:
        """Calculate overall supply chain resilience score"""
        try:
            # Base resilience score
            resilience = 50.0
            
            # Supplier diversity bonus
            supplier_concentration = supplier_analysis.get('concentration_risk', 0.5)
            resilience += (1.0 - supplier_concentration) * 20
            
            # Geographic diversification bonus
            geo_diversification = geographic_analysis.get('geographic_diversification', 0.5)
            resilience += geo_diversification * 15
            
            # Facility redundancy bonus
            operational_redundancy = facility_analysis.get('operational_redundancy', 0.0)
            resilience += operational_redundancy * 10 / 100  # Convert percentage to factor
            
            # High-risk country penalty
            high_risk_countries = geographic_analysis.get('high_risk_countries', [])
            resilience -= len(high_risk_countries) * 5
            
            # Ensure score is within bounds
            return max(0.0, min(100.0, resilience))
            
        except Exception as e:
            logger.error(f"Error calculating resilience score: {str(e)}")
            return 50.0
    
    def _assess_supply_chain_risks(self, supplier_analysis: Dict[str, Any],
                                 facility_analysis: Dict[str, Any],
                                 geographic_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Assess overall supply chain risks"""
        try:
            risks = {
                'concentration_risk': 'low',
                'geographic_risk': 'low',
                'operational_risk': 'low',
                'overall_risk': 'low'
            }
            
            # Assess concentration risk
            concentration = max(
                supplier_analysis.get('concentration_risk', 0),
                geographic_analysis.get('country_concentration', 0)
            )
            
            if concentration > 0.7:
                risks['concentration_risk'] = 'high'
            elif concentration > 0.5:
                risks['concentration_risk'] = 'medium'
            
            # Assess geographic risk
            high_risk_countries = geographic_analysis.get('high_risk_countries', [])
            if len(high_risk_countries) > 2:
                risks['geographic_risk'] = 'high'
            elif len(high_risk_countries) > 0:
                risks['geographic_risk'] = 'medium'
            
            # Assess operational risk
            redundancy = facility_analysis.get('operational_redundancy', 0)
            if redundancy < 30:
                risks['operational_risk'] = 'high'
            elif redundancy < 60:
                risks['operational_risk'] = 'medium'
            
            # Calculate overall risk
            risk_scores = {'low': 1, 'medium': 2, 'high': 3}
            
            avg_risk = (
                risk_scores[risks['concentration_risk']] +
                risk_scores[risks['geographic_risk']] +
                risk_scores[risks['operational_risk']]
            ) / 3
            
            if avg_risk >= 2.5:
                risks['overall_risk'] = 'high'
            elif avg_risk >= 1.5:
                risks['overall_risk'] = 'medium'
            
            return risks
            
        except Exception as e:
            logger.error(f"Error assessing supply chain risks: {str(e)}")
            return {'error': str(e)}
    
    def _identify_single_points_of_failure(self, supply_chain_map: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify single points of failure in supply chain"""
        vulnerabilities = []
        
        try:
            # Check critical dependencies
            critical_deps = supply_chain_map.get('critical_dependencies', [])
            
            for dep in critical_deps:
                if dep.get('criticality_score', 0) > 0.8:
                    vulnerabilities.append({
                        'type': 'single_point_of_failure',
                        'description': f"Critical dependency on {dep['entity'].get('name', 'Unknown')}",
                        'severity': 'high',
                        'severity_score': 90,
                        'entity': dep['entity'],
                        'recommendations': [
                            'Identify alternative suppliers/facilities',
                            'Develop backup sourcing strategies',
                            'Increase inventory buffers for critical items'
                        ]
                    })
            
            return vulnerabilities
            
        except Exception as e:
            logger.error(f"Error identifying single points of failure: {str(e)}")
            return []
    
    def _identify_geographic_vulnerabilities(self, supply_chain_map: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify geographic concentration vulnerabilities"""
        vulnerabilities = []
        
        try:
            geo_analysis = supply_chain_map.get('geographic_distribution', {})
            high_risk_countries = geo_analysis.get('high_risk_countries', [])
            country_concentration = geo_analysis.get('country_concentration', 0)
            
            # High-risk country exposure
            if high_risk_countries:
                vulnerabilities.append({
                    'type': 'geographic_risk',
                    'description': f"Operations in high-risk countries: {', '.join(high_risk_countries)}",
                    'severity': 'high' if len(high_risk_countries) > 2 else 'medium',
                    'severity_score': 70 + len(high_risk_countries) * 10,
                    'countries': high_risk_countries,
                    'recommendations': [
                        'Develop contingency plans for high-risk regions',
                        'Consider geographic diversification',
                        'Implement enhanced monitoring for political/economic risks'
                    ]
                })
            
            # Geographic concentration
            if country_concentration > 0.6:
                vulnerabilities.append({
                    'type': 'geographic_concentration',
                    'description': 'High geographic concentration increases disruption risk',
                    'severity': 'medium',
                    'severity_score': 60,
                    'concentration_index': country_concentration,
                    'recommendations': [
                        'Diversify supplier base across multiple countries',
                        'Establish regional backup facilities',
                        'Reduce dependency on single geographic regions'
                    ]
                })
            
            return vulnerabilities
            
        except Exception as e:
            logger.error(f"Error identifying geographic vulnerabilities: {str(e)}")
            return []
    
    def _identify_sector_vulnerabilities(self, supply_chain_map: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify sector concentration vulnerabilities"""
        vulnerabilities = []
        
        try:
            supplier_analysis = supply_chain_map.get('supplier_network', {})
            sectors = supplier_analysis.get('sectors', {})
            
            # Check for over-reliance on critical sectors
            for sector, suppliers in sectors.items():
                sector_info = self.critical_sectors.get(sector, {'criticality': 0.5, 'concentration_risk': 0.5})
                
                if (len(suppliers) > len(sectors) * 0.4 and  # More than 40% of suppliers in one sector
                    sector_info['criticality'] > 0.7):
                    
                    vulnerabilities.append({
                        'type': 'sector_concentration',
                        'description': f'High concentration in critical sector: {sector}',
                        'severity': 'medium',
                        'severity_score': 55,
                        'sector': sector,
                        'supplier_count': len(suppliers),
                        'recommendations': [
                            f'Diversify suppliers outside of {sector} sector',
                            'Develop alternative sourcing strategies',
                            'Monitor sector-specific risks and trends'
                        ]
                    })
            
            return vulnerabilities
            
        except Exception as e:
            logger.error(f"Error identifying sector vulnerabilities: {str(e)}")
            return []
    
    def _calculate_concentration_index(self, values: List[int]) -> float:
        """Calculate concentration index (Herfindahl-Hirschman Index)"""
        if not values or sum(values) == 0:
            return 0.0
        
        total = sum(values)
        shares = [v / total for v in values]
        return sum(share ** 2 for share in shares)
    
    def _calculate_herfindahl_index(self, shares: List[float]) -> float:
        """Calculate Herfindahl-Hirschman Index from market shares"""
        return sum(share ** 2 for share in shares)
    
    def _calculate_operational_redundancy(self, facility_types: Dict[str, List]) -> float:
        """Calculate operational redundancy score"""
        if not facility_types:
            return 0.0
        
        redundancy_score = 0.0
        for facility_type, facilities in facility_types.items():
            if len(facilities) > 1:
                # More facilities of same type = higher redundancy
                redundancy_score += min(len(facilities) - 1, 3) * 20  # Max 60 points per type
        
        return min(100.0, redundancy_score)
    
    def _is_high_risk_country(self, country: str) -> bool:
        """Check if country is considered high-risk"""
        high_risk_countries = {
            'AFG', 'SYR', 'YEM', 'LBY', 'SOM', 'CAF', 'COD', 'SDN', 'SSD',
            'IRQ', 'MMR', 'VEN', 'HTI', 'MLI', 'BFA', 'NER', 'TCD'
        }
        return country.upper() in high_risk_countries
    
    def _identify_dependency_risks(self, entity: Dict[str, Any]) -> List[str]:
        """Identify specific risks for a dependency"""
        risks = []
        
        country = entity.get('country', '').upper()
        if self._is_high_risk_country(country):
            risks.append('High-risk country location')
        
        sector = entity.get('sector', '')
        if sector in self.critical_sectors:
            sector_info = self.critical_sectors[sector]
            if sector_info['concentration_risk'] > 0.7:
                risks.append('High sector concentration risk')
        
        capacity = entity.get('capacity_percentage', 0)
        if capacity > 70:
            risks.append('High capacity dependency')
        
        return risks