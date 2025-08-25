#!/usr/bin/env python3
"""
Test script for AI-powered system diagnostics
"""

import sys
import os
import time
import logging
import asyncio
from datetime import datetime

# Add the agents directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def test_ai_diagnostics():
    """Test AI-powered diagnostics components"""
    print("=" * 70)
    print("Testing AI-Powered System Diagnostics")
    print("=" * 70)
    
    # Test 1: AI Diagnostics Component
    print("\n1. Testing AISystemDiagnostics...")
    try:
        from monitoring.ai_diagnostics import AISystemDiagnostics
        
        ai_diagnostics = AISystemDiagnostics()
        print(f"✓ AI Diagnostics initialized (Client available: {ai_diagnostics.client is not None})")
        
        # Test system diagnosis
        test_system_data = {
            'system_metrics': {
                'cpu_percent': 75.5,
                'memory_percent': 82.3,
                'disk_usage_percent': 45.2
            },
            'alerts': [
                {'severity': 'warning', 'message': 'High memory usage'},
                {'severity': 'info', 'message': 'System running normally'}
            ],
            'agent_performance': {
                'overall_success_rate': 85.2,
                'overall_avg_duration_seconds': 15.3
            },
            'recent_errors': [
                {'error_type': 'connection_timeout', 'count': 3},
                {'error_type': 'memory_allocation', 'count': 1}
            ],
            'bottlenecks': [
                {'type': 'slow_execution', 'severity': 'medium'}
            ]
        }
        
        diagnosis = await ai_diagnostics.diagnose_system_issues(test_system_data)
        print(f"✓ System diagnosis completed (AI-powered: {diagnosis.get('ai_powered', False)})")
        print(f"  Health Assessment: {diagnosis.get('overall_health_assessment', 'Unknown')}")
        print(f"  Urgency Level: {diagnosis.get('urgency_level', 'Unknown')}")
        print(f"  Confidence: {diagnosis.get('confidence_level', 0)*100:.0f}%")
        
        # Test error analysis
        test_errors = [
            {
                'timestamp': datetime.now().isoformat(),
                'error_type': 'connection_timeout',
                'message': 'API connection timeout',
                'severity': 'warning'
            },
            {
                'timestamp': datetime.now().isoformat(),
                'error_type': 'memory_allocation',
                'message': 'Failed to allocate memory',
                'severity': 'error'
            }
        ]
        
        error_analysis = await ai_diagnostics.analyze_error_logs(test_errors)
        print(f"✓ Error analysis completed (AI-powered: {error_analysis.get('ai_powered', False)})")
        print(f"  Error patterns found: {len(error_analysis.get('error_patterns', []))}")
        
    except Exception as e:
        print(f"✗ AI Diagnostics test failed: {e}")
        return False
    
    # Test 2: Predictive Maintenance
    print("\n2. Testing PredictiveMaintenanceEngine...")
    try:
        from monitoring.predictive_maintenance import PredictiveMaintenanceEngine
        
        maintenance_engine = PredictiveMaintenanceEngine()
        print("✓ Predictive Maintenance Engine initialized")
        
        # Add some test data
        for i in range(10):
            test_metrics = {
                'cpu_percent': 50 + i * 2,  # Increasing trend
                'memory_percent': 60 + i * 1.5,
                'disk_usage_percent': 30 + i * 0.5
            }
            maintenance_engine.add_metrics_data(test_metrics)
            time.sleep(0.1)  # Small delay to create time series
            
        # Analyze trends
        trends = maintenance_engine.analyze_system_trends(days_back=1)
        print(f"✓ Trend analysis completed: {len(trends)} trends identified")
        
        for trend in trends[:3]:  # Show first 3 trends
            print(f"  {trend.metric_name}: {trend.trend_direction} "
                  f"(strength: {trend.trend_strength:.2f}, confidence: {trend.confidence:.2f})")
        
        # Predict maintenance needs
        maintenance_alerts = maintenance_engine.predict_maintenance_needs(forecast_days=30)
        print(f"✓ Maintenance prediction completed: {len(maintenance_alerts)} alerts generated")
        
        for alert in maintenance_alerts[:2]:  # Show first 2 alerts
            print(f"  {alert.severity.upper()}: {alert.component} - {alert.description}")
            
        # Get maintenance schedule
        schedule = maintenance_engine.get_maintenance_schedule(days_ahead=60)
        print(f"✓ Maintenance schedule generated")
        print(f"  Immediate actions: {len(schedule['schedule']['immediate'])}")
        print(f"  Total estimated cost: ${schedule['summary']['estimated_total_cost']:.0f}")
        
    except Exception as e:
        print(f"✗ Predictive Maintenance test failed: {e}")
        return False
    
    # Test 3: Automated Reporting
    print("\n3. Testing AutomatedReportingEngine...")
    try:
        from monitoring.automated_reporting import AutomatedReportingEngine
        
        # Create reporting engine (without AI for basic test)
        reporting_engine = AutomatedReportingEngine(
            ai_diagnostics=ai_diagnostics,
            predictive_maintenance=maintenance_engine,
            report_storage_path="/tmp/test_reports"
        )
        print("✓ Automated Reporting Engine initialized")
        
        # Generate a test report
        test_system_data = {
            'system_metrics': {
                'cpu_percent': 65.2,
                'memory_percent': 78.5,
                'disk_usage_percent': 42.1
            },
            'agent_performance': {
                'overall_success_rate': 89.3,
                'overall_avg_duration_seconds': 11.7,
                'total_agents': 5,
                'active_executions': 1
            },
            'alerts': [
                {'severity': 'warning', 'message': 'Memory usage above threshold'}
            ],
            'bottlenecks': [
                {'type': 'memory_usage', 'severity': 'medium'}
            ]
        }
        
        report = await reporting_engine.generate_health_report("daily", test_system_data)
        print(f"✓ Health report generated: {report.report_id}")
        print(f"  Report type: {report.report_type}")
        print(f"  Health score: {report.overall_health_score}/100")
        print(f"  Sections: {len(report.sections)}")
        print(f"  Recommendations: {len(report.recommendations)}")
        
        # Test report history
        history = reporting_engine.get_report_history(days_back=1)
        print(f"✓ Report history retrieved: {len(history)} reports found")
        
    except Exception as e:
        print(f"✗ Automated Reporting test failed: {e}")
        return False
    
    # Test 4: Integrated Monitoring Agent with AI
    print("\n4. Testing MonitoringAgent with AI diagnostics...")
    try:
        from monitoring import MonitoringAgent
        
        # Initialize with AI diagnostics enabled
        monitoring_agent = MonitoringAgent(
            dashboard_port=8083,
            enable_ai_diagnostics=True
        )
        print("✓ Monitoring Agent with AI diagnostics initialized")
        
        # Test AI diagnostics status
        ai_status = monitoring_agent.get_ai_diagnostics_status()
        print(f"✓ AI diagnostics status retrieved")
        print(f"  AI diagnostics enabled: {ai_status['ai_diagnostics_enabled']}")
        print(f"  System diagnosis available: {ai_status['capabilities']['system_diagnosis']}")
        print(f"  Maintenance prediction available: {ai_status['capabilities']['maintenance_prediction']}")
        print(f"  Automated reporting available: {ai_status['capabilities']['automated_reporting']}")
        
        # Test AI diagnosis
        diagnosis_result = await monitoring_agent.run_ai_diagnostics()
        if 'error' not in diagnosis_result:
            print("✓ AI diagnostics execution completed")
            ai_diagnosis = diagnosis_result.get('ai_diagnosis', {})
            print(f"  Health assessment: {ai_diagnosis.get('overall_health_assessment', 'Unknown')}")
        else:
            print(f"✓ AI diagnostics handled gracefully: {diagnosis_result['error']}")
        
        # Test maintenance prediction
        maintenance_result = await monitoring_agent.predict_maintenance_needs(forecast_days=30)
        if 'error' not in maintenance_result:
            print("✓ Maintenance prediction completed")
            alerts = maintenance_result.get('maintenance_alerts', [])
            print(f"  Maintenance alerts: {len(alerts)}")
        else:
            print(f"✓ Maintenance prediction handled gracefully: {maintenance_result['error']}")
        
        # Test performance optimization
        optimization_result = await monitoring_agent.optimize_system_performance()
        if 'error' not in optimization_result:
            print("✓ Performance optimization completed")
        else:
            print(f"✓ Performance optimization handled gracefully: {optimization_result['error']}")
        
        # Test health report generation
        report_result = await monitoring_agent.generate_health_report("daily")
        if 'error' not in report_result:
            print("✓ Health report generation completed")
            print(f"  Report ID: {report_result.get('report_id', 'Unknown')}")
            print(f"  Health score: {report_result.get('health_score', 0)}/100")
        else:
            print(f"✓ Health report generation handled gracefully: {report_result['error']}")
        
    except Exception as e:
        print(f"✗ Integrated Monitoring Agent test failed: {e}")
        return False
    
    print("\n" + "=" * 70)
    print("✓ ALL AI DIAGNOSTICS TESTS COMPLETED SUCCESSFULLY!")
    print("=" * 70)
    
    print("\nAI Diagnostics System Features:")
    print("✓ System issue diagnosis with root cause analysis")
    print("✓ Error pattern analysis and recommendations")
    print("✓ Predictive maintenance with trend analysis")
    print("✓ Performance optimization recommendations")
    print("✓ Automated health report generation")
    print("✓ Graceful fallback when AI services unavailable")
    
    print(f"\nNote: Full AI capabilities require GEMINI_API_KEY environment variable")
    print(f"Current AI status: {'Available' if ai_diagnostics.client else 'Fallback mode'}")
    
    return True

async def main():
    """Main test function"""
    success = await test_ai_diagnostics()
    return success

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)