"""
Prometheus Metrics Collector for M&A Analysis System

This module provides Prometheus-compatible metrics collection without requiring
the full Prometheus server installation. It creates metrics in Prometheus format
that can be scraped by Prometheus or viewed directly.
"""

import time
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import threading
from collections import defaultdict
import os

@dataclass
class PrometheusMetric:
    """Prometheus metric definition"""
    name: str
    metric_type: str  # counter, gauge, histogram, summary
    help_text: str
    labels: Dict[str, str]
    value: float
    timestamp: Optional[float] = None

class PrometheusMetrics:
    """
    Prometheus-compatible metrics collector for the M&A analysis system
    """
    
    def __init__(self, metrics_port: int = 8000, export_path: str = "/tmp/prometheus_metrics.txt"):
        self.metrics_port = metrics_port
        self.export_path = export_path
        self.metrics: Dict[str, PrometheusMetric] = {}
        self.lock = threading.Lock()
        self.logger = logging.getLogger(__name__)
        
        # Initialize system metrics
        self._initialize_metrics()
        
    def _initialize_metrics(self):
        """Initialize standard metrics for the M&A system"""
        
        # System metrics
        self.register_metric(
            "system_cpu_usage_percent",
            "gauge",
            "Current CPU usage percentage",
            {}
        )
        
        self.register_metric(
            "system_memory_usage_percent", 
            "gauge",
            "Current memory usage percentage",
            {}
        )
        
        self.register_metric(
            "system_disk_usage_percent",
            "gauge", 
            "Current disk usage percentage",
            {}
        )
        
        # Agent metrics
        self.register_metric(
            "agent_executions_total",
            "counter",
            "Total number of agent executions",
            {"agent_id": "", "status": ""}
        )
        
        self.register_metric(
            "agent_execution_duration_seconds",
            "histogram",
            "Agent execution duration in seconds",
            {"agent_id": ""}
        )
        
        self.register_metric(
            "agent_memory_usage_bytes",
            "gauge",
            "Agent memory usage in bytes",
            {"agent_id": ""}
        )
        
        self.register_metric(
            "agent_success_rate",
            "gauge",
            "Agent success rate percentage",
            {"agent_id": ""}
        )
        
        # Deal processing metrics
        self.register_metric(
            "deals_processed_total",
            "counter",
            "Total number of deals processed",
            {"status": ""}
        )
        
        self.register_metric(
            "deal_processing_duration_seconds",
            "histogram",
            "Deal processing duration in seconds",
            {}
        )
        
        # API metrics
        self.register_metric(
            "api_requests_total",
            "counter",
            "Total API requests",
            {"endpoint": "", "method": "", "status": ""}
        )
        
        self.register_metric(
            "api_request_duration_seconds",
            "histogram",
            "API request duration in seconds",
            {"endpoint": "", "method": ""}
        )
        
    def register_metric(self, name: str, metric_type: str, help_text: str, labels: Dict[str, str]):
        """Register a new metric"""
        with self.lock:
            self.metrics[name] = PrometheusMetric(
                name=name,
                metric_type=metric_type,
                help_text=help_text,
                labels=labels,
                value=0.0
            )
            
    def set_gauge(self, name: str, value: float, labels: Optional[Dict[str, str]] = None):
        """Set a gauge metric value"""
        with self.lock:
            metric_key = self._get_metric_key(name, labels)
            if name in self.metrics:
                metric = self.metrics[name]
                if metric.metric_type != "gauge":
                    self.logger.warning(f"Metric {name} is not a gauge")
                    return
                    
                # Create new metric instance with labels
                self.metrics[metric_key] = PrometheusMetric(
                    name=name,
                    metric_type=metric.metric_type,
                    help_text=metric.help_text,
                    labels=labels or {},
                    value=value,
                    timestamp=time.time()
                )
            else:
                self.logger.warning(f"Metric {name} not registered")
                
    def increment_counter(self, name: str, value: float = 1.0, labels: Optional[Dict[str, str]] = None):
        """Increment a counter metric"""
        with self.lock:
            metric_key = self._get_metric_key(name, labels)
            if name in self.metrics:
                metric = self.metrics[name]
                if metric.metric_type != "counter":
                    self.logger.warning(f"Metric {name} is not a counter")
                    return
                    
                # Get existing value or create new
                if metric_key in self.metrics:
                    current_value = self.metrics[metric_key].value
                else:
                    current_value = 0.0
                    
                self.metrics[metric_key] = PrometheusMetric(
                    name=name,
                    metric_type=metric.metric_type,
                    help_text=metric.help_text,
                    labels=labels or {},
                    value=current_value + value,
                    timestamp=time.time()
                )
            else:
                self.logger.warning(f"Metric {name} not registered")
                
    def observe_histogram(self, name: str, value: float, labels: Optional[Dict[str, str]] = None):
        """Observe a value for a histogram metric (simplified implementation)"""
        with self.lock:
            metric_key = self._get_metric_key(name, labels)
            if name in self.metrics:
                metric = self.metrics[name]
                if metric.metric_type != "histogram":
                    self.logger.warning(f"Metric {name} is not a histogram")
                    return
                    
                # For simplicity, we'll store the latest value
                # In a full implementation, this would maintain buckets
                self.metrics[metric_key] = PrometheusMetric(
                    name=name,
                    metric_type=metric.metric_type,
                    help_text=metric.help_text,
                    labels=labels or {},
                    value=value,
                    timestamp=time.time()
                )
            else:
                self.logger.warning(f"Metric {name} not registered")
                
    def _get_metric_key(self, name: str, labels: Optional[Dict[str, str]]) -> str:
        """Generate a unique key for metric with labels"""
        if not labels:
            return name
        label_str = ",".join(f"{k}={v}" for k, v in sorted(labels.items()))
        return f"{name}{{{label_str}}}"
        
    def update_system_metrics(self, system_metrics):
        """Update system metrics from SystemMonitor"""
        self.set_gauge("system_cpu_usage_percent", system_metrics.cpu_percent)
        self.set_gauge("system_memory_usage_percent", system_metrics.memory_percent)
        self.set_gauge("system_disk_usage_percent", system_metrics.disk_usage_percent)
        
    def update_agent_metrics(self, agent_id: str, performance_metrics):
        """Update agent metrics from AgentPerformanceTracker"""
        labels = {"agent_id": agent_id}
        
        self.set_gauge("agent_success_rate", performance_metrics.success_rate, labels)
        self.set_gauge("agent_memory_usage_bytes", performance_metrics.avg_memory_mb * 1024 * 1024, labels)
        
        # Update counters
        self.increment_counter("agent_executions_total", 
                             performance_metrics.successful_executions, 
                             {**labels, "status": "success"})
        self.increment_counter("agent_executions_total", 
                             performance_metrics.failed_executions,
                             {**labels, "status": "failed"})
                             
        # Update histogram
        self.observe_histogram("agent_execution_duration_seconds", 
                             performance_metrics.avg_duration_seconds, labels)
                             
    def record_api_request(self, endpoint: str, method: str, status_code: int, duration: float):
        """Record API request metrics"""
        labels = {"endpoint": endpoint, "method": method, "status": str(status_code)}
        self.increment_counter("api_requests_total", 1.0, labels)
        
        duration_labels = {"endpoint": endpoint, "method": method}
        self.observe_histogram("api_request_duration_seconds", duration, duration_labels)
        
    def record_deal_processing(self, status: str, duration: Optional[float] = None):
        """Record deal processing metrics"""
        self.increment_counter("deals_processed_total", 1.0, {"status": status})
        
        if duration is not None:
            self.observe_histogram("deal_processing_duration_seconds", duration)
            
    def export_prometheus_format(self) -> str:
        """Export metrics in Prometheus text format"""
        with self.lock:
            lines = []
            
            # Group metrics by name
            metrics_by_name = defaultdict(list)
            for metric_key, metric in self.metrics.items():
                metrics_by_name[metric.name].append((metric_key, metric))
                
            for metric_name, metric_list in metrics_by_name.items():
                # Get the first metric for help and type
                first_metric = metric_list[0][1]
                
                # Add help and type comments
                lines.append(f"# HELP {metric_name} {first_metric.help_text}")
                lines.append(f"# TYPE {metric_name} {first_metric.metric_type}")
                
                # Add metric values
                for metric_key, metric in metric_list:
                    if metric.labels:
                        label_str = ",".join(f'{k}="{v}"' for k, v in metric.labels.items())
                        lines.append(f"{metric_name}{{{label_str}}} {metric.value}")
                    else:
                        lines.append(f"{metric_name} {metric.value}")
                        
                lines.append("")  # Empty line between metrics
                
            return "\n".join(lines)
            
    def export_to_file(self, filepath: Optional[str] = None):
        """Export metrics to file in Prometheus format"""
        filepath = filepath or self.export_path
        
        try:
            prometheus_text = self.export_prometheus_format()
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            with open(filepath, 'w') as f:
                f.write(prometheus_text)
                
            self.logger.info(f"Exported Prometheus metrics to {filepath}")
            
        except Exception as e:
            self.logger.error(f"Failed to export metrics: {e}")
            
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get a summary of current metrics"""
        with self.lock:
            summary = {
                "timestamp": datetime.now().isoformat(),
                "total_metrics": len(self.metrics),
                "metrics_by_type": defaultdict(int),
                "sample_metrics": {}
            }
            
            for metric in self.metrics.values():
                summary["metrics_by_type"][metric.metric_type] += 1
                
            # Add some sample metrics
            for name in ["system_cpu_usage_percent", "system_memory_usage_percent", 
                        "agent_success_rate"]:
                if name in self.metrics:
                    summary["sample_metrics"][name] = self.metrics[name].value
                    
            return summary
            
    def start_auto_export(self, interval_seconds: int = 60):
        """Start automatic export of metrics to file"""
        def export_loop():
            while True:
                try:
                    self.export_to_file()
                    time.sleep(interval_seconds)
                except Exception as e:
                    self.logger.error(f"Error in auto-export loop: {e}")
                    time.sleep(interval_seconds)
                    
        export_thread = threading.Thread(target=export_loop, daemon=True)
        export_thread.start()
        self.logger.info(f"Started auto-export with {interval_seconds}s interval")
        
    def clear_metrics(self):
        """Clear all metric values (keep definitions)"""
        with self.lock:
            for metric in self.metrics.values():
                metric.value = 0.0
                metric.timestamp = None
            self.logger.info("Cleared all metric values")