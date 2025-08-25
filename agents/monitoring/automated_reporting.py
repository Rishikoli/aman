"""
Automated System Health Reporting

This module provides automated generation of comprehensive system health reports
with AI-powered insights, trend analysis, and executive summaries.
"""

import logging
import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import asyncio

logger = logging.getLogger(__name__)

@dataclass
class ReportSection:
    """Report section data structure"""
    title: str
    content: str
    severity: str  # info, warning, critical
    recommendations: List[str]
    metrics: Dict[str, Any]

@dataclass
class HealthReport:
    """Complete health report structure"""
    report_id: str
    generated_at: datetime
    report_type: str  # daily, weekly, monthly, incident
    overall_health_score: int  # 0-100
    executive_summary: str
    sections: List[ReportSection]
    key_metrics: Dict[str, Any]
    trends: Dict[str, Any]
    alerts: List[Dict[str, Any]]
    recommendations: List[str]
    next_actions: List[str]
    ai_insights: Dict[str, Any]

class AutomatedReportingEngine:
    """
    Automated system health reporting engine with AI-powered insights
    """
    
    def __init__(self, 
                 ai_diagnostics,
                 predictive_maintenance,
                 report_storage_path: str = "/tmp/health_reports"):
        
        self.ai_diagnostics = ai_diagnostics
        self.predictive_maintenance = predictive_maintenance
        self.report_storage_path = report_storage_path
        self.logger = logging.getLogger(__name__)
        
        # Ensure report storage directory exists
        os.makedirs(report_storage_path, exist_ok=True)
        
        # Report templates and configurations
        self.report_configs = {
            'daily': {
                'frequency_hours': 24,
                'include_trends': True,
                'include_predictions': False,
                'detail_level': 'summary'
            },
            'weekly': {
                'frequency_hours': 168,  # 7 days
                'include_trends': True,
                'include_predictions': True,
                'detail_level': 'detailed'
            },
            'monthly': {
                'frequency_hours': 720,  # 30 days
                'include_trends': True,
                'include_predictions': True,
                'detail_level': 'comprehensive'
            },
            'incident': {
                'frequency_hours': 0,  # On-demand
                'include_trends': True,
                'include_predictions': False,
                'detail_level': 'detailed'
            }
        }
        
    async def generate_health_report(self, 
                                   report_type: str = "daily",
                                   system_data: Optional[Dict[str, Any]] = None) -> HealthReport:
        """
        Generate comprehensive health report
        
        Args:
            report_type: Type of report (daily, weekly, monthly, incident)
            system_data: Current system data (if not provided, will be collected)
            
        Returns:
            Complete health report
        """
        try:
            self.logger.info(f"Generating {report_type} health report...")
            
            report_id = f"{report_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            config = self.report_configs.get(report_type, self.report_configs['daily'])
            
            # Collect system data if not provided
            if system_data is None:
                system_data = await self._collect_system_data()
                
            # Generate AI insights
            ai_insights = await self._generate_ai_insights(system_data, config)
            
            # Generate report sections
            sections = await self._generate_report_sections(system_data, config, ai_insights)
            
            # Calculate overall health score
            health_score = self._calculate_health_score(system_data, ai_insights)
            
            # Generate executive summary
            executive_summary = await self._generate_executive_summary(
                system_data, ai_insights, health_score, config
            )
            
            # Extract key metrics
            key_metrics = self._extract_key_metrics(system_data)
            
            # Generate trends analysis
            trends = self._generate_trends_analysis(system_data, config)
            
            # Extract alerts
            alerts = system_data.get('alerts', [])
            
            # Generate recommendations
            recommendations = self._compile_recommendations(ai_insights, sections)
            
            # Generate next actions
            next_actions = self._generate_next_actions(ai_insights, health_score)
            
            # Create health report
            report = HealthReport(
                report_id=report_id,
                generated_at=datetime.now(),
                report_type=report_type,
                overall_health_score=health_score,
                executive_summary=executive_summary,
                sections=sections,
                key_metrics=key_metrics,
                trends=trends,
                alerts=alerts,
                recommendations=recommendations,
                next_actions=next_actions,
                ai_insights=ai_insights
            )
            
            # Save report
            await self._save_report(report)
            
            self.logger.info(f"Generated {report_type} health report: {report_id}")
            return report
            
        except Exception as e:
            self.logger.error(f"Error generating health report: {e}")
            raise
            
    async def _collect_system_data(self) -> Dict[str, Any]:
        """Collect comprehensive system data for reporting"""
        # This would typically collect data from the monitoring system
        # For now, return a placeholder structure
        return {
            'system_metrics': {
                'cpu_percent': 45.2,
                'memory_percent': 67.8,
                'disk_usage_percent': 23.4,
                'network_bytes_sent': 1024000,
                'network_bytes_recv': 2048000
            },
            'agent_performance': {
                'overall_success_rate': 87.5,
                'overall_avg_duration_seconds': 12.3,
                'total_agents': 5,
                'active_executions': 2
            },
            'alerts': [
                {
                    'severity': 'warning',
                    'message': 'High memory usage detected',
                    'timestamp': datetime.now().isoformat()
                }
            ],
            'bottlenecks': [
                {
                    'type': 'slow_execution',
                    'agent_id': 'legal_agent',
                    'severity': 'medium',
                    'description': 'Legal agent showing slower than average execution times'
                }
            ],
            'recent_errors': [
                {
                    'error_type': 'connection_timeout',
                    'count': 3,
                    'last_occurrence': datetime.now().isoformat()
                }
            ]
        }
        
    async def _generate_ai_insights(self, system_data: Dict[str, Any], 
                                  config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate AI-powered insights for the report"""
        insights = {}
        
        try:
            # System diagnosis
            diagnosis = await self.ai_diagnostics.diagnose_system_issues(system_data)
            insights['system_diagnosis'] = diagnosis
            
            # Error analysis if errors present
            if system_data.get('recent_errors'):
                error_analysis = await self.ai_diagnostics.analyze_error_logs(
                    system_data['recent_errors']
                )
                insights['error_analysis'] = error_analysis
                
            # Performance optimization
            performance_optimization = await self.ai_diagnostics.optimize_system_performance(
                system_data
            )
            insights['performance_optimization'] = performance_optimization
            
            # Predictive maintenance (for weekly/monthly reports)
            if config.get('include_predictions', False):
                maintenance_prediction = await self.ai_diagnostics.predict_system_maintenance(
                    {'metrics_history': system_data}
                )
                insights['maintenance_prediction'] = maintenance_prediction
                
            # Comprehensive health report
            health_report = await self.ai_diagnostics.generate_health_report(system_data)
            insights['ai_health_report'] = health_report
            
        except Exception as e:
            self.logger.error(f"Error generating AI insights: {e}")
            insights['error'] = f"AI insights unavailable: {str(e)}"
            
        return insights
        
    async def _generate_report_sections(self, system_data: Dict[str, Any], 
                                      config: Dict[str, Any],
                                      ai_insights: Dict[str, Any]) -> List[ReportSection]:
        """Generate individual report sections"""
        sections = []
        
        # System Performance Section
        system_section = self._create_system_performance_section(system_data, ai_insights)
        sections.append(system_section)
        
        # Agent Performance Section
        agent_section = self._create_agent_performance_section(system_data, ai_insights)
        sections.append(agent_section)
        
        # Alerts and Issues Section
        alerts_section = self._create_alerts_section(system_data, ai_insights)
        sections.append(alerts_section)
        
        # AI Insights Section
        ai_section = self._create_ai_insights_section(ai_insights)
        sections.append(ai_section)
        
        # Predictive Maintenance Section (for detailed reports)
        if config.get('include_predictions', False):
            maintenance_section = self._create_maintenance_section(ai_insights)
            sections.append(maintenance_section)
            
        return sections
        
    def _create_system_performance_section(self, system_data: Dict[str, Any], 
                                         ai_insights: Dict[str, Any]) -> ReportSection:
        """Create system performance section"""
        metrics = system_data.get('system_metrics', {})
        
        # Determine severity based on metrics
        severity = "info"
        if metrics.get('cpu_percent', 0) > 80 or metrics.get('memory_percent', 0) > 85:
            severity = "warning"
        if metrics.get('cpu_percent', 0) > 95 or metrics.get('memory_percent', 0) > 95:
            severity = "critical"
            
        content = f"""
System Resource Utilization:
- CPU Usage: {metrics.get('cpu_percent', 0):.1f}%
- Memory Usage: {metrics.get('memory_percent', 0):.1f}%
- Disk Usage: {metrics.get('disk_usage_percent', 0):.1f}%
- Network I/O: {metrics.get('network_bytes_sent', 0)/1024:.1f}KB sent, {metrics.get('network_bytes_recv', 0)/1024:.1f}KB received

Performance Status: {severity.upper()}
        """.strip()
        
        recommendations = []
        if metrics.get('cpu_percent', 0) > 80:
            recommendations.append("Consider CPU optimization or scaling")
        if metrics.get('memory_percent', 0) > 85:
            recommendations.append("Monitor memory usage and consider increasing allocation")
        if metrics.get('disk_usage_percent', 0) > 90:
            recommendations.append("Free up disk space or add storage capacity")
            
        return ReportSection(
            title="System Performance",
            content=content,
            severity=severity,
            recommendations=recommendations,
            metrics=metrics
        )
        
    def _create_agent_performance_section(self, system_data: Dict[str, Any], 
                                        ai_insights: Dict[str, Any]) -> ReportSection:
        """Create agent performance section"""
        agent_data = system_data.get('agent_performance', {})
        
        success_rate = agent_data.get('overall_success_rate', 0)
        avg_duration = agent_data.get('overall_avg_duration_seconds', 0)
        
        # Determine severity
        severity = "info"
        if success_rate < 80 or avg_duration > 30:
            severity = "warning"
        if success_rate < 60 or avg_duration > 60:
            severity = "critical"
            
        content = f"""
Agent Performance Summary:
- Overall Success Rate: {success_rate:.1f}%
- Average Execution Time: {avg_duration:.1f} seconds
- Total Agents: {agent_data.get('total_agents', 0)}
- Active Executions: {agent_data.get('active_executions', 0)}

Performance Status: {severity.upper()}
        """.strip()
        
        recommendations = []
        if success_rate < 80:
            recommendations.append("Investigate agent failures and improve error handling")
        if avg_duration > 30:
            recommendations.append("Optimize agent performance and consider parallel processing")
            
        return ReportSection(
            title="Agent Performance",
            content=content,
            severity=severity,
            recommendations=recommendations,
            metrics=agent_data
        )
        
    def _create_alerts_section(self, system_data: Dict[str, Any], 
                             ai_insights: Dict[str, Any]) -> ReportSection:
        """Create alerts and issues section"""
        alerts = system_data.get('alerts', [])
        bottlenecks = system_data.get('bottlenecks', [])
        
        # Determine severity based on alert levels
        severity = "info"
        critical_alerts = [a for a in alerts if a.get('severity') == 'critical']
        warning_alerts = [a for a in alerts if a.get('severity') == 'warning']
        
        if critical_alerts:
            severity = "critical"
        elif warning_alerts:
            severity = "warning"
            
        content = f"""
Active Alerts: {len(alerts)}
- Critical: {len(critical_alerts)}
- Warning: {len(warning_alerts)}
- Info: {len(alerts) - len(critical_alerts) - len(warning_alerts)}

Identified Bottlenecks: {len(bottlenecks)}
        """.strip()
        
        if alerts:
            content += "\n\nRecent Alerts:"
            for alert in alerts[:5]:  # Show top 5 alerts
                content += f"\n- {alert.get('severity', 'info').upper()}: {alert.get('message', 'No message')}"
                
        recommendations = []
        if critical_alerts:
            recommendations.append("Address critical alerts immediately")
        if bottlenecks:
            recommendations.append("Investigate and resolve identified bottlenecks")
            
        return ReportSection(
            title="Alerts and Issues",
            content=content,
            severity=severity,
            recommendations=recommendations,
            metrics={'alerts_count': len(alerts), 'bottlenecks_count': len(bottlenecks)}
        )
        
    def _create_ai_insights_section(self, ai_insights: Dict[str, Any]) -> ReportSection:
        """Create AI insights section"""
        diagnosis = ai_insights.get('system_diagnosis', {})
        
        content = f"""
AI-Powered System Analysis:
- Health Assessment: {diagnosis.get('overall_health_assessment', 'Unknown')}
- Confidence Level: {diagnosis.get('confidence_level', 0)*100:.0f}%
- AI Analysis Available: {'Yes' if diagnosis.get('ai_powered', False) else 'No'}
        """.strip()
        
        if diagnosis.get('root_cause_analysis'):
            content += "\n\nRoot Cause Analysis:"
            for cause in diagnosis['root_cause_analysis'][:3]:
                content += f"\n- {cause}"
                
        severity = "info"
        if diagnosis.get('urgency_level') == 'high':
            severity = "warning"
        elif diagnosis.get('urgency_level') == 'critical':
            severity = "critical"
            
        recommendations = diagnosis.get('system_recommendations', [])
        
        return ReportSection(
            title="AI Insights",
            content=content,
            severity=severity,
            recommendations=recommendations,
            metrics={'ai_powered': diagnosis.get('ai_powered', False)}
        )
        
    def _create_maintenance_section(self, ai_insights: Dict[str, Any]) -> ReportSection:
        """Create predictive maintenance section"""
        maintenance = ai_insights.get('maintenance_prediction', {})
        
        content = f"""
Predictive Maintenance Forecast:
- Forecast Available: {'Yes' if maintenance.get('ai_powered', False) else 'No'}
- Confidence Level: {maintenance.get('confidence_level', 0)*100:.0f}%
        """.strip()
        
        if maintenance.get('maintenance_forecast'):
            forecast = maintenance['maintenance_forecast']
            content += f"\n\nUpcoming Maintenance Needs:"
            for period, description in forecast.items():
                content += f"\n- {period.replace('_', ' ').title()}: {description}"
                
        recommendations = maintenance.get('recommended_actions', [])
        
        return ReportSection(
            title="Predictive Maintenance",
            content=content,
            severity="info",
            recommendations=recommendations,
            metrics=maintenance.get('resource_requirements', {})
        )
        
    def _calculate_health_score(self, system_data: Dict[str, Any], 
                              ai_insights: Dict[str, Any]) -> int:
        """Calculate overall system health score (0-100)"""
        score = 100
        
        # System metrics impact
        metrics = system_data.get('system_metrics', {})
        if metrics.get('cpu_percent', 0) > 90:
            score -= 20
        elif metrics.get('cpu_percent', 0) > 80:
            score -= 10
            
        if metrics.get('memory_percent', 0) > 90:
            score -= 20
        elif metrics.get('memory_percent', 0) > 80:
            score -= 10
            
        # Agent performance impact
        agent_data = system_data.get('agent_performance', {})
        success_rate = agent_data.get('overall_success_rate', 100)
        if success_rate < 60:
            score -= 30
        elif success_rate < 80:
            score -= 15
            
        # Alerts impact
        alerts = system_data.get('alerts', [])
        critical_alerts = [a for a in alerts if a.get('severity') == 'critical']
        warning_alerts = [a for a in alerts if a.get('severity') == 'warning']
        
        score -= len(critical_alerts) * 10
        score -= len(warning_alerts) * 5
        
        # AI insights impact
        diagnosis = ai_insights.get('system_diagnosis', {})
        if diagnosis.get('urgency_level') == 'critical':
            score -= 15
        elif diagnosis.get('urgency_level') == 'high':
            score -= 10
            
        return max(0, min(100, score))
        
    async def _generate_executive_summary(self, system_data: Dict[str, Any], 
                                        ai_insights: Dict[str, Any],
                                        health_score: int,
                                        config: Dict[str, Any]) -> str:
        """Generate executive summary"""
        
        # Determine overall status
        if health_score >= 90:
            status = "EXCELLENT"
        elif health_score >= 75:
            status = "GOOD"
        elif health_score >= 60:
            status = "FAIR"
        elif health_score >= 40:
            status = "POOR"
        else:
            status = "CRITICAL"
            
        # Get key metrics
        metrics = system_data.get('system_metrics', {})
        agent_data = system_data.get('agent_performance', {})
        alerts = system_data.get('alerts', [])
        
        summary = f"""
EXECUTIVE SUMMARY - System Health Report

Overall Health Score: {health_score}/100 ({status})

Key Performance Indicators:
• System CPU Usage: {metrics.get('cpu_percent', 0):.1f}%
• Memory Utilization: {metrics.get('memory_percent', 0):.1f}%
• Agent Success Rate: {agent_data.get('overall_success_rate', 0):.1f}%
• Active Alerts: {len(alerts)} ({len([a for a in alerts if a.get('severity') == 'critical'])} critical)

System Status: The M&A Analysis System is currently operating at {status.lower()} performance levels.
        """.strip()
        
        # Add AI insights if available
        diagnosis = ai_insights.get('system_diagnosis', {})
        if diagnosis.get('ai_powered'):
            summary += f"\n\nAI Analysis: {diagnosis.get('overall_health_assessment', 'Analysis unavailable')}"
            
        # Add urgent recommendations
        if health_score < 60:
            summary += "\n\nIMMEDIATE ACTION REQUIRED: System performance is below acceptable thresholds."
            
        return summary
        
    def _extract_key_metrics(self, system_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract key metrics for the report"""
        return {
            'system_metrics': system_data.get('system_metrics', {}),
            'agent_performance': system_data.get('agent_performance', {}),
            'alerts_summary': {
                'total': len(system_data.get('alerts', [])),
                'critical': len([a for a in system_data.get('alerts', []) if a.get('severity') == 'critical']),
                'warning': len([a for a in system_data.get('alerts', []) if a.get('severity') == 'warning'])
            },
            'bottlenecks_count': len(system_data.get('bottlenecks', []))
        }
        
    def _generate_trends_analysis(self, system_data: Dict[str, Any], 
                                config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate trends analysis"""
        if not config.get('include_trends', False):
            return {}
            
        # This would typically analyze historical data
        # For now, return placeholder trends
        return {
            'cpu_trend': 'stable',
            'memory_trend': 'increasing',
            'agent_performance_trend': 'improving',
            'error_rate_trend': 'decreasing'
        }
        
    def _compile_recommendations(self, ai_insights: Dict[str, Any], 
                               sections: List[ReportSection]) -> List[str]:
        """Compile all recommendations from various sources"""
        recommendations = []
        
        # Add recommendations from sections
        for section in sections:
            recommendations.extend(section.recommendations)
            
        # Add AI recommendations
        diagnosis = ai_insights.get('system_diagnosis', {})
        recommendations.extend(diagnosis.get('system_recommendations', []))
        
        # Remove duplicates and return top recommendations
        unique_recommendations = list(dict.fromkeys(recommendations))
        return unique_recommendations[:10]  # Top 10 recommendations
        
    def _generate_next_actions(self, ai_insights: Dict[str, Any], 
                             health_score: int) -> List[str]:
        """Generate prioritized next actions"""
        actions = []
        
        if health_score < 40:
            actions.append("URGENT: Investigate critical system issues immediately")
            actions.append("Scale system resources to handle current load")
            
        if health_score < 60:
            actions.append("Review and address system bottlenecks")
            actions.append("Implement monitoring alerts for key metrics")
            
        if health_score < 80:
            actions.append("Optimize system performance")
            actions.append("Review agent configurations")
            
        # Add AI-suggested actions
        diagnosis = ai_insights.get('system_diagnosis', {})
        if diagnosis.get('urgency_level') in ['high', 'critical']:
            actions.insert(0, "Address AI-identified critical issues")
            
        # Always include routine actions
        actions.append("Continue monitoring system health")
        actions.append("Schedule next health review")
        
        return actions[:8]  # Top 8 actions
        
    async def _save_report(self, report: HealthReport):
        """Save health report to storage"""
        try:
            filename = f"{report.report_id}.json"
            filepath = os.path.join(self.report_storage_path, filename)
            
            # Convert report to dictionary for JSON serialization
            report_dict = asdict(report)
            
            # Convert datetime objects to ISO strings
            report_dict['generated_at'] = report.generated_at.isoformat()
            
            with open(filepath, 'w') as f:
                json.dump(report_dict, f, indent=2, default=str)
                
            self.logger.info(f"Saved health report to {filepath}")
            
        except Exception as e:
            self.logger.error(f"Error saving health report: {e}")
            raise
            
    def get_report_history(self, days_back: int = 30) -> List[str]:
        """Get list of available reports from the last N days"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days_back)
            reports = []
            
            for filename in os.listdir(self.report_storage_path):
                if filename.endswith('.json'):
                    filepath = os.path.join(self.report_storage_path, filename)
                    file_time = datetime.fromtimestamp(os.path.getmtime(filepath))
                    
                    if file_time >= cutoff_date:
                        reports.append(filename)
                        
            return sorted(reports, reverse=True)  # Most recent first
            
        except Exception as e:
            self.logger.error(f"Error getting report history: {e}")
            return []
            
    async def load_report(self, report_id: str) -> Optional[HealthReport]:
        """Load a specific health report"""
        try:
            filename = f"{report_id}.json"
            filepath = os.path.join(self.report_storage_path, filename)
            
            if not os.path.exists(filepath):
                return None
                
            with open(filepath, 'r') as f:
                report_dict = json.load(f)
                
            # Convert back to HealthReport object
            # This is a simplified conversion - in production would need proper deserialization
            return report_dict
            
        except Exception as e:
            self.logger.error(f"Error loading report {report_id}: {e}")
            return None