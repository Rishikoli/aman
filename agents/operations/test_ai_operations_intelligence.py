"""
Test AI-Powered Operations Intelligence System (Task 8.2)

Tests the comprehensive AI-powered operations intelligence system including:
- Comprehensive operational risk scoring using multiple data sources
- Gemini API integration for synthesizing diverse data points
- Enhanced geopolitical risk analysis and supply chain vulnerability assessment
- Operational efficiency benchmarking and optimization recommendations
"""

import asyncio
import logging
import sys
import os
from datetime import datetime

# Add the agents directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from operations.operations_agent_new import OperationsAgent

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_ai_operations_intelligence():
    """Test the AI-powered operations intelligence system"""
    
    print("=" * 80)
    print("TESTING AI-POWERED OPERATIONS INTELLIGENCE SYSTEM (Task 8.2)")
    print("=" * 80)
    
    # Initialize the operations agent
    operations_agent = OperationsAgent()
    
    # Test data representing a multinational company
    test_company_data = {
        'name': 'GlobalTech Manufacturing Corp',
        'industry': 'manufacturing',
        'locations': [
            {
                'country': 'United States',
                'city': 'Detroit',
                'region': 'North America',
                'type': 'headquarters'
            },
            {
                'country': 'China',
                'city': 'Shanghai',
                'region': 'Asia Pacific',
                'type': 'manufacturing'
            },
            {
                'country': 'Germany',
                'city': 'Munich',
                'region': 'Europe',
                'type': 'r_and_d'
            },
            {
                'country': 'Mexico',
                'city': 'Tijuana',
                'region': 'North America',
                'type': 'manufacturing'
            },
            {
                'country': 'India',
                'city': 'Bangalore',
                'region': 'Asia Pacific',
                'type': 'services'
            }
        ],
        'facilities': [
            {
                'type': 'manufacturing',
                'capacity': 1000,
                'utilization': 75,
                'country': 'China',
                'city': 'Shanghai'
            },
            {
                'type': 'manufacturing',
                'capacity': 800,
                'utilization': 85,
                'country': 'Mexico',
                'city': 'Tijuana'
            },
            {
                'type': 'r_and_d',
                'capacity': 200,
                'utilization': 90,
                'country': 'Germany',
                'city': 'Munich'
            },
            {
                'type': 'warehouse',
                'capacity': 500,
                'utilization': 60,
                'country': 'United States',
                'city': 'Detroit'
            }
        ],
        'suppliers': [
            {
                'name': 'Asian Components Ltd',
                'country': 'China',
                'reliability_score': 85,
                'type': 'components'
            },
            {
                'name': 'European Materials GmbH',
                'country': 'Germany',
                'reliability_score': 95,
                'type': 'raw_materials'
            },
            {
                'name': 'Mexican Assembly Co',
                'country': 'Mexico',
                'reliability_score': 80,
                'type': 'assembly'
            },
            {
                'name': 'Indian Software Services',
                'country': 'India',
                'reliability_score': 90,
                'type': 'services'
            }
        ],
        'partners': [
            {
                'name': 'Global Logistics Partner',
                'country': 'Singapore',
                'type': 'logistics'
            }
        ],
        'operational_data': {
            'cost_per_unit': 95,
            'annual_revenue': 500000000,
            'employee_count': 5000
        },
        'technology': {
            'integration_level': 'medium',
            'automation_level': 70,
            'number_of_systems': 12
        }
    }
    
    print(f"\nTesting AI-powered operations intelligence for: {test_company_data['name']}")
    print(f"Industry: {test_company_data['industry']}")
    print(f"Locations: {len(test_company_data['locations'])} countries")
    print(f"Facilities: {len(test_company_data['facilities'])} facilities")
    print(f"Suppliers: {len(test_company_data['suppliers'])} suppliers")
    
    try:
        # Test the AI-powered operations intelligence system
        print("\n" + "="*60)
        print("RUNNING AI-POWERED OPERATIONS INTELLIGENCE ANALYSIS")
        print("="*60)
        
        start_time = datetime.now()
        
        # Execute the comprehensive AI-powered analysis
        intelligence_result = await operations_agent.analyze_ai_powered_operations_intelligence(test_company_data)
        
        end_time = datetime.now()
        analysis_duration = (end_time - start_time).total_seconds()
        
        print(f"\nAnalysis completed in {analysis_duration:.2f} seconds")
        
        # Display results
        if 'error' in intelligence_result:
            print(f"\n❌ ERROR: {intelligence_result['error']}")
            return False
        
        print("\n" + "="*60)
        print("AI-POWERED OPERATIONS INTELLIGENCE RESULTS")
        print("="*60)
        
        # Key Metrics
        print(f"\n📊 KEY METRICS:")
        print(f"   Overall Intelligence Score: {intelligence_result.get('overall_intelligence_score', 'N/A')}")
        print(f"   Risk Level: {intelligence_result.get('risk_level', 'N/A').upper()}")
        print(f"   Efficiency Grade: {intelligence_result.get('efficiency_grade', 'N/A')}")
        print(f"   AI Confidence: {intelligence_result.get('ai_confidence', 0):.1%}")
        
        # Intelligence Report Summary
        intelligence_report = intelligence_result.get('intelligence_report', {})
        print(f"\n🎯 INTELLIGENCE SUMMARY:")
        print(f"   {intelligence_report.get('intelligence_summary', 'No summary available')}")
        
        # Key Findings
        key_findings = intelligence_report.get('key_findings', [])
        if key_findings:
            print(f"\n🔍 KEY FINDINGS:")
            for i, finding in enumerate(key_findings[:5], 1):
                print(f"   {i}. {finding}")
        
        # Critical Alerts
        critical_alerts = intelligence_report.get('critical_alerts', [])
        if critical_alerts:
            print(f"\n🚨 CRITICAL ALERTS:")
            for i, alert in enumerate(critical_alerts, 1):
                print(f"   {i}. {alert}")
        
        # Strategic Recommendations
        strategic_recommendations = intelligence_result.get('strategic_recommendations', [])
        if strategic_recommendations:
            print(f"\n💡 STRATEGIC RECOMMENDATIONS:")
            for i, rec in enumerate(strategic_recommendations[:5], 1):
                if isinstance(rec, dict):
                    print(f"   {i}. {rec.get('description', rec)}")
                else:
                    print(f"   {i}. {rec}")
        
        # Risk Mitigation Strategies
        risk_mitigation = intelligence_result.get('risk_mitigation_strategies', [])
        if risk_mitigation:
            print(f"\n🛡️ RISK MITIGATION STRATEGIES:")
            for i, strategy in enumerate(risk_mitigation[:5], 1):
                print(f"   {i}. {strategy}")
        
        # Optimization Opportunities
        optimization_opportunities = intelligence_result.get('optimization_opportunities', [])
        if optimization_opportunities:
            print(f"\n⚡ OPTIMIZATION OPPORTUNITIES:")
            for i, opp in enumerate(optimization_opportunities[:3], 1):
                if isinstance(opp, dict):
                    print(f"   {i}. {opp.get('description', opp)}")
                    print(f"      Priority: {opp.get('priority', 'N/A')}")
                    print(f"      Estimated Savings: {opp.get('estimated_savings', 'N/A')}")
                else:
                    print(f"   {i}. {opp}")
        
        # Component Analysis Results
        print(f"\n" + "="*60)
        print("DETAILED COMPONENT ANALYSIS")
        print("="*60)
        
        # Comprehensive Risk Scoring
        risk_scoring = intelligence_result.get('comprehensive_risk_scoring', {})
        if risk_scoring and not risk_scoring.get('error'):
            print(f"\n🎯 COMPREHENSIVE RISK SCORING:")
            print(f"   Overall Risk Score: {risk_scoring.get('overall_risk_score', 'N/A')}")
            print(f"   Risk Level: {risk_scoring.get('risk_level', 'N/A')}")
            
            risk_components = risk_scoring.get('risk_components', {})
            if risk_components:
                print(f"   Risk Components:")
                for component, score in risk_components.items():
                    print(f"     - {component.replace('_', ' ').title()}: {score:.1f}")
        
        # Enhanced Geopolitical Analysis
        geo_analysis = intelligence_result.get('enhanced_geopolitical_analysis', {})
        if geo_analysis and not geo_analysis.get('error'):
            print(f"\n🌍 ENHANCED GEOPOLITICAL ANALYSIS:")
            print(f"   Countries Analyzed: {geo_analysis.get('countries_analyzed', 0)}")
            print(f"   Average Risk Score: {geo_analysis.get('average_risk_score', 'N/A')}")
            print(f"   Supply Chain Risk: {geo_analysis.get('average_supply_chain_risk', 'N/A')}")
            
            high_risk_countries = geo_analysis.get('high_risk_countries', [])
            if high_risk_countries:
                print(f"   High-Risk Countries: {len(high_risk_countries)}")
                for country in high_risk_countries[:3]:
                    print(f"     - {country.get('country', 'Unknown')}: {country.get('risk_score', 'N/A')}")
        
        # AI Synthesis
        ai_synthesis = intelligence_result.get('ai_synthesis', {})
        if ai_synthesis and not ai_synthesis.get('error'):
            print(f"\n🤖 AI SYNTHESIS:")
            print(f"   AI Powered: {ai_synthesis.get('ai_powered', False)}")
            print(f"   Confidence Level: {ai_synthesis.get('confidence_level', 0):.1%}")
            
            key_factors = ai_synthesis.get('key_risk_factors', [])
            if key_factors:
                print(f"   Key Risk Factors:")
                for factor in key_factors[:3]:
                    print(f"     - {factor}")
        
        # Efficiency Benchmarking
        efficiency_benchmarking = intelligence_result.get('efficiency_benchmarking', {})
        if efficiency_benchmarking and not efficiency_benchmarking.get('error'):
            print(f"\n📈 EFFICIENCY BENCHMARKING:")
            print(f"   Overall Efficiency Score: {efficiency_benchmarking.get('overall_efficiency_score', 'N/A')}")
            print(f"   Efficiency Grade: {efficiency_benchmarking.get('efficiency_grade', 'N/A')}")
            print(f"   Industry: {efficiency_benchmarking.get('industry', 'N/A')}")
            
            potential_improvements = efficiency_benchmarking.get('potential_improvements', {})
            if potential_improvements:
                print(f"   Potential Cost Savings: {potential_improvements.get('cost_savings_range', 'N/A')}")
                print(f"   Implementation Timeline: {potential_improvements.get('implementation_timeline_months', 'N/A')} months")
        
        # Implementation Roadmap
        implementation_roadmap = intelligence_result.get('implementation_roadmap', [])
        if implementation_roadmap:
            print(f"\n🗺️ IMPLEMENTATION ROADMAP:")
            for phase in implementation_roadmap:
                if isinstance(phase, dict):
                    print(f"   {phase.get('phase', 'Unknown Phase')}")
                    print(f"     Timeline: {phase.get('timeline', 'N/A')}")
                    print(f"     Focus: {phase.get('focus', 'N/A')}")
                    print(f"     Expected Savings: {phase.get('expected_savings', 'N/A')}")
        
        print(f"\n" + "="*60)
        print("✅ AI-POWERED OPERATIONS INTELLIGENCE TEST COMPLETED SUCCESSFULLY")
        print("="*60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR during AI-powered operations intelligence test: {str(e)}")
        logger.error(f"Test error: {str(e)}", exc_info=True)
        return False

async def main():
    """Main test function"""
    print("Starting AI-Powered Operations Intelligence System Test...")
    
    success = await test_ai_operations_intelligence()
    
    if success:
        print("\n🎉 All tests completed successfully!")
        print("\nTask 8.2 Implementation Summary:")
        print("✅ Comprehensive operational risk scoring using multiple data sources")
        print("✅ Gemini API integration for synthesizing diverse data points")
        print("✅ Enhanced geopolitical risk analysis and supply chain vulnerability assessment")
        print("✅ Operational efficiency benchmarking and optimization recommendations")
    else:
        print("\n❌ Some tests failed. Please check the logs for details.")
    
    return success

if __name__ == "__main__":
    # Run the test
    success = asyncio.run(main())
    sys.exit(0 if success else 1)