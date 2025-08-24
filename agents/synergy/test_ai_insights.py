#!/usr/bin/env python3
"""
Test AI insights generation for synergy analysis
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
        'gemini': 'mock_api_key'  # Mock API key for testing
    }
}

# Import the synergy engine classes
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
    time_to_realize: int
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
    time_to_realize: int
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
    timeline_impact: int
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
    Simplified version with AI insights for testing
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.gemini_api_key = CONFIG['api_keys']['gemini']
        self.discount_rate = 0.10
        
    def generate_ai_insights(self, synergy_analysis: SynergyAnalysis) -> Dict[str, Any]:
        """
        Generate AI-powered strategic insights using mock Gemini API
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
            
            # Generate insights based on the analysis
            insights = self._generate_strategic_insights(synergy_analysis)
            
            return {
                "ai_insights": insights,
                "generated_at": datetime.now().isoformat(),
                "confidence_score": synergy_analysis.confidence_level,
                "context_summary": self._generate_context_summary(synergy_analysis)
            }
            
        except Exception as e:
            self.logger.error(f"Error generating AI insights: {e}")
            return {"error": f"Failed to generate AI insights: {str(e)}"}
    
    def _generate_strategic_insights(self, analysis: SynergyAnalysis) -> str:
        """
        Generate strategic insights based on synergy analysis
        """
        insights = []
        
        # Strategic Assessment
        if analysis.net_present_value > 0:
            insights.append("✅ STRATEGIC ASSESSMENT: This acquisition shows strong synergy potential with positive NPV.")
        else:
            insights.append("⚠️ STRATEGIC ASSESSMENT: This acquisition shows negative NPV - consider restructuring deal terms.")
        
        # Value Driver Analysis
        cost_value = sum(s.annual_savings for s in analysis.cost_synergies)
        revenue_value = sum(s.annual_revenue_potential for s in analysis.revenue_synergies)
        
        if cost_value > revenue_value:
            insights.append(f"💰 VALUE DRIVERS: Cost synergies (${cost_value/1000000:.1f}M) are the primary value driver.")
        else:
            insights.append(f"📈 VALUE DRIVERS: Revenue synergies (${revenue_value/1000000:.1f}M) are the primary value driver.")
        
        # Risk Assessment
        high_risks = [r for r in analysis.integration_risks if r.severity == RiskLevel.HIGH]
        if high_risks:
            insights.append(f"🚨 RISK ALERT: {len(high_risks)} high-severity integration risks identified requiring immediate attention.")
        
        # Timeline Assessment
        if analysis.time_to_break_even <= 12:
            insights.append(f"⚡ TIMELINE: Fast break-even ({analysis.time_to_break_even} months) indicates strong synergy execution potential.")
        elif analysis.time_to_break_even <= 24:
            insights.append(f"⏰ TIMELINE: Moderate break-even timeline ({analysis.time_to_break_even} months) requires careful execution planning.")
        else:
            insights.append(f"🐌 TIMELINE: Extended break-even ({analysis.time_to_break_even} months) suggests challenging synergy realization.")
        
        # Key Success Factors
        insights.append("\n🎯 KEY SUCCESS FACTORS:")
        if any(s.type == SynergyType.PERSONNEL for s in analysis.cost_synergies):
            insights.append("  • Implement comprehensive change management for personnel consolidation")
        if any(s.type == SynergyType.TECHNOLOGY for s in analysis.cost_synergies):
            insights.append("  • Execute phased technology integration with minimal business disruption")
        if any(s.type == SynergyType.REVENUE for s in analysis.revenue_synergies):
            insights.append("  • Develop integrated sales strategy to maximize cross-selling opportunities")
        
        # Additional Opportunities
        insights.append("\n💡 ADDITIONAL OPPORTUNITIES TO EXPLORE:")
        insights.append("  • Supply chain consolidation and vendor renegotiation")
        insights.append("  • Joint product development leveraging combined R&D capabilities")
        insights.append("  • Shared services center for back-office functions")
        insights.append("  • Combined procurement power for better vendor terms")
        
        # Risk Mitigation Priorities
        if analysis.integration_risks:
            insights.append("\n🛡️ RISK MITIGATION PRIORITIES:")
            for i, risk in enumerate(analysis.integration_risks[:3], 1):  # Top 3 risks
                insights.append(f"  {i}. {risk.category}: {risk.description}")
        
        # Integration Timeline Recommendations
        insights.append(f"\n📅 INTEGRATION TIMELINE RECOMMENDATIONS:")
        if analysis.confidence_level > 0.7:
            insights.append("  • Aggressive 12-18 month integration timeline with quarterly milestone reviews")
        elif analysis.confidence_level > 0.5:
            insights.append("  • Moderate 18-24 month integration timeline with bi-annual milestone reviews")
        else:
            insights.append("  • Conservative 24-36 month integration timeline with extensive risk monitoring")
        
        return "\n".join(insights)
    
    def _generate_context_summary(self, analysis: SynergyAnalysis) -> Dict[str, Any]:
        """
        Generate context summary for the analysis
        """
        return {
            "deal_overview": f"{analysis.acquirer_name} acquiring {analysis.target_name}",
            "financial_metrics": {
                "total_annual_value": analysis.total_estimated_value,
                "net_present_value": analysis.net_present_value,
                "break_even_months": analysis.time_to_break_even,
                "confidence_percentage": round(analysis.confidence_level * 100, 1)
            },
            "synergy_breakdown": {
                "cost_synergies_count": len(analysis.cost_synergies),
                "revenue_synergies_count": len(analysis.revenue_synergies),
                "integration_risks_count": len(analysis.integration_risks)
            },
            "risk_profile": {
                "high_risks": len([r for r in analysis.integration_risks if r.severity == RiskLevel.HIGH]),
                "medium_risks": len([r for r in analysis.integration_risks if r.severity == RiskLevel.MEDIUM]),
                "low_risks": len([r for r in analysis.integration_risks if r.severity == RiskLevel.LOW])
            }
        }

def create_sample_analysis() -> SynergyAnalysis:
    """
    Create a sample synergy analysis for testing AI insights
    """
    cost_synergies = [
        CostSynergy(
            type=SynergyType.PERSONNEL,
            description="Eliminate 50 duplicate positions across departments",
            annual_savings=4000000,
            one_time_costs=1200000,
            time_to_realize=6,
            risk_level=RiskLevel.MEDIUM,
            confidence=0.75,
            affected_departments=["HR", "Finance", "Operations", "IT"],
            implementation_complexity="Medium - requires careful change management"
        ),
        CostSynergy(
            type=SynergyType.TECHNOLOGY,
            description="Consolidate software licenses and eliminate duplicate systems",
            annual_savings=800000,
            one_time_costs=400000,
            time_to_realize=12,
            risk_level=RiskLevel.MEDIUM,
            confidence=0.70,
            affected_departments=["IT", "Operations", "Finance"],
            implementation_complexity="High - requires system integration"
        )
    ]
    
    revenue_synergies = [
        RevenueSynergy(
            type=SynergyType.REVENUE,
            description="Cross-sell products to 200 existing customers",
            annual_revenue_potential=2500000,
            investment_required=750000,
            time_to_realize=12,
            risk_level=RiskLevel.MEDIUM,
            confidence=0.65,
            market_segments=["Existing Customer Base"],
            competitive_advantage="Established customer relationships"
        ),
        RevenueSynergy(
            type=SynergyType.MARKET,
            description="Expand into 2 new geographic markets",
            annual_revenue_potential=5000000,
            investment_required=2000000,
            time_to_realize=24,
            risk_level=RiskLevel.HIGH,
            confidence=0.50,
            market_segments=["Europe", "Asia"],
            competitive_advantage="Combined product portfolio"
        )
    ]
    
    integration_risks = [
        IntegrationRisk(
            category="Cultural Integration",
            description="Significant cultural differences between organizations",
            severity=RiskLevel.HIGH,
            probability=0.70,
            impact="Potential employee turnover and productivity loss",
            mitigation_strategies=[
                "Comprehensive change management program",
                "Cultural integration committees",
                "Gradual integration timeline"
            ],
            timeline_impact=6,
            cost_impact=500000
        ),
        IntegrationRisk(
            category="Technology Integration",
            description="Complex system integration requirements",
            severity=RiskLevel.MEDIUM,
            probability=0.60,
            impact="Potential system disruptions and delays",
            mitigation_strategies=[
                "Phased migration approach",
                "Dedicated integration team",
                "Parallel system operation"
            ],
            timeline_impact=3,
            cost_impact=300000
        )
    ]
    
    return SynergyAnalysis(
        deal_id="DEAL_AI_TEST_001",
        acquirer_name="GlobalTech Solutions",
        target_name="InnovateNow Corp",
        cost_synergies=cost_synergies,
        revenue_synergies=revenue_synergies,
        integration_risks=integration_risks,
        total_estimated_value=12300000,  # Total annual value
        net_present_value=28500000,     # 5-year NPV
        time_to_break_even=8,           # 8 months
        confidence_level=0.68,          # 68% confidence
        analysis_timestamp=datetime.now()
    )

def main():
    """
    Test AI insights generation
    """
    print("=== SYNERGY DISCOVERY ENGINE - AI INSIGHTS TEST ===\n")
    
    # Create sample analysis
    analysis = create_sample_analysis()
    
    # Initialize engine
    engine = SynergyDiscoveryEngine()
    
    # Generate AI insights
    insights = engine.generate_ai_insights(analysis)
    
    # Display results
    print("📊 SYNERGY ANALYSIS SUMMARY")
    print("=" * 60)
    print(f"Deal: {analysis.acquirer_name} acquiring {analysis.target_name}")
    print(f"Total Annual Value: ${analysis.total_estimated_value:,.0f}")
    print(f"Net Present Value: ${analysis.net_present_value:,.0f}")
    print(f"Break-even Timeline: {analysis.time_to_break_even} months")
    print(f"Confidence Level: {analysis.confidence_level:.1%}")
    
    print(f"\n🤖 AI-POWERED STRATEGIC INSIGHTS")
    print("=" * 60)
    if "error" in insights:
        print(f"Error: {insights['error']}")
    else:
        print(insights["ai_insights"])
        
        print(f"\n📋 CONTEXT SUMMARY")
        print("=" * 60)
        context = insights["context_summary"]
        print(f"Financial Metrics:")
        for key, value in context["financial_metrics"].items():
            if isinstance(value, (int, float)) and value > 1000:
                print(f"  • {key.replace('_', ' ').title()}: ${value:,.0f}")
            else:
                print(f"  • {key.replace('_', ' ').title()}: {value}")
        
        print(f"\nSynergy Breakdown:")
        for key, value in context["synergy_breakdown"].items():
            print(f"  • {key.replace('_', ' ').title()}: {value}")
        
        print(f"\nRisk Profile:")
        for key, value in context["risk_profile"].items():
            print(f"  • {key.replace('_', ' ').title()}: {value}")
    
    print(f"\n✅ AI INSIGHTS TEST COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    main()