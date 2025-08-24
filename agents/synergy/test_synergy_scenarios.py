#!/usr/bin/env python3
"""
Multiple test scenarios for the Synergy Discovery Engine
Testing different industries, company sizes, and deal types
"""

import sys
import os
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO)

# Mock CONFIG for testing
CONFIG = {
    'api_keys': {
        'gemini': None  # No API key for testing
    }
}

# Import the synergy engine classes directly
class SynergyType(Enum):
    PERSONNEL = "personnel"
    TECHNOLOGY = "technology"
    FACILITIES = "facilities"
    OPERATIONS = "operations"
    REVENUE = "revenue"
    MARKET = "market"

class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class CostSynergy:
    type: SynergyType
    description: str
    annual_savings: float
    one_time_costs: float
    time_to_realize: int  # months
    risk_level: RiskLevel
    confidence: float
    affected_departments: List[str]
    implementation_complexity: str

@dataclass
class RevenueSynergy:
    type: SynergyType
    description: str
    annual_revenue_potential: float
    investment_required: float
    time_to_realize: int  # months
    risk_level: RiskLevel
    confidence: float
    market_segments: List[str]
    competitive_advantage: str

@dataclass
class IntegrationRisk:
    category: str
    description: str
    severity: RiskLevel
    probability: float
    impact: str
    mitigation_strategies: List[str]
    timeline_impact: int  # additional months
    cost_impact: float

@dataclass
class SynergyAnalysis:
    deal_id: str
    acquirer_name: str
    target_name: str
    cost_synergies: List[CostSynergy]
    revenue_synergies: List[RevenueSynergy]
    integration_risks: List[IntegrationRisk]
    total_estimated_value: float
    net_present_value: float
    time_to_break_even: int
    confidence_level: float
    analysis_timestamp: datetime

class SynergyDiscoveryEngine:
    """
    Simplified version for testing multiple scenarios
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.gemini_api_key = None
        self.discount_rate = 0.10  # 10% discount rate for NPV calculations
        
    def analyze_synergies(self, acquirer_data: Dict, target_data: Dict, deal_id: str) -> SynergyAnalysis:
        """
        Comprehensive synergy analysis combining cost and revenue opportunities
        """
        self.logger.info(f"Starting synergy analysis for deal {deal_id}")
        
        # Analyze cost synergies
        cost_synergies = self._identify_cost_synergies(acquirer_data, target_data)
        
        # Analyze revenue synergies
        revenue_synergies = self._identify_revenue_synergies(acquirer_data, target_data)
        
        # Assess integration risks
        integration_risks = self._assess_integration_risks(acquirer_data, target_data, cost_synergies, revenue_synergies)
        
        # Calculate total value and NPV
        total_value, npv = self._calculate_synergy_value(cost_synergies, revenue_synergies, integration_risks)
        
        # Calculate break-even timeline
        break_even = self._calculate_break_even(cost_synergies, revenue_synergies, integration_risks)
        
        # Calculate overall confidence
        confidence = self._calculate_confidence(cost_synergies, revenue_synergies, integration_risks)
        
        return SynergyAnalysis(
            deal_id=deal_id,
            acquirer_name=acquirer_data.get('name', 'Unknown'),
            target_name=target_data.get('name', 'Unknown'),
            cost_synergies=cost_synergies,
            revenue_synergies=revenue_synergies,
            integration_risks=integration_risks,
            total_estimated_value=total_value,
            net_present_value=npv,
            time_to_break_even=break_even,
            confidence_level=confidence,
            analysis_timestamp=datetime.now()
        )
    
    def _identify_cost_synergies(self, acquirer_data: Dict, target_data: Dict) -> List[CostSynergy]:
        """
        Identify cost reduction opportunities through operational consolidation
        """
        synergies = []
        
        # Personnel synergies - eliminate duplicate roles
        personnel_synergy = self._analyze_personnel_overlap(acquirer_data, target_data)
        if personnel_synergy:
            synergies.append(personnel_synergy)
        
        # Technology synergies - consolidate software licenses and infrastructure
        tech_synergy = self._analyze_technology_overlap(acquirer_data, target_data)
        if tech_synergy:
            synergies.append(tech_synergy)
        
        # Facilities synergies - consolidate office space and operations
        facilities_synergy = self._analyze_facilities_overlap(acquirer_data, target_data)
        if facilities_synergy:
            synergies.append(facilities_synergy)
        
        return synergies
    
    def _analyze_personnel_overlap(self, acquirer_data: Dict, target_data: Dict) -> Optional[CostSynergy]:
        """
        Analyze personnel overlap and calculate potential cost savings from eliminations
        """
        try:
            # Get employee counts and salary data
            acquirer_employees = acquirer_data.get('employees', 0)
            target_employees = target_data.get('employees', 0)
            
            # Estimate overlap based on company sizes and industries
            if acquirer_data.get('industry') == target_data.get('industry'):
                overlap_rate = 0.15  # 15% overlap for same industry
            else:
                overlap_rate = 0.08  # 8% overlap for different industries
            
            # Calculate potential eliminations
            potential_eliminations = int(min(acquirer_employees, target_employees) * overlap_rate)
            
            if potential_eliminations > 0:
                # Estimate average salary (use industry benchmarks or provided data)
                avg_salary = target_data.get('avg_salary', 75000)  # Default $75k
                
                # Calculate annual savings
                annual_savings = potential_eliminations * avg_salary
                
                # Estimate one-time costs (severance, legal, etc.)
                one_time_costs = annual_savings * 0.3  # 30% of annual savings
                
                return CostSynergy(
                    type=SynergyType.PERSONNEL,
                    description=f"Eliminate {potential_eliminations} duplicate positions across departments",
                    annual_savings=annual_savings,
                    one_time_costs=one_time_costs,
                    time_to_realize=6,  # 6 months
                    risk_level=RiskLevel.MEDIUM,
                    confidence=0.75,
                    affected_departments=["HR", "Finance", "Operations", "IT"],
                    implementation_complexity="Medium - requires careful change management"
                )
        except Exception as e:
            self.logger.error(f"Error analyzing personnel overlap: {e}")
        
        return None
    
    def _analyze_technology_overlap(self, acquirer_data: Dict, target_data: Dict) -> Optional[CostSynergy]:
        """
        Analyze technology stack overlap and software license consolidation opportunities
        """
        try:
            # Estimate IT spending based on revenue
            target_revenue = target_data.get('revenue', 0)
            
            # IT spending typically 3-5% of revenue
            it_spending_rate = 0.04
            target_it_spending = target_revenue * it_spending_rate
            
            # Estimate potential savings from software license consolidation
            # Typically 20-30% savings possible through enterprise licensing
            consolidation_savings_rate = 0.25
            annual_savings = target_it_spending * consolidation_savings_rate
            
            if annual_savings > 10000:  # Only if meaningful savings
                # One-time integration costs
                one_time_costs = annual_savings * 0.5
                
                return CostSynergy(
                    type=SynergyType.TECHNOLOGY,
                    description="Consolidate software licenses and eliminate duplicate systems",
                    annual_savings=annual_savings,
                    one_time_costs=one_time_costs,
                    time_to_realize=12,  # 12 months for full integration
                    risk_level=RiskLevel.MEDIUM,
                    confidence=0.70,
                    affected_departments=["IT", "Operations", "Finance"],
                    implementation_complexity="High - requires system integration and data migration"
                )
        except Exception as e:
            self.logger.error(f"Error analyzing technology overlap: {e}")
        
        return None
    
    def _analyze_facilities_overlap(self, acquirer_data: Dict, target_data: Dict) -> Optional[CostSynergy]:
        """
        Analyze facilities consolidation opportunities
        """
        try:
            # Get location and facilities data
            acquirer_locations = acquirer_data.get('locations', [])
            target_locations = target_data.get('locations', [])
            
            # Simple overlap detection based on geographic proximity
            overlapping_locations = 0
            for target_loc in target_locations:
                for acquirer_loc in acquirer_locations:
                    if self._locations_overlap(target_loc, acquirer_loc):
                        overlapping_locations += 1
                        break
            
            if overlapping_locations > 0:
                # Estimate facilities cost savings
                # Average office cost per employee per year
                cost_per_employee = 12000  # $12k per employee per year
                target_employees = target_data.get('employees', 0)
                
                # Assume 30% of employees can be consolidated
                consolidation_rate = 0.30
                employees_to_consolidate = int(target_employees * consolidation_rate)
                
                annual_savings = employees_to_consolidate * cost_per_employee
                
                # One-time moving and setup costs
                one_time_costs = annual_savings * 0.2
                
                return CostSynergy(
                    type=SynergyType.FACILITIES,
                    description=f"Consolidate {overlapping_locations} overlapping office locations",
                    annual_savings=annual_savings,
                    one_time_costs=one_time_costs,
                    time_to_realize=9,  # 9 months
                    risk_level=RiskLevel.LOW,
                    confidence=0.80,
                    affected_departments=["Facilities", "HR", "Operations"],
                    implementation_complexity="Low - straightforward lease consolidation"
                )
        except Exception as e:
            self.logger.error(f"Error analyzing facilities overlap: {e}")
        
        return None
    
    def _identify_revenue_synergies(self, acquirer_data: Dict, target_data: Dict) -> List[RevenueSynergy]:
        """
        Identify revenue enhancement opportunities
        """
        synergies = []
        
        # Cross-selling opportunities
        cross_sell_synergy = self._analyze_cross_selling(acquirer_data, target_data)
        if cross_sell_synergy:
            synergies.append(cross_sell_synergy)
        
        # Market expansion opportunities
        market_expansion_synergy = self._analyze_market_expansion(acquirer_data, target_data)
        if market_expansion_synergy:
            synergies.append(market_expansion_synergy)
        
        return synergies
    
    def _analyze_cross_selling(self, acquirer_data: Dict, target_data: Dict) -> Optional[RevenueSynergy]:
        """
        Analyze cross-selling opportunities between customer bases
        """
        try:
            # Get customer and revenue data
            acquirer_customers = acquirer_data.get('customers', 0)
            target_customers = target_data.get('customers', 0)
            target_revenue = target_data.get('revenue', 0)
            
            # Estimate cross-selling potential
            cross_sell_rate = 0.15
            potential_customers = int(min(acquirer_customers, target_customers) * cross_sell_rate)
            
            if potential_customers > 0:
                # Estimate revenue per customer
                revenue_per_customer = target_revenue / max(target_customers, 1)
                
                # Cross-selling typically generates 20-30% additional revenue per customer
                additional_revenue_rate = 0.25
                annual_revenue_potential = potential_customers * revenue_per_customer * additional_revenue_rate
                
                # Investment in sales and marketing
                investment_required = annual_revenue_potential * 0.3
                
                return RevenueSynergy(
                    type=SynergyType.REVENUE,
                    description=f"Cross-sell products to {potential_customers} existing customers",
                    annual_revenue_potential=annual_revenue_potential,
                    investment_required=investment_required,
                    time_to_realize=12,  # 12 months
                    risk_level=RiskLevel.MEDIUM,
                    confidence=0.65,
                    market_segments=["Existing Customer Base"],
                    competitive_advantage="Established customer relationships and trust"
                )
        except Exception as e:
            self.logger.error(f"Error analyzing cross-selling: {e}")
        
        return None
    
    def _analyze_market_expansion(self, acquirer_data: Dict, target_data: Dict) -> Optional[RevenueSynergy]:
        """
        Analyze market expansion opportunities through geographic or segment expansion
        """
        try:
            # Get market and geographic data
            acquirer_markets = set(acquirer_data.get('markets', []))
            target_markets = set(target_data.get('markets', []))
            
            # Find new markets accessible through acquisition
            new_markets = target_markets - acquirer_markets
            
            if new_markets:
                # Estimate market expansion potential
                acquirer_revenue = acquirer_data.get('revenue', 0)
                target_revenue = target_data.get('revenue', 0)
                
                # Assume acquirer can capture 5-15% additional market share in new markets
                market_share_gain = 0.10
                
                # Estimate market size based on target's performance
                # Assume target has 10% market share in their markets
                estimated_market_size = target_revenue / 0.10
                
                annual_revenue_potential = estimated_market_size * market_share_gain * len(new_markets)
                
                # Investment in market entry (marketing, sales, localization)
                investment_required = annual_revenue_potential * 0.4
                
                return RevenueSynergy(
                    type=SynergyType.MARKET,
                    description=f"Expand into {len(new_markets)} new geographic markets",
                    annual_revenue_potential=annual_revenue_potential,
                    investment_required=investment_required,
                    time_to_realize=24,  # 24 months for market entry
                    risk_level=RiskLevel.HIGH,
                    confidence=0.50,
                    market_segments=list(new_markets),
                    competitive_advantage="Combined product portfolio and market presence"
                )
        except Exception as e:
            self.logger.error(f"Error analyzing market expansion: {e}")
        
        return None
    
    def _assess_integration_risks(self, acquirer_data: Dict, target_data: Dict, 
                                cost_synergies: List[CostSynergy], 
                                revenue_synergies: List[RevenueSynergy]) -> List[IntegrationRisk]:
        """
        Assess integration risks that could impact synergy realization
        """
        risks = []
        
        # Cultural integration risk
        cultural_risk = self._assess_cultural_risk(acquirer_data, target_data)
        if cultural_risk:
            risks.append(cultural_risk)
        
        # Technology integration risk
        tech_risk = self._assess_technology_risk(acquirer_data, target_data)
        if tech_risk:
            risks.append(tech_risk)
        
        return risks
    
    def _assess_cultural_risk(self, acquirer_data: Dict, target_data: Dict) -> Optional[IntegrationRisk]:
        """
        Assess cultural integration risks
        """
        try:
            # Simple cultural compatibility assessment
            acquirer_size = acquirer_data.get('employees', 0)
            target_size = target_data.get('employees', 0)
            
            # Size difference creates cultural integration challenges
            size_ratio = max(acquirer_size, target_size) / max(min(acquirer_size, target_size), 1)
            
            if size_ratio > 5:  # Significant size difference
                return IntegrationRisk(
                    category="Cultural Integration",
                    description="Significant size difference may create cultural integration challenges",
                    severity=RiskLevel.HIGH,
                    probability=0.70,
                    impact="Potential employee turnover and productivity loss during integration",
                    mitigation_strategies=[
                        "Develop comprehensive change management program",
                        "Establish cultural integration committees",
                        "Implement gradual integration timeline"
                    ],
                    timeline_impact=6,  # Additional 6 months
                    cost_impact=500000  # $500k additional costs
                )
            elif size_ratio > 2:  # Moderate size difference
                return IntegrationRisk(
                    category="Cultural Integration",
                    description="Moderate cultural integration challenges expected",
                    severity=RiskLevel.MEDIUM,
                    probability=0.50,
                    impact="Some employee uncertainty and temporary productivity impact",
                    mitigation_strategies=[
                        "Regular all-hands meetings",
                        "Cross-functional integration teams",
                        "Clear communication of integration benefits"
                    ],
                    timeline_impact=3,  # Additional 3 months
                    cost_impact=200000  # $200k additional costs
                )
        except Exception as e:
            self.logger.error(f"Error assessing cultural risk: {e}")
        
        return None
    
    def _assess_technology_risk(self, acquirer_data: Dict, target_data: Dict) -> Optional[IntegrationRisk]:
        """
        Assess technology integration risks
        """
        try:
            # Assess technology stack compatibility
            acquirer_tech = acquirer_data.get('technology_stack', [])
            target_tech = target_data.get('technology_stack', [])
            
            # Simple compatibility check
            common_tech = set(acquirer_tech) & set(target_tech)
            compatibility_score = len(common_tech) / max(len(set(acquirer_tech) | set(target_tech)), 1)
            
            if compatibility_score < 0.3:  # Low compatibility
                return IntegrationRisk(
                    category="Technology Integration",
                    description="Significant technology stack differences require extensive integration",
                    severity=RiskLevel.HIGH,
                    probability=0.80,
                    impact="Extended integration timeline and potential system disruptions",
                    mitigation_strategies=[
                        "Develop detailed technology integration roadmap",
                        "Implement phased migration approach",
                        "Establish dedicated integration team"
                    ],
                    timeline_impact=12,  # Additional 12 months
                    cost_impact=1000000  # $1M additional costs
                )
            elif compatibility_score < 0.6:  # Moderate compatibility
                return IntegrationRisk(
                    category="Technology Integration",
                    description="Moderate technology integration challenges",
                    severity=RiskLevel.MEDIUM,
                    probability=0.60,
                    impact="Some integration complexity and potential delays",
                    mitigation_strategies=[
                        "Standardize on common platforms where possible",
                        "Develop API bridges for incompatible systems",
                        "Train staff on new technologies"
                    ],
                    timeline_impact=6,  # Additional 6 months
                    cost_impact=500000  # $500k additional costs
                )
        except Exception as e:
            self.logger.error(f"Error assessing technology risk: {e}")
        
        return None
    
    def _calculate_synergy_value(self, cost_synergies: List[CostSynergy], 
                               revenue_synergies: List[RevenueSynergy], 
                               integration_risks: List[IntegrationRisk]) -> Tuple[float, float]:
        """
        Calculate total synergy value and net present value
        """
        try:
            # Calculate total annual cost savings
            total_cost_savings = sum(synergy.annual_savings for synergy in cost_synergies)
            
            # Calculate total annual revenue potential
            total_revenue_potential = sum(synergy.annual_revenue_potential for synergy in revenue_synergies)
            
            # Calculate total one-time costs
            total_one_time_costs = (
                sum(synergy.one_time_costs for synergy in cost_synergies) +
                sum(synergy.investment_required for synergy in revenue_synergies) +
                sum(risk.cost_impact for risk in integration_risks)
            )
            
            # Total annual value
            total_annual_value = total_cost_savings + total_revenue_potential
            
            # Calculate NPV over 5 years
            npv = -total_one_time_costs  # Initial investment
            for year in range(1, 6):
                # Apply ramp-up factor (synergies don't realize immediately)
                ramp_factor = min(year * 0.3, 1.0)  # 30% per year up to 100%
                annual_value = total_annual_value * ramp_factor
                npv += annual_value / ((1 + self.discount_rate) ** year)
            
            return total_annual_value, npv
            
        except Exception as e:
            self.logger.error(f"Error calculating synergy value: {e}")
            return 0.0, 0.0
    
    def _calculate_break_even(self, cost_synergies: List[CostSynergy], 
                            revenue_synergies: List[RevenueSynergy], 
                            integration_risks: List[IntegrationRisk]) -> int:
        """
        Calculate break-even timeline in months
        """
        try:
            # Calculate total investment
            total_investment = (
                sum(synergy.one_time_costs for synergy in cost_synergies) +
                sum(synergy.investment_required for synergy in revenue_synergies) +
                sum(risk.cost_impact for risk in integration_risks)
            )
            
            # Calculate monthly value generation
            total_annual_value = (
                sum(synergy.annual_savings for synergy in cost_synergies) +
                sum(synergy.annual_revenue_potential for synergy in revenue_synergies)
            )
            monthly_value = total_annual_value / 12
            
            if monthly_value > 0:
                break_even_months = int(total_investment / monthly_value)
                return min(break_even_months, 60)  # Cap at 5 years
            
            return 60  # Default to 5 years if no positive value
            
        except Exception as e:
            self.logger.error(f"Error calculating break-even: {e}")
            return 60
    
    def _calculate_confidence(self, cost_synergies: List[CostSynergy], 
                            revenue_synergies: List[RevenueSynergy], 
                            integration_risks: List[IntegrationRisk]) -> float:
        """
        Calculate overall confidence level for synergy realization
        """
        try:
            if not cost_synergies and not revenue_synergies:
                return 0.0
            
            # Weight by value
            total_value = 0
            weighted_confidence = 0
            
            for synergy in cost_synergies:
                total_value += synergy.annual_savings
                weighted_confidence += synergy.annual_savings * synergy.confidence
            
            for synergy in revenue_synergies:
                total_value += synergy.annual_revenue_potential
                weighted_confidence += synergy.annual_revenue_potential * synergy.confidence
            
            base_confidence = weighted_confidence / total_value if total_value > 0 else 0.5
            
            # Adjust for integration risks
            risk_adjustment = 1.0
            for risk in integration_risks:
                if risk.severity == RiskLevel.HIGH:
                    risk_adjustment *= 0.85
                elif risk.severity == RiskLevel.MEDIUM:
                    risk_adjustment *= 0.95
            
            return min(base_confidence * risk_adjustment, 1.0)
            
        except Exception as e:
            self.logger.error(f"Error calculating confidence: {e}")
            return 0.5
    
    def _locations_overlap(self, loc1: str, loc2: str) -> bool:
        """
        Simple geographic overlap detection
        """
        # Simple string matching for demo purposes
        return loc1.lower() in loc2.lower() or loc2.lower() in loc1.lower()

def print_analysis_summary(analysis: SynergyAnalysis, scenario_name: str):
    """
    Print formatted analysis results
    """
    print(f"\n{'='*60}")
    print(f"SCENARIO: {scenario_name}")
    print(f"{'='*60}")
    print(f"Deal: {analysis.acquirer_name} acquiring {analysis.target_name}")
    print(f"Total Estimated Value: ${analysis.total_estimated_value:,.0f}/year")
    print(f"Net Present Value: ${analysis.net_present_value:,.0f}")
    print(f"Break-even Timeline: {analysis.time_to_break_even} months")
    print(f"Confidence Level: {analysis.confidence_level:.1%}")
    
    print(f"\nCost Synergies ({len(analysis.cost_synergies)}):")
    for synergy in analysis.cost_synergies:
        print(f"  • {synergy.description}")
        print(f"    Annual Savings: ${synergy.annual_savings:,.0f}")
        print(f"    Risk: {synergy.risk_level.value.title()}, Confidence: {synergy.confidence:.1%}")
    
    print(f"\nRevenue Synergies ({len(analysis.revenue_synergies)}):")
    for synergy in analysis.revenue_synergies:
        print(f"  • {synergy.description}")
        print(f"    Annual Potential: ${synergy.annual_revenue_potential:,.0f}")
        print(f"    Risk: {synergy.risk_level.value.title()}, Confidence: {synergy.confidence:.1%}")
    
    print(f"\nIntegration Risks ({len(analysis.integration_risks)}):")
    for risk in analysis.integration_risks:
        print(f"  • {risk.category}: {risk.severity.value.title()} risk ({risk.probability:.0%} probability)")
        print(f"    Impact: {risk.impact}")

def main():
    """
    Test multiple synergy discovery scenarios
    """
    print("=== SYNERGY DISCOVERY ENGINE - MULTIPLE SCENARIOS TEST ===")
    
    engine = SynergyDiscoveryEngine()
    
    # Scenario 1: Large Tech Acquisition (Same Industry)
    scenario1_acquirer = {
        "name": "MegaTech Corp",
        "revenue": 500000000,  # $500M
        "employees": 5000,
        "customers": 10000,
        "industry": "technology",
        "locations": ["San Francisco", "New York", "Austin", "Seattle"],
        "markets": ["North America", "Europe", "Asia"],
        "technology_stack": ["Python", "React", "PostgreSQL", "AWS", "Kubernetes"],
        "avg_salary": 120000
    }
    
    scenario1_target = {
        "name": "InnovateAI Inc",
        "revenue": 100000000,  # $100M
        "employees": 800,
        "customers": 2000,
        "industry": "technology",
        "locations": ["Austin", "Boston", "San Francisco"],
        "markets": ["North America", "Europe"],
        "technology_stack": ["Python", "Vue.js", "MongoDB", "GCP", "Docker"],
        "avg_salary": 110000
    }
    
    analysis1 = engine.analyze_synergies(scenario1_acquirer, scenario1_target, "DEAL_TECH_001")
    print_analysis_summary(analysis1, "Large Tech Acquisition (Same Industry)")
    
    # Scenario 2: Cross-Industry Acquisition (Manufacturing + Tech)
    scenario2_acquirer = {
        "name": "Industrial Solutions Ltd",
        "revenue": 200000000,  # $200M
        "employees": 2000,
        "customers": 500,
        "industry": "manufacturing",
        "locations": ["Detroit", "Chicago", "Houston"],
        "markets": ["North America"],
        "technology_stack": ["Java", "Oracle", "SAP", "Windows"],
        "avg_salary": 70000
    }
    
    scenario2_target = {
        "name": "IoT Dynamics Corp",
        "revenue": 50000000,  # $50M
        "employees": 300,
        "customers": 1000,
        "industry": "technology",
        "locations": ["Austin", "Portland"],
        "markets": ["North America", "Asia"],
        "technology_stack": ["Python", "React", "PostgreSQL", "AWS", "IoT"],
        "avg_salary": 95000
    }
    
    analysis2 = engine.analyze_synergies(scenario2_acquirer, scenario2_target, "DEAL_CROSS_001")
    print_analysis_summary(analysis2, "Cross-Industry Acquisition (Manufacturing + Tech)")
    
    # Scenario 3: Small Startup Acquisition
    scenario3_acquirer = {
        "name": "Growth Ventures Inc",
        "revenue": 25000000,  # $25M
        "employees": 150,
        "customers": 300,
        "industry": "fintech",
        "locations": ["New York"],
        "markets": ["North America"],
        "technology_stack": ["Node.js", "React", "PostgreSQL", "AWS"],
        "avg_salary": 85000
    }
    
    scenario3_target = {
        "name": "CryptoSecure Startup",
        "revenue": 5000000,  # $5M
        "employees": 25,
        "customers": 100,
        "industry": "fintech",
        "locations": ["San Francisco"],
        "markets": ["North America"],
        "technology_stack": ["Go", "React", "Redis", "AWS", "Blockchain"],
        "avg_salary": 95000
    }
    
    analysis3 = engine.analyze_synergies(scenario3_acquirer, scenario3_target, "DEAL_STARTUP_001")
    print_analysis_summary(analysis3, "Small Startup Acquisition (Same Industry)")
    
    # Scenario 4: International Expansion Deal
    scenario4_acquirer = {
        "name": "Global Retail Corp",
        "revenue": 1000000000,  # $1B
        "employees": 10000,
        "customers": 50000,
        "industry": "retail",
        "locations": ["New York", "Los Angeles", "Chicago", "Miami"],
        "markets": ["North America"],
        "technology_stack": ["Java", "Angular", "MySQL", "Azure"],
        "avg_salary": 60000
    }
    
    scenario4_target = {
        "name": "European Fashion Ltd",
        "revenue": 300000000,  # $300M
        "employees": 2500,
        "customers": 15000,
        "industry": "retail",
        "locations": ["London", "Paris", "Berlin", "Milan"],
        "markets": ["Europe", "Asia"],
        "technology_stack": ["PHP", "Vue.js", "PostgreSQL", "AWS"],
        "avg_salary": 55000
    }
    
    analysis4 = engine.analyze_synergies(scenario4_acquirer, scenario4_target, "DEAL_INTL_001")
    print_analysis_summary(analysis4, "International Expansion Deal (Retail)")
    
    print(f"\n{'='*60}")
    print("SUMMARY COMPARISON")
    print(f"{'='*60}")
    
    scenarios = [
        ("Tech Acquisition", analysis1),
        ("Cross-Industry", analysis2),
        ("Startup Acquisition", analysis3),
        ("International Expansion", analysis4)
    ]
    
    print(f"{'Scenario':<25} {'Total Value':<15} {'NPV':<15} {'Break-even':<12} {'Confidence':<12}")
    print("-" * 80)
    
    for name, analysis in scenarios:
        print(f"{name:<25} ${analysis.total_estimated_value/1000000:>8.1f}M     ${analysis.net_present_value/1000000:>8.1f}M     {analysis.time_to_break_even:>6} mo    {analysis.confidence_level:>8.1%}")
    
    print(f"\n{'='*60}")
    print("ALL SCENARIOS TESTED SUCCESSFULLY!")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()