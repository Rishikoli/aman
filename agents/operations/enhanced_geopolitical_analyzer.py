"""
Enhanced Geopolitical Risk Analysis Module

Analyzes geopolitical risks for M&A operations with enhanced supply chain vulnerability assessment
"""

import logging
import asyncio
from typing import Dict, List, Any, Optional, Tuple
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class EnhancedGeopoliticalAnalyzer:
    """
    Enhanced geopolitical risk analyzer with supply chain vulnerability assessment
    """
    
    def __init__(self):
        self.risk_indicators = {
            'political_stability': 0.3,
            'regulatory_quality': 0.25,
            'rule_of_law': 0.2,
            'control_of_corruption': 0.15,
            'voice_accountability': 0.1
        }
        
        # Enhanced risk factors for supply chain analysis
        self.supply_chain_risk_factors = {
            'trade_restrictions': 0.25,
            'border_security': 0.20,
            'infrastructure_quality': 0.20,
            'currency_stability': 0.15,
            'labor_stability': 0.10,
            'natural_disaster_risk': 0.10
        }
        
        # Critical supply chain chokepoints
        self.critical_chokepoints = {
            'suez_canal': ['egypt'],
            'strait_of_hormuz': ['iran', 'oman', 'uae'],
            'strait_of_malacca': ['malaysia', 'singapore', 'indonesia'],
            'panama_canal': ['panama'],
            'bosphorus_strait': ['turkey'],
            'strait_of_gibraltar': ['spain', 'morocco']
        }
        
    async def assess_country_risk(self, country: str, wb_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enhanced country risk assessment with supply chain considerations
        
        Args:
            country: Country name or code
            wb_data: World Bank governance indicators
            
        Returns:
            Enhanced country risk assessment
        """
        try:
            logger.info(f"Assessing enhanced geopolitical risk for {country}")
            
            # Calculate governance risk score
            governance_score = self._calculate_governance_score(wb_data)
            
            # Assess economic stability
            economic_risk = self._assess_economic_risk(wb_data)
            
            # Evaluate political risk factors
            political_risk = self._evaluate_political_risk(country, wb_data)
            
            # NEW: Assess supply chain vulnerability
            supply_chain_risk = await self._assess_supply_chain_vulnerability(country, wb_data)
            
            # NEW: Evaluate strategic chokepoint exposure
            chokepoint_risk = self._evaluate_chokepoint_risk(country)
            
            # Calculate enhanced overall risk score
            overall_risk = self._calculate_enhanced_overall_risk(
                governance_score, economic_risk, political_risk, 
                supply_chain_risk, chokepoint_risk
            )
            
            # Identify comprehensive risk factors
            risk_factors = self._identify_enhanced_risk_factors(
                country, wb_data, overall_risk, supply_chain_risk, chokepoint_risk
            )
            
            # NEW: Generate supply chain recommendations
            supply_chain_recommendations = self._generate_supply_chain_recommendations(
                country, supply_chain_risk, chokepoint_risk
            )
            
            return {
                'country': country,
                'risk_score': overall_risk,
                'governance_score': governance_score,
                'economic_risk': economic_risk,
                'political_risk': political_risk,
                'supply_chain_risk': supply_chain_risk,
                'chokepoint_risk': chokepoint_risk,
                'risk_factors': risk_factors,
                'supply_chain_recommendations': supply_chain_recommendations,
                'risk_level': self._categorize_risk_level(overall_risk),
                'vulnerability_assessment': self._create_vulnerability_assessment(
                    supply_chain_risk, chokepoint_risk
                ),
                'assessment_date': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error assessing country risk for {country}: {str(e)}")
            return {
                'country': country,
                'error': str(e),
                'risk_score': 50,  # Default moderate risk
                'assessment_date': datetime.now().isoformat()
            }
    
    async def _assess_supply_chain_vulnerability(self, country: str, wb_data: Dict[str, Any]) -> float:
        """
        Assess supply chain vulnerability for the country
        
        Args:
            country: Country name
            wb_data: World Bank data
            
        Returns:
            Supply chain vulnerability score (0-100, higher = more vulnerable)
        """
        try:
            vulnerability_score = 0.0
            
            # Trade restrictions assessment
            trade_risk = self._assess_trade_restrictions(country, wb_data)
            vulnerability_score += trade_risk * self.supply_chain_risk_factors['trade_restrictions']
            
            # Border security and customs efficiency
            border_risk = self._assess_border_security(country, wb_data)
            vulnerability_score += border_risk * self.supply_chain_risk_factors['border_security']
            
            # Infrastructure quality
            infrastructure_risk = self._assess_infrastructure_quality(country, wb_data)
            vulnerability_score += infrastructure_risk * self.supply_chain_risk_factors['infrastructure_quality']
            
            # Currency stability
            currency_risk = self._assess_currency_stability(country, wb_data)
            vulnerability_score += currency_risk * self.supply_chain_risk_factors['currency_stability']
            
            # Labor stability
            labor_risk = self._assess_labor_stability(country, wb_data)
            vulnerability_score += labor_risk * self.supply_chain_risk_factors['labor_stability']
            
            # Natural disaster risk
            disaster_risk = self._assess_natural_disaster_risk(country)
            vulnerability_score += disaster_risk * self.supply_chain_risk_factors['natural_disaster_risk']
            
            return min(100, max(0, vulnerability_score))
            
        except Exception as e:
            logger.error(f"Error assessing supply chain vulnerability: {str(e)}")
            return 50.0
    
    def _assess_trade_restrictions(self, country: str, wb_data: Dict[str, Any]) -> float:
        """Assess trade restriction risks"""
        try:
            # Base assessment on regulatory quality and known trade issues
            regulatory_quality = wb_data.get('governance_indicators', {}).get('regulatory_quality', 0)
            
            # Convert WB scale to risk score
            base_risk = max(0, 50 - (regulatory_quality * 20))
            
            # Adjust for known trade restriction issues
            high_restriction_countries = [
                'russia', 'china', 'iran', 'north korea', 'cuba', 'venezuela',
                'myanmar', 'belarus', 'syria'
            ]
            
            country_lower = country.lower()
            if any(restricted in country_lower for restricted in high_restriction_countries):
                base_risk += 30
            
            return min(100, base_risk)
            
        except Exception as e:
            logger.error(f"Error assessing trade restrictions: {str(e)}")
            return 50.0
    
    def _assess_border_security(self, country: str, wb_data: Dict[str, Any]) -> float:
        """Assess border security and customs efficiency risks"""
        try:
            # Use rule of law as proxy for border security efficiency
            rule_of_law = wb_data.get('governance_indicators', {}).get('rule_of_law', 0)
            
            # Convert to risk score
            border_risk = max(0, 50 - (rule_of_law * 20))
            
            # Adjust for countries with known border issues
            high_border_risk_countries = [
                'afghanistan', 'syria', 'somalia', 'yemen', 'libya',
                'mali', 'burkina faso', 'niger', 'chad'
            ]
            
            country_lower = country.lower()
            if any(risk_country in country_lower for risk_country in high_border_risk_countries):
                border_risk += 25
            
            return min(100, border_risk)
            
        except Exception as e:
            logger.error(f"Error assessing border security: {str(e)}")
            return 50.0
    
    def _assess_infrastructure_quality(self, country: str, wb_data: Dict[str, Any]) -> float:
        """Assess infrastructure quality risks"""
        try:
            # Use economic indicators as proxy for infrastructure quality
            economic_indicators = wb_data.get('economic_indicators', {})
            gdp_per_capita = economic_indicators.get('gdp_per_capita', 10000)
            
            # Lower GDP per capita generally correlates with poorer infrastructure
            if gdp_per_capita < 5000:
                infrastructure_risk = 70
            elif gdp_per_capita < 15000:
                infrastructure_risk = 50
            elif gdp_per_capita < 30000:
                infrastructure_risk = 30
            else:
                infrastructure_risk = 20
            
            return infrastructure_risk
            
        except Exception as e:
            logger.error(f"Error assessing infrastructure quality: {str(e)}")
            return 50.0
    
    def _assess_currency_stability(self, country: str, wb_data: Dict[str, Any]) -> float:
        """Assess currency stability risks"""
        try:
            economic_indicators = wb_data.get('economic_indicators', {})
            inflation_rate = economic_indicators.get('inflation_rate', 5)
            
            # High inflation indicates currency instability
            if inflation_rate > 20:
                currency_risk = 80
            elif inflation_rate > 10:
                currency_risk = 60
            elif inflation_rate > 5:
                currency_risk = 40
            else:
                currency_risk = 20
            
            # Adjust for countries with known currency issues
            currency_crisis_countries = [
                'venezuela', 'turkey', 'argentina', 'lebanon', 'sri lanka',
                'zimbabwe', 'iran'
            ]
            
            country_lower = country.lower()
            if any(crisis_country in country_lower for crisis_country in currency_crisis_countries):
                currency_risk = min(100, currency_risk + 30)
            
            return currency_risk
            
        except Exception as e:
            logger.error(f"Error assessing currency stability: {str(e)}")
            return 50.0
    
    def _assess_labor_stability(self, country: str, wb_data: Dict[str, Any]) -> float:
        """Assess labor stability and strike risks"""
        try:
            # Use unemployment rate and political stability as proxies
            economic_indicators = wb_data.get('economic_indicators', {})
            governance_indicators = wb_data.get('governance_indicators', {})
            
            unemployment = economic_indicators.get('unemployment_rate', 8)
            political_stability = governance_indicators.get('political_stability', 0)
            
            # High unemployment increases labor unrest risk
            labor_risk = min(60, unemployment * 3)
            
            # Poor political stability increases strike risk
            if political_stability < -1:
                labor_risk += 25
            elif political_stability < 0:
                labor_risk += 10
            
            return min(100, labor_risk)
            
        except Exception as e:
            logger.error(f"Error assessing labor stability: {str(e)}")
            return 50.0
    
    def _assess_natural_disaster_risk(self, country: str) -> float:
        """Assess natural disaster risks"""
        try:
            # Simple assessment based on known high-risk regions
            high_disaster_risk_countries = [
                'japan', 'philippines', 'indonesia', 'chile', 'peru',
                'bangladesh', 'myanmar', 'haiti', 'nepal'
            ]
            
            moderate_disaster_risk_countries = [
                'india', 'china', 'mexico', 'turkey', 'italy',
                'greece', 'iran', 'pakistan', 'afghanistan'
            ]
            
            country_lower = country.lower()
            
            if any(risk_country in country_lower for risk_country in high_disaster_risk_countries):
                return 70
            elif any(risk_country in country_lower for risk_country in moderate_disaster_risk_countries):
                return 45
            else:
                return 25  # Base risk for all countries
                
        except Exception as e:
            logger.error(f"Error assessing natural disaster risk: {str(e)}")
            return 30.0
    
    def _evaluate_chokepoint_risk(self, country: str) -> float:
        """Evaluate strategic chokepoint exposure risk"""
        try:
            country_lower = country.lower()
            chokepoint_risk = 0.0
            
            # Check if country controls or is near critical chokepoints
            for chokepoint, countries in self.critical_chokepoints.items():
                if any(choke_country in country_lower for choke_country in countries):
                    # Countries controlling chokepoints have higher risk
                    if chokepoint in ['suez_canal', 'strait_of_hormuz']:
                        chokepoint_risk += 30  # Critical global trade routes
                    elif chokepoint in ['strait_of_malacca', 'panama_canal']:
                        chokepoint_risk += 25  # Major trade routes
                    else:
                        chokepoint_risk += 15  # Regional importance
            
            return min(100, chokepoint_risk)
            
        except Exception as e:
            logger.error(f"Error evaluating chokepoint risk: {str(e)}")
            return 0.0
    
    def _calculate_enhanced_overall_risk(self, governance_score: float, economic_risk: float, 
                                       political_risk: float, supply_chain_risk: float, 
                                       chokepoint_risk: float) -> float:
        """Calculate enhanced overall geopolitical risk score"""
        try:
            # Enhanced weighted average including supply chain factors
            weights = {
                'governance': 0.25,
                'economic': 0.20,
                'political': 0.25,
                'supply_chain': 0.20,
                'chokepoint': 0.10
            }
            
            overall_risk = (
                governance_score * weights['governance'] +
                economic_risk * weights['economic'] +
                political_risk * weights['political'] +
                supply_chain_risk * weights['supply_chain'] +
                chokepoint_risk * weights['chokepoint']
            )
            
            return round(overall_risk, 2)
            
        except Exception as e:
            logger.error(f"Error calculating enhanced overall risk: {str(e)}")
            return 50.0
    
    def _identify_enhanced_risk_factors(self, country: str, wb_data: Dict[str, Any], 
                                      overall_risk: float, supply_chain_risk: float, 
                                      chokepoint_risk: float) -> List[str]:
        """Identify enhanced risk factors including supply chain vulnerabilities"""
        risk_factors = []
        
        try:
            # Original risk factors
            governance_indicators = wb_data.get('governance_indicators', {})
            economic_indicators = wb_data.get('economic_indicators', {})
            
            # Governance-related risks
            if governance_indicators.get('political_stability', 0) < -1:
                risk_factors.append("Political instability and potential for conflict")
            
            if governance_indicators.get('regulatory_quality', 0) < -1:
                risk_factors.append("Poor regulatory environment and business climate")
            
            if governance_indicators.get('rule_of_law', 0) < -1:
                risk_factors.append("Weak rule of law and legal system")
            
            if governance_indicators.get('control_of_corruption', 0) < -1:
                risk_factors.append("High levels of corruption")
            
            # Economic risks
            gdp_growth = economic_indicators.get('gdp_growth')
            if gdp_growth is not None and gdp_growth < 0:
                risk_factors.append(f"Economic recession with {gdp_growth:.1f}% GDP decline")
            
            inflation = economic_indicators.get('inflation_rate')
            if inflation is not None and inflation > 10:
                risk_factors.append(f"High inflation rate at {inflation:.1f}%")
            
            unemployment = economic_indicators.get('unemployment_rate')
            if unemployment is not None and unemployment > 15:
                risk_factors.append(f"High unemployment at {unemployment:.1f}%")
            
            # NEW: Supply chain specific risks
            if supply_chain_risk > 70:
                risk_factors.append("Critical supply chain vulnerabilities identified")
            elif supply_chain_risk > 50:
                risk_factors.append("Significant supply chain risks present")
            
            if chokepoint_risk > 20:
                risk_factors.append("Strategic chokepoint exposure increases supply chain risk")
            
            # Overall risk assessment
            if overall_risk > 80:
                risk_factors.append("Critical risk level - operations strongly discouraged")
            elif overall_risk > 60:
                risk_factors.append("High risk level - enhanced due diligence required")
            
            return risk_factors
            
        except Exception as e:
            logger.error(f"Error identifying enhanced risk factors: {str(e)}")
            return ["Unable to assess specific risk factors"]
    
    def _generate_supply_chain_recommendations(self, country: str, supply_chain_risk: float, 
                                             chokepoint_risk: float) -> List[str]:
        """Generate supply chain specific recommendations"""
        recommendations = []
        
        try:
            if supply_chain_risk > 70:
                recommendations.append("Implement comprehensive supply chain diversification strategy")
                recommendations.append("Establish multiple backup suppliers outside high-risk regions")
                recommendations.append("Consider supply chain insurance for critical components")
            elif supply_chain_risk > 50:
                recommendations.append("Develop contingency plans for supply chain disruptions")
                recommendations.append("Monitor supply chain risks continuously")
            
            if chokepoint_risk > 20:
                recommendations.append("Evaluate alternative shipping routes to reduce chokepoint dependency")
                recommendations.append("Consider regional supply chain hubs to minimize transit risks")
            
            # Country-specific recommendations
            country_lower = country.lower()
            if any(restricted in country_lower for restricted in ['russia', 'china', 'iran']):
                recommendations.append("Review sanctions compliance requirements regularly")
                recommendations.append("Establish alternative sourcing outside sanctioned regions")
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating supply chain recommendations: {str(e)}")
            return ["Conduct detailed supply chain risk assessment"]
    
    def _create_vulnerability_assessment(self, supply_chain_risk: float, chokepoint_risk: float) -> Dict[str, Any]:
        """Create comprehensive vulnerability assessment"""
        try:
            vulnerability_level = 'low'
            if supply_chain_risk > 70 or chokepoint_risk > 30:
                vulnerability_level = 'high'
            elif supply_chain_risk > 50 or chokepoint_risk > 15:
                vulnerability_level = 'medium'
            
            return {
                'vulnerability_level': vulnerability_level,
                'supply_chain_score': supply_chain_risk,
                'chokepoint_score': chokepoint_risk,
                'key_vulnerabilities': self._identify_key_vulnerabilities(supply_chain_risk, chokepoint_risk),
                'mitigation_priority': 'high' if vulnerability_level == 'high' else 'medium'
            }
            
        except Exception as e:
            logger.error(f"Error creating vulnerability assessment: {str(e)}")
            return {'vulnerability_level': 'unknown', 'error': str(e)}
    
    def _identify_key_vulnerabilities(self, supply_chain_risk: float, chokepoint_risk: float) -> List[str]:
        """Identify key vulnerabilities based on risk scores"""
        vulnerabilities = []
        
        if supply_chain_risk > 60:
            vulnerabilities.append("Supply chain disruption risk")
        if chokepoint_risk > 20:
            vulnerabilities.append("Strategic chokepoint dependency")
        if supply_chain_risk > 70:
            vulnerabilities.append("Critical supplier concentration")
        
        return vulnerabilities
    
    def _calculate_governance_score(self, wb_data: Dict[str, Any]) -> float:
        """Calculate governance risk score from World Bank indicators"""
        try:
            governance_indicators = wb_data.get('governance_indicators', {})
            
            if not governance_indicators:
                return 50.0  # Default moderate risk
            
            # World Bank governance indicators are typically on a scale from -2.5 to 2.5
            # Convert to 0-100 risk scale (higher score = higher risk)
            
            total_score = 0
            total_weight = 0
            
            for indicator, weight in self.risk_indicators.items():
                value = governance_indicators.get(indicator)
                if value is not None:
                    # Convert WB scale (-2.5 to 2.5) to risk scale (0-100)
                    # Higher WB score = better governance = lower risk
                    risk_score = max(0, min(100, 50 - (value * 20)))
                    total_score += risk_score * weight
                    total_weight += weight
            
            if total_weight > 0:
                return total_score / total_weight
            else:
                return 50.0
                
        except Exception as e:
            logger.error(f"Error calculating governance score: {str(e)}")
            return 50.0
    
    def _assess_economic_risk(self, wb_data: Dict[str, Any]) -> float:
        """Assess economic stability risk"""
        try:
            economic_indicators = wb_data.get('economic_indicators', {})
            
            if not economic_indicators:
                return 50.0
            
            risk_factors = []
            
            # GDP growth volatility
            gdp_growth = economic_indicators.get('gdp_growth')
            if gdp_growth is not None:
                if gdp_growth < -2:
                    risk_factors.append(30)  # High risk for negative growth
                elif gdp_growth < 2:
                    risk_factors.append(20)  # Moderate risk for low growth
                else:
                    risk_factors.append(10)  # Low risk for healthy growth
            
            # Inflation rate
            inflation = economic_indicators.get('inflation_rate')
            if inflation is not None:
                if inflation > 10:
                    risk_factors.append(25)  # High risk for high inflation
                elif inflation > 5:
                    risk_factors.append(15)  # Moderate risk
                else:
                    risk_factors.append(5)   # Low risk for stable inflation
            
            # Unemployment rate
            unemployment = economic_indicators.get('unemployment_rate')
            if unemployment is not None:
                if unemployment > 15:
                    risk_factors.append(20)  # High risk
                elif unemployment > 8:
                    risk_factors.append(10)  # Moderate risk
                else:
                    risk_factors.append(5)   # Low risk
            
            if risk_factors:
                return min(100, sum(risk_factors))
            else:
                return 50.0
                
        except Exception as e:
            logger.error(f"Error assessing economic risk: {str(e)}")
            return 50.0
    
    def _evaluate_political_risk(self, country: str, wb_data: Dict[str, Any]) -> float:
        """Evaluate political risk factors"""
        try:
            # Base political risk assessment
            base_risk = 30.0
            
            # Adjust based on known high-risk regions/countries
            high_risk_regions = [
                'afghanistan', 'syria', 'yemen', 'somalia', 'south sudan',
                'venezuela', 'myanmar', 'haiti', 'mali', 'burkina faso'
            ]
            
            moderate_risk_regions = [
                'russia', 'belarus', 'iran', 'north korea', 'cuba',
                'zimbabwe', 'nicaragua', 'eritrea'
            ]
            
            country_lower = country.lower()
            
            if any(risk_country in country_lower for risk_country in high_risk_regions):
                base_risk += 40
            elif any(risk_country in country_lower for risk_country in moderate_risk_regions):
                base_risk += 20
            
            # Adjust based on governance indicators
            governance_indicators = wb_data.get('governance_indicators', {})
            political_stability = governance_indicators.get('political_stability')
            
            if political_stability is not None:
                # Convert WB scale to risk adjustment
                if political_stability < -1.5:
                    base_risk += 25
                elif political_stability < -0.5:
                    base_risk += 10
                elif political_stability > 1.0:
                    base_risk -= 10
            
            return min(100, max(0, base_risk))
            
        except Exception as e:
            logger.error(f"Error evaluating political risk: {str(e)}")
            return 50.0
    
    def _categorize_risk_level(self, risk_score: float) -> str:
        """Categorize numerical risk score into risk level"""
        if risk_score < 30:
            return 'low'
        elif risk_score < 60:
            return 'medium'
        elif risk_score < 80:
            return 'high'
        else:
            return 'critical'