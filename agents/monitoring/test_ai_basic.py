#!/usr/bin/env python3
"""
Basic test for AI diagnostics components
"""

import sys
import os
import asyncio
import logging

# Add the agents directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def test_ai_components():
    """Test AI diagnostics components"""
    print("=" * 50)
    print("Testing AI Diagnostics Components")
    print("=" * 50)
    
    # Test 1: AI Diagnostics
    print("\n1. Testing AISystemDiagnostics...")
    try:
        from monitoring.ai_diagnostics import AISystemDiagnostics
        
        ai_diagnostics = AISystemDiagnostics()
        print(f"✓ AI Diagnostics initialized (Client: {ai_diagnostics.client is not None})")
        
        # Test system diagnosis with fallback
        test_data = {
            'system_metrics': {'cpu_percent': 75.0, 'memory_percent': 80.0},
            'alerts': [{'severity': 'warning', 'message': 'Test alert'}]
        }
        
        diagnosis = await ai_diagnostics.diagnose_system_issues(test_data)
        print(f"✓ System diagnosis completed (AI-powered: {diagnosis.get('ai_powered', False)})")
        
    except Exception as e:
        print(f"✗ AI Diagnostics test failed: {e}")
        return False
    
    # Test 2: Predictive Maintenance
    print("\n2. Testing PredictiveMaintenanceEngine...")
    try:
        from monitoring.predictive_maintenance import PredictiveMaintenanceEngine
        
        maintenance = PredictiveMaintenanceEngine()
        print("✓ Predictive Maintenance initialized")
        
        # Add test data
        maintenance.add_metrics_data({'cpu_percent': 60.0, 'memory_percent': 70.0})
        print("✓ Test data added")
        
    except Exception as e:
        print(f"✗ Predictive Maintenance test failed: {e}")
        return False
    
    # Test 3: Monitoring Agent with AI
    print("\n3. Testing MonitoringAgent with AI...")
    try:
        from monitoring import MonitoringAgent
        
        agent = MonitoringAgent(dashboard_port=8084, enable_ai_diagnostics=True)
        print("✓ Monitoring Agent with AI initialized")
        
        # Test AI status
        status = agent.get_ai_diagnostics_status()
        print(f"✓ AI status retrieved (enabled: {status['ai_diagnostics_enabled']})")
        
    except Exception as e:
        print(f"✗ Monitoring Agent test failed: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("✓ ALL BASIC AI TESTS PASSED!")
    print("=" * 50)
    
    print("\nAI Diagnostics Features Available:")
    print("✓ System issue diagnosis with fallback")
    print("✓ Predictive maintenance engine")
    print("✓ Integrated monitoring agent")
    print("✓ Graceful handling when AI unavailable")
    
    return True

if __name__ == "__main__":
    success = asyncio.run(test_ai_components())
    sys.exit(0 if success else 1)