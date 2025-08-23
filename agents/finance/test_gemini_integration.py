#!/usr/bin/env python3
"""
Test Gemini AI Integration
"""

import sys
import os
import json

# Add the agents directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from finance.finance_agent import FinanceAgent

def test_gemini_ai_analysis():
    """Test AI-powered financial analysis"""
    print("Testing Gemini AI Integration...")
    print("=" * 50)
    
    # Initialize agent
    agent = FinanceAgent()
    
    # Test connection
    connection_test = agent.gemini_analyzer.test_connection()
    print(f"✓ Gemini Connection: {connection_test['success']}")
    print(f"  Message: {connection_test['message']}")
    
    if not connection_test['success']:
        print("❌ Gemini not available - stopping test")
        return
    
    # Create test data with anomalies
    dummy_data = agent._create_dummy_financial_data()
    
    # Add some anomalies to make it interesting
    dummy_data['statements']['incomeStatement'][0]['revenue'] = -50000000  # Negative revenue
    dummy_data['statements']['balanceSheet'][0]['totalDebt'] = 500000000   # Very high debt
    
    print("\n" + "=" * 50)
    print("Testing AI Anomaly Explanation...")
    
    # Detect anomalies
    anomalies = agent.analysis_engine.detect_financial_anomalies(dummy_data)
    print(f"✓ Anomalies detected: {len(anomalies.get('anomalies', []))}")
    
    if anomalies.get('anomalies'):
        # Get AI explanation
        print("🤖 Getting AI explanation...")
        explanation = agent.gemini_analyzer.explain_financial_anomaly(anomalies)
        
        if explanation.get('business_reasons'):
            print("✓ AI Explanation Generated:")
            print(f"  Business Reasons: {len(explanation['business_reasons'])}")
            for i, reason in enumerate(explanation['business_reasons'][:2], 1):
                print(f"    {i}. {reason}")
            
            print(f"  Severity Assessment: {explanation.get('severity_assessment', 'N/A')}")
            print(f"  Investigation Areas: {len(explanation.get('investigation_areas', []))}")
        else:
            print("⚠ AI explanation format unexpected")
            print(f"  Keys: {list(explanation.keys())}")
    
    print("\n" + "=" * 50)
    print("Testing AI Forecast Validation...")
    
    # Create forecasts
    forecasts = agent.analysis_engine.create_financial_forecasts(dummy_data, 2)
    print(f"✓ Forecasts created: {len(forecasts.get('forecasts', {}))}")
    
    if forecasts.get('forecasts'):
        # Get AI validation
        print("🤖 Getting AI forecast validation...")
        validation = agent.gemini_analyzer.validate_financial_forecasts(forecasts)
        
        if validation.get('reasonableness'):
            print("✓ AI Validation Generated:")
            print(f"  Reasonableness: {validation['reasonableness'][:100]}...")
            print(f"  Confidence Rating: {validation.get('confidence_rating', 'N/A')}/10")
            print(f"  Key Assumptions: {len(validation.get('key_assumptions', []))}")
        else:
            print("⚠ AI validation format unexpected")
            print(f"  Keys: {list(validation.keys())}")
    
    print("\n" + "=" * 50)
    print("🎉 Gemini AI Integration Test Complete!")

if __name__ == "__main__":
    test_gemini_ai_analysis()