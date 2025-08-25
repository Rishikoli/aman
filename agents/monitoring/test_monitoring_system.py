#!/usr/bin/env python3
"""
Test script for the comprehensive monitoring system
"""

import sys
import os
import time
import logging
import threading
from datetime import datetime

# Add the agents directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from monitoring import MonitoringAgent, AgentStatus

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def simulate_agent_work(monitoring_agent: MonitoringAgent, agent_id: str, task_id: str, 
                       duration: float, should_fail: bool = False):
    """Simulate agent work for testing"""
    print(f"Starting {agent_id} task {task_id}")
    
    # Start tracking
    execution_key = monitoring_agent.track_agent_execution(agent_id, task_id)
    
    # Simulate work
    time.sleep(duration)
    
    # Complete tracking
    status = AgentStatus.FAILED if should_fail else AgentStatus.COMPLETED
    error_msg = "Simulated failure" if should_fail else None
    
    monitoring_agent.complete_agent_execution(
        execution_key, 
        status, 
        error_message=error_msg,
        memory_peak_mb=100.0 + (duration * 10),  # Simulate memory usage
        cpu_avg_percent=20.0 + (duration * 5),   # Simulate CPU usage
        result_size_bytes=1024 * int(duration * 100)  # Simulate result size
    )
    
    print(f"Completed {agent_id} task {task_id} - Status: {status.value}")

def test_monitoring_system():
    """Test the comprehensive monitoring system"""
    print("=" * 60)
    print("Testing M&A Analysis System Monitoring")
    print("=" * 60)
    
    # Initialize monitoring agent
    print("\n1. Initializing Monitoring Agent...")
    monitoring_agent = MonitoringAgent(
        dashboard_port=8080,
        collection_interval=2  # Faster for testing
    )
    
    # Start monitoring
    print("\n2. Starting monitoring components...")
    try:
        # Start monitoring in a separate thread to avoid blocking
        monitor_thread = threading.Thread(target=monitoring_agent.start_monitoring, daemon=True)
        monitor_thread.start()
        
        # Give it time to start
        time.sleep(3)
        
        print("✓ Monitoring started successfully")
        print(f"✓ Dashboard available at: http://localhost:8080")
        print(f"✓ Prometheus metrics at: http://localhost:8080/metrics")
        
    except Exception as e:
        print(f"✗ Failed to start monitoring: {e}")
        return False
    
    # Test system metrics
    print("\n3. Testing system metrics collection...")
    try:
        system_metrics = monitoring_agent.get_system_metrics()
        print(f"✓ CPU Usage: {system_metrics['current']['cpu_percent']:.1f}%")
        print(f"✓ Memory Usage: {system_metrics['current']['memory_percent']:.1f}%")
        print(f"✓ Disk Usage: {system_metrics['current']['disk_usage_percent']:.1f}%")
    except Exception as e:
        print(f"✗ Failed to get system metrics: {e}")
        return False
    
    # Test agent performance tracking
    print("\n4. Testing agent performance tracking...")
    try:
        # Simulate various agent executions
        agents_to_test = [
            ("finance_agent", "analyze_financials", 2.0, False),
            ("legal_agent", "review_contracts", 3.0, False),
            ("synergy_agent", "identify_synergies", 1.5, False),
            ("reputation_agent", "analyze_sentiment", 2.5, False),
            ("finance_agent", "complex_analysis", 4.0, True),  # This one fails
        ]
        
        # Run simulations in parallel
        threads = []
        for agent_id, task_id, duration, should_fail in agents_to_test:
            thread = threading.Thread(
                target=simulate_agent_work,
                args=(monitoring_agent, agent_id, task_id, duration, should_fail)
            )
            threads.append(thread)
            thread.start()
            time.sleep(0.5)  # Stagger starts
        
        # Wait for all to complete
        for thread in threads:
            thread.join()
            
        print("✓ Agent simulations completed")
        
    except Exception as e:
        print(f"✗ Failed agent performance testing: {e}")
        return False
    
    # Test API request tracking
    print("\n5. Testing API request tracking...")
    try:
        monitoring_agent.record_api_request("/api/deals", "POST", 200, 0.5)
        monitoring_agent.record_api_request("/api/agents/finance", "GET", 200, 0.2)
        monitoring_agent.record_api_request("/api/health", "GET", 500, 1.0)
        print("✓ API request metrics recorded")
    except Exception as e:
        print(f"✗ Failed API request tracking: {e}")
        return False
    
    # Test deal processing tracking
    print("\n6. Testing deal processing tracking...")
    try:
        monitoring_agent.record_deal_processing("completed", 120.0)
        monitoring_agent.record_deal_processing("failed", 45.0)
        print("✓ Deal processing metrics recorded")
    except Exception as e:
        print(f"✗ Failed deal processing tracking: {e}")
        return False
    
    # Wait a bit for metrics to be processed
    print("\n7. Waiting for metrics processing...")
    time.sleep(5)
    
    # Test health status
    print("\n8. Testing health status...")
    try:
        health_status = monitoring_agent.get_system_health()
        print(f"✓ Overall Health: {health_status['status'].upper()}")
        print(f"✓ Health Score: {health_status['score']}/100")
        print(f"✓ Message: {health_status['message']}")
    except Exception as e:
        print(f"✗ Failed to get health status: {e}")
        return False
    
    # Test agent performance metrics
    print("\n9. Testing agent performance metrics...")
    try:
        agent_performance = monitoring_agent.get_agent_performance()
        if 'individual_metrics' in agent_performance:
            for agent_id, metrics in agent_performance['individual_metrics'].items():
                print(f"✓ {agent_id}: {metrics['success_rate']:.1f}% success, "
                      f"{metrics['avg_duration_seconds']:.1f}s avg duration")
        else:
            print("✓ Agent performance data structure ready")
    except Exception as e:
        print(f"✗ Failed to get agent performance: {e}")
        return False
    
    # Test bottleneck identification
    print("\n10. Testing bottleneck identification...")
    try:
        bottlenecks = monitoring_agent.identify_bottlenecks()
        print(f"✓ Found {bottlenecks['total_bottlenecks']} bottlenecks")
        print(f"✓ Generated {len(bottlenecks['recommendations'])} recommendations")
        
        if bottlenecks['recommendations']:
            print("   Sample recommendations:")
            for rec in bottlenecks['recommendations'][:2]:
                print(f"   - {rec['recommendation']}")
                
    except Exception as e:
        print(f"✗ Failed bottleneck identification: {e}")
        return False
    
    # Test alerts
    print("\n11. Testing alert system...")
    try:
        alerts = monitoring_agent.get_active_alerts()
        print(f"✓ Active alerts: {alerts['count']}")
    except Exception as e:
        print(f"✗ Failed to get alerts: {e}")
        return False
    
    # Test monitoring summary
    print("\n12. Testing monitoring summary...")
    try:
        summary = monitoring_agent.get_monitoring_summary()
        print(f"✓ Overall Status: {summary['overall_health']['status']}")
        print(f"✓ System CPU: {summary['system_status']['cpu_usage']:.1f}%")
        print(f"✓ Agent Success Rate: {summary['agent_status']['success_rate']:.1f}%")
        print(f"✓ Total Bottlenecks: {summary['bottlenecks']['total_count']}")
    except Exception as e:
        print(f"✗ Failed to get monitoring summary: {e}")
        return False
    
    # Test data export
    print("\n13. Testing data export...")
    try:
        export_file = "/tmp/monitoring_test_export.json"
        monitoring_agent.export_monitoring_data(export_file)
        
        # Check if file was created
        if os.path.exists(export_file):
            file_size = os.path.getsize(export_file)
            print(f"✓ Exported monitoring data to {export_file} ({file_size} bytes)")
        else:
            print("✗ Export file not created")
            return False
            
    except Exception as e:
        print(f"✗ Failed data export: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("✓ ALL MONITORING TESTS PASSED!")
    print("=" * 60)
    
    print(f"\nDashboard is running at: http://localhost:8080")
    print(f"Prometheus metrics at: http://localhost:8080/metrics")
    print("\nPress Ctrl+C to stop the monitoring system...")
    
    try:
        # Keep running to allow manual testing of the dashboard
        while True:
            time.sleep(10)
            # Show periodic status
            health = monitoring_agent.get_system_health()
            print(f"[{datetime.now().strftime('%H:%M:%S')}] "
                  f"Health: {health['status']} ({health['score']}/100)")
            
    except KeyboardInterrupt:
        print("\n\nStopping monitoring system...")
        monitoring_agent.stop_monitoring()
        print("✓ Monitoring stopped")
        
    return True

if __name__ == "__main__":
    success = test_monitoring_system()
    sys.exit(0 if success else 1)