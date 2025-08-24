"""
Intelligent Synergy Discovery System

This module implements comprehensive synergy identification and valuation capabilities
using pandas/NumPy-based financial modeling and AI-powered strategic analysis.

Requirements satisfied:
- 6.4: Single-variable cost savings estimates (eliminated positions, etc.)
- 6.5: Integration risk identification and dependency highlighting
"""

import pandas as pd
import numpy as np
import requests
import json
import logging
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import CONFIG

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
    Intelligent synergy discovery system that identifies cost savings, revenue opportunities,
    and integration risks using financial modeling and AI-powered analysis.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.gemini_api_key = CONFIG['api_keys']['gemini']
        self.discount_rate = 0.10  # 10% discount rate for NPV calculations
        
    def analyze_synergies(self, acquirer_data: Dict, target_data: Dict, deal_id: str) -> SynergyAnalysis:
        """
        Comprehensive synergy analysis combining cost and revenue opportunities
        
        Args:
            acquirer_data: Financial and operational data for acquiring company
            target_data: Financial and operational data for target company
            deal_id: Unique identifier for the M&A deal
            
        Returns:
            SynergyAnalysis: Complete synergy assessment with valuations
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
        
        # Operations synergies - streamline processes and eliminate redundancies
        operations_synergy = self._analyze_operations_overlap(acquirer_data, target_data)
        if operations_synergy:
            synergies.append(operations_synergy)
        
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
            acquirer_revenue = acquirer_data.get('revenue', 0)
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
    
    def _analyze_operations_overlap(self, acquirer_data: Dict, target_data: Dict) -> Optional[CostSynergy]:
        """
        Analyze operational process consolidation opportunities
        """
        try:
            # Estimate operational efficiency gains
            target_revenue = target_data.get('revenue', 0)
            
            # Operational costs typically 60-70% of revenue
            operational_cost_rate = 0.65
            target_operational_costs = target_revenue * operational_cost_rate
            
            # Efficiency gains from process standardization (2-5%)
            efficiency_gain_rate = 0.03
            annual_savings = target_operational_costs * efficiency_gain_rate
            
            if annual_savings > 50000:  # Only if meaningful savings
                # Implementation costs for process reengineering
                one_time_costs = annual_savings * 0.4
                
                return CostSynergy(
                    type=SynergyType.OPERATIONS,
                    description="Streamline operations and eliminate process redundancies",
                    annual_savings=annual_savings,
                    one_time_costs=one_time_costs,
                    time_to_realize=18,  # 18 months for full process integration
                    risk_level=RiskLevel.HIGH,
                    confidence=0.60,
                    affected_departments=["Operations", "Supply Chain", "Customer Service"],
                    implementation_complexity="High - requires extensive process reengineering"
                )
        except Exception as e:
            self.logger.error(f"Error analyzing operations overlap: {e}")
        
        return None
    
    def _identify_revenue_synergies(self, acquirer_data: Dict, target_data: Dict) -> List[RevenueSynergy]:
        """
        Identify revenue enhancement opportunities through market expansion and cross-selling
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
            # Assume 10-20% of customers could purchase additional products
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
        
        # Regulatory risk
        regulatory_risk = self._assess_regulatory_risk(acquirer_data, target_data)
        if regulatory_risk:
            risks.append(regulatory_risk)
        
        # Customer retention risk
        customer_risk = self._assess_customer_retention_risk(acquirer_data, target_data)
        if customer_risk:
            risks.append(customer_risk)
        
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
                        "Implement gradual integration timeline",
                        "Provide extensive communication and training"
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
                        "Establish dedicated integration team",
                        "Plan for temporary parallel systems"
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
    
    def _assess_regulatory_risk(self, acquirer_data: Dict, target_data: Dict) -> Optional[IntegrationRisk]:
        """
        Assess regulatory approval and compliance risks
        """
        try:
            # Check for regulated industries
            regulated_industries = ['banking', 'healthcare', 'telecommunications', 'utilities', 'insurance']
            
            acquirer_industry = acquirer_data.get('industry', '').lower()
            target_industry = target_data.get('industry', '').lower()
            
            if acquirer_industry in regulated_industries or target_industry in regulated_industries:
                return IntegrationRisk(
                    category="Regulatory Compliance",
                    description="Regulated industry requires extensive regulatory approval process",
                    severity=RiskLevel.HIGH,
                    probability=0.90,
                    impact="Potential delays in deal closure and integration activities",
                    mitigation_strategies=[
                        "Engage regulatory experts early in process",
                        "Prepare comprehensive regulatory filing",
                        "Develop contingency plans for regulatory conditions",
                        "Maintain separate operations until approval"
                    ],
                    timeline_impact=9,  # Additional 9 months
                    cost_impact=750000  # $750k additional costs
                )
        except Exception as e:
            self.logger.error(f"Error assessing regulatory risk: {e}")
        
        return None
    
    def _assess_customer_retention_risk(self, acquirer_data: Dict, target_data: Dict) -> Optional[IntegrationRisk]:
        """
        Assess customer retention risks during integration
        """
        try:
            # Assess customer concentration risk
            target_customers = target_data.get('customers', 0)
            target_revenue = target_data.get('revenue', 0)
            
            if target_customers > 0:
                revenue_per_customer = target_revenue / target_customers
                
                # High revenue per customer indicates concentration risk
                if revenue_per_customer > 100000:  # $100k+ per customer
                    return IntegrationRisk(
                        category="Customer Retention",
                        description="High customer concentration creates retention risk during integration",
                        severity=RiskLevel.HIGH,
                        probability=0.40,
                        impact="Loss of key customers could significantly impact revenue synergies",
                        mitigation_strategies=[
                            "Develop customer retention program",
                            "Assign dedicated account managers during transition",
                            "Communicate integration benefits to key customers",
                            "Offer service level guarantees during integration"
                        ],
                        timeline_impact=0,  # No timeline impact
                        cost_impact=300000  # $300k retention program costs
                    )
        except Exception as e:
            self.logger.error(f"Error assessing customer retention risk: {e}")
        
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
        # In production, would use proper geocoding and distance calculation
        return loc1.lower() in loc2.lower() or loc2.lower() in loc1.lower()
    
    def generate_ai_insights(self, synergy_analysis: SynergyAnalysis) -> Dict[str, Any]:
        """
        Generate AI-powered strategic insights using Gemini API
        """
        if not self.gemini_api_key:
            self.logger.warning("Gemini API key not configured, skipping AI insights")
            return {"error": "AI insights not available - API key not configured"}
        
        try:
            # Prepare context for AI analysis
            context = {
                "deal": {
                    "acquirer": synergy_analysis.acquirer_name,
                    "target": synergy_analysis.target_name,
                    "total_value": synergy_analysis.total_estimated_value,
                    "npv": synergy_analysis.net_present_value,
                    "break_even": synergy_analysis.time_to_break_even,
                    "confidence": synergy_analysis.confidence_level
                },
                "cost_synergies": [asdict(synergy) for synergy in synergy_analysis.cost_synergies],
                "revenue_synergies": [asdict(synergy) for synergy in synergy_analysis.revenue_synergies],
                "risks": [asdict(risk) for risk in synergy_analysis.integration_risks]
            }
            
            prompt = f"""
            Analyze this M&A synergy assessment and provide strategic insights:
            
            Deal: {synergy_analysis.acquirer_name} acquiring {synergy_analysis.target_name}
            Total Estimated Value: ${synergy_analysis.total_estimated_value:,.0f}
            Net Present Value: ${synergy_analysis.net_present_value:,.0f}
            Break-even Timeline: {synergy_analysis.time_to_break_even} months
            Confidence Level: {synergy_analysis.confidence_level:.1%}
            
            Cost Synergies: {len(synergy_analysis.cost_synergies)} identified
            Revenue Synergies: {len(synergy_analysis.revenue_synergies)} identified
            Integration Risks: {len(synergy_analysis.integration_risks)} identified
            
            Please provide:
            1. Strategic assessment of the synergy potential
            2. Key success factors for realization
            3. Additional creative synergy opportunities to explore
            4. Risk mitigation priorities
            5. Integration timeline recommendations
            
            Keep response concise and actionable.
            """
            
            # Make API call to Gemini (placeholder - would need actual API implementation)
            insights = self._call_gemini_api(prompt)
            
            return {
                "ai_insights": insights,
                "generated_at": datetime.now().isoformat(),
                "confidence_score": synergy_analysis.confidence_level
            }
            
        except Exception as e:
            self.logger.error(f"Error generating AI insights: {e}")
            return {"error": f"Failed to generate AI insights: {str(e)}"}
    
    def _call_gemini_api(self, prompt: str) -> str:
        """
        Call Gemini API for AI-powered insights (placeholder implementation)
        """
        # This is a placeholder - actual implementation would call Gemini API
        return """
        Strategic Assessment: This acquisition shows strong synergy potential with balanced cost and revenue opportunities.
        
        Key Success Factors:
        - Careful change management for personnel consolidation
        - Phased technology integration approach
        - Strong customer retention program during transition
        
        Additional Opportunities:
        - Explore supply chain consolidation synergies
        - Consider joint product development initiatives
        - Evaluate shared services center opportunities
        
        Risk Mitigation Priorities:
        1. Cultural integration planning
        2. Technology compatibility assessment
        3. Regulatory approval timeline management
        
        Integration Timeline: Recommend 18-24 month integration timeline with quarterly milestone reviews.
        """

# Example usage and testing
if __name__ == "__main__":
    # Sample data for testing
    acquirer_data = {
        "name": "TechCorp Inc",
        "revenue": 50000000,
        "employees": 500,
        "customers": 1000,
        "industry": "technology",
        "locations": ["New York", "San Francisco"],
        "markets": ["North America", "Europe"],
        "technology_stack": ["Python", "React", "PostgreSQL", "AWS"],
        "avg_salary": 85000
    }
    
    target_data = {
        "name": "InnovateSoft LLC",
        "revenue": 20000000,
        "employees": 200,
        "customers": 500,
        "industry": "technology",
        "locations": ["Austin", "New York"],
        "markets": ["North America"],
        "technology_stack": ["Java", "Angular", "MySQL", "Azure"],
        "avg_salary": 80000
    }
    
    # Initialize engine and run analysis
    engine = SynergyDiscoveryEngine()
    analysis = engine.analyze_synergies(acquirer_data, target_data, "DEAL_001")
    
    # Generate AI insights
    insights = engine.generate_ai_insights(analysis)
    
    # Print results
    print(f"\n=== SYNERGY ANALYSIS RESULTS ===")
    print(f"Deal: {analysis.acquirer_name} acquiring {analysis.target_name}")
    print(f"Total Estimated Value: ${analysis.total_estimated_value:,.0f}")
    print(f"Net Present Value: ${analysis.net_present_value:,.0f}")
    print(f"Break-even Timeline: {analysis.time_to_break_even} months")
    print(f"Confidence Level: {analysis.confidence_level:.1%}")
    
    print(f"\nCost Synergies ({len(analysis.cost_synergies)}):")
    for synergy in analysis.cost_synergies:
        print(f"  - {synergy.description}: ${synergy.annual_savings:,.0f}/year")
    
    print(f"\nRevenue Synergies ({len(analysis.revenue_synergies)}):")
    for synergy in analysis.revenue_synergies:
        print(f"  - {synergy.description}: ${synergy.annual_revenue_potential:,.0f}/year")
    
    print(f"\nIntegration Risks ({len(analysis.integration_risks)}):")
    for risk in analysis.integration_risks:
        print(f"  - {risk.category}: {risk.severity.value} risk")
    
    print(f"\nAI Insights:")
    print(insights.get("ai_insights", "Not available"))