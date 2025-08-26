"""
Test script for Legal Data Integration
Tests SEC EDGAR and OpenCorporates integration
"""

import sys
import logging
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from legal.legal_data_integration import LegalDataIntegration

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def test_sec_edgar_integration():
    """Test SEC EDGAR API integration"""
    print("\n" + "="*60)
    print("TESTING SEC EDGAR INTEGRATION")
    print("="*60)
    
    integration = LegalDataIntegration()
    
    # Test with Apple Inc. (well-known public company)
    test_ticker = "AAPL"
    
    try:
        print(f"\nTesting SEC EDGAR data retrieval for {test_ticker}...")
        
        sec_data = integration.sec_client.get_company_legal_intelligence(test_ticker)
        
        if sec_data and not sec_data.get('error'):
            print("✅ SEC EDGAR integration successful!")
            print(f"Company: {sec_data.get('company_info', {}).get('name', 'Unknown')}")
            
            legal_analysis = sec_data.get('legal_analysis', {})
            if legal_analysis:
                print(f"Legal proceedings found: {legal_analysis.get('legal_proceedings', {}).get('found', False)}")
                print(f"Risk factors found: {legal_analysis.get('risk_factors', {}).get('found', False)}")
            
            recent_8k = sec_data.get('recent_material_events', [])
            print(f"Recent 8-K filings (90 days): {len(recent_8k)}")
            
        else:
            print(f"❌ SEC EDGAR integration failed: {sec_data.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ SEC EDGAR test error: {e}")

def test_opencorporates_integration():
    """Test OpenCorporates API integration"""
    print("\n" + "="*60)
    print("TESTING OPENCORPORATES INTEGRATION")
    print("="*60)
    
    integration = LegalDataIntegration()
    
    # Test with a common company name
    test_company = "Apple Inc"
    
    try:
        print(f"\nTesting OpenCorporates data retrieval for {test_company}...")
        
        corporate_data = integration.opencorporates_client.verify_company_ownership(test_company)
        
        if corporate_data and corporate_data.get('found'):
            print("✅ OpenCorporates integration successful!")
            matched_company = corporate_data.get('matched_company', {})
            print(f"Matched company: {matched_company.get('name', 'Unknown')}")
            print(f"Jurisdiction: {matched_company.get('jurisdiction_code', 'Unknown')}")
            print(f"Status: {matched_company.get('current_status', 'Unknown')}")
            
            officers = corporate_data.get('officers', [])
            print(f"Officers found: {len(officers)}")
            
            structure_analysis = corporate_data.get('structure_analysis', {})
            print(f"Governance score: {structure_analysis.get('governance_score', 0)}/100")
            
        else:
            print(f"❌ OpenCorporates integration failed: {corporate_data.get('error', 'Company not found')}")
            
    except Exception as e:
        print(f"❌ OpenCorporates test error: {e}")

def test_comprehensive_integration():
    """Test comprehensive legal intelligence integration"""
    print("\n" + "="*60)
    print("TESTING COMPREHENSIVE LEGAL INTELLIGENCE")
    print("="*60)
    
    integration = LegalDataIntegration()
    
    # Test with Microsoft (another well-known public company)
    test_ticker = "MSFT"
    test_company_name = "Microsoft Corporation"
    
    try:
        print(f"\nTesting comprehensive analysis for {test_ticker}...")
        
        results = integration.get_comprehensive_legal_intelligence(test_ticker, test_company_name)
        
        if results and not results.get('error'):
            print("✅ Comprehensive integration successful!")
            print(f"Data sources used: {', '.join(results.get('data_sources', []))}")
            
            risk_score = results.get('overall_risk_score', {})
            print(f"Overall risk score: {risk_score.get('score', 0)}/100 ({risk_score.get('risk_level', 'unknown')})")
            
            integrated_risks = results.get('integrated_risks', [])
            print(f"Total risks identified: {len(integrated_risks)}")
            
            high_risks = [r for r in integrated_risks if r['severity'] == 'high']
            print(f"High-severity risks: {len(high_risks)}")
            
            compliance_status = results.get('compliance_status', {})
            print(f"Compliance status: {compliance_status.get('overall_status', 'unknown')}")
            
            recommendations = results.get('recommendations', [])
            print(f"Recommendations generated: {len(recommendations)}")
            
            if recommendations:
                print("\nTop recommendations:")
                for i, rec in enumerate(recommendations[:3], 1):
                    print(f"  {i}. {rec}")
            
        else:
            print(f"❌ Comprehensive integration failed: {results.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Comprehensive integration test error: {e}")

def test_risk_summary():
    """Test legal risk summary functionality"""
    print("\n" + "="*60)
    print("TESTING LEGAL RISK SUMMARY")
    print("="*60)
    
    integration = LegalDataIntegration()
    
    test_ticker = "TSLA"  # Tesla - often has interesting legal developments
    
    try:
        print(f"\nTesting risk summary for {test_ticker}...")
        
        summary = integration.get_legal_risk_summary(test_ticker, "Tesla Inc")
        
        if summary and not summary.get('error'):
            print("✅ Risk summary generation successful!")
            print(f"Data sources available: {summary.get('data_sources_available', 0)}")
            print(f"Overall risk level: {summary.get('overall_risk_score', {}).get('risk_level', 'unknown')}")
            print(f"Compliance status: {summary.get('compliance_status', 'unknown')}")
            print(f"High priority risks: {summary.get('high_priority_risks', 0)}")
            print(f"Requires immediate attention: {summary.get('requires_immediate_attention', False)}")
            
        else:
            print(f"❌ Risk summary failed: {summary.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Risk summary test error: {e}")

def main():
    """Run all integration tests"""
    print("LEGAL DATA INTEGRATION TEST SUITE")
    print("="*60)
    
    # Test individual components
    test_sec_edgar_integration()
    test_opencorporates_integration()
    
    # Test integrated functionality
    test_comprehensive_integration()
    test_risk_summary()
    
    print("\n" + "="*60)
    print("INTEGRATION TESTS COMPLETED")
    print("="*60)
    print("\nNote: Some tests may fail due to API rate limits or network issues.")
    print("This is normal for free tier APIs. The integration code handles these gracefully.")

if __name__ == "__main__":
    main()