"""
Comprehensive Operational Risk Scoring System

Integrates multiple data sources to provide comprehensive operational risk assessment
"""

import logging
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import asyncio

logger = logging.getLogger(__name__)

class OperationalRiskScorer:
    """
    Comprehensive operational risk scoring system that integrates multiple data sources
    """
    
    def __init__(self):
        self.risk_weights = {
            'geopolitical': 0.25,
            'supply_chain': 0.20,
            'sanctions_compliance': 0.20,
            'operational_efficiency': 0.15,
            'geographic_diversification': 0.10,
            'infrastructure_quality': 0.10
        }
        
        self.risk_thresholds = {
            'low': 30,
            'medium': 60,
            'high': 80
        }
    
    async def calculate_comprehensive_risk_score(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate comprehensive operational risk score from multiple data sources
        
        Args:
            analysis_data: Dictionary containing all operational analysis results
            
        Returns:
            Comprehensive risk assessment with detailed scoring breakdown
        """
        try:
            logger.info("Calculating comprehensive operational risk score")
            
            # Extract individual risk components
            risk_components = await self._extract_risk_components(analysis_data)
            
            # Calculate weighted risk score
            overall_score = self._calculate_weighted_score(risk_components)
            
            # Identify critical risk factors
            critical_factors = self._identify_critical_factors(risk_components)
            
            # Generate risk level assessment
            risk_level = self._determine_risk_level(overall_score)
            
            # Calculate confidence metrics
            confidence_metrics = self._calculate_confidence_metrics(analysis_data)
            
            # Generate risk trend analysis
            risk_trends = self._analyze_risk_trends(risk_components)
            
            return {
                'overall_risk_score': round(overall_score, 2),
                'risk_level': risk_level,
                'risk_components': risk_components,
                'critical_factors': critical_factors,
                'confidence_metrics': confidence_metrics,
                'risk_trends': risk_trends,
                'scoring_methodology': self._get_scoring_methodology(),
                'assessment_timestamp': datetime.now().isoformat(),
                'recommendations': self._generate_risk_recommendations(overall_score, critical_factors)
            }
            
        except Exception as e:
            logger.error(f"Error calculating comprehensive risk score: {str(e)}")
            return {
                'error': str(e),
                'overall_risk_score': 50.0,
                'risk_level': 'medium',
                'assessment_timestamp': datetime.now().isoformat()
            }
    
    async def _extract_risk_components(self, analysis_data: Dict[str, Any]) -> Dict[str, float]:
        """Extract and normalize risk scores from different analysis components"""
        risk_components = {}
        
        # Geopolitical risk
        geo_risks = analysis_data.get('geopolitical_risks', {})
        if geo_risks and not geo_risks.get('error'):
            avg_geo_score = geo_risks.get('average_risk_score', 50)
            risk_components['geopolitical'] = avg_geo_score
        else:
            risk_components['geopolitical'] = 50.0  # Default moderate risk
        
        # Supply chain risk
        supply_chain = analysis_data.get('supply_chain_analysis', {})
        if supply_chain and not supply_chain.get('error'):
            resilience_score = supply_chain.get('resilience_score', 50)
            # Convert resilience to risk (higher resilience = lower risk)
            risk_components['supply_chain'] = 100 - resilience_score
        else:
            risk_components['supply_chain'] = 50.0
        
        # Sanctions compliance risk
        sanctions = analysis_data.get('sanctions_compliance', {})
        if sanctions and not sanctions.get('error'):
            compliance_score = sanctions.get('compliance_score', 50)
            # Convert compliance to risk (higher compliance = lower risk)
            risk_components['sanctions_compliance'] = 100 - compliance_score
        else:
            risk_components['sanctions_compliance'] = 50.0
        
        # Operational efficiency risk
        efficiency = analysis_data.get('operational_efficiency', {})
        if efficiency and not efficiency.get('error'):
            efficiency_score = efficiency.get('cost_optimization_score', 50)
            # Convert efficiency to risk (higher efficiency = lower risk)
            risk_components['operational_efficiency'] = 100 - efficiency_score
        else:
            risk_components['operational_efficiency'] = 50.0
        
        # Geographic diversification risk
        geo_div = self._assess_geographic_diversification_risk(analysis_data)
        risk_components['geographic_diversification'] = geo_div
        
        # Infrastructure quality risk
        infra_risk = self._assess_infrastructure_risk(analysis_data)
        risk_components['infrastructure_quality'] = infra_risk
        
        return risk_components
    
    def _calculate_weighted_score(self, risk_components: Dict[str, float]) -> float:
        """Calculate weighted overall risk score"""
        total_score = 0.0
        total_weight = 0.0
        
        for component, score in risk_components.items():
            weight = self.risk_weights.get(component, 0.0)
            total_score += score * weight
            total_weight += weight
        
        # Normalize if weights don't sum to 1.0
        if total_weight > 0:
            return total_score / total_weight
        else:
            return 50.0  # Default moderate risk
    
    def _identify_critical_factors(self, risk_components: Dict[str, float]) -> List[Dict[str, Any]]:
        """Identify critical risk factors that require immediate attention"""
        critical_factors = []
        
        for component, score in risk_components.items():
            if score > self.risk_thresholds['high']:
                severity = 'critical' if score > 90 else 'high'
                critical_factors.append({
                    'component': component,
                    'risk_score': score,
                    'severity': severity,
                    'description': self._get_risk_description(component, score),
                    'impact': self._assess_risk_impact(component, score)
                })
        
        # Sort by risk score (highest first)
        critical_factors.sort(key=lambda x: x['risk_score'], reverse=True)
        
        return critical_factors
    
    def _determine_risk_level(self, overall_score: float) -> str:
        """Determine overall risk level based on score"""
        if overall_score < self.risk_thresholds['low']:
            return 'low'
        elif overall_score < self.risk_thresholds['medium']:
            return 'medium'
        elif overall_score < self.risk_thresholds['high']:
            return 'high'
        else:
            return 'critical'
    
    def _calculate_confidence_metrics(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate confidence metrics for the risk assessment"""
        data_completeness = 0.0
        data_quality = 0.0
        source_reliability = 0.0
        
        # Assess data completeness
        expected_components = ['geopolitical_risks', 'supply_chain_analysis', 
                             'sanctions_compliance', 'operational_efficiency']
        available_components = sum(1 for comp in expected_components 
                                 if comp in analysis_data and not analysis_data[comp].get('error'))
        data_completeness = (available_components / len(expected_components)) * 100
        
        # Assess data quality (based on presence of detailed metrics)
        quality_indicators = 0
        total_indicators = 0
        
        for component in expected_components:
            if component in analysis_data:
                comp_data = analysis_data[component]
                if isinstance(comp_data, dict) and not comp_data.get('error'):
                    # Count meaningful data points
                    meaningful_keys = [k for k, v in comp_data.items() 
                                     if v is not None and v != '' and k != 'error']
                    quality_indicators += len(meaningful_keys)
                    total_indicators += 5  # Expected number of meaningful metrics per component
        
        data_quality = (quality_indicators / max(total_indicators, 1)) * 100
        
        # Source reliability (based on successful API calls and data freshness)
        source_reliability = min(100, (data_completeness + data_quality) / 2)
        
        return {
            'data_completeness': round(data_completeness, 1),
            'data_quality': round(data_quality, 1),
            'source_reliability': round(source_reliability, 1),
            'overall_confidence': round((data_completeness + data_quality + source_reliability) / 3, 1)
        }
    
    def _analyze_risk_trends(self, risk_components: Dict[str, float]) -> Dict[str, Any]:
        """Analyze risk trends and patterns"""
        # Simple trend analysis based on current scores
        # In production, this would compare with historical data
        
        high_risk_areas = [comp for comp, score in risk_components.items() if score > 70]
        moderate_risk_areas = [comp for comp, score in risk_components.items() if 40 <= score <= 70]
        low_risk_areas = [comp for comp, score in risk_components.items() if score < 40]
        
        # Calculate risk distribution
        risk_distribution = {
            'high_risk_count': len(high_risk_areas),
            'moderate_risk_count': len(moderate_risk_areas),
            'low_risk_count': len(low_risk_areas)
        }
        
        # Identify risk concentration
        max_risk_component = max(risk_components.items(), key=lambda x: x[1])
        min_risk_component = min(risk_components.items(), key=lambda x: x[1])
        
        return {
            'risk_distribution': risk_distribution,
            'highest_risk_area': {
                'component': max_risk_component[0],
                'score': max_risk_component[1]
            },
            'lowest_risk_area': {
                'component': min_risk_component[0],
                'score': min_risk_component[1]
            },
            'risk_concentration': len(high_risk_areas) / len(risk_components) * 100,
            'trend_summary': self._generate_trend_summary(risk_distribution)
        }
    
    def _assess_geographic_diversification_risk(self, analysis_data: Dict[str, Any]) -> float:
        """Assess risk based on geographic diversification"""
        geo_risks = analysis_data.get('geopolitical_risks', {})
        
        if not geo_risks or geo_risks.get('error'):
            return 50.0  # Default moderate risk
        
        countries_analyzed = geo_risks.get('countries_analyzed', 0)
        high_risk_countries = len(geo_risks.get('high_risk_countries', []))
        
        if countries_analyzed == 0:
            return 70.0  # High risk due to lack of diversification data
        
        # Calculate diversification risk
        if countries_analyzed == 1:
            diversification_risk = 80.0  # High concentration risk
        elif countries_analyzed <= 3:
            diversification_risk = 60.0  # Moderate concentration risk
        else:
            diversification_risk = 30.0  # Good diversification
        
        # Adjust for high-risk country exposure
        if high_risk_countries > 0:
            risk_country_penalty = min(40, high_risk_countries * 15)
            diversification_risk += risk_country_penalty
        
        return min(100, diversification_risk)
    
    def _assess_infrastructure_risk(self, analysis_data: Dict[str, Any]) -> float:
        """Assess infrastructure quality risk"""
        efficiency_data = analysis_data.get('operational_efficiency', {})
        
        if not efficiency_data or efficiency_data.get('error'):
            return 50.0  # Default moderate risk
        
        # Use geographic efficiency as proxy for infrastructure quality
        geo_efficiency = efficiency_data.get('geographic_efficiency', 50)
        
        # Convert efficiency to risk (higher efficiency = lower risk)
        infrastructure_risk = 100 - geo_efficiency
        
        return infrastructure_risk
    
    def _get_risk_description(self, component: str, score: float) -> str:
        """Get description for risk component"""
        descriptions = {
            'geopolitical': f'Geopolitical instability in operational regions (Risk Score: {score:.1f})',
            'supply_chain': f'Supply chain vulnerabilities and dependencies (Risk Score: {score:.1f})',
            'sanctions_compliance': f'Sanctions compliance issues detected (Risk Score: {score:.1f})',
            'operational_efficiency': f'Operational inefficiencies identified (Risk Score: {score:.1f})',
            'geographic_diversification': f'Geographic concentration risk (Risk Score: {score:.1f})',
            'infrastructure_quality': f'Infrastructure quality concerns (Risk Score: {score:.1f})'
        }
        
        return descriptions.get(component, f'Risk in {component} (Score: {score:.1f})')
    
    def _assess_risk_impact(self, component: str, score: float) -> str:
        """Assess the potential impact of the risk"""
        if score > 90:
            return 'severe'
        elif score > 70:
            return 'high'
        elif score > 50:
            return 'moderate'
        else:
            return 'low'
    
    def _get_scoring_methodology(self) -> Dict[str, Any]:
        """Return the scoring methodology for transparency"""
        return {
            'risk_weights': self.risk_weights,
            'risk_thresholds': self.risk_thresholds,
            'scoring_approach': 'Weighted average of normalized risk components',
            'scale': '0-100 (0=lowest risk, 100=highest risk)',
            'components': list(self.risk_weights.keys())
        }
    
    def _generate_risk_recommendations(self, overall_score: float, critical_factors: List[Dict[str, Any]]) -> List[str]:
        """Generate risk mitigation recommendations"""
        recommendations = []
        
        # Overall risk recommendations
        if overall_score > 80:
            recommendations.append("CRITICAL: Comprehensive risk mitigation strategy required before proceeding")
            recommendations.append("Consider postponing acquisition until major risks are addressed")
        elif overall_score > 60:
            recommendations.append("Develop detailed risk mitigation plan with specific timelines")
            recommendations.append("Negotiate risk-sharing mechanisms in acquisition terms")
        elif overall_score > 40:
            recommendations.append("Monitor identified risks closely during integration")
            recommendations.append("Implement standard risk management protocols")
        else:
            recommendations.append("Maintain current risk monitoring practices")
        
        # Component-specific recommendations
        for factor in critical_factors[:3]:  # Top 3 critical factors
            component = factor['component']
            
            if component == 'geopolitical':
                recommendations.append("Consider political risk insurance for high-risk regions")
            elif component == 'supply_chain':
                recommendations.append("Diversify supplier base and establish backup sourcing")
            elif component == 'sanctions_compliance':
                recommendations.append("Immediate sanctions compliance review and remediation")
            elif component == 'operational_efficiency':
                recommendations.append("Develop operational improvement plan with clear metrics")
            elif component == 'geographic_diversification':
                recommendations.append("Evaluate geographic expansion opportunities")
            elif component == 'infrastructure_quality':
                recommendations.append("Assess infrastructure investment requirements")
        
        return recommendations
    
    def _generate_trend_summary(self, risk_distribution: Dict[str, int]) -> str:
        """Generate a summary of risk trends"""
        high_count = risk_distribution['high_risk_count']
        moderate_count = risk_distribution['moderate_risk_count']
        low_count = risk_distribution['low_risk_count']
        
        if high_count > moderate_count + low_count:
            return "Risk profile dominated by high-risk factors"
        elif moderate_count > high_count + low_count:
            return "Balanced risk profile with moderate concerns"
        elif low_count > high_count + moderate_count:
            return "Generally low-risk profile with manageable concerns"
        else:
            return "Mixed risk profile requiring balanced approach"