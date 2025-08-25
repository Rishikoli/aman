#!/usr/bin/env python3
"""
Debug test for AI diagnostics
"""

import sys
import os
import traceback

# Add the agents directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from monitoring.ai_diagnostics import AISystemDiagnostics
    print("✓ AI diagnostics imported successfully")
    
    # Try to create instance
    ai_diagnostics = AISystemDiagnostics()
    print("✓ AI diagnostics instance created")
    
except Exception as e:
    print(f"✗ Error: {e}")
    print("Full traceback:")
    traceback.print_exc()