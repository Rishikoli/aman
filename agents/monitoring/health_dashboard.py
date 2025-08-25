"""
Real-time Health Dashboard for M&A Analysis System

This module provides a comprehensive health dashboard that aggregates metrics
from system monitoring, agent performance tracking, and Prometheus metrics.
"""

import json
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import threading
from flask import Flask, jsonify, render_template_string
import os

from .system_monitor import SystemMonitor
from .agent_performance_tracker import AgentPerformanceTracker, AgentStatus
from .prometheus_metrics import PrometheusMetrics

@dataclass
class HealthStatus:
    """Overall system health status"""
    status: str  # healthy, warning, critical
    score: int   # 0-100
    message: str
    timestamp: datetime

@dataclass
class AlertRule:
    """Alert rule definition"""
    name: str
    condition: str
    threshold: float
    severity: str
    enabled: bool = True

class HealthDashboard:
    """
    Real-time health dashboard for the M&A analysis system
    """
    
    def __init__(self, 
                 system_monitor: SystemMonitor,
                 performance_tracker: AgentPerformanceTracker,
                 prometheus_metrics: PrometheusMetrics,
                 port: int = 8080):
        
        self.system_monitor = system_monitor
        self.performance_tracker = performance_tracker
        self.prometheus_metrics = prometheus_metrics
        self.port = port
        self.logger = logging.getLogger(__name__)
        
        # Flask app for web dashboard
        self.app = Flask(__name__)
        self.setup_routes()
        
        # Alert rules
        self.alert_rules = self._initialize_alert_rules()
        self.active_alerts: List[Dict[str, Any]] = []
        
        # Dashboard state
        self.is_running = False
        self.dashboard_thread = None
        
    def _initialize_alert_rules(self) -> List[AlertRule]:
        """Initialize default alert rules"""
        return [
            AlertRule("high_cpu", "cpu_percent > threshold", 85.0, "warning"),
            AlertRule("critical_cpu", "cpu_percent > threshold", 95.0, "critical"),
            AlertRule("high_memory", "memory_percent > threshold", 90.0, "warning"),
            AlertRule("critical_memory", "memory_percent > threshold", 95.0, "critical"),
            AlertRule("high_disk", "disk_percent > threshold", 90.0, "warning"),
            AlertRule("low_success_rate", "success_rate < threshold", 80.0, "warning"),
            AlertRule("critical_success_rate", "success_rate < threshold", 50.0, "critical"),
            AlertRule("slow_agent", "avg_duration > threshold", 300.0, "warning"),
            AlertRule("very_slow_agent", "avg_duration > threshold", 600.0, "critical"),
        ]
        
    def setup_routes(self):
        """Setup Flask routes for the dashboard"""
        
        @self.app.route('/')
        def dashboard():
            """Main dashboard page"""
            return render_template_string(self._get_dashboard_template())
            
        @self.app.route('/api/health')
        def health_status():
            """Get overall health status"""
            return jsonify(self.get_health_status())
            
        @self.app.route('/api/system')
        def system_metrics():
            """Get system metrics"""
            return jsonify(self.get_system_metrics())
            
        @self.app.route('/api/agents')
        def agent_metrics():
            """Get agent performance metrics"""
            return jsonify(self.get_agent_metrics())
            
        @self.app.route('/api/alerts')
        def alerts():
            """Get active alerts"""
            return jsonify(self.get_active_alerts())
            
        @self.app.route('/api/prometheus')
        def prometheus_metrics():
            """Get Prometheus metrics"""
            return jsonify(self.prometheus_metrics.get_metrics_summary())
            
        @self.app.route('/metrics')
        def prometheus_export():
            """Prometheus metrics endpoint"""
            return self.prometheus_metrics.export_prometheus_format(), 200, {'Content-Type': 'text/plain'}
            
    def start_dashboard(self):
        """Start the health dashboard web server"""
        if self.is_running:
            self.logger.warning("Dashboard already running")
            return
            
        self.is_running = True
        
        # Start monitoring updates
        self.dashboard_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.dashboard_thread.start()
        
        # Start Flask app
        self.logger.info(f"Starting health dashboard on port {self.port}")
        self.app.run(host='0.0.0.0', port=self.port, debug=False, threaded=True)
        
    def stop_dashboard(self):
        """Stop the health dashboard"""
        self.is_running = False
        if self.dashboard_thread:
            self.dashboard_thread.join(timeout=5)
        self.logger.info("Health dashboard stopped")
        
    def _monitoring_loop(self):
        """Main monitoring loop for updating metrics and checking alerts"""
        while self.is_running:
            try:
                # Update Prometheus metrics
                system_metrics = self.system_monitor.get_current_metrics()
                self.prometheus_metrics.update_system_metrics(system_metrics)
                
                # Update agent metrics
                agent_metrics = self.performance_tracker.get_agent_metrics()
                for agent_id, metrics in agent_metrics.items():
                    self.prometheus_metrics.update_agent_metrics(agent_id, metrics)
                
                # Check alerts
                self._check_alerts()
                
                # Export metrics
                self.prometheus_metrics.export_to_file()
                
                time.sleep(30)  # Update every 30 seconds
                
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                time.sleep(30)
                
    def _check_alerts(self):
        """Check alert rules and update active alerts"""
        new_alerts = []
        
        # Get current metrics
        system_metrics = self.system_monitor.get_current_metrics()
        agent_metrics = self.performance_tracker.get_agent_metrics()
        
        # Check system alerts
        for rule in self.alert_rules:
            if not rule.enabled:
                continue
                
            alert_triggered = False
            alert_value = None
            alert_context = ""
            
            if rule.name in ["high_cpu", "critical_cpu"]:
                alert_value = system_metrics.cpu_percent
                if alert_value > rule.threshold:
                    alert_triggered = True
                    alert_context = f"CPU usage: {alert_value:.1f}%"
                    
            elif rule.name in ["high_memory", "critical_memory"]:
                alert_value = system_metrics.memory_percent
                if alert_value > rule.threshold:
                    alert_triggered = True
                    alert_context = f"Memory usage: {alert_value:.1f}%"
                    
            elif rule.name == "high_disk":
                alert_value = system_metrics.disk_usage_percent
                if alert_value > rule.threshold:
                    alert_triggered = True
                    alert_context = f"Disk usage: {alert_value:.1f}%"
                    
            if alert_triggered:
                new_alerts.append({
                    "rule_name": rule.name,
                    "severity": rule.severity,
                    "message": f"{rule.name}: {alert_context}",
                    "value": alert_value,
                    "threshold": rule.threshold,
                    "timestamp": datetime.now().isoformat(),
                    "type": "system"
                })
                
        # Check agent alerts
        for agent_id, metrics in agent_metrics.items():
            for rule in self.alert_rules:
                if not rule.enabled:
                    continue
                    
                alert_triggered = False
                alert_value = None
                
                if rule.name in ["low_success_rate", "critical_success_rate"]:
                    alert_value = metrics.success_rate
                    if alert_value < rule.threshold and metrics.total_executions >= 5:
                        alert_triggered = True
                        
                elif rule.name in ["slow_agent", "very_slow_agent"]:
                    alert_value = metrics.avg_duration_seconds
                    if alert_value > rule.threshold:
                        alert_triggered = True
                        
                if alert_triggered:
                    new_alerts.append({
                        "rule_name": rule.name,
                        "severity": rule.severity,
                        "message": f"{agent_id} {rule.name}: {alert_value:.1f}",
                        "value": alert_value,
                        "threshold": rule.threshold,
                        "timestamp": datetime.now().isoformat(),
                        "type": "agent",
                        "agent_id": agent_id
                    })
                    
        # Update active alerts (keep only recent ones)
        cutoff_time = datetime.now() - timedelta(hours=1)
        self.active_alerts = [
            alert for alert in self.active_alerts 
            if datetime.fromisoformat(alert["timestamp"]) > cutoff_time
        ]
        
        # Add new alerts
        self.active_alerts.extend(new_alerts)
        
        if new_alerts:
            self.logger.warning(f"Generated {len(new_alerts)} new alerts")
            
    def get_health_status(self) -> Dict[str, Any]:
        """Get overall system health status"""
        try:
            # Get current metrics
            system_metrics = self.system_monitor.get_current_metrics()
            agent_summary = self.performance_tracker.get_system_performance_summary()
            bottlenecks = self.performance_tracker.identify_bottlenecks()
            
            # Calculate health score (0-100)
            score = 100
            status = "healthy"
            messages = []
            
            # System health factors
            if system_metrics.cpu_percent > 90:
                score -= 20
                status = "critical"
                messages.append(f"Critical CPU usage: {system_metrics.cpu_percent:.1f}%")
            elif system_metrics.cpu_percent > 80:
                score -= 10
                status = "warning" if status == "healthy" else status
                messages.append(f"High CPU usage: {system_metrics.cpu_percent:.1f}%")
                
            if system_metrics.memory_percent > 90:
                score -= 20
                status = "critical"
                messages.append(f"Critical memory usage: {system_metrics.memory_percent:.1f}%")
            elif system_metrics.memory_percent > 80:
                score -= 10
                status = "warning" if status == "healthy" else status
                messages.append(f"High memory usage: {system_metrics.memory_percent:.1f}%")
                
            # Agent health factors
            if agent_summary["overall_success_rate"] < 50:
                score -= 30
                status = "critical"
                messages.append(f"Critical agent success rate: {agent_summary['overall_success_rate']:.1f}%")
            elif agent_summary["overall_success_rate"] < 80:
                score -= 15
                status = "warning" if status == "healthy" else status
                messages.append(f"Low agent success rate: {agent_summary['overall_success_rate']:.1f}%")
                
            # Bottleneck factors
            high_severity_bottlenecks = [b for b in bottlenecks if b["severity"] == "high"]
            if high_severity_bottlenecks:
                score -= len(high_severity_bottlenecks) * 10
                status = "critical"
                messages.extend([b["description"] for b in high_severity_bottlenecks[:3]])
                
            # Ensure score doesn't go below 0
            score = max(0, score)
            
            # Default message if healthy
            if not messages:
                messages = ["All systems operating normally"]
                
            return {
                "status": status,
                "score": score,
                "message": "; ".join(messages),
                "timestamp": datetime.now().isoformat(),
                "details": {
                    "system_cpu": system_metrics.cpu_percent,
                    "system_memory": system_metrics.memory_percent,
                    "system_disk": system_metrics.disk_usage_percent,
                    "agent_success_rate": agent_summary["overall_success_rate"],
                    "active_agents": agent_summary["total_agents"],
                    "active_executions": agent_summary["active_executions"],
                    "bottlenecks_count": len(bottlenecks)
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error getting health status: {e}")
            return {
                "status": "unknown",
                "score": 0,
                "message": f"Error retrieving health status: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
            
    def get_system_metrics(self) -> Dict[str, Any]:
        """Get detailed system metrics"""
        try:
            current_metrics = self.system_monitor.get_current_metrics()
            health_summary = self.system_monitor.get_system_health_summary()
            
            return {
                "current": asdict(current_metrics),
                "summary": health_summary,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Error getting system metrics: {e}")
            return {"error": str(e)}
            
    def get_agent_metrics(self) -> Dict[str, Any]:
        """Get detailed agent performance metrics"""
        try:
            performance_summary = self.performance_tracker.get_system_performance_summary()
            agent_metrics = self.performance_tracker.get_agent_metrics()
            active_executions = self.performance_tracker.get_active_executions()
            bottlenecks = self.performance_tracker.identify_bottlenecks()
            
            return {
                "summary": performance_summary,
                "individual_metrics": {
                    agent_id: asdict(metrics) 
                    for agent_id, metrics in agent_metrics.items()
                },
                "active_executions": len(active_executions),
                "bottlenecks": bottlenecks,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Error getting agent metrics: {e}")
            return {"error": str(e)}
            
    def get_active_alerts(self) -> Dict[str, Any]:
        """Get active alerts"""
        return {
            "alerts": self.active_alerts,
            "count": len(self.active_alerts),
            "timestamp": datetime.now().isoformat()
        }
        
    def _get_dashboard_template(self) -> str:
        """Get HTML template for the dashboard"""
        return """
<!DOCTYPE html>
<html>
<head>
    <title>M&A Analysis System - Health Dashboard</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { text-align: center; margin-bottom: 30px; }
        .status-card { background: white; border-radius: 8px; padding: 20px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .status-healthy { border-left: 5px solid #4CAF50; }
        .status-warning { border-left: 5px solid #FF9800; }
        .status-critical { border-left: 5px solid #F44336; }
        .metrics-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
        .metric-card { background: white; border-radius: 8px; padding: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .metric-value { font-size: 2em; font-weight: bold; color: #333; }
        .metric-label { color: #666; margin-bottom: 10px; }
        .alert { padding: 10px; margin: 5px 0; border-radius: 4px; }
        .alert-warning { background-color: #fff3cd; border: 1px solid #ffeaa7; }
        .alert-critical { background-color: #f8d7da; border: 1px solid #f5c6cb; }
        .refresh-btn { background: #007bff; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; }
        .timestamp { color: #666; font-size: 0.9em; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>M&A Analysis System - Health Dashboard</h1>
            <button class="refresh-btn" onclick="refreshData()">Refresh</button>
        </div>
        
        <div id="health-status" class="status-card">
            <h2>System Health</h2>
            <div id="health-content">Loading...</div>
        </div>
        
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-label">CPU Usage</div>
                <div id="cpu-usage" class="metric-value">-</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Memory Usage</div>
                <div id="memory-usage" class="metric-value">-</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Agent Success Rate</div>
                <div id="success-rate" class="metric-value">-</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Active Agents</div>
                <div id="active-agents" class="metric-value">-</div>
            </div>
        </div>
        
        <div class="status-card">
            <h2>Active Alerts</h2>
            <div id="alerts-content">Loading...</div>
        </div>
        
        <div class="status-card">
            <h2>Agent Performance</h2>
            <div id="agent-performance">Loading...</div>
        </div>
    </div>

    <script>
        function refreshData() {
            fetchHealthStatus();
            fetchAlerts();
            fetchAgentMetrics();
        }
        
        function fetchHealthStatus() {
            fetch('/api/health')
                .then(response => response.json())
                .then(data => {
                    const statusCard = document.getElementById('health-status');
                    statusCard.className = 'status-card status-' + data.status;
                    
                    document.getElementById('health-content').innerHTML = 
                        '<h3>Status: ' + data.status.toUpperCase() + ' (Score: ' + data.score + '/100)</h3>' +
                        '<p>' + data.message + '</p>' +
                        '<div class="timestamp">Last updated: ' + new Date(data.timestamp).toLocaleString() + '</div>';
                    
                    if (data.details) {
                        document.getElementById('cpu-usage').textContent = data.details.system_cpu.toFixed(1) + '%';
                        document.getElementById('memory-usage').textContent = data.details.system_memory.toFixed(1) + '%';
                        document.getElementById('success-rate').textContent = data.details.agent_success_rate.toFixed(1) + '%';
                        document.getElementById('active-agents').textContent = data.details.active_agents;
                    }
                })
                .catch(error => console.error('Error fetching health status:', error));
        }
        
        function fetchAlerts() {
            fetch('/api/alerts')
                .then(response => response.json())
                .then(data => {
                    const alertsContent = document.getElementById('alerts-content');
                    if (data.alerts.length === 0) {
                        alertsContent.innerHTML = '<p>No active alerts</p>';
                    } else {
                        alertsContent.innerHTML = data.alerts.map(alert => 
                            '<div class="alert alert-' + alert.severity + '">' +
                            '<strong>' + alert.severity.toUpperCase() + ':</strong> ' + alert.message +
                            ' <span class="timestamp">(' + new Date(alert.timestamp).toLocaleTimeString() + ')</span>' +
                            '</div>'
                        ).join('');
                    }
                })
                .catch(error => console.error('Error fetching alerts:', error));
        }
        
        function fetchAgentMetrics() {
            fetch('/api/agents')
                .then(response => response.json())
                .then(data => {
                    const agentContent = document.getElementById('agent-performance');
                    if (data.individual_metrics) {
                        let html = '<table style="width: 100%; border-collapse: collapse;">';
                        html += '<tr><th>Agent</th><th>Success Rate</th><th>Avg Duration</th><th>Total Executions</th></tr>';
                        
                        for (const [agentId, metrics] of Object.entries(data.individual_metrics)) {
                            html += '<tr style="border-bottom: 1px solid #ddd;">';
                            html += '<td style="padding: 8px;">' + agentId + '</td>';
                            html += '<td style="padding: 8px;">' + metrics.success_rate.toFixed(1) + '%</td>';
                            html += '<td style="padding: 8px;">' + metrics.avg_duration_seconds.toFixed(1) + 's</td>';
                            html += '<td style="padding: 8px;">' + metrics.total_executions + '</td>';
                            html += '</tr>';
                        }
                        html += '</table>';
                        agentContent.innerHTML = html;
                    } else {
                        agentContent.innerHTML = '<p>No agent metrics available</p>';
                    }
                })
                .catch(error => console.error('Error fetching agent metrics:', error));
        }
        
        // Auto-refresh every 30 seconds
        setInterval(refreshData, 30000);
        
        // Initial load
        refreshData();
    </script>
</body>
</html>
        """