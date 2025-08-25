#!/usr/bin/env python3
"""
Simple test to identify import issues
"""

import sys
import os

# Add the agents directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    print("Testing AI diagnostics import...")
    from monitoring.ai_diagnostics import AISystemDiagnostics
    print("✓ AI diagnostics imported successfully")
except Exception as e:
    print(f"✗ AI diagnostics import failed: {e}")

try:
    print("Testing predictive maintenance import...")
    from monitoring.predictive_maintenance import PredictiveMaintenanceEngine
    print("✓ Predictive maintenance imported successfully")
except Exception as e:
    print(f"✗ Predictive maintenance import failed: {e}")

try:
    print("Testing automated reporting import...")
    from monitoring.automated_reporting import AutomatedReportingEngine
    print("✓ Automated reporting imported successfully")
except Exception as e:
    print(f"✗ Automated reporting import failed: {e}")

print("Import test completed")