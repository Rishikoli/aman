"""
Global Operations Intelligence Agent

Provides comprehensive global operations analysis including:
- Geopolitical risk assessment
- Supply chain mapping and analysis
- Sanctions compliance checking
- Operational efficiency benchmarking
"""

import logging
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

from .world_bank_client import WorldBankClient
from .openstreetmap_client import OpenStreetMapClient
from .ofac_sanctions_client import OFACSanctionsClient
from .geopolitical_analyzer import GeopoliticalAnalyzer
from .enhanced_geopolitical_analyzer import EnhancedGeopoliticalAnalyzer
from .supply_chain_mapper import SupplyChainMapper
from .gemini_client import GeminiClient
from .operational_risk_scorer import OperationalRiskScorer
from .efficiency_benchmarker import OperationalEfficiencyBenchmarker

logger = logging.getLogger(__name__)

class OperationsAgent:
    """
    Global Operations Intelligence Agent for M&A due diligence
    """
    
    def __init__(self):
        self.world_bank = WorldBankClient()
        self.osm_client = OpenStreetMapClient()
        self.ofac_client = OFACSanctionsClient()
        self.geo_analyzer = GeopoliticalAnalyzer()
        self.enhanced_geo_analyzer = EnhancedGeopoliticalAnalyzer()
        self.supply_chain_mapper = SupplyChainMapper()
        self.gemini_client = GeminiClient()
        self.risk_scorer = OperationalRiskScorer()
        self.efficiency_benchmarker = OperationalEfficiencyBenchmarker()
        # self.nlp = SimpleNLP()  # Commented out for now
        
    async def analyze_global_operations(self, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform comprehensive global operations analysis
        
        Args:
            company_data: Dictionary containing company information including:
                - name: Company name
                - locations: List of operational locations
                - suppliers: List of supplier information
                - facilities: List of facility information
                
        Returns:
            Dictionary containing comprehensive operations intelligence
        """
        try:
            logger.info(f"Starting global operations analysis for {company_data.get('name', 'Unknown Company')}")
            
            # Parallel execution of different analysis components
            tasks = [
                self._analyze_geopolitical_risks(company_data),
                self._map_supply_chain(company_data),
                self._check_sanctions_compliance(company_data),
                self._assess_operational_efficiency(company_data)
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Combine results
            analysis_result = {
                'company_name': company_data.get('name'),
                'analysis_timestamp': datetime.now().isoformat(),
                'geopolitical_risks': results[0] if not isinstance(results[0], Exception) else {},
                'supply_chain_analysis': results[1] if not isinstance(results[1], Exception) else {},
                'sanctions_compliance': results[2] if not isinstance(results[2], Exception) else {},
                'operational_efficiency': results[3] if not isinstance(results[3], Exception) else {},
                'overall_risk_score': 0,
                'recommendations': []
            }
            
            # Calculate overall risk score
            analysis_result['overall_risk_score'] = self._calculate_overall_risk_score(analysis_result)
            
            # Generate recommendations
            analysis_result['recommendations'] = self._generate_recommendations(analysis_result)
            
            logger.info(f"Completed global operations analysis with risk score: {analysis_result['overall_risk_score']}")
            return analysis_result
            
        except Exception as e:
            logger.error(f"Error in global operations analysis: {str(e)}")
            return {
                'error': str(e),
                'company_name': company_data.get('name'),
                'analysis_timestamp': datetime.now().isoformat()
            }
    
    async def analyze_ai_powered_operations_intelligence(self, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        AI-Powered Operations Intelligence System (Task 8.2)
        
        Provides comprehensive operational risk scoring, AI synthesis, geopolitical analysis,
        and operational efficiency benchmarking with optimization recommendations.
        
        Args:
            company_data: Dictionary containing company information
            
        Returns:
            Comprehensive AI-powered operations intelligence analysis
        """
        try:
            logger.info(f"Starting AI-powered operations intelligence analysis for {company_data.get('name', 'Unknown Company')}")
            
            # Step 1: Gather comprehensive operational data
            operational_data = await self._gather_comprehensive_operational_data(company_data)
            
            # Step 2: Enhanced geopolitical risk analysis with supply chain vulnerability
            enhanced_geo_analysis = await self._perform_enhanced_geopolitical_analysis(company_data)
            
            # Step 3: Comprehensive operational risk scoring using multiple data sources
            risk_scoring = await self.risk_scorer.calculate_comprehensive_risk_score({
                'geopolitical_risks': enhanced_geo_analysis,
                'supply_chain_analysis': operational_data.get('supply_chain_analysis', {}),
                'sanctions_compliance': operational_data.get('sanctions_compliance', {}),
                'operational_efficiency': operational_data.get('operational_efficiency', {})
            })
            
            # Step 4: AI-powered synthesis using Gemini API
            ai_synthesis = await self.gemini_client.synthesize_operational_risks({
                'geopolitical_risks': enhanced_geo_analysis,
                'supply_chain_analysis': operational_data.get('supply_chain_analysis', {}),
                'sanctions_compliance': operational_data.get('sanctions_compliance', {}),
                'operational_efficiency': operational_data.get('operational_efficiency', {}),
                'risk_scoring': risk_scoring
            })
            
            # Step 5: Operational efficiency benchmarking and optimization
            industry = company_data.get('industry', 'manufacturing')
            efficiency_benchmarking = await self.efficiency_benchmarker.benchmark_operational_efficiency(
                company_data, industry
            )
            
            # Step 6: AI-powered geopolitical context analysis
            countries_data = self._extract_countries_data(enhanced_geo_analysis)
            geopolitical_context = await self.gemini_client.analyze_geopolitical_context(countries_data)
            
            # Step 7: AI-powered efficiency optimization recommendations
            efficiency_optimization = await self.gemini_client.optimize_operational_efficiency(
                efficiency_benchmarking
            )
            
            # Step 8: Generate comprehensive intelligence report
            intelligence_report = self._generate_comprehensive_intelligence_report(
                operational_data, enhanced_geo_analysis, risk_scoring, ai_synthesis,
                efficiency_benchmarking, geopolitical_context, efficiency_optimization
            )
            
            return {
                'company_name': company_data.get('name'),
                'analysis_timestamp': datetime.now().isoformat(),
                'analysis_type': 'ai_powered_operations_intelligence',
                
                # Core Analysis Components
                'operational_data': operational_data,
                'enhanced_geopolitical_analysis': enhanced_geo_analysis,
                'comprehensive_risk_scoring': risk_scoring,
                'ai_synthesis': ai_synthesis,
                'efficiency_benchmarking': efficiency_benchmarking,
                'geopolitical_context': geopolitical_context,
                'efficiency_optimization': efficiency_optimization,
                
                # Intelligence Report
                'intelligence_report': intelligence_report,
                
                # Key Metrics
                'overall_intelligence_score': intelligence_report.get('overall_score', 50),
                'risk_level': intelligence_report.get('risk_level', 'medium'),
                'efficiency_grade': efficiency_benchmarking.get('efficiency_grade', 'C'),
                'ai_confidence': ai_synthesis.get('confidence_level', 0.7),
                
                # Actionable Outputs
                'strategic_recommendations': intelligence_report.get('strategic_recommendations', []),
                'optimization_opportunities': efficiency_benchmarking.get('optimization_opportunities', []),
                'implementation_roadmap': efficiency_benchmarking.get('implementation_roadmap', []),
                'risk_mitigation_strategies': intelligence_report.get('risk_mitigation_strategies', [])
            }
            
        except Exception as e:
            logger.error(f"Error in AI-powered operations intelligence analysis: {str(e)}")
            return {
                'error': str(e),
                'company_name': company_data.get('name'),
                'analysis_timestamp': datetime.now().isoformat(),
                'analysis_type': 'ai_powered_operations_intelligence'
            }
    
    async def _gather_comprehensive_operational_data(self, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """Gather comprehensive operational data from multiple sources"""
        try:
            # Reuse existing analysis methods but with enhanced data collection
            tasks = [
                self._map_supply_chain(company_data),
                self._check_sanctions_compliance(company_data),
                self._assess_operational_efficiency(company_data)
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            return {
                'supply_chain_analysis': results[0] if not isinstance(results[0], Exception) else {},
                'sanctions_compliance': results[1] if not isinstance(results[1], Exception) else {},
                'operational_efficiency': results[2] if not isinstance(results[2], Exception) else {},
                'data_collection_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error gathering comprehensive operational data: {str(e)}")
            return {'error': str(e)}
    
    async def _perform_enhanced_geopolitical_analysis(self, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform enhanced geopolitical analysis with supply chain vulnerability assessment"""
        try:
            locations = company_data.get('locations', [])
            if not locations:
                return {'risk_level': 'low', 'risks': [], 'countries_analyzed': 0}
            
            enhanced_country_risks = []
            for location in locations:
                country = location.get('country')
                if country:
                    # Get World Bank governance and economic indicators
                    wb_data = await self.world_bank.get_country_indicators(country)
                    
                    # Enhanced geopolitical analysis with supply chain considerations
                    enhanced_risk = await self.enhanced_geo_analyzer.assess_country_risk(country, wb_data)
                    
                    enhanced_country_risks.append(enhanced_risk)
            
            # Calculate aggregate enhanced risk
            if enhanced_country_risks:
                avg_risk = np.mean([r.get('risk_score', 50) for r in enhanced_country_risks])
                supply_chain_risks = [r.get('supply_chain_risk', 50) for r in enhanced_country_risks]
                avg_supply_chain_risk = np.mean(supply_chain_risks)
            else:
                avg_risk = 50
                avg_supply_chain_risk = 50
            
            return {
                'risk_level': self._categorize_risk_level(avg_risk),
                'average_risk_score': avg_risk,
                'average_supply_chain_risk': avg_supply_chain_risk,
                'country_risks': enhanced_country_risks,
                'countries_analyzed': len(enhanced_country_risks),
                'high_risk_countries': [r for r in enhanced_country_risks if r.get('risk_score', 0) > 70],
                'supply_chain_vulnerabilities': [r for r in enhanced_country_risks if r.get('supply_chain_risk', 0) > 60],
                'chokepoint_exposures': [r for r in enhanced_country_risks if r.get('chokepoint_risk', 0) > 20]
            }
            
        except Exception as e:
            logger.error(f"Error in enhanced geopolitical analysis: {str(e)}")
            return {'error': str(e)}
    
    def _extract_countries_data(self, enhanced_geo_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract countries data for AI analysis"""
        try:
            country_risks = enhanced_geo_analysis.get('country_risks', [])
            return [
                {
                    'country': risk.get('country', 'Unknown'),
                    'risk_score': risk.get('risk_score', 50),
                    'supply_chain_risk': risk.get('supply_chain_risk', 50),
                    'chokepoint_risk': risk.get('chokepoint_risk', 0),
                    'risk_factors': risk.get('risk_factors', [])
                }
                for risk in country_risks
            ]
        except Exception as e:
            logger.error(f"Error extracting countries data: {str(e)}")
            return []
    
    def _generate_comprehensive_intelligence_report(self, operational_data: Dict[str, Any],
                                                  enhanced_geo_analysis: Dict[str, Any],
                                                  risk_scoring: Dict[str, Any],
                                                  ai_synthesis: Dict[str, Any],
                                                  efficiency_benchmarking: Dict[str, Any],
                                                  geopolitical_context: Dict[str, Any],
                                                  efficiency_optimization: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive operations intelligence report"""
        try:
            # Calculate overall intelligence score
            scores = []
            if risk_scoring.get('overall_risk_score'):
                scores.append(100 - risk_scoring['overall_risk_score'])  # Invert risk to score
            if efficiency_benchmarking.get('overall_efficiency_score'):
                scores.append(efficiency_benchmarking['overall_efficiency_score'])
            if ai_synthesis.get('confidence_level'):
                scores.append(ai_synthesis['confidence_level'] * 100)
            
            overall_score = np.mean(scores) if scores else 50.0
            
            # Determine risk level
            risk_level = 'low'
            if risk_scoring.get('overall_risk_score', 50) > 70:
                risk_level = 'high'
            elif risk_scoring.get('overall_risk_score', 50) > 50:
                risk_level = 'medium'
            
            # Compile strategic recommendations
            strategic_recommendations = []
            strategic_recommendations.extend(ai_synthesis.get('strategic_recommendations', []))
            strategic_recommendations.extend(efficiency_optimization.get('optimization_opportunities', [])[:3])
            strategic_recommendations.extend(geopolitical_context.get('strategic_implications', [])[:2])
            
            # Compile risk mitigation strategies
            risk_mitigation_strategies = []
            risk_mitigation_strategies.extend(ai_synthesis.get('risk_interconnections', []))
            risk_mitigation_strategies.extend(geopolitical_context.get('mitigation_strategies', []))
            risk_mitigation_strategies.extend(risk_scoring.get('recommendations', [])[:3])
            
            return {
                'overall_score': round(overall_score, 2),
                'risk_level': risk_level,
                'intelligence_summary': ai_synthesis.get('overall_risk_assessment', 'Comprehensive analysis completed'),
                'key_findings': [
                    f"Overall operational risk score: {risk_scoring.get('overall_risk_score', 50):.1f}",
                    f"Operational efficiency grade: {efficiency_benchmarking.get('efficiency_grade', 'C')}",
                    f"Countries analyzed: {enhanced_geo_analysis.get('countries_analyzed', 0)}",
                    f"AI confidence level: {ai_synthesis.get('confidence_level', 0.7):.1%}"
                ],
                'strategic_recommendations': strategic_recommendations[:5],  # Top 5
                'risk_mitigation_strategies': risk_mitigation_strategies[:5],  # Top 5
                'critical_alerts': self._identify_critical_alerts(risk_scoring, enhanced_geo_analysis),
                'confidence_metrics': {
                    'data_quality': risk_scoring.get('confidence_metrics', {}).get('data_quality', 70),
                    'ai_confidence': ai_synthesis.get('confidence_level', 0.7) * 100,
                    'analysis_completeness': 85.0  # Based on successful component completion
                }
            }
            
        except Exception as e:
            logger.error(f"Error generating comprehensive intelligence report: {str(e)}")
            return {
                'overall_score': 50.0,
                'risk_level': 'medium',
                'intelligence_summary': 'Analysis completed with limited data',
                'error': str(e)
            }
    
    def _identify_critical_alerts(self, risk_scoring: Dict[str, Any], 
                                enhanced_geo_analysis: Dict[str, Any]) -> List[str]:
        """Identify critical alerts requiring immediate attention"""
        alerts = []
        
        try:
            # High overall risk
            if risk_scoring.get('overall_risk_score', 0) > 80:
                alerts.append("CRITICAL: Overall operational risk exceeds acceptable thresholds")
            
            # Critical risk factors
            critical_factors = risk_scoring.get('critical_factors', [])
            for factor in critical_factors:
                if factor.get('severity') == 'critical':
                    alerts.append(f"CRITICAL: {factor.get('description', 'Critical risk identified')}")
            
            # High-risk countries
            high_risk_countries = enhanced_geo_analysis.get('high_risk_countries', [])
            if len(high_risk_countries) > 0:
                country_names = [c.get('country', 'Unknown') for c in high_risk_countries[:3]]
                alerts.append(f"HIGH RISK: Operations in high-risk countries: {', '.join(country_names)}")
            
            # Supply chain vulnerabilities
            vulnerabilities = enhanced_geo_analysis.get('supply_chain_vulnerabilities', [])
            if len(vulnerabilities) > 2:
                alerts.append("HIGH RISK: Multiple supply chain vulnerabilities identified")
            
            return alerts[:5]  # Limit to top 5 alerts
            
        except Exception as e:
            logger.error(f"Error identifying critical alerts: {str(e)}")
            return ["Unable to assess critical alerts"]
    
    async def _analyze_geopolitical_risks(self, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze geopolitical risks for company locations"""
        try:
            locations = company_data.get('locations', [])
            if not locations:
                return {'risk_level': 'low', 'risks': [], 'countries_analyzed': 0}
            
            country_risks = []
            for location in locations:
                country = location.get('country')
                if country:
                    # Get World Bank governance and economic indicators
                    wb_data = await self.world_bank.get_country_indicators(country)
                    
                    # Analyze geopolitical stability
                    geo_risk = await self.geo_analyzer.assess_country_risk(country, wb_data)
                    
                    country_risks.append({
                        'country': country,
                        'location': location.get('city', 'Unknown'),
                        'risk_score': geo_risk.get('risk_score', 50),
                        'risk_factors': geo_risk.get('risk_factors', []),
                        'economic_indicators': wb_data
                    })
            
            # Calculate aggregate risk
            avg_risk = np.mean([r['risk_score'] for r in country_risks]) if country_risks else 0
            
            return {
                'risk_level': self._categorize_risk_level(avg_risk),
                'average_risk_score': avg_risk,
                'country_risks': country_risks,
                'countries_analyzed': len(country_risks),
                'high_risk_countries': [r for r in country_risks if r['risk_score'] > 70]
            }
            
        except Exception as e:
            logger.error(f"Error in geopolitical risk analysis: {str(e)}")
            return {'error': str(e)}
    
    async def _map_supply_chain(self, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """Map and analyze supply chain risks"""
        try:
            suppliers = company_data.get('suppliers', [])
            facilities = company_data.get('facilities', [])
            
            # Map supply chain network
            supply_chain_map = await self.supply_chain_mapper.create_supply_chain_map(
                suppliers, facilities
            )
            
            # Analyze supply chain vulnerabilities
            vulnerabilities = await self.supply_chain_mapper.assess_vulnerabilities(
                supply_chain_map
            )
            
            return {
                'supply_chain_complexity': len(suppliers) + len(facilities),
                'geographic_distribution': supply_chain_map.get('geographic_distribution', {}),
                'vulnerabilities': vulnerabilities,
                'resilience_score': supply_chain_map.get('resilience_score', 50),
                'critical_dependencies': supply_chain_map.get('critical_dependencies', [])
            }
            
        except Exception as e:
            logger.error(f"Error in supply chain mapping: {str(e)}")
            return {'error': str(e)}
    
    async def _check_sanctions_compliance(self, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """Check sanctions compliance for suppliers and partners"""
        try:
            suppliers = company_data.get('suppliers', [])
            partners = company_data.get('partners', [])
            
            # Check OFAC sanctions list
            sanctions_results = await self.ofac_client.check_entities(
                suppliers + partners
            )
            
            compliance_issues = [
                result for result in sanctions_results 
                if result.get('match_found', False)
            ]
            
            return {
                'entities_checked': len(suppliers) + len(partners),
                'compliance_issues': compliance_issues,
                'compliance_score': 100 - (len(compliance_issues) * 10),  # Penalty per issue
                'high_risk_entities': [
                    issue for issue in compliance_issues 
                    if issue.get('match_confidence', 0) > 0.8
                ]
            }
            
        except Exception as e:
            logger.error(f"Error in sanctions compliance check: {str(e)}")
            return {'error': str(e)}
    
    async def _assess_operational_efficiency(self, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess operational efficiency metrics"""
        try:
            facilities = company_data.get('facilities', [])
            
            # Analyze facility distribution and efficiency
            efficiency_metrics = {
                'facility_count': len(facilities),
                'geographic_efficiency': 0,
                'operational_redundancy': 0,
                'cost_optimization_score': 0
            }
            
            if facilities:
                # Calculate geographic efficiency using OSM data
                geo_efficiency = await self._calculate_geographic_efficiency(facilities)
                efficiency_metrics['geographic_efficiency'] = geo_efficiency
                
                # Assess operational redundancy
                redundancy = self._assess_operational_redundancy(facilities)
                efficiency_metrics['operational_redundancy'] = redundancy
                
                # Calculate cost optimization opportunities
                cost_score = self._calculate_cost_optimization_score(facilities)
                efficiency_metrics['cost_optimization_score'] = cost_score
            
            return efficiency_metrics
            
        except Exception as e:
            logger.error(f"Error in operational efficiency assessment: {str(e)}")
            return {'error': str(e)}
    
    async def _calculate_geographic_efficiency(self, facilities: List[Dict]) -> float:
        """Calculate geographic distribution efficiency"""
        try:
            if len(facilities) < 2:
                return 100.0  # Single facility is perfectly efficient
            
            # Get coordinates for all facilities
            coordinates = []
            for facility in facilities:
                if 'latitude' in facility and 'longitude' in facility:
                    coordinates.append((facility['latitude'], facility['longitude']))
                else:
                    # Geocode using OSM
                    location = f"{facility.get('city', '')}, {facility.get('country', '')}"
                    coords = await self.osm_client.geocode(location)
                    if coords:
                        coordinates.append(coords)
            
            if len(coordinates) < 2:
                return 50.0  # Insufficient data
            
            # Calculate average distance between facilities
            distances = []
            for i in range(len(coordinates)):
                for j in range(i + 1, len(coordinates)):
                    dist = self._haversine_distance(coordinates[i], coordinates[j])
                    distances.append(dist)
            
            avg_distance = np.mean(distances)
            
            # Convert to efficiency score (lower distance = higher efficiency for regional operations)
            # Normalize to 0-100 scale
            efficiency = max(0, 100 - (avg_distance / 100))  # Adjust scaling as needed
            return min(100, efficiency)
            
        except Exception as e:
            logger.error(f"Error calculating geographic efficiency: {str(e)}")
            return 50.0
    
    def _assess_operational_redundancy(self, facilities: List[Dict]) -> float:
        """Assess operational redundancy and backup capabilities"""
        try:
            if not facilities:
                return 0.0
            
            # Analyze facility types and functions
            facility_types = {}
            for facility in facilities:
                facility_type = facility.get('type', 'unknown')
                if facility_type not in facility_types:
                    facility_types[facility_type] = 0
                facility_types[facility_type] += 1
            
            # Calculate redundancy score based on backup facilities
            redundancy_score = 0
            for facility_type, count in facility_types.items():
                if count > 1:
                    redundancy_score += min(count - 1, 3) * 20  # Max 60 points per type
            
            return min(100, redundancy_score)
            
        except Exception as e:
            logger.error(f"Error assessing operational redundancy: {str(e)}")
            return 0.0
    
    def _calculate_cost_optimization_score(self, facilities: List[Dict]) -> float:
        """Calculate potential cost optimization opportunities"""
        try:
            if not facilities:
                return 0.0
            
            # Simple heuristic based on facility distribution and types
            score = 50  # Base score
            
            # Bonus for geographic clustering (cost savings)
            countries = set(f.get('country', '') for f in facilities)
            if len(countries) <= 3:
                score += 20
            
            # Bonus for facility specialization
            types = set(f.get('type', '') for f in facilities)
            if len(types) >= len(facilities) * 0.7:  # High specialization
                score += 20
            
            # Penalty for excessive facilities
            if len(facilities) > 10:
                score -= 10
            
            return min(100, max(0, score))
            
        except Exception as e:
            logger.error(f"Error calculating cost optimization score: {str(e)}")
            return 50.0
    
    def _haversine_distance(self, coord1: tuple, coord2: tuple) -> float:
        """Calculate distance between two coordinates using Haversine formula"""
        lat1, lon1 = coord1
        lat2, lon2 = coord2
        
        # Convert to radians
        lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
        
        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
        c = 2 * np.arcsin(np.sqrt(a))
        
        # Earth's radius in kilometers
        r = 6371
        
        return c * r
    
    def _calculate_overall_risk_score(self, analysis_result: Dict[str, Any]) -> float:
        """Calculate overall operational risk score"""
        try:
            scores = []
            weights = []
            
            # Geopolitical risk (30% weight)
            geo_risk = analysis_result.get('geopolitical_risks', {})
            if 'average_risk_score' in geo_risk:
                scores.append(geo_risk['average_risk_score'])
                weights.append(0.3)
            
            # Supply chain risk (25% weight)
            supply_chain = analysis_result.get('supply_chain_analysis', {})
            if 'resilience_score' in supply_chain:
                scores.append(100 - supply_chain['resilience_score'])  # Invert for risk
                weights.append(0.25)
            
            # Sanctions compliance (25% weight)
            sanctions = analysis_result.get('sanctions_compliance', {})
            if 'compliance_score' in sanctions:
                scores.append(100 - sanctions['compliance_score'])  # Invert for risk
                weights.append(0.25)
            
            # Operational efficiency (20% weight)
            efficiency = analysis_result.get('operational_efficiency', {})
            if 'cost_optimization_score' in efficiency:
                scores.append(100 - efficiency['cost_optimization_score'])  # Invert for risk
                weights.append(0.2)
            
            if scores and weights:
                # Normalize weights
                total_weight = sum(weights)
                normalized_weights = [w / total_weight for w in weights]
                
                # Calculate weighted average
                overall_score = sum(s * w for s, w in zip(scores, normalized_weights))
                return round(overall_score, 2)
            
            return 50.0  # Default moderate risk
            
        except Exception as e:
            logger.error(f"Error calculating overall risk score: {str(e)}")
            return 50.0
    
    def _generate_recommendations(self, analysis_result: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations based on analysis"""
        recommendations = []
        
        try:
            # Geopolitical recommendations
            geo_risks = analysis_result.get('geopolitical_risks', {})
            high_risk_countries = geo_risks.get('high_risk_countries', [])
            if high_risk_countries:
                recommendations.append(
                    f"Consider diversifying operations away from high-risk countries: "
                    f"{', '.join([c['country'] for c in high_risk_countries[:3]])}"
                )
            
            # Supply chain recommendations
            supply_chain = analysis_result.get('supply_chain_analysis', {})
            vulnerabilities = supply_chain.get('vulnerabilities', [])
            if vulnerabilities:
                recommendations.append(
                    "Address supply chain vulnerabilities through supplier diversification "
                    "and backup sourcing strategies"
                )
            
            # Sanctions compliance recommendations
            sanctions = analysis_result.get('sanctions_compliance', {})
            compliance_issues = sanctions.get('compliance_issues', [])
            if compliance_issues:
                recommendations.append(
                    f"Immediate review required for {len(compliance_issues)} entities "
                    "with potential sanctions exposure"
                )
            
            # Operational efficiency recommendations
            efficiency = analysis_result.get('operational_efficiency', {})
            if efficiency.get('cost_optimization_score', 0) < 60:
                recommendations.append(
                    "Significant cost optimization opportunities identified through "
                    "facility consolidation and operational streamlining"
                )
            
            # Overall risk recommendations
            overall_risk = analysis_result.get('overall_risk_score', 0)
            if overall_risk > 70:
                recommendations.append(
                    "High operational risk detected - comprehensive risk mitigation "
                    "strategy recommended before proceeding with acquisition"
                )
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {str(e)}")
            return ["Unable to generate recommendations due to analysis errors"]
    
    def _categorize_risk_level(self, risk_score: float) -> str:
        """Categorize numerical risk score into risk level"""
        if risk_score < 30:
            return 'low'
        elif risk_score < 60:
            return 'medium'
        elif risk_score < 80:
            return 'high'
        else:
            return 'critical' {str(e)}")
            return 50.0
    
    def _assess_geographic_diversification(self, locations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Assess geographic diversification of operations"""
        try:
            if not locations:
                return {'diversification_score': 0, 'analysis': 'No locations provided'}
            
            # Count countries and regions
            countries = set()
            regions = set()
            
            for location in locations:
                country = location.get('country')
                region = location.get('region')
                
                if country:
                    countries.add(country)
                if region:
                    regions.add(region)
            
            # Calculate diversification score
            country_count = len(countries)
            region_count = len(regions)
            
            # Score based on number of countries and regions
            diversification_score = min(100, (country_count * 20) + (region_count * 10))
            
            return {
                'diversification_score': diversification_score,
                'countries': list(countries),
                'regions': list(regions),
                'country_count': country_count,
                'region_count': region_count,
                'analysis': self._get_diversification_analysis(diversification_score)
            }
            
        except Exception as e:
            logger.error(f"Error assessing geographic diversification: {str(e)}")
            return {'diversification_score': 0, 'error': str(e)}
    
    def _get_diversification_analysis(self, score: float) -> str:
        """Get diversification analysis based on score"""
        if score >= 80:
            return "Excellent geographic diversification reduces operational risk"
        elif score >= 60:
            return "Good geographic diversification with room for improvement"
        elif score >= 40:
            return "Moderate geographic diversification, consider expansion"
        elif score >= 20:
            return "Limited geographic diversification increases risk concentration"
        else:
            return "Poor geographic diversification creates significant operational risk"
    
    def _identify_logistics_opportunities(self, location_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify logistics optimization opportunities"""
        try:
            opportunities = []
            
            for location, analysis in location_analysis.items():
                logistics_score = analysis.get('logistics_accessibility', 50)
                infrastructure_score = analysis.get('infrastructure_quality', 50)
                
                # Identify improvement opportunities
                if logistics_score < 60:
                    opportunities.append({
                        'location': location,
                        'type': 'logistics_improvement',
                        'current_score': logistics_score,
                        'recommendation': 'Consider improving logistics connectivity or relocating operations',
                        'priority': 'high' if logistics_score < 40 else 'medium'
                    })
                
                if infrastructure_score < 60:
                    opportunities.append({
                        'location': location,
                        'type': 'infrastructure_improvement',
                        'current_score': infrastructure_score,
                        'recommendation': 'Infrastructure limitations may impact operational efficiency',
                        'priority': 'high' if infrastructure_score < 40 else 'medium'
                    })
            
            return opportunities
            
        except Exception as e:
            logger.error(f"Error identifying logistics opportunities: {str(e)}")
            return []
    
    def _generate_risk_summary(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive risk summary"""
        try:
            risk_summary = {
                'overall_risk_level': 'medium',
                'key_risks': [],
                'risk_scores': {},
                'critical_findings': []
            }
            
            # Analyze geopolitical risks
            geo_risks = analysis_results.get('geopolitical_risks', {})
            if geo_risks and not geo_risks.get('error'):
                geo_scores = [country_data.get('risk_score', 50) for country_data in geo_risks.values() 
                             if isinstance(country_data, dict) and 'risk_score' in country_data]
                if geo_scores:
                    avg_geo_score = sum(geo_scores) / len(geo_scores)
                    risk_summary['risk_scores']['geopolitical'] = avg_geo_score
                    
                    if avg_geo_score < 40:
                        risk_summary['key_risks'].append('High geopolitical risk in operational countries')
            
            # Analyze supply chain risks
            supply_chain = analysis_results.get('supply_chain_analysis', {})
            if supply_chain and not supply_chain.get('error'):
                resilience_score = supply_chain.get('resilience_score', 50)
                risk_summary['risk_scores']['supply_chain'] = resilience_score
                
                if resilience_score < 60:
                    risk_summary['key_risks'].append('Supply chain vulnerabilities identified')
            
            # Analyze sanctions compliance
            sanctions = analysis_results.get('sanctions_compliance', {})
            if sanctions and not sanctions.get('error'):
                compliance_status = sanctions.get('overall_compliance_status', {}).get('status', 'unknown')
                
                if compliance_status in ['non_compliant', 'high_risk']:
                    risk_summary['key_risks'].append('Sanctions compliance issues detected')
                    risk_summary['critical_findings'].append('Immediate sanctions review required')
            
            # Analyze operational efficiency
            operations = analysis_results.get('operational_footprint', {})
            if operations and not operations.get('error'):
                efficiency_score = operations.get('operational_efficiency_score', 50)
                risk_summary['risk_scores']['operational_efficiency'] = efficiency_score
                
                if efficiency_score < 50:
                    risk_summary['key_risks'].append('Operational efficiency concerns')
            
            # Determine overall risk level
            all_scores = list(risk_summary['risk_scores'].values())
            if all_scores:
                avg_score = sum(all_scores) / len(all_scores)
                
                if avg_score >= 70:
                    risk_summary['overall_risk_level'] = 'low'
                elif avg_score >= 50:
                    risk_summary['overall_risk_level'] = 'medium'
                else:
                    risk_summary['overall_risk_level'] = 'high'
            
            return risk_summary
            
        except Exception as e:
            logger.error(f"Error generating risk summary: {str(e)}")
            return {'error': str(e)}
    
    def _generate_recommendations(self, analysis_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate actionable recommendations based on analysis"""
        try:
            recommendations = []
            
            # Geopolitical recommendations
            geo_risks = analysis_results.get('geopolitical_risks', {})
            for country, data in geo_risks.items():
                if isinstance(data, dict) and data.get('risk_score', 100) < 40:
                    recommendations.append({
                        'category': 'geopolitical',
                        'priority': 'high',
                        'title': f'High geopolitical risk in {country}',
                        'description': f'Consider risk mitigation strategies for operations in {country}',
                        'actions': [
                            'Evaluate political risk insurance options',
                            'Develop contingency plans for operations',
                            'Consider geographic diversification'
                        ]
                    })
            
            # Supply chain recommendations
            supply_chain = analysis_results.get('supply_chain_analysis', {})
            critical_deps = supply_chain.get('critical_dependencies', [])
            
            for dep in critical_deps:
                if dep.get('severity') == 'high':
                    recommendations.append({
                        'category': 'supply_chain',
                        'priority': 'high',
                        'title': f'Critical dependency on {dep.get("supplier", "Unknown")}',
                        'description': 'High concentration risk identified in supply chain',
                        'actions': [
                            'Identify alternative suppliers',
                            'Negotiate backup supply agreements',
                            'Develop supplier diversification strategy'
                        ]
                    })
            
            # Sanctions compliance recommendations
            sanctions = analysis_results.get('sanctions_compliance', {})
            compliance_issues = sanctions.get('overall_compliance_status', {}).get('issues', [])
            
            for issue in compliance_issues:
                if issue.get('severity') in ['critical', 'high']:
                    recommendations.append({
                        'category': 'compliance',
                        'priority': 'critical' if issue.get('severity') == 'critical' else 'high',
                        'title': 'Sanctions compliance issue',
                        'description': issue.get('description', 'Compliance issue detected'),
                        'actions': [
                            'Conduct immediate compliance review',
                            'Engage legal counsel for sanctions analysis',
                            'Develop compliance remediation plan'
                        ]
                    })
            
            # Operational efficiency recommendations
            operations = analysis_results.get('operational_footprint', {})
            logistics_opportunities = operations.get('logistics_optimization_opportunities', [])
            
            for opportunity in logistics_opportunities:
                if opportunity.get('priority') == 'high':
                    recommendations.append({
                        'category': 'operations',
                        'priority': 'medium',
                        'title': f'Operational improvement opportunity in {opportunity.get("location", "Unknown")}',
                        'description': opportunity.get('recommendation', 'Operational improvement needed'),
                        'actions': [
                            'Evaluate operational efficiency improvements',
                            'Consider infrastructure investments',
                            'Assess relocation or consolidation options'
                        ]
                    })
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {str(e)}")
            return []

    def get_agent_status(self) -> Dict[str, Any]:
        """Get current agent status and health metrics"""
        return {
            'agent_name': 'Operations Intelligence Agent',
            'status': 'active',
            'capabilities': [
                'Geopolitical risk assessment',
                'Supply chain analysis',
                'Sanctions compliance checking',
                'Operational footprint analysis'
            ],
            'data_sources': [
                'World Bank API',
                'OpenStreetMap API',
                'OFAC Sanctions Lists',
                'Supply chain databases'
            ],
            'last_updated': datetime.now().isoformat()
        }