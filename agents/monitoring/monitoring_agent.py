"""
Comprehensive System Health Monitoring Agent

This is the main monitoring agent that coordinates all monitoring components
and provides a unified interface for system health monitoring with AI-powered diagnostics.
"""

import logging
import time
import threading
import asyncio
from typing import Dict, Any, Optional, List
from datetime import datetime

from .system_monitor import SystemMonitor
from .agent_performance_tracker import AgentPerformanceTracker, AgentStatus
from .prometheus_metrics import PrometheusMetrics
from .health_dashboard import HealthDashboard
from .ai_diagnostics import AISystemDiagnostics
from .predictive_maintenance import PredictiveMaintenanceEngine
from .automated_reporting import AutomatedReportingEngine

class MonitoringAgent:
    """
    Main monitoring agent that coordinates all monitoring components
    """
    
    def __init__(self, 
                 dashboard_port: int = 8080,
                 metrics_export_path: str = "/tmp/prometheus_metrics.txt",
                 collection_interval: int = 5,
                 enable_ai_diagnostics: bool = True):
        
        self.logger = logging.getLogger(__name__)
        
        # Initialize monitoring components
        self.system_monitor = SystemMonitor(collection_interval=collection_interval)
        self.performance_tracker = AgentPerformanceTracker()
        self.prometheus_metrics = PrometheusMetrics(export_path=metrics_export_path)
        
        # Initialize AI-powered components
        self.ai_diagnostics = AISystemDiagnostics() if enable_ai_diagnostics else None
        self.predictive_maintenance = PredictiveMaintenanceEngine()
        
        # Initialize automated reporting
        self.automated_reporting = AutomatedReportingEngine(
            ai_diagnostics=self.ai_diagnostics,
            predictive_maintenance=self.predictive_maintenance
        ) if self.ai_diagnostics else None
        
        # Initialize dashboard
        self.health_dashboard = HealthDashboard(
            system_monitor=self.system_monitor,
            performance_tracker=self.performance_tracker,
            prometheus_metrics=self.prometheus_metrics,
            port=dashboard_port
        )
        
        self.is_running = False
        self.enable_ai_diagnostics = enable_ai_diagnostics
        self.logger.info(f"Monitoring Agent initialized (AI diagnostics: {'enabled' if enable_ai_diagnostics else 'disabled'})")
        
    def start_monitoring(self):
        """Start all monitoring components"""
        if self.is_running:
            self.logger.warning("Monitoring already started")
            return
            
        self.logger.info("Starting comprehensive system monitoring...")
        
        try:
            # Start system monitoring
            self.system_monitor.start_monitoring()
            
            # Start Prometheus metrics auto-export
            self.prometheus_metrics.start_auto_export(interval_seconds=60)
            
            # Start health dashboard
            dashboard_thread = threading.Thread(
                target=self.health_dashboard.start_dashboard, 
                daemon=True
            )
            dashboard_thread.start()
            
            self.is_running = True
            self.logger.info("All monitoring components started successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to start monitoring: {e}")
            self.stop_monitoring()
            raise
            
    def stop_monitoring(self):
        """Stop all monitoring components"""
        if not self.is_running:
            return
            
        self.logger.info("Stopping monitoring components...")
        
        try:
            self.system_monitor.stop_monitoring()
            self.health_dashboard.stop_dashboard()
            self.is_running = False
            self.logger.info("Monitoring stopped successfully")
            
        except Exception as e:
            self.logger.error(f"Error stopping monitoring: {e}")
            
    def track_agent_execution(self, agent_id: str, task_id: str) -> str:
        """Start tracking an agent execution"""
        return self.performance_tracker.start_execution(agent_id, task_id)
        
    def complete_agent_execution(self, execution_key: str, status: AgentStatus, 
                                error_message: Optional[str] = None,
                                memory_peak_mb: Optional[float] = None,
                                cpu_avg_percent: Optional[float] = None,
                                result_size_bytes: Optional[int] = None):
        """Complete tracking an agent execution"""
        self.performance_tracker.end_execution(
            execution_key, status, error_message, 
            memory_peak_mb, cpu_avg_percent, result_size_bytes
        )
        
    def record_api_request(self, endpoint: str, method: str, status_code: int, duration: float):
        """Record API request metrics"""
        self.prometheus_metrics.record_api_request(endpoint, method, status_code, duration)
        
    def record_deal_processing(self, status: str, duration: Optional[float] = None):
        """Record deal processing metrics"""
        self.prometheus_metrics.record_deal_processing(status, duration)
        
    def get_system_health(self) -> Dict[str, Any]:
        """Get comprehensive system health status"""
        return self.health_dashboard.get_health_status()
        
    def get_system_metrics(self) -> Dict[str, Any]:
        """Get detailed system metrics"""
        return self.health_dashboard.get_system_metrics()
        
    def get_agent_performance(self) -> Dict[str, Any]:
        """Get agent performance metrics"""
        return self.health_dashboard.get_agent_metrics()
        
    def get_active_alerts(self) -> Dict[str, Any]:
        """Get active system alerts"""
        return self.health_dashboard.get_active_alerts()
        
    def identify_bottlenecks(self) -> Dict[str, Any]:
        """Identify system and agent bottlenecks"""
        system_bottlenecks = []
        
        # Get system anomalies
        system_anomalies = self.system_monitor.detect_anomalies()
        system_bottlenecks.extend(system_anomalies)
        
        # Get agent bottlenecks
        agent_bottlenecks = self.performance_tracker.identify_bottlenecks()
        
        return {
            "timestamp": datetime.now().isoformat(),
            "system_bottlenecks": system_bottlenecks,
            "agent_bottlenecks": agent_bottlenecks,
            "total_bottlenecks": len(system_bottlenecks) + len(agent_bottlenecks),
            "recommendations": self._generate_bottleneck_recommendations(
                system_bottlenecks, agent_bottlenecks
            )
        }
        
    def _generate_bottleneck_recommendations(self, system_bottlenecks: list, 
                                           agent_bottlenecks: list) -> list:
        """Generate recommendations for addressing bottlenecks"""
        recommendations = []
        
        # System recommendations
        for bottleneck in system_bottlenecks:
            if bottleneck["type"] == "cpu_spike":
                recommendations.append({
                    "type": "system",
                    "priority": "high",
                    "recommendation": "Consider scaling CPU resources or optimizing CPU-intensive processes",
                    "details": f"CPU usage: {bottleneck['current_value']:.1f}%"
                })
            elif bottleneck["type"] == "memory_spike":
                recommendations.append({
                    "type": "system", 
                    "priority": "high",
                    "recommendation": "Consider increasing memory allocation or optimizing memory usage",
                    "details": f"Memory usage: {bottleneck['current_value']:.1f}%"
                })
                
        # Agent recommendations
        for bottleneck in agent_bottlenecks:
            if bottleneck["type"] == "low_success_rate":
                recommendations.append({
                    "type": "agent",
                    "priority": "high",
                    "recommendation": f"Investigate {bottleneck['agent_name']} failures and improve error handling",
                    "details": f"Success rate: {bottleneck['value']:.1f}%"
                })
            elif bottleneck["type"] == "slow_execution":
                recommendations.append({
                    "type": "agent",
                    "priority": "medium", 
                    "recommendation": f"Optimize {bottleneck['agent_name']} performance or consider parallel processing",
                    "details": f"Average duration: {bottleneck['value']:.1f}s"
                })
            elif bottleneck["type"] == "high_memory_usage":
                recommendations.append({
                    "type": "agent",
                    "priority": "medium",
                    "recommendation": f"Optimize {bottleneck['agent_name']} memory usage or implement memory cleanup",
                    "details": f"Memory usage: {bottleneck['value']:.1f}MB"
                })
                
        return recommendations
        
    def export_monitoring_data(self, filepath: str):
        """Export comprehensive monitoring data"""
        monitoring_data = {
            "timestamp": datetime.now().isoformat(),
            "system_health": self.get_system_health(),
            "system_metrics": self.get_system_metrics(),
            "agent_performance": self.get_agent_performance(),
            "active_alerts": self.get_active_alerts(),
            "bottlenecks": self.identify_bottlenecks(),
            "prometheus_metrics": self.prometheus_metrics.get_metrics_summary()
        }
        
        import json
        with open(filepath, 'w') as f:
            json.dump(monitoring_data, f, indent=2)
            
        self.logger.info(f"Exported monitoring data to {filepath}")
        
    def get_monitoring_summary(self) -> Dict[str, Any]:
        """Get a comprehensive monitoring summary"""
        health_status = self.get_system_health()
        bottlenecks = self.identify_bottlenecks()
        
        return {
            "timestamp": datetime.now().isoformat(),
            "overall_health": {
                "status": health_status["status"],
                "score": health_status["score"],
                "message": health_status["message"]
            },
            "system_status": {
                "cpu_usage": health_status.get("details", {}).get("system_cpu", 0),
                "memory_usage": health_status.get("details", {}).get("system_memory", 0),
                "disk_usage": health_status.get("details", {}).get("system_disk", 0)
            },
            "agent_status": {
                "success_rate": health_status.get("details", {}).get("agent_success_rate", 0),
                "active_agents": health_status.get("details", {}).get("active_agents", 0),
                "active_executions": health_status.get("details", {}).get("active_executions", 0)
            },
            "bottlenecks": {
                "total_count": bottlenecks["total_bottlenecks"],
                "system_count": len(bottlenecks["system_bottlenecks"]),
                "agent_count": len(bottlenecks["agent_bottlenecks"]),
                "recommendations_count": len(bottlenecks["recommendations"])
            },
            "monitoring_status": {
                "is_running": self.is_running,
                "ai_diagnostics_enabled": self.enable_ai_diagnostics,
                "components": {
                    "system_monitor": self.system_monitor.is_monitoring,
                    "performance_tracker": True,  # Always active
                    "prometheus_metrics": True,   # Always active
                    "health_dashboard": self.health_dashboard.is_running,
                    "ai_diagnostics": self.ai_diagnostics is not None,
                    "predictive_maintenance": True,
                    "automated_reporting": self.automated_reporting is not None
                }
            }
        }
        
    # AI-Powered Diagnostics Methods
    
    async def run_ai_diagnostics(self) -> Dict[str, Any]:
        """Run comprehensive AI-powered system diagnostics"""
        if not self.ai_diagnostics:
            return {"error": "AI diagnostics not enabled"}
            
        try:
            # Collect comprehensive system data
            system_data = {
                "system_metrics": self.get_system_metrics(),
                "agent_performance": self.get_agent_performance(),
                "alerts": self.get_active_alerts(),
                "bottlenecks": self.identify_bottlenecks(),
                "recent_errors": self._get_recent_errors()
            }
            
            # Run AI diagnosis
            diagnosis = await self.ai_diagnostics.diagnose_system_issues(system_data)
            
            return {
                "timestamp": datetime.now().isoformat(),
                "ai_diagnosis": diagnosis,
                "system_data_summary": {
                    "metrics_collected": len(system_data),
                    "alerts_analyzed": len(system_data.get("alerts", {}).get("alerts", [])),
                    "bottlenecks_identified": system_data.get("bottlenecks", {}).get("total_bottlenecks", 0)
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error running AI diagnostics: {e}")
            return {"error": f"AI diagnostics failed: {str(e)}"}
            
    async def analyze_error_patterns(self) -> Dict[str, Any]:
        """Analyze error patterns using AI"""
        if not self.ai_diagnostics:
            return {"error": "AI diagnostics not enabled"}
            
        try:
            # Get recent error data
            error_logs = self._get_recent_errors()
            
            if not error_logs:
                return {"message": "No recent errors to analyze"}
                
            # Run AI error analysis
            analysis = await self.ai_diagnostics.analyze_error_logs(error_logs)
            
            return {
                "timestamp": datetime.now().isoformat(),
                "error_analysis": analysis,
                "errors_analyzed": len(error_logs)
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing error patterns: {e}")
            return {"error": f"Error pattern analysis failed: {str(e)}"}
            
    async def predict_maintenance_needs(self, forecast_days: int = 90) -> Dict[str, Any]:
        """Predict system maintenance needs"""
        try:
            # Feed current data to predictive maintenance engine
            current_metrics = self.get_system_metrics()
            current_performance = self.get_agent_performance()
            
            self.predictive_maintenance.add_metrics_data(current_metrics)
            self.predictive_maintenance.add_performance_data(current_performance)
            
            # Get maintenance predictions
            maintenance_alerts = self.predictive_maintenance.predict_maintenance_needs(forecast_days)
            maintenance_schedule = self.predictive_maintenance.get_maintenance_schedule(forecast_days)
            
            # Get AI insights if available
            ai_prediction = None
            if self.ai_diagnostics:
                historical_data = {
                    "metrics_history": current_metrics,
                    "performance_trends": current_performance,
                    "system_age_days": 30  # Placeholder
                }
                ai_prediction = await self.ai_diagnostics.predict_system_maintenance(historical_data)
            
            return {
                "timestamp": datetime.now().isoformat(),
                "forecast_period_days": forecast_days,
                "maintenance_alerts": [
                    {
                        "alert_id": alert.alert_id,
                        "component": alert.component,
                        "severity": alert.severity,
                        "predicted_failure_date": alert.predicted_failure_date.isoformat(),
                        "confidence": alert.confidence,
                        "description": alert.description,
                        "recommended_actions": alert.recommended_actions,
                        "estimated_downtime": alert.estimated_downtime,
                        "estimated_cost": alert.estimated_cost
                    }
                    for alert in maintenance_alerts
                ],
                "maintenance_schedule": maintenance_schedule,
                "ai_prediction": ai_prediction
            }
            
        except Exception as e:
            self.logger.error(f"Error predicting maintenance needs: {e}")
            return {"error": f"Maintenance prediction failed: {str(e)}"}
            
    async def optimize_system_performance(self) -> Dict[str, Any]:
        """Get AI-powered system performance optimization recommendations"""
        if not self.ai_diagnostics:
            return {"error": "AI diagnostics not enabled"}
            
        try:
            # Collect performance data
            performance_data = {
                "current_metrics": self.get_system_metrics(),
                "bottlenecks": self.identify_bottlenecks(),
                "resource_usage": self.get_system_metrics(),
                "agent_metrics": self.get_agent_performance()
            }
            
            # Get AI optimization recommendations
            optimization = await self.ai_diagnostics.optimize_system_performance(performance_data)
            
            return {
                "timestamp": datetime.now().isoformat(),
                "optimization_analysis": optimization,
                "current_performance_summary": {
                    "system_health_score": self.get_system_health().get("score", 0),
                    "bottlenecks_count": performance_data["bottlenecks"].get("total_bottlenecks", 0)
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error optimizing system performance: {e}")
            return {"error": f"Performance optimization failed: {str(e)}"}
            
    async def generate_health_report(self, report_type: str = "daily") -> Dict[str, Any]:
        """Generate comprehensive AI-powered health report"""
        if not self.automated_reporting:
            return {"error": "Automated reporting not enabled"}
            
        try:
            # Generate comprehensive health report
            report = await self.automated_reporting.generate_health_report(report_type)
            
            return {
                "timestamp": datetime.now().isoformat(),
                "report_generated": True,
                "report_id": report.report_id,
                "report_type": report.report_type,
                "health_score": report.overall_health_score,
                "executive_summary": report.executive_summary,
                "sections_count": len(report.sections),
                "recommendations_count": len(report.recommendations),
                "ai_insights_available": bool(report.ai_insights)
            }
            
        except Exception as e:
            self.logger.error(f"Error generating health report: {e}")
            return {"error": f"Health report generation failed: {str(e)}"}
            
    def _get_recent_errors(self) -> List[Dict[str, Any]]:
        """Get recent error data for analysis"""
        # This would typically collect from system logs
        # For now, return placeholder error data
        return [
            {
                "timestamp": datetime.now().isoformat(),
                "error_type": "connection_timeout",
                "message": "Connection timeout to external API",
                "component": "api_client",
                "severity": "warning"
            },
            {
                "timestamp": datetime.now().isoformat(),
                "error_type": "memory_allocation",
                "message": "Failed to allocate memory for large dataset",
                "component": "data_processor",
                "severity": "error"
            }
        ]
        
    def get_ai_diagnostics_status(self) -> Dict[str, Any]:
        """Get status of AI diagnostics components"""
        return {
            "timestamp": datetime.now().isoformat(),
            "ai_diagnostics_enabled": self.enable_ai_diagnostics,
            "components_status": {
                "ai_diagnostics": {
                    "available": self.ai_diagnostics is not None,
                    "client_initialized": self.ai_diagnostics.client is not None if self.ai_diagnostics else False
                },
                "predictive_maintenance": {
                    "available": True,
                    "metrics_history_size": len(self.predictive_maintenance.metrics_history),
                    "performance_history_size": len(self.predictive_maintenance.performance_history)
                },
                "automated_reporting": {
                    "available": self.automated_reporting is not None,
                    "report_storage_path": self.automated_reporting.report_storage_path if self.automated_reporting else None
                }
            },
            "capabilities": {
                "system_diagnosis": self.ai_diagnostics is not None,
                "error_pattern_analysis": self.ai_diagnostics is not None,
                "maintenance_prediction": True,
                "performance_optimization": self.ai_diagnostics is not None,
                "automated_reporting": self.automated_reporting is not None
            }
        }