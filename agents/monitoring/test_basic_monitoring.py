#!/usr/bin/env python3
"""
Basic test script for the monitoring system components
"""

import sys
import os
import time
import logging

# Add the agents directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_system_monitor():
    """Test the SystemMonitor component"""
    print("Testing SystemMonitor...")
    
    try:
        from monitoring.system_monitor import SystemMonitor
        
        monitor = SystemMonitor(collection_interval=1)
        
        # Test getting current metrics
        metrics = monitor.get_current_metrics()
        print(f"✓ CPU: {metrics.cpu_percent:.1f}%")
        print(f"✓ Memory: {metrics.memory_percent:.1f}%")
        print(f"✓ Disk: {metrics.disk_usage_percent:.1f}%")
        
        # Test health summary
        health = monitor.get_system_health_summary()
        print(f"✓ Health Status: {health['health_status']}")
        print(f"✓ Bottlenecks: {len(health['bottlenecks'])}")
        
        return True
        
    except Exception as e:
        print(f"✗ SystemMonitor test failed: {e}")
        return False

def test_performance_tracker():
    """Test the AgentPerformanceTracker component"""
    print("\nTesting AgentPerformanceTracker...")
    
    try:
        from monitoring.agent_performance_tracker import AgentPerformanceTracker, AgentStatus
        
        tracker = AgentPerformanceTracker()
        
        # Test tracking an execution
        execution_key = tracker.start_execution("test_agent", "test_task")
        print(f"✓ Started tracking: {execution_key}")
        
        # Simulate some work
        time.sleep(1)
        
        # Complete the execution
        tracker.end_execution(execution_key, AgentStatus.COMPLETED, 
                            memory_peak_mb=50.0, cpu_avg_percent=25.0)
        print("✓ Completed tracking")
        
        # Get metrics
        metrics = tracker.get_agent_metrics()
        print(f"✓ Tracked agents: {len(metrics)}")
        
        return True
        
    except Exception as e:
        print(f"✗ AgentPerformanceTracker test failed: {e}")
        return False

def test_prometheus_metrics():
    """Test the PrometheusMetrics component"""
    print("\nTesting PrometheusMetrics...")
    
    try:
        from monitoring.prometheus_metrics import PrometheusMetrics
        
        metrics = PrometheusMetrics()
        
        # Test setting metrics
        metrics.set_gauge("system_cpu_usage_percent", 45.5)
        metrics.increment_counter("api_requests_total", 1.0, {"endpoint": "/test"})
        
        # Test export
        prometheus_text = metrics.export_prometheus_format()
        print(f"✓ Generated Prometheus format ({len(prometheus_text)} chars)")
        
        # Test summary
        summary = metrics.get_metrics_summary()
        print(f"✓ Total metrics: {summary['total_metrics']}")
        
        return True
        
    except Exception as e:
        print(f"✗ PrometheusMetrics test failed: {e}")
        return False

def test_monitoring_agent():
    """Test the main MonitoringAgent"""
    print("\nTesting MonitoringAgent...")
    
    try:
        from monitoring.monitoring_agent import MonitoringAgent
        
        agent = MonitoringAgent(dashboard_port=8081)  # Use different port
        
        # Test basic functionality without starting the full system
        execution_key = agent.track_agent_execution("test_agent", "test_task")
        print(f"✓ Started agent tracking: {execution_key}")
        
        time.sleep(0.5)
        
        from monitoring.agent_performance_tracker import AgentStatus
        agent.complete_agent_execution(execution_key, AgentStatus.COMPLETED)
        print("✓ Completed agent tracking")
        
        # Test metrics recording
        agent.record_api_request("/api/test", "GET", 200, 0.1)
        agent.record_deal_processing("completed", 30.0)
        print("✓ Recorded metrics")
        
        return True
        
    except Exception as e:
        print(f"✗ MonitoringAgent test failed: {e}")
        return False

def main():
    """Run all basic tests"""
    print("=" * 50)
    print("Basic Monitoring System Tests")
    print("=" * 50)
    
    tests = [
        test_system_monitor,
        test_performance_tracker,
        test_prometheus_metrics,
        test_monitoring_agent
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        else:
            break  # Stop on first failure
    
    print("\n" + "=" * 50)
    if passed == total:
        print(f"✓ ALL {total} TESTS PASSED!")
        print("✓ Monitoring system is working correctly")
    else:
        print(f"✗ {passed}/{total} tests passed")
        print("✗ Some components need attention")
    print("=" * 50)
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)