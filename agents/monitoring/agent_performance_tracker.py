"""
Agent Performance Tracker for monitoring M&A analysis agents
"""

import time
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from collections import defaultdict, deque
import threading
from enum import Enum

class AgentStatus(Enum):
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"

@dataclass
class AgentExecution:
    """Single agent execution record"""
    agent_id: str
    task_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    status: AgentStatus = AgentStatus.RUNNING
    duration_seconds: Optional[float] = None
    memory_peak_mb: Optional[float] = None
    cpu_avg_percent: Optional[float] = None
    error_message: Optional[str] = None
    result_size_bytes: Optional[int] = None
    
    def complete(self, status: AgentStatus, error_message: Optional[str] = None):
        """Mark execution as complete"""
        self.end_time = datetime.now()
        self.status = status
        self.duration_seconds = (self.end_time - self.start_time).total_seconds()
        self.error_message = error_message

@dataclass
class AgentPerformanceMetrics:
    """Performance metrics for an agent"""
    agent_id: str
    total_executions: int
    successful_executions: int
    failed_executions: int
    avg_duration_seconds: float
    min_duration_seconds: float
    max_duration_seconds: float
    avg_memory_mb: float
    avg_cpu_percent: float
    success_rate: float
    last_execution: Optional[datetime] = None
    current_status: AgentStatus = AgentStatus.IDLE

class AgentPerformanceTracker:
    """
    Tracks performance metrics for all M&A analysis agents
    """
    
    def __init__(self, history_size: int = 1000):
        self.history_size = history_size
        self.executions = deque(maxlen=history_size)
        self.active_executions: Dict[str, AgentExecution] = {}
        self.agent_metrics: Dict[str, AgentPerformanceMetrics] = {}
        self.lock = threading.Lock()
        self.logger = logging.getLogger(__name__)
        
        # Known M&A agents
        self.known_agents = {
            "finance_agent": "Financial Analysis Agent",
            "legal_agent": "Legal & Compliance Agent", 
            "synergy_agent": "Synergy Analysis Agent",
            "reputation_agent": "Reputation Analysis Agent",
            "operations_agent": "Operations Intelligence Agent",
            "orchestrator": "Deal Orchestrator"
        }
        
    def start_execution(self, agent_id: str, task_id: str) -> str:
        """Start tracking an agent execution"""
        execution_key = f"{agent_id}_{task_id}_{int(time.time())}"
        
        with self.lock:
            execution = AgentExecution(
                agent_id=agent_id,
                task_id=task_id,
                start_time=datetime.now()
            )
            
            self.active_executions[execution_key] = execution
            self.logger.info(f"Started tracking execution: {execution_key}")
            
        return execution_key
        
    def end_execution(self, execution_key: str, status: AgentStatus, 
                     error_message: Optional[str] = None,
                     memory_peak_mb: Optional[float] = None,
                     cpu_avg_percent: Optional[float] = None,
                     result_size_bytes: Optional[int] = None):
        """End tracking an agent execution"""
        with self.lock:
            if execution_key not in self.active_executions:
                self.logger.warning(f"Execution key not found: {execution_key}")
                return
                
            execution = self.active_executions[execution_key]
            execution.complete(status, error_message)
            execution.memory_peak_mb = memory_peak_mb
            execution.cpu_avg_percent = cpu_avg_percent
            execution.result_size_bytes = result_size_bytes
            
            # Move to history
            self.executions.append(execution)
            del self.active_executions[execution_key]
            
            # Update agent metrics
            self._update_agent_metrics(execution)
            
            self.logger.info(f"Completed tracking execution: {execution_key} - Status: {status.value}")
            
    def _update_agent_metrics(self, execution: AgentExecution):
        """Update performance metrics for an agent"""
        agent_id = execution.agent_id
        
        # Get all executions for this agent
        agent_executions = [e for e in self.executions if e.agent_id == agent_id]
        
        if not agent_executions:
            return
            
        # Calculate metrics
        total_executions = len(agent_executions)
        successful_executions = len([e for e in agent_executions if e.status == AgentStatus.COMPLETED])
        failed_executions = len([e for e in agent_executions if e.status == AgentStatus.FAILED])
        
        durations = [e.duration_seconds for e in agent_executions if e.duration_seconds is not None]
        memory_usage = [e.memory_peak_mb for e in agent_executions if e.memory_peak_mb is not None]
        cpu_usage = [e.cpu_avg_percent for e in agent_executions if e.cpu_avg_percent is not None]
        
        self.agent_metrics[agent_id] = AgentPerformanceMetrics(
            agent_id=agent_id,
            total_executions=total_executions,
            successful_executions=successful_executions,
            failed_executions=failed_executions,
            avg_duration_seconds=sum(durations) / len(durations) if durations else 0,
            min_duration_seconds=min(durations) if durations else 0,
            max_duration_seconds=max(durations) if durations else 0,
            avg_memory_mb=sum(memory_usage) / len(memory_usage) if memory_usage else 0,
            avg_cpu_percent=sum(cpu_usage) / len(cpu_usage) if cpu_usage else 0,
            success_rate=(successful_executions / total_executions * 100) if total_executions > 0 else 0,
            last_execution=max([e.start_time for e in agent_executions]),
            current_status=AgentStatus.IDLE  # Will be updated by active executions
        )
        
    def get_agent_metrics(self, agent_id: Optional[str] = None) -> Dict[str, AgentPerformanceMetrics]:
        """Get performance metrics for agents"""
        with self.lock:
            if agent_id:
                return {agent_id: self.agent_metrics.get(agent_id)} if agent_id in self.agent_metrics else {}
            return self.agent_metrics.copy()
            
    def get_active_executions(self) -> Dict[str, AgentExecution]:
        """Get currently active executions"""
        with self.lock:
            return self.active_executions.copy()
            
    def get_execution_history(self, agent_id: Optional[str] = None, 
                            hours: int = 24) -> List[AgentExecution]:
        """Get execution history for the last N hours"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        with self.lock:
            history = [e for e in self.executions if e.start_time >= cutoff_time]
            if agent_id:
                history = [e for e in history if e.agent_id == agent_id]
            return history
            
    def identify_bottlenecks(self) -> List[Dict[str, Any]]:
        """Identify performance bottlenecks across agents"""
        bottlenecks = []
        
        with self.lock:
            for agent_id, metrics in self.agent_metrics.items():
                agent_name = self.known_agents.get(agent_id, agent_id)
                
                # Check success rate
                if metrics.success_rate < 80 and metrics.total_executions >= 5:
                    bottlenecks.append({
                        "type": "low_success_rate",
                        "agent_id": agent_id,
                        "agent_name": agent_name,
                        "severity": "high" if metrics.success_rate < 50 else "medium",
                        "value": metrics.success_rate,
                        "description": f"{agent_name} has low success rate: {metrics.success_rate:.1f}%"
                    })
                    
                # Check average duration
                if metrics.avg_duration_seconds > 300:  # 5 minutes
                    bottlenecks.append({
                        "type": "slow_execution",
                        "agent_id": agent_id,
                        "agent_name": agent_name,
                        "severity": "high" if metrics.avg_duration_seconds > 600 else "medium",
                        "value": metrics.avg_duration_seconds,
                        "description": f"{agent_name} has slow average execution: {metrics.avg_duration_seconds:.1f}s"
                    })
                    
                # Check memory usage
                if metrics.avg_memory_mb > 1000:  # 1GB
                    bottlenecks.append({
                        "type": "high_memory_usage",
                        "agent_id": agent_id,
                        "agent_name": agent_name,
                        "severity": "high" if metrics.avg_memory_mb > 2000 else "medium",
                        "value": metrics.avg_memory_mb,
                        "description": f"{agent_name} has high memory usage: {metrics.avg_memory_mb:.1f}MB"
                    })
                    
        return bottlenecks
        
    def get_system_performance_summary(self) -> Dict[str, Any]:
        """Get comprehensive system performance summary"""
        with self.lock:
            active_count = len(self.active_executions)
            total_agents = len(self.agent_metrics)
            
            # Calculate overall metrics
            if self.agent_metrics:
                overall_success_rate = sum(m.success_rate for m in self.agent_metrics.values()) / len(self.agent_metrics)
                overall_avg_duration = sum(m.avg_duration_seconds for m in self.agent_metrics.values()) / len(self.agent_metrics)
            else:
                overall_success_rate = 0
                overall_avg_duration = 0
                
            # Get recent activity
            recent_executions = self.get_execution_history(hours=1)
            recent_failures = [e for e in recent_executions if e.status == AgentStatus.FAILED]
            
            # Identify bottlenecks
            bottlenecks = self.identify_bottlenecks()
            
            return {
                "timestamp": datetime.now().isoformat(),
                "active_executions": active_count,
                "total_agents": total_agents,
                "overall_success_rate": round(overall_success_rate, 2),
                "overall_avg_duration_seconds": round(overall_avg_duration, 2),
                "recent_executions_1h": len(recent_executions),
                "recent_failures_1h": len(recent_failures),
                "bottlenecks": bottlenecks,
                "agent_status": {
                    agent_id: {
                        "name": self.known_agents.get(agent_id, agent_id),
                        "success_rate": metrics.success_rate,
                        "avg_duration": metrics.avg_duration_seconds,
                        "last_execution": metrics.last_execution.isoformat() if metrics.last_execution else None
                    }
                    for agent_id, metrics in self.agent_metrics.items()
                }
            }
            
    def export_performance_data(self, filepath: str):
        """Export performance data to JSON file"""
        with self.lock:
            data = {
                "timestamp": datetime.now().isoformat(),
                "agent_metrics": {
                    agent_id: asdict(metrics) 
                    for agent_id, metrics in self.agent_metrics.items()
                },
                "execution_history": [
                    {
                        **asdict(execution),
                        "start_time": execution.start_time.isoformat(),
                        "end_time": execution.end_time.isoformat() if execution.end_time else None,
                        "status": execution.status.value
                    }
                    for execution in self.executions
                ]
            }
            
            # Convert datetime fields for JSON serialization
            for agent_data in data["agent_metrics"].values():
                if agent_data["last_execution"]:
                    agent_data["last_execution"] = agent_data["last_execution"].isoformat()
                agent_data["current_status"] = agent_data["current_status"].value
                
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
            
        self.logger.info(f"Exported performance data to {filepath}")
        
    def reset_metrics(self):
        """Reset all performance metrics and history"""
        with self.lock:
            self.executions.clear()
            self.active_executions.clear()
            self.agent_metrics.clear()
            self.logger.info("Reset all performance metrics")