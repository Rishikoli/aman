#!/usr/bin/env python3
"""
Integration example showing how to use the monitoring system with M&A agents
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

class MockMAAgent:
    """Mock M&A agent for demonstration"""
    
    def __init__(self, agent_id: str, monitoring_agent: MonitoringAgent):
        self.agent_id = agent_id
        self.monitoring_agent = monitoring_agent
        self.logger = logging.getLogger(f"agents.{agent_id}")
        
    def analyze_deal(self, deal_id: str, complexity: str = "medium") -> dict:
        """Simulate deal analysis with monitoring"""
        task_id = f"analyze_deal_{deal_id}"
        
        # Start monitoring
        execution_key = self.monitoring_agent.track_agent_execution(self.agent_id, task_id)
        
        try:
            self.logger.info(f"Starting analysis for deal {deal_id}")
            
            # Simulate different processing times based on complexity
            processing_times = {"simple": 1.0, "medium": 3.0, "complex": 6.0}
            processing_time = processing_times.get(complexity, 3.0)
            
            # Simulate work with periodic updates
            for i in range(int(processing_time)):
                time.sleep(1)
                self.logger.info(f"Processing step {i+1}/{int(processing_time)}")
                
            # Simulate occasional failures
            import random
            should_fail = random.random() < 0.1  # 10% failure rate
            
            if should_fail:
                raise Exception("Simulated processing error")
                
            # Generate mock results
            result = {
                "deal_id": deal_id,
                "agent_id": self.agent_id,
                "analysis_complete": True,
                "risk_score": random.randint(1, 10),
                "findings": [f"Finding {i}" for i in range(random.randint(1, 5))],
                "processing_time": processing_time
            }
            
            # Complete monitoring successfully
            self.monitoring_agent.complete_agent_execution(
                execution_key,
                AgentStatus.COMPLETED,
                memory_peak_mb=50.0 + (processing_time * 10),
                cpu_avg_percent=20.0 + (processing_time * 5),
                result_size_bytes=len(str(result))
            )
            
            self.logger.info(f"Successfully completed analysis for deal {deal_id}")
            return result
            
        except Exception as e:
            # Complete monitoring with failure
            self.monitoring_agent.complete_agent_execution(
                execution_key,
                AgentStatus.FAILED,
                error_message=str(e),
                memory_peak_mb=30.0,
                cpu_avg_percent=15.0
            )
            
            self.logger.error(f"Failed to analyze deal {deal_id}: {e}")
            raise

class DealOrchestrator:
    """Mock deal orchestrator that coordinates multiple agents"""
    
    def __init__(self, monitoring_agent: MonitoringAgent):
        self.monitoring_agent = monitoring_agent
        self.logger = logging.getLogger("orchestrator")
        
        # Initialize mock agents
        self.agents = {
            "finance_agent": MockMAAgent("finance_agent", monitoring_agent),
            "legal_agent": MockMAAgent("legal_agent", monitoring_agent),
            "synergy_agent": MockMAAgent("synergy_agent", monitoring_agent),
            "reputation_agent": MockMAAgent("reputation_agent", monitoring_agent),
            "operations_agent": MockMAAgent("operations_agent", monitoring_agent)
        }
        
    def process_deal(self, deal_id: str) -> dict:
        """Process a complete deal with all agents"""
        self.logger.info(f"Starting comprehensive analysis for deal {deal_id}")
        
        # Record deal processing start
        start_time = time.time()
        
        try:
            results = {}
            
            # Run agents in parallel
            threads = []
            agent_results = {}
            
            def run_agent(agent_name, agent):
                try:
                    complexity = "complex" if agent_name == "legal_agent" else "medium"
                    agent_results[agent_name] = agent.analyze_deal(deal_id, complexity)
                except Exception as e:
                    agent_results[agent_name] = {"error": str(e)}
                    
            # Start all agents
            for agent_name, agent in self.agents.items():
                thread = threading.Thread(target=run_agent, args=(agent_name, agent))
                threads.append(thread)
                thread.start()
                
            # Wait for all agents to complete
            for thread in threads:
                thread.join()
                
            # Compile results
            results = {
                "deal_id": deal_id,
                "timestamp": datetime.now().isoformat(),
                "agent_results": agent_results,
                "overall_status": "completed" if all("error" not in r for r in agent_results.values()) else "partial_failure"
            }
            
            # Record successful deal processing
            duration = time.time() - start_time
            self.monitoring_agent.record_deal_processing("completed", duration)
            
            self.logger.info(f"Completed deal analysis for {deal_id} in {duration:.1f}s")
            return results
            
        except Exception as e:
            # Record failed deal processing
            duration = time.time() - start_time
            self.monitoring_agent.record_deal_processing("failed", duration)
            
            self.logger.error(f"Failed to process deal {deal_id}: {e}")
            raise

def demonstrate_monitoring_integration():
    """Demonstrate the monitoring system with M&A agents"""
    print("=" * 70)
    print("M&A Analysis System - Monitoring Integration Demo")
    print("=" * 70)
    
    # Initialize monitoring
    print("\n1. Initializing monitoring system...")
    monitoring_agent = MonitoringAgent(dashboard_port=8082, collection_interval=2)
    
    # Start monitoring in background
    monitor_thread = threading.Thread(target=monitoring_agent.start_monitoring, daemon=True)
    monitor_thread.start()
    time.sleep(2)
    
    print("✓ Monitoring system started")
    print("✓ Dashboard: http://localhost:8082")
    print("✓ Metrics: http://localhost:8082/metrics")
    
    # Initialize orchestrator
    print("\n2. Initializing deal orchestrator...")
    orchestrator = DealOrchestrator(monitoring_agent)
    print("✓ Deal orchestrator ready with 5 agents")
    
    # Process multiple deals
    print("\n3. Processing sample deals...")
    deals_to_process = [
        "DEAL_001_TechAcquisition",
        "DEAL_002_HealthcareMerger", 
        "DEAL_003_FinancialServices",
        "DEAL_004_ManufacturingBuyout"
    ]
    
    for i, deal_id in enumerate(deals_to_process):
        print(f"\n   Processing {deal_id} ({i+1}/{len(deals_to_process)})...")
        
        try:
            # Record API request for deal creation
            api_start = time.time()
            result = orchestrator.process_deal(deal_id)
            api_duration = time.time() - api_start
            
            # Record API metrics
            monitoring_agent.record_api_request(f"/api/deals/{deal_id}", "POST", 200, api_duration)
            
            # Show results summary
            successful_agents = sum(1 for r in result["agent_results"].values() if "error" not in r)
            total_agents = len(result["agent_results"])
            print(f"   ✓ {successful_agents}/{total_agents} agents completed successfully")
            
        except Exception as e:
            print(f"   ✗ Failed to process {deal_id}: {e}")
            monitoring_agent.record_api_request(f"/api/deals/{deal_id}", "POST", 500, 1.0)
            
        # Brief pause between deals
        time.sleep(1)
    
    # Wait for metrics to be processed
    print("\n4. Processing metrics...")
    time.sleep(3)
    
    # Show monitoring results
    print("\n5. Monitoring Results:")
    print("-" * 50)
    
    # System health
    health = monitoring_agent.get_system_health()
    print(f"Overall Health: {health['status'].upper()} ({health['score']}/100)")
    print(f"Message: {health['message']}")
    
    # Agent performance
    agent_perf = monitoring_agent.get_agent_performance()
    if 'individual_metrics' in agent_perf:
        print(f"\nAgent Performance:")
        for agent_id, metrics in agent_perf['individual_metrics'].items():
            print(f"  {agent_id}:")
            print(f"    Success Rate: {metrics['success_rate']:.1f}%")
            print(f"    Avg Duration: {metrics['avg_duration_seconds']:.1f}s")
            print(f"    Total Executions: {metrics['total_executions']}")
    
    # Bottlenecks
    bottlenecks = monitoring_agent.identify_bottlenecks()
    print(f"\nBottlenecks Found: {bottlenecks['total_bottlenecks']}")
    if bottlenecks['recommendations']:
        print("Recommendations:")
        for rec in bottlenecks['recommendations'][:3]:
            print(f"  - {rec['recommendation']}")
    
    # Active alerts
    alerts = monitoring_agent.get_active_alerts()
    print(f"\nActive Alerts: {alerts['count']}")
    
    # Export comprehensive report
    print("\n6. Exporting monitoring report...")
    report_file = "/tmp/ma_monitoring_report.json"
    monitoring_agent.export_monitoring_data(report_file)
    
    if os.path.exists(report_file):
        file_size = os.path.getsize(report_file)
        print(f"✓ Report exported to {report_file} ({file_size} bytes)")
    
    print("\n" + "=" * 70)
    print("✓ MONITORING INTEGRATION DEMO COMPLETED")
    print("=" * 70)
    
    print(f"\nMonitoring Dashboard: http://localhost:8082")
    print(f"Prometheus Metrics: http://localhost:8082/metrics")
    print("\nThe monitoring system is now tracking:")
    print("- System resource usage (CPU, Memory, Disk)")
    print("- Agent performance and bottlenecks")
    print("- API request metrics")
    print("- Deal processing statistics")
    print("- Real-time health status and alerts")
    
    print("\nPress Ctrl+C to stop...")
    
    try:
        # Keep running for manual inspection
        while True:
            time.sleep(10)
            summary = monitoring_agent.get_monitoring_summary()
            print(f"[{datetime.now().strftime('%H:%M:%S')}] "
                  f"Health: {summary['overall_health']['status']} "
                  f"({summary['overall_health']['score']}/100) | "
                  f"CPU: {summary['system_status']['cpu_usage']:.1f}% | "
                  f"Agents: {summary['agent_status']['success_rate']:.1f}% success")
                  
    except KeyboardInterrupt:
        print("\n\nShutting down monitoring system...")
        monitoring_agent.stop_monitoring()
        print("✓ Monitoring stopped")

if __name__ == "__main__":
    demonstrate_monitoring_integration()