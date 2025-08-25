"""
Geopolitical Risk Analyzer

Analyzes geopolitical risks based on country data and global events
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import numpy as np

logger = logging.getLogger(__name__)

class GeopoliticalAnalyzer:
    """
    Analyzer for geopolitical risks and country stability assessment
    """
    
    def __init__(self):
        # Risk factors and their weights
        self.risk_factors = {
            'governance': 0.25,
            'economic_stability': 0.25,
            'political_stability': 0.20,
            'regional_conflicts': 0.15,
            'sanctions_risk': 0.10,
            'natural_disasters': 0.05
        }
        
        # Country risk profiles (simplified for demo)
        self.country_risk_profiles = self._initialize_country_profiles()
    
    def _initialize_country_profiles(self) -> Dict[str, Dict[str, Any]]:
        """Initialize country risk profiles with known risk factors"""
        return {
            # Low risk countries
            'CHE': {'base_risk': 10, 'stability': 'very_high', 'conflicts': []},
            'NOR': {'base_risk': 12, 'stability': 'very_high', 'conflicts': []},
            'DNK': {'base_risk': 13, 'stability': 'very_high', 'conflicts': []},
            'SWE': {'base_risk': 14, 'stability': 'very_high', 'conflicts': []},
            'FIN': {'base_risk': 15, 'stability': 'very_high', 'conflicts': []},
            'DEU': {'base_risk': 16, 'stability': 'high', 'conflicts': []},
            'NLD': {'base_risk': 17, 'stability': 'high', 'conflicts': []},
            'CAN': {'base_risk': 18, 'stability': 'high', 'conflicts': []},
            'AUS': {'base_risk': 19, 'stability': 'high', 'conflicts': []},
            'USA': {'base_risk': 20, 'stability': 'high', 'conflicts': []},
            
            # Medium risk countries
            'GBR': {'base_risk': 25, 'stability': 'high', 'conflicts': []},
            'FRA': {'base_risk': 28, 'stability': 'high', 'conflicts': []},
            'JPN': {'base_risk': 30, 'stability': 'high', 'conflicts': []},
            'KOR': {'base_risk': 35, 'stability': 'medium', 'conflicts': ['north_korea']},
            'ITA': {'base_risk': 38, 'stability': 'medium', 'conflicts': []},
            'ESP': {'base_risk': 32, 'stability': 'medium', 'conflicts': []},
            'BRA': {'base_risk': 45, 'stability': 'medium', 'conflicts': []},
            'IND': {'base_risk': 50, 'stability': 'medium', 'conflicts': ['pakistan', 'china']},
            'CHN': {'base_risk': 55, 'stability': 'medium', 'conflicts': ['taiwan', 'south_china_sea']},
            'MEX': {'base_risk': 48, 'stability': 'medium', 'conflicts': []},
            
            # Higher risk countries
            'RUS': {'base_risk': 70, 'stability': 'low', 'conflicts': ['ukraine', 'sanctions']},
            'TUR': {'base_risk': 60, 'stability': 'medium', 'conflicts': ['syria', 'kurdish']},
            'IRN': {'base_risk': 75, 'stability': 'low', 'conflicts': ['sanctions', 'regional']},
            'VEN': {'base_risk': 80, 'stability': 'very_low', 'conflicts': ['economic_crisis']},
            'PRK': {'base_risk': 90, 'stability': 'very_low', 'conflicts': ['sanctions', 'isolation']},
            'AFG': {'base_risk': 95, 'stability': 'very_low', 'conflicts': ['taliban', 'instability']},
            'SYR': {'base_risk': 95, 'stability': 'very_low', 'conflicts': ['civil_war']},
            'YEM': {'base_risk': 90, 'stability': 'very_low', 'conflicts': ['civil_war']},
            'LBY': {'base_risk': 85, 'stability': 'very_low', 'conflicts': ['civil_war']},
            'MMR': {'base_risk': 80, 'stability': 'very_low', 'conflicts': ['military_coup']},
        }
    
    async def assess_country_risk(self, country_code: str, world_bank_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess comprehensive geopolitical risk for a country
        
        Args:
            country_code: ISO 3-letter country code
            world_bank_data: World Bank indicators data
            
        Returns:
            Comprehensive risk assessment
        """
        try:
            logger.info(f"Assessing geopolitical risk for {country_code}")
            
            # Get base country profile
            country_profile = self.country_risk_profiles.get(
                country_code, 
                {'base_risk': 50, 'stability': 'medium', 'conflicts': []}
            )
            
            # Calculate component risk scores
            governance_risk = self._assess_governance_risk(world_bank_data)
            economic_risk = self._assess_economic_stability_risk(world_bank_data)
            political_risk = self._assess_political_stability_risk(country_code, country_profile)
            conflict_risk = self._assess_regional_conflict_risk(country_code, country_profile)
            sanctions_risk = self._assess_sanctions_risk(country_code, country_profile)
            disaster_risk = self._assess_natural_disaster_risk(country_code)
            
            # Calculate weighted overall risk
            overall_risk = (
                governance_risk * self.risk_factors['governance'] +
                economic_risk * self.risk_factors['economic_stability'] +
                political_risk * self.risk_factors['political_stability'] +
                conflict_risk * self.risk_factors['regional_conflicts'] +
                sanctions_risk * self.risk_factors['sanctions_risk'] +
                disaster_risk * self.risk_factors['natural_disasters']
            )
            
            # Generate risk factors list
            risk_factors = self._identify_risk_factors(
                governance_risk, economic_risk, political_risk, 
                conflict_risk, sanctions_risk, disaster_risk, country_profile
            )
            
            return {
                'country_code': country_code,
                'risk_score': round(overall_risk, 2),
                'risk_level': self._categorize_risk_level(overall_risk),
                'component_risks': {
                    'governance': governance_risk,
                    'economic_stability': economic_risk,
                    'political_stability': political_risk,
                    'regional_conflicts': conflict_risk,
                    'sanctions': sanctions_risk,
                    'natural_disasters': disaster_risk
                },
                'risk_factors': risk_factors,
                'recommendations': self._generate_country_recommendations(overall_risk, risk_factors),
                'assessment_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error assessing country risk for {country_code}: {str(e)}")
            return {
                'country_code': country_code,
                'risk_score': 50.0,
                'risk_level': 'medium',
                'error': str(e)
            }
    
    def _assess_governance_risk(self, world_bank_data: Dict[str, Any]) -> float:
        """Assess governance risk from World Bank governance indicators"""
        try:
            governance_indicators = ['CC.EST', 'GE.EST', 'RL.EST', 'RQ.EST', 'VA.EST']
            scores = []
            
            indicators = world_bank_data.get('indicators', {})
            for indicator in governance_indicators:
                indicator_data = indicators.get(indicator, {})
                value = indicator_data.get('latest_value')
                
                if value is not None:
                    # World Bank governance indicators range from -2.5 to 2.5
                    # Convert to 0-100 risk scale (higher governance score = lower risk)
                    risk_score = 50 - (value * 20)  # Convert to 0-100 scale
                    scores.append(max(0, min(100, risk_score)))
            
            if scores:
                return sum(scores) / len(scores)
            else:
                return 50.0  # Default moderate risk
                
        except Exception as e:
            logger.error(f"Error assessing governance risk: {str(e)}")
            return 50.0
    
    def _assess_economic_stability_risk(self, world_bank_data: Dict[str, Any]) -> float:
        """Assess economic stability risk"""
        try:
            risk_score = 50  # Base score
            indicators = world_bank_data.get('indicators', {})
            
            # GDP per capita (higher = lower risk)
            gdp_per_capita = indicators.get('NY.GDP.PCAP.CD', {}).get('latest_value')
            if gdp_per_capita:
                if gdp_per_capita > 50000:
                    risk_score -= 15
                elif gdp_per_capita > 25000:
                    risk_score -= 10
                elif gdp_per_capita > 10000:
                    risk_score -= 5
                elif gdp_per_capita < 5000:
                    risk_score += 15
            
            # Inflation (higher = higher risk)
            inflation = indicators.get('FP.CPI.TOTL.ZG', {}).get('latest_value')
            if inflation:
                if inflation > 20:
                    risk_score += 25
                elif inflation > 10:
                    risk_score += 15
                elif inflation > 5:
                    risk_score += 5
                elif inflation < 0:  # Deflation
                    risk_score += 10
            
            # Unemployment (higher = higher risk)
            unemployment = indicators.get('SL.UEM.TOTL.ZS', {}).get('latest_value')
            if unemployment:
                if unemployment > 20:
                    risk_score += 20
                elif unemployment > 15:
                    risk_score += 15
                elif unemployment > 10:
                    risk_score += 10
            
            # Government debt (higher = higher risk)
            debt = indicators.get('GC.DOD.TOTL.GD.ZS', {}).get('latest_value')
            if debt:
                if debt > 120:
                    risk_score += 20
                elif debt > 90:
                    risk_score += 15
                elif debt > 60:
                    risk_score += 10
            
            return max(0, min(100, risk_score))
            
        except Exception as e:
            logger.error(f"Error assessing economic stability risk: {str(e)}")
            return 50.0
    
    def _assess_political_stability_risk(self, country_code: str, country_profile: Dict[str, Any]) -> float:
        """Assess political stability risk"""
        try:
            base_risk = country_profile.get('base_risk', 50)
            stability = country_profile.get('stability', 'medium')
            
            # Adjust based on stability rating
            stability_adjustments = {
                'very_high': -20,
                'high': -10,
                'medium': 0,
                'low': 15,
                'very_low': 30
            }
            
            risk_score = base_risk + stability_adjustments.get(stability, 0)
            
            # Additional adjustments for recent events (simplified)
            current_year = datetime.now().year
            
            # Recent election years might increase short-term instability
            if country_code in ['USA', 'FRA', 'DEU', 'GBR'] and current_year % 4 == 0:
                risk_score += 5
            
            return max(0, min(100, risk_score))
            
        except Exception as e:
            logger.error(f"Error assessing political stability risk: {str(e)}")
            return 50.0
    
    def _assess_regional_conflict_risk(self, country_code: str, country_profile: Dict[str, Any]) -> float:
        """Assess regional conflict and security risk"""
        try:
            conflicts = country_profile.get('conflicts', [])
            base_risk = 20  # Base regional risk
            
            # Add risk for each active conflict
            conflict_risk_map = {
                'ukraine': 30,
                'taiwan': 25,
                'south_china_sea': 20,
                'north_korea': 25,
                'pakistan': 15,
                'china': 10,
                'syria': 35,
                'kurdish': 15,
                'sanctions': 20,
                'regional': 15,
                'economic_crisis': 25,
                'isolation': 30,
                'taliban': 40,
                'instability': 35,
                'civil_war': 45,
                'military_coup': 40
            }
            
            for conflict in conflicts:
                base_risk += conflict_risk_map.get(conflict, 10)
            
            # Regional proximity adjustments
            high_risk_regions = {
                'Middle East': ['IRQ', 'SYR', 'LBN', 'JOR', 'ISR', 'PSE'],
                'Eastern Europe': ['UKR', 'BLR', 'MDA'],
                'Central Asia': ['AFG', 'PAK', 'KAZ', 'UZB', 'TJK'],
                'West Africa': ['MLI', 'BFA', 'NER', 'NGA'],
                'Horn of Africa': ['SOM', 'ETH', 'ERI', 'SDN', 'SSD']
            }
            
            for region, countries in high_risk_regions.items():
                if country_code in countries:
                    base_risk += 15
                    break
            
            return max(0, min(100, base_risk))
            
        except Exception as e:
            logger.error(f"Error assessing regional conflict risk: {str(e)}")
            return 20.0
    
    def _assess_sanctions_risk(self, country_code: str, country_profile: Dict[str, Any]) -> float:
        """Assess sanctions and international isolation risk"""
        try:
            # Countries currently under significant sanctions
            sanctioned_countries = {
                'RUS': 80,  # Comprehensive sanctions
                'IRN': 75,  # Long-term sanctions
                'PRK': 90,  # Comprehensive sanctions
                'CUB': 60,  # US embargo
                'VEN': 70,  # Targeted sanctions
                'SYR': 85,  # Comprehensive sanctions
                'MMR': 65,  # Post-coup sanctions
                'BLR': 70,  # EU/US sanctions
            }
            
            if country_code in sanctioned_countries:
                return sanctioned_countries[country_code]
            
            # Countries at risk of future sanctions
            at_risk_countries = {
                'CHN': 25,  # Trade tensions
                'TUR': 20,  # Regional conflicts
                'SAU': 15,  # Human rights concerns
                'EGY': 10,  # Governance issues
            }
            
            if country_code in at_risk_countries:
                return at_risk_countries[country_code]
            
            return 5.0  # Minimal sanctions risk for most countries
            
        except Exception as e:
            logger.error(f"Error assessing sanctions risk: {str(e)}")
            return 5.0
    
    def _assess_natural_disaster_risk(self, country_code: str) -> float:
        """Assess natural disaster and climate risk"""
        try:
            # Simplified natural disaster risk by country
            disaster_risk_map = {
                # High earthquake risk
                'JPN': 40, 'CHL': 35, 'NZL': 30, 'TUR': 35, 'GRC': 25,
                'ITA': 25, 'IRN': 30, 'PHL': 35, 'IDN': 40, 'MEX': 30,
                
                # High hurricane/typhoon risk
                'USA': 25, 'CUB': 35, 'HTI': 40, 'DOM': 35, 'PHL': 35,
                'VNM': 30, 'BGD': 35, 'IND': 25,
                
                # High flood risk
                'BGD': 40, 'NLD': 20, 'VNM': 30, 'THA': 25, 'PAK': 30,
                
                # High drought risk
                'AUS': 25, 'ZAF': 30, 'KEN': 35, 'ETH': 40, 'SOM': 45,
                
                # Volcanic risk
                'IDN': 35, 'PHL': 30, 'ITA': 20, 'ISL': 25,
                
                # Climate change vulnerability
                'MDV': 50, 'TUV': 50, 'KIR': 50, 'MHL': 50, 'VUT': 45,
                'FJI': 40, 'SLB': 40, 'TON': 40, 'WSM': 35, 'PLW': 35
            }
            
            return disaster_risk_map.get(country_code, 10.0)  # Default low risk
            
        except Exception as e:
            logger.error(f"Error assessing natural disaster risk: {str(e)}")
            return 10.0
    
    def _identify_risk_factors(self, governance_risk: float, economic_risk: float, 
                             political_risk: float, conflict_risk: float, 
                             sanctions_risk: float, disaster_risk: float,
                             country_profile: Dict[str, Any]) -> List[str]:
        """Identify specific risk factors based on component scores"""
        risk_factors = []
        
        if governance_risk > 60:
            risk_factors.append("Weak governance and institutional capacity")
        if economic_risk > 60:
            risk_factors.append("Economic instability and financial risks")
        if political_risk > 60:
            risk_factors.append("Political instability and policy uncertainty")
        if conflict_risk > 40:
            risk_factors.append("Regional conflicts and security threats")
        if sanctions_risk > 30:
            risk_factors.append("International sanctions and isolation risk")
        if disaster_risk > 30:
            risk_factors.append("Natural disaster and climate vulnerability")
        
        # Add specific conflicts from country profile
        conflicts = country_profile.get('conflicts', [])
        if conflicts:
            risk_factors.append(f"Active conflicts: {', '.join(conflicts)}")
        
        return risk_factors
    
    def _generate_country_recommendations(self, overall_risk: float, risk_factors: List[str]) -> List[str]:
        """Generate recommendations based on risk assessment"""
        recommendations = []
        
        if overall_risk > 70:
            recommendations.append("Consider avoiding operations in this country due to high risk")
            recommendations.append("If operations are necessary, implement comprehensive risk mitigation")
        elif overall_risk > 50:
            recommendations.append("Implement enhanced due diligence and risk monitoring")
            recommendations.append("Consider political risk insurance for significant investments")
        elif overall_risk > 30:
            recommendations.append("Monitor political and economic developments regularly")
            recommendations.append("Maintain contingency plans for potential disruptions")
        else:
            recommendations.append("Country presents acceptable risk for business operations")
        
        # Specific recommendations based on risk factors
        if any("sanctions" in factor.lower() for factor in risk_factors):
            recommendations.append("Ensure strict compliance with international sanctions regimes")
        
        if any("conflict" in factor.lower() for factor in risk_factors):
            recommendations.append("Monitor security situation and maintain evacuation plans")
        
        if any("economic" in factor.lower() for factor in risk_factors):
            recommendations.append("Hedge currency exposure and monitor financial stability")
        
        return recommendations
    
    def _categorize_risk_level(self, risk_score: float) -> str:
        """Categorize numerical risk score into risk level"""
        if risk_score < 25:
            return 'low'
        elif risk_score < 50:
            return 'medium'
        elif risk_score < 75:
            return 'high'
        else:
            return 'critical'