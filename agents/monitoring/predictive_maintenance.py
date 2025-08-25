"""
Predictive Maintenance Engine for M&A Analysis System

This module provides predictive maintenance capabilities using historical data
analysis and machine learning techniques to forecast system maintenance needs.
"""

import logging
import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from collections import deque
import statistics

try:
    import numpy as np
except ImportError:
    # Fallback for systems without numpy
    class MockNumpy:
        @staticmethod
        def array(data):
            return data
        @staticmethod
        def sum(data):
            return sum(data)
        @staticmethod
        def mean(data):
            return sum(data) / len(data) if data else 0
        @staticmethod
        def sqrt(data):
            return [x**0.5 for x in data]
    np = MockNumpy()

logger = logging.getLogger(__name__)

@dataclass
class MaintenanceAlert:
    """Maintenance alert data structure"""
    alert_id: str
    component: str
    severity: str  # low, medium, high, critical
    predicted_failure_date: datetime
    confidence: float
    description: str
    recommended_actions: List[str]
    estimated_downtime: float  # hours
    estimated_cost: float

@dataclass
class PerformanceTrend:
    """Performance trend analysis"""
    metric_name: str
    trend_direction: str  # improving, stable, degrading
    trend_strength: float  # 0.0 to 1.0
    current_value: float
    predicted_value: float
    prediction_date: datetime
    confidence: float

class PredictiveMaintenanceEngine:
    """
    Predictive maintenance engine using statistical analysis and trend detection
    """
    
    def __init__(self, history_size: int = 10000):
        self.history_size = history_size
        self.metrics_history = deque(maxlen=history_size)
        self.performance_history = deque(maxlen=history_size)
        self.error_history = deque(maxlen=history_size)
        self.maintenance_alerts = []
        self.logger = logging.getLogger(__name__)
        
        # Thresholds for predictive analysis
        self.thresholds = {
            'cpu_degradation': 0.8,  # 80% sustained usage
            'memory_growth_rate': 0.05,  # 5% growth per day
            'disk_growth_rate': 0.02,  # 2% growth per day
            'error_rate_increase': 0.1,  # 10% increase in error rate
            'response_time_degradation': 0.2,  # 20% increase in response time
            'success_rate_decline': 0.05  # 5% decline in success rate
        }
        
    def add_metrics_data(self, metrics_data: Dict[str, Any]):
        """Add new metrics data for analysis"""
        timestamped_data = {
            'timestamp': datetime.now(),
            'data': metrics_data
        }
        self.metrics_history.append(timestamped_data)
        
    def add_performance_data(self, performance_data: Dict[str, Any]):
        """Add new performance data for analysis"""
        timestamped_data = {
            'timestamp': datetime.now(),
            'data': performance_data
        }
        self.performance_history.append(timestamped_data)
        
    def add_error_data(self, error_data: Dict[str, Any]):
        """Add new error data for analysis"""
        timestamped_data = {
            'timestamp': datetime.now(),
            'data': error_data
        }
        self.error_history.append(timestamped_data)
        
    def analyze_system_trends(self, days_back: int = 30) -> List[PerformanceTrend]:
        """
        Analyze system performance trends over the specified period
        
        Args:
            days_back: Number of days to analyze
            
        Returns:
            List of performance trends
        """
        cutoff_date = datetime.now() - timedelta(days=days_back)
        
        # Filter data to the specified period
        recent_metrics = [
            entry for entry in self.metrics_history 
            if entry['timestamp'] >= cutoff_date
        ]
        
        if len(recent_metrics) < 10:
            self.logger.warning(f"Insufficient data for trend analysis: {len(recent_metrics)} points")
            return []
            
        trends = []
        
        # Analyze CPU trend
        cpu_trend = self._analyze_metric_trend(recent_metrics, 'cpu_percent', 'CPU Usage')
        if cpu_trend:
            trends.append(cpu_trend)
            
        # Analyze memory trend
        memory_trend = self._analyze_metric_trend(recent_metrics, 'memory_percent', 'Memory Usage')
        if memory_trend:
            trends.append(memory_trend)
            
        # Analyze disk trend
        disk_trend = self._analyze_metric_trend(recent_metrics, 'disk_usage_percent', 'Disk Usage')
        if disk_trend:
            trends.append(disk_trend)
            
        # Analyze agent performance trends
        agent_trends = self._analyze_agent_performance_trends(days_back)
        trends.extend(agent_trends)
        
        return trends
        
    def _analyze_metric_trend(self, data: List[Dict], metric_key: str, metric_name: str) -> Optional[PerformanceTrend]:
        """Analyze trend for a specific metric"""
        try:
            # Extract metric values and timestamps
            values = []
            timestamps = []
            
            for entry in data:
                if metric_key in entry['data']:
                    values.append(entry['data'][metric_key])
                    timestamps.append(entry['timestamp'])
                    
            if len(values) < 5:
                return None
                
            # Calculate trend using linear regression
            x = np.array([(ts - timestamps[0]).total_seconds() for ts in timestamps])
            y = np.array(values)
            
            # Simple linear regression
            n = len(x)
            sum_x = np.sum(x)
            sum_y = np.sum(y)
            sum_xy = np.sum(x * y)
            sum_x2 = np.sum(x * x)
            
            slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
            intercept = (sum_y - slope * sum_x) / n
            
            # Calculate correlation coefficient for trend strength
            mean_x = np.mean(x)
            mean_y = np.mean(y)
            
            numerator = np.sum((x - mean_x) * (y - mean_y))
            denominator = np.sqrt(np.sum((x - mean_x)**2) * np.sum((y - mean_y)**2))
            
            correlation = numerator / denominator if denominator != 0 else 0
            trend_strength = abs(correlation)
            
            # Determine trend direction
            if slope > 0.01:
                trend_direction = "degrading" if metric_name in ["CPU Usage", "Memory Usage", "Disk Usage"] else "improving"
            elif slope < -0.01:
                trend_direction = "improving" if metric_name in ["CPU Usage", "Memory Usage", "Disk Usage"] else "degrading"
            else:
                trend_direction = "stable"
                
            # Predict future value (30 days ahead)
            future_seconds = 30 * 24 * 3600  # 30 days in seconds
            predicted_value = slope * (x[-1] + future_seconds) + intercept
            prediction_date = datetime.now() + timedelta(days=30)
            
            # Calculate confidence based on trend strength and data quality
            confidence = min(0.9, trend_strength * 0.8 + (len(values) / 100) * 0.2)
            
            return PerformanceTrend(
                metric_name=metric_name,
                trend_direction=trend_direction,
                trend_strength=trend_strength,
                current_value=values[-1],
                predicted_value=max(0, min(100, predicted_value)),  # Clamp to 0-100%
                prediction_date=prediction_date,
                confidence=confidence
            )
            
        except Exception as e:
            self.logger.error(f"Error analyzing trend for {metric_name}: {e}")
            return None
            
    def _analyze_agent_performance_trends(self, days_back: int) -> List[PerformanceTrend]:
        """Analyze agent performance trends"""
        cutoff_date = datetime.now() - timedelta(days=days_back)
        
        recent_performance = [
            entry for entry in self.performance_history 
            if entry['timestamp'] >= cutoff_date
        ]
        
        if len(recent_performance) < 5:
            return []
            
        trends = []
        
        # Analyze overall success rate trend
        success_rates = []
        timestamps = []
        
        for entry in recent_performance:
            if 'overall_success_rate' in entry['data']:
                success_rates.append(entry['data']['overall_success_rate'])
                timestamps.append(entry['timestamp'])
                
        if len(success_rates) >= 5:
            trend = self._calculate_simple_trend(success_rates, timestamps, "Agent Success Rate")
            if trend:
                trends.append(trend)
                
        # Analyze response time trend
        response_times = []
        timestamps = []
        
        for entry in recent_performance:
            if 'overall_avg_duration_seconds' in entry['data']:
                response_times.append(entry['data']['overall_avg_duration_seconds'])
                timestamps.append(entry['timestamp'])
                
        if len(response_times) >= 5:
            trend = self._calculate_simple_trend(response_times, timestamps, "Agent Response Time")
            if trend:
                trends.append(trend)
                
        return trends
        
    def _calculate_simple_trend(self, values: List[float], timestamps: List[datetime], 
                               metric_name: str) -> Optional[PerformanceTrend]:
        """Calculate simple trend for a list of values"""
        try:
            if len(values) < 3:
                return None
                
            # Calculate simple moving average trend
            recent_avg = statistics.mean(values[-5:]) if len(values) >= 5 else statistics.mean(values)
            older_avg = statistics.mean(values[:5]) if len(values) >= 10 else statistics.mean(values[:-2])
            
            trend_change = (recent_avg - older_avg) / older_avg if older_avg != 0 else 0
            
            # Determine trend direction
            if abs(trend_change) < 0.05:  # Less than 5% change
                trend_direction = "stable"
                trend_strength = 0.3
            elif trend_change > 0:
                if metric_name in ["Agent Success Rate"]:
                    trend_direction = "improving"
                else:
                    trend_direction = "degrading"
                trend_strength = min(1.0, abs(trend_change) * 2)
            else:
                if metric_name in ["Agent Success Rate"]:
                    trend_direction = "degrading"
                else:
                    trend_direction = "improving"
                trend_strength = min(1.0, abs(trend_change) * 2)
                
            # Simple prediction (extend current trend)
            predicted_value = recent_avg * (1 + trend_change)
            prediction_date = datetime.now() + timedelta(days=30)
            
            confidence = min(0.8, trend_strength * 0.6 + (len(values) / 50) * 0.4)
            
            return PerformanceTrend(
                metric_name=metric_name,
                trend_direction=trend_direction,
                trend_strength=trend_strength,
                current_value=values[-1],
                predicted_value=predicted_value,
                prediction_date=prediction_date,
                confidence=confidence
            )
            
        except Exception as e:
            self.logger.error(f"Error calculating trend for {metric_name}: {e}")
            return None
            
    def predict_maintenance_needs(self, forecast_days: int = 90) -> List[MaintenanceAlert]:
        """
        Predict maintenance needs based on current trends
        
        Args:
            forecast_days: Number of days to forecast ahead
            
        Returns:
            List of maintenance alerts
        """
        alerts = []
        
        # Analyze current trends
        trends = self.analyze_system_trends(days_back=30)
        
        for trend in trends:
            alert = self._generate_maintenance_alert(trend, forecast_days)
            if alert:
                alerts.append(alert)
                
        # Analyze error patterns for additional alerts
        error_alerts = self._analyze_error_patterns(forecast_days)
        alerts.extend(error_alerts)
        
        # Sort alerts by severity and predicted failure date
        alerts.sort(key=lambda x: (
            {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}[x.severity],
            x.predicted_failure_date
        ))
        
        self.maintenance_alerts = alerts
        return alerts
        
    def _generate_maintenance_alert(self, trend: PerformanceTrend, 
                                  forecast_days: int) -> Optional[MaintenanceAlert]:
        """Generate maintenance alert based on performance trend"""
        try:
            alert_id = f"trend_{trend.metric_name.lower().replace(' ', '_')}_{int(datetime.now().timestamp())}"
            
            # Determine if trend requires maintenance alert
            if trend.trend_direction == "stable":
                return None
                
            # Calculate severity based on trend and predicted value
            severity = "low"
            estimated_downtime = 1.0  # hours
            estimated_cost = 500.0  # dollars
            
            if trend.metric_name in ["CPU Usage", "Memory Usage", "Disk Usage"]:
                if trend.predicted_value > 95:
                    severity = "critical"
                    estimated_downtime = 4.0
                    estimated_cost = 5000.0
                elif trend.predicted_value > 90:
                    severity = "high"
                    estimated_downtime = 2.0
                    estimated_cost = 2000.0
                elif trend.predicted_value > 85:
                    severity = "medium"
                    estimated_downtime = 1.0
                    estimated_cost = 1000.0
                    
            elif trend.metric_name == "Agent Success Rate":
                if trend.predicted_value < 50:
                    severity = "critical"
                    estimated_downtime = 6.0
                    estimated_cost = 10000.0
                elif trend.predicted_value < 70:
                    severity = "high"
                    estimated_downtime = 3.0
                    estimated_cost = 5000.0
                elif trend.predicted_value < 85:
                    severity = "medium"
                    estimated_downtime = 1.5
                    estimated_cost = 2000.0
                    
            # Skip low-severity alerts with low confidence
            if severity == "low" and trend.confidence < 0.5:
                return None
                
            # Calculate predicted failure date
            days_to_failure = forecast_days
            if trend.trend_strength > 0.7:
                # Accelerate prediction for strong trends
                days_to_failure = int(forecast_days * (1 - trend.trend_strength * 0.3))
                
            predicted_failure_date = datetime.now() + timedelta(days=days_to_failure)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(trend.metric_name, severity)
            
            description = f"{trend.metric_name} showing {trend.trend_direction} trend. " \
                         f"Current: {trend.current_value:.1f}, Predicted: {trend.predicted_value:.1f}"
            
            return MaintenanceAlert(
                alert_id=alert_id,
                component=trend.metric_name,
                severity=severity,
                predicted_failure_date=predicted_failure_date,
                confidence=trend.confidence,
                description=description,
                recommended_actions=recommendations,
                estimated_downtime=estimated_downtime,
                estimated_cost=estimated_cost
            )
            
        except Exception as e:
            self.logger.error(f"Error generating maintenance alert: {e}")
            return None
            
    def _generate_recommendations(self, metric_name: str, severity: str) -> List[str]:
        """Generate maintenance recommendations based on metric and severity"""
        recommendations = []
        
        if metric_name == "CPU Usage":
            if severity in ["critical", "high"]:
                recommendations.extend([
                    "Scale up CPU resources immediately",
                    "Identify and optimize CPU-intensive processes",
                    "Consider load balancing across multiple instances"
                ])
            else:
                recommendations.extend([
                    "Monitor CPU usage trends closely",
                    "Review and optimize resource-intensive operations",
                    "Plan for capacity scaling"
                ])
                
        elif metric_name == "Memory Usage":
            if severity in ["critical", "high"]:
                recommendations.extend([
                    "Increase memory allocation immediately",
                    "Investigate memory leaks in applications",
                    "Implement memory cleanup procedures"
                ])
            else:
                recommendations.extend([
                    "Monitor memory usage patterns",
                    "Optimize memory-intensive operations",
                    "Plan for memory capacity expansion"
                ])
                
        elif metric_name == "Disk Usage":
            if severity in ["critical", "high"]:
                recommendations.extend([
                    "Free up disk space immediately",
                    "Archive or delete old data",
                    "Add additional storage capacity"
                ])
            else:
                recommendations.extend([
                    "Implement data retention policies",
                    "Monitor disk usage growth",
                    "Plan for storage expansion"
                ])
                
        elif metric_name == "Agent Success Rate":
            if severity in ["critical", "high"]:
                recommendations.extend([
                    "Investigate agent failures immediately",
                    "Review error logs for patterns",
                    "Implement additional error handling"
                ])
            else:
                recommendations.extend([
                    "Monitor agent performance trends",
                    "Review and optimize agent code",
                    "Implement proactive error detection"
                ])
                
        return recommendations
        
    def _analyze_error_patterns(self, forecast_days: int) -> List[MaintenanceAlert]:
        """Analyze error patterns to predict maintenance needs"""
        alerts = []
        
        if len(self.error_history) < 10:
            return alerts
            
        # Analyze recent error frequency
        recent_errors = list(self.error_history)[-100:]  # Last 100 errors
        
        # Group errors by type/component
        error_groups = {}
        for entry in recent_errors:
            error_type = entry['data'].get('error_type', 'unknown')
            if error_type not in error_groups:
                error_groups[error_type] = []
            error_groups[error_type].append(entry)
            
        # Generate alerts for error patterns
        for error_type, errors in error_groups.items():
            if len(errors) >= 5:  # Minimum threshold for pattern analysis
                alert = self._create_error_pattern_alert(error_type, errors, forecast_days)
                if alert:
                    alerts.append(alert)
                    
        return alerts
        
    def _create_error_pattern_alert(self, error_type: str, errors: List[Dict], 
                                  forecast_days: int) -> Optional[MaintenanceAlert]:
        """Create maintenance alert based on error patterns"""
        try:
            # Calculate error frequency trend
            recent_count = len([e for e in errors if 
                              (datetime.now() - e['timestamp']).days <= 7])
            older_count = len([e for e in errors if 
                             7 < (datetime.now() - e['timestamp']).days <= 14])
            
            if older_count == 0:
                return None
                
            frequency_change = (recent_count - older_count) / older_count
            
            # Only create alert if error frequency is increasing significantly
            if frequency_change < 0.5:  # Less than 50% increase
                return None
                
            severity = "medium"
            if frequency_change > 2.0:  # More than 200% increase
                severity = "high"
            elif frequency_change > 5.0:  # More than 500% increase
                severity = "critical"
                
            alert_id = f"error_pattern_{error_type}_{int(datetime.now().timestamp())}"
            
            predicted_failure_date = datetime.now() + timedelta(
                days=max(7, forecast_days // 2)  # Errors tend to escalate faster
            )
            
            description = f"Increasing frequency of {error_type} errors. " \
                         f"Recent: {recent_count}, Previous: {older_count} " \
                         f"({frequency_change*100:.0f}% increase)"
            
            recommendations = [
                f"Investigate root cause of {error_type} errors",
                "Review error logs for common patterns",
                "Implement additional error handling",
                "Consider preventive measures"
            ]
            
            confidence = min(0.8, frequency_change / 3.0)  # Higher change = higher confidence
            
            return MaintenanceAlert(
                alert_id=alert_id,
                component=f"Error Pattern: {error_type}",
                severity=severity,
                predicted_failure_date=predicted_failure_date,
                confidence=confidence,
                description=description,
                recommended_actions=recommendations,
                estimated_downtime=2.0,
                estimated_cost=1500.0
            )
            
        except Exception as e:
            self.logger.error(f"Error creating error pattern alert: {e}")
            return None
            
    def get_maintenance_schedule(self, days_ahead: int = 90) -> Dict[str, Any]:
        """
        Generate optimal maintenance schedule based on predictions
        
        Args:
            days_ahead: Number of days to schedule ahead
            
        Returns:
            Maintenance schedule with recommended actions and timing
        """
        alerts = self.predict_maintenance_needs(days_ahead)
        
        # Group alerts by time periods
        schedule = {
            'immediate': [],  # Next 7 days
            'short_term': [],  # 8-30 days
            'medium_term': [],  # 31-60 days
            'long_term': []  # 61+ days
        }
        
        now = datetime.now()
        
        for alert in alerts:
            days_until = (alert.predicted_failure_date - now).days
            
            if days_until <= 7:
                schedule['immediate'].append(alert)
            elif days_until <= 30:
                schedule['short_term'].append(alert)
            elif days_until <= 60:
                schedule['medium_term'].append(alert)
            else:
                schedule['long_term'].append(alert)
                
        # Calculate total estimated costs and downtime
        total_cost = sum(alert.estimated_cost for alert in alerts)
        total_downtime = sum(alert.estimated_downtime for alert in alerts)
        
        return {
            'schedule_generated': now.isoformat(),
            'forecast_period_days': days_ahead,
            'schedule': schedule,
            'summary': {
                'total_alerts': len(alerts),
                'critical_alerts': len([a for a in alerts if a.severity == 'critical']),
                'high_priority_alerts': len([a for a in alerts if a.severity == 'high']),
                'estimated_total_cost': total_cost,
                'estimated_total_downtime_hours': total_downtime,
                'immediate_action_required': len(schedule['immediate']) > 0
            }
        }
        
    def export_predictions(self, filepath: str):
        """Export maintenance predictions to JSON file"""
        try:
            predictions_data = {
                'export_timestamp': datetime.now().isoformat(),
                'trends': [
                    {
                        'metric_name': trend.metric_name,
                        'trend_direction': trend.trend_direction,
                        'trend_strength': trend.trend_strength,
                        'current_value': trend.current_value,
                        'predicted_value': trend.predicted_value,
                        'prediction_date': trend.prediction_date.isoformat(),
                        'confidence': trend.confidence
                    }
                    for trend in self.analyze_system_trends()
                ],
                'maintenance_alerts': [
                    {
                        'alert_id': alert.alert_id,
                        'component': alert.component,
                        'severity': alert.severity,
                        'predicted_failure_date': alert.predicted_failure_date.isoformat(),
                        'confidence': alert.confidence,
                        'description': alert.description,
                        'recommended_actions': alert.recommended_actions,
                        'estimated_downtime': alert.estimated_downtime,
                        'estimated_cost': alert.estimated_cost
                    }
                    for alert in self.maintenance_alerts
                ],
                'maintenance_schedule': self.get_maintenance_schedule()
            }
            
            with open(filepath, 'w') as f:
                json.dump(predictions_data, f, indent=2)
                
            self.logger.info(f"Exported maintenance predictions to {filepath}")
            
        except Exception as e:
            self.logger.error(f"Error exporting predictions: {e}")
            raise