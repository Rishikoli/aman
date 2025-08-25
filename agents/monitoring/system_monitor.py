"""
System Monitor using psutil for comprehensive system resource monitoring
"""

import psutil
import time
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import threading
from collections import deque

@dataclass
class SystemMetrics:
    """System metrics data structure"""
    timestamp: datetime
    cpu_percent: float
    memory_percent: float
    memory_available: int
    memory_used: int
    disk_usage_percent: float
    disk_free: int
    disk_used: int
    network_bytes_sent: int
    network_bytes_recv: int
    process_count: int
    load_average: Optional[List[float]] = None

@dataclass
class ProcessMetrics:
    """Process-specific metrics"""
    pid: int
    name: str
    cpu_percent: float
    memory_percent: float
    memory_rss: int
    status: str
    create_time: float
    num_threads: int

class SystemMonitor:
    """
    Comprehensive system monitoring using psutil
    """
    
    def __init__(self, collection_interval: int = 5, history_size: int = 1000):
        self.collection_interval = collection_interval
        self.history_size = history_size
        self.metrics_history = deque(maxlen=history_size)
        self.process_metrics = {}
        self.is_monitoring = False
        self.monitor_thread = None
        self.logger = logging.getLogger(__name__)
        
        # Initialize network counters for delta calculations
        self._last_network_stats = psutil.net_io_counters()
        self._last_network_time = time.time()
        
    def start_monitoring(self):
        """Start continuous system monitoring"""
        if self.is_monitoring:
            self.logger.warning("Monitoring already started")
            return
            
        self.is_monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitor_thread.start()
        self.logger.info(f"System monitoring started with {self.collection_interval}s interval")
        
    def stop_monitoring(self):
        """Stop system monitoring"""
        self.is_monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=10)
        self.logger.info("System monitoring stopped")
        
    def _monitoring_loop(self):
        """Main monitoring loop"""
        while self.is_monitoring:
            try:
                metrics = self.collect_system_metrics()
                self.metrics_history.append(metrics)
                time.sleep(self.collection_interval)
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                time.sleep(self.collection_interval)
                
    def collect_system_metrics(self) -> SystemMetrics:
        """Collect current system metrics"""
        # CPU metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        
        # Memory metrics
        memory = psutil.virtual_memory()
        
        # Disk metrics (root partition)
        disk = psutil.disk_usage('/')
        
        # Network metrics
        current_network = psutil.net_io_counters()
        current_time = time.time()
        
        # Calculate network rates
        time_delta = current_time - self._last_network_time
        bytes_sent_rate = (current_network.bytes_sent - self._last_network_stats.bytes_sent) / time_delta if time_delta > 0 else 0
        bytes_recv_rate = (current_network.bytes_recv - self._last_network_stats.bytes_recv) / time_delta if time_delta > 0 else 0
        
        self._last_network_stats = current_network
        self._last_network_time = current_time
        
        # Process count
        process_count = len(psutil.pids())
        
        # Load average (Unix-like systems only)
        load_avg = None
        try:
            load_avg = list(psutil.getloadavg())
        except AttributeError:
            # Windows doesn't have load average
            pass
            
        return SystemMetrics(
            timestamp=datetime.now(),
            cpu_percent=cpu_percent,
            memory_percent=memory.percent,
            memory_available=memory.available,
            memory_used=memory.used,
            disk_usage_percent=disk.percent,
            disk_free=disk.free,
            disk_used=disk.used,
            network_bytes_sent=int(bytes_sent_rate),
            network_bytes_recv=int(bytes_recv_rate),
            process_count=process_count,
            load_average=load_avg
        )
        
    def get_process_metrics(self, process_name_filter: Optional[str] = None) -> List[ProcessMetrics]:
        """Get metrics for all processes or filtered by name"""
        processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 
                                       'memory_info', 'status', 'create_time', 'num_threads']):
            try:
                pinfo = proc.info
                if process_name_filter and process_name_filter.lower() not in pinfo['name'].lower():
                    continue
                    
                processes.append(ProcessMetrics(
                    pid=pinfo['pid'],
                    name=pinfo['name'],
                    cpu_percent=pinfo['cpu_percent'] or 0.0,
                    memory_percent=pinfo['memory_percent'] or 0.0,
                    memory_rss=pinfo['memory_info'].rss if pinfo['memory_info'] else 0,
                    status=pinfo['status'],
                    create_time=pinfo['create_time'],
                    num_threads=pinfo['num_threads'] or 0
                ))
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                # Process disappeared or access denied
                continue
                
        return sorted(processes, key=lambda x: x.cpu_percent, reverse=True)
        
    def get_current_metrics(self) -> SystemMetrics:
        """Get current system metrics without storing in history"""
        return self.collect_system_metrics()
        
    def get_metrics_history(self, minutes: int = 60) -> List[SystemMetrics]:
        """Get metrics history for the last N minutes"""
        cutoff_time = datetime.now() - timedelta(minutes=minutes)
        return [m for m in self.metrics_history if m.timestamp >= cutoff_time]
        
    def get_system_health_summary(self) -> Dict[str, Any]:
        """Get comprehensive system health summary"""
        current = self.get_current_metrics()
        recent_history = self.get_metrics_history(minutes=10)
        
        if not recent_history:
            recent_history = [current]
            
        # Calculate averages
        avg_cpu = sum(m.cpu_percent for m in recent_history) / len(recent_history)
        avg_memory = sum(m.memory_percent for m in recent_history) / len(recent_history)
        avg_disk = sum(m.disk_usage_percent for m in recent_history) / len(recent_history)
        
        # Identify bottlenecks
        bottlenecks = []
        if avg_cpu > 80:
            bottlenecks.append("High CPU usage")
        if avg_memory > 85:
            bottlenecks.append("High memory usage")
        if avg_disk > 90:
            bottlenecks.append("High disk usage")
            
        # Get top processes
        top_processes = self.get_process_metrics()[:5]
        
        return {
            "timestamp": current.timestamp.isoformat(),
            "current_metrics": asdict(current),
            "averages_10min": {
                "cpu_percent": round(avg_cpu, 2),
                "memory_percent": round(avg_memory, 2),
                "disk_usage_percent": round(avg_disk, 2)
            },
            "bottlenecks": bottlenecks,
            "top_processes": [asdict(p) for p in top_processes],
            "health_status": "healthy" if not bottlenecks else "warning" if len(bottlenecks) < 2 else "critical"
        }
        
    def detect_anomalies(self, threshold_multiplier: float = 2.0) -> List[Dict[str, Any]]:
        """Detect system anomalies based on historical data"""
        if len(self.metrics_history) < 10:
            return []
            
        recent_metrics = list(self.metrics_history)[-10:]
        historical_metrics = list(self.metrics_history)[:-10] if len(self.metrics_history) > 10 else []
        
        if not historical_metrics:
            return []
            
        anomalies = []
        
        # Calculate historical averages
        hist_avg_cpu = sum(m.cpu_percent for m in historical_metrics) / len(historical_metrics)
        hist_avg_memory = sum(m.memory_percent for m in historical_metrics) / len(historical_metrics)
        
        # Calculate recent averages
        recent_avg_cpu = sum(m.cpu_percent for m in recent_metrics) / len(recent_metrics)
        recent_avg_memory = sum(m.memory_percent for m in recent_metrics) / len(recent_metrics)
        
        # Detect CPU anomalies
        if recent_avg_cpu > hist_avg_cpu * threshold_multiplier:
            anomalies.append({
                "type": "cpu_spike",
                "severity": "high" if recent_avg_cpu > 90 else "medium",
                "current_value": recent_avg_cpu,
                "historical_average": hist_avg_cpu,
                "description": f"CPU usage spike detected: {recent_avg_cpu:.1f}% vs historical {hist_avg_cpu:.1f}%"
            })
            
        # Detect memory anomalies
        if recent_avg_memory > hist_avg_memory * threshold_multiplier:
            anomalies.append({
                "type": "memory_spike",
                "severity": "high" if recent_avg_memory > 90 else "medium",
                "current_value": recent_avg_memory,
                "historical_average": hist_avg_memory,
                "description": f"Memory usage spike detected: {recent_avg_memory:.1f}% vs historical {hist_avg_memory:.1f}%"
            })
            
        return anomalies
        
    def export_metrics(self, filepath: str, format: str = "json"):
        """Export metrics history to file"""
        if format.lower() == "json":
            data = [asdict(m) for m in self.metrics_history]
            # Convert datetime to string for JSON serialization
            for item in data:
                item['timestamp'] = item['timestamp'].isoformat()
                
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
        else:
            raise ValueError(f"Unsupported format: {format}")
            
        self.logger.info(f"Exported {len(self.metrics_history)} metrics to {filepath}")