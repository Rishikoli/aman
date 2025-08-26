"""
Compliance Reporting System
Provides audit trail query, compliance documentation generation, and regulatory format adaptation.
"""

import json
import csv
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Union
from pathlib import Path
import sqlite3
from dataclasses import dataclass
from .audit_logger import AuditLogger

@dataclass
class ComplianceReport:
    """Data structure for compliance reports."""
    report_id: str
    report_type: str
    generated_at: datetime
    period_start: datetime
    period_end: datetime
    total_actions: int
    successful_actions: int
    failed_actions: int
    agents_involved: List[str]
    deals_analyzed: List[str]
    compliance_score: float
    findings: List[Dict[str, Any]]
    recommendations: List[str]

class ComplianceReporter:
    """
    Compliance reporting system for M&A due diligence audit trails.
    Generates regulatory-compliant reports and documentation.
    """
    
    def __init__(self, audit_logger: AuditLogger):
        self.audit_logger = audit_logger
        self.report_templates = self._load_report_templates()
    
    def _load_report_templates(self) -> Dict[str, Dict[str, Any]]:
        """Load report templates for different regulatory formats."""
        return {
            'sox_compliance': {
                'name': 'Sarbanes-Oxley Compliance Report',
                'sections': ['executive_summary', 'control_activities', 'risk_assessment', 'audit_trail'],
                'required_fields': ['timestamp', 'user_id', 'action_type', 'data_integrity', 'approval_chain']
            },
            'gdpr_compliance': {
                'name': 'GDPR Data Processing Report',
                'sections': ['data_processing_activities', 'consent_management', 'data_lineage', 'retention_policy'],
                'required_fields': ['data_subject', 'processing_purpose', 'legal_basis', 'data_categories']
            },
            'sec_filing': {
                'name': 'SEC Due Diligence Documentation',
                'sections': ['methodology', 'data_sources', 'analysis_procedures', 'findings', 'conclusions'],
                'required_fields': ['deal_id', 'analysis_date', 'responsible_party', 'verification_status']
            },
            'internal_audit': {
                'name': 'Internal Audit Report',
                'sections': ['scope', 'procedures', 'findings', 'management_response', 'action_plan'],
                'required_fields': ['audit_period', 'auditor', 'risk_level', 'control_effectiveness']
            }
        }
    
    def query_audit_trail(self,
                         start_date: Optional[datetime] = None,
                         end_date: Optional[datetime] = None,
                         deal_id: Optional[str] = None,
                         agent_id: Optional[str] = None,
                         action_type: Optional[str] = None,
                         status: Optional[str] = None,
                         user_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Query audit trail with flexible filtering options.
        
        Args:
            start_date: Start date for filtering
            end_date: End date for filtering
            deal_id: Filter by specific deal
            agent_id: Filter by specific agent
            action_type: Filter by action type
            status: Filter by status (SUCCESS, ERROR, WARNING)
            user_id: Filter by user
            
        Returns:
            List of audit log entries matching the criteria
        """
        query = """
            SELECT al.*, 
                   GROUP_CONCAT(dl.source_type || ':' || dl.transformation_type) as lineage_summary,
                   GROUP_CONCAT(ad.decision_type || ':' || ad.confidence_score) as decisions_summary
            FROM audit_log al
            LEFT JOIN data_lineage dl ON al.id = dl.audit_log_id
            LEFT JOIN agent_decisions ad ON al.id = ad.audit_log_id
            WHERE 1=1
        """
        
        params = []
        
        if start_date:
            query += " AND al.timestamp >= ?"
            params.append(start_date.isoformat())
        
        if end_date:
            query += " AND al.timestamp <= ?"
            params.append(end_date.isoformat())
        
        if deal_id:
            query += " AND al.deal_id = ?"
            params.append(deal_id)
        
        if agent_id:
            query += " AND al.agent_id = ?"
            params.append(agent_id)
        
        if action_type:
            query += " AND al.action_type = ?"
            params.append(action_type)
        
        if status:
            query += " AND al.status = ?"
            params.append(status)
        
        if user_id:
            query += " AND al.user_id = ?"
            params.append(user_id)
        
        query += " GROUP BY al.id ORDER BY al.timestamp DESC"
        
        with self.audit_logger._get_connection() as conn:
            cursor = conn.execute(query, params)
            results = []
            
            for row in cursor.fetchall():
                result = dict(row)
                # Parse JSON fields
                if result['metadata']:
                    result['metadata'] = json.loads(result['metadata'])
                results.append(result)
            
            return results
    
    def generate_compliance_report(self,
                                 report_type: str,
                                 start_date: datetime,
                                 end_date: datetime,
                                 deal_ids: Optional[List[str]] = None,
                                 output_format: str = 'json') -> ComplianceReport:
        """
        Generate a comprehensive compliance report.
        
        Args:
            report_type: Type of compliance report (sox_compliance, gdpr_compliance, etc.)
            start_date: Report period start date
            end_date: Report period end date
            deal_ids: Specific deals to include (None for all)
            output_format: Output format (json, xml, csv, html)
            
        Returns:
            ComplianceReport object
        """
        if report_type not in self.report_templates:
            raise ValueError(f"Unknown report type: {report_type}")
        
        # Query audit data for the period
        audit_data = self.query_audit_trail(start_date=start_date, end_date=end_date)
        
        # Filter by deal IDs if specified
        if deal_ids:
            audit_data = [entry for entry in audit_data if entry['deal_id'] in deal_ids]
        
        # Calculate compliance metrics
        total_actions = len(audit_data)
        successful_actions = len([entry for entry in audit_data if entry['status'] == 'SUCCESS'])
        failed_actions = len([entry for entry in audit_data if entry['status'] == 'ERROR'])
        
        agents_involved = list(set([entry['agent_id'] for entry in audit_data]))
        deals_analyzed = list(set([entry['deal_id'] for entry in audit_data if entry['deal_id']]))
        
        # Calculate compliance score (percentage of successful actions)
        compliance_score = (successful_actions / total_actions * 100) if total_actions > 0 else 100.0
        
        # Generate findings based on report type
        findings = self._generate_findings(report_type, audit_data)
        recommendations = self._generate_recommendations(report_type, findings, compliance_score)
        
        report = ComplianceReport(
            report_id=f"{report_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            report_type=report_type,
            generated_at=datetime.now(),
            period_start=start_date,
            period_end=end_date,
            total_actions=total_actions,
            successful_actions=successful_actions,
            failed_actions=failed_actions,
            agents_involved=agents_involved,
            deals_analyzed=deals_analyzed,
            compliance_score=compliance_score,
            findings=findings,
            recommendations=recommendations
        )
        
        return report
    
    def _generate_findings(self, report_type: str, audit_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate findings based on report type and audit data."""
        findings = []
        
        if report_type == 'sox_compliance':
            # SOX compliance findings
            findings.extend(self._analyze_sox_compliance(audit_data))
        elif report_type == 'gdpr_compliance':
            # GDPR compliance findings
            findings.extend(self._analyze_gdpr_compliance(audit_data))
        elif report_type == 'sec_filing':
            # SEC filing findings
            findings.extend(self._analyze_sec_compliance(audit_data))
        elif report_type == 'internal_audit':
            # Internal audit findings
            findings.extend(self._analyze_internal_controls(audit_data))
        
        return findings
    
    def _analyze_sox_compliance(self, audit_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze SOX compliance requirements."""
        findings = []
        
        # Check for proper segregation of duties
        user_actions = {}
        for entry in audit_data:
            user_id = entry.get('user_id', 'system')
            if user_id not in user_actions:
                user_actions[user_id] = set()
            user_actions[user_id].add(entry['action_type'])
        
        # Flag users with conflicting duties
        for user_id, actions in user_actions.items():
            if 'DATA_MODIFICATION' in actions and 'DATA_APPROVAL' in actions:
                findings.append({
                    'type': 'SOX_SEGREGATION_VIOLATION',
                    'severity': 'HIGH',
                    'description': f'User {user_id} has both modification and approval privileges',
                    'recommendation': 'Implement proper segregation of duties'
                })
        
        # Check for audit trail completeness
        incomplete_trails = [entry for entry in audit_data if not entry.get('input_data_hash')]
        if incomplete_trails:
            findings.append({
                'type': 'SOX_AUDIT_TRAIL_INCOMPLETE',
                'severity': 'MEDIUM',
                'description': f'{len(incomplete_trails)} actions lack complete audit trail',
                'recommendation': 'Ensure all actions include input data hashing'
            })
        
        return findings
    
    def _analyze_gdpr_compliance(self, audit_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze GDPR compliance requirements."""
        findings = []
        
        # Check for data processing without clear purpose
        unclear_purposes = []
        for entry in audit_data:
            if 'DATA_PROCESSING' in entry['action_type']:
                metadata = entry.get('metadata')
                if metadata is None or not metadata.get('processing_purpose'):
                    unclear_purposes.append(entry)
        
        if unclear_purposes:
            findings.append({
                'type': 'GDPR_PURPOSE_UNCLEAR',
                'severity': 'HIGH',
                'description': f'{len(unclear_purposes)} data processing actions lack clear purpose',
                'recommendation': 'Document processing purpose for all data operations'
            })
        
        # Check for data retention compliance
        old_data_actions = [
            entry for entry in audit_data 
            if datetime.fromisoformat(entry['timestamp']) < datetime.now() - timedelta(days=365)
        ]
        
        if old_data_actions:
            findings.append({
                'type': 'GDPR_RETENTION_REVIEW',
                'severity': 'MEDIUM',
                'description': f'{len(old_data_actions)} actions involve data older than 1 year',
                'recommendation': 'Review data retention policies and delete unnecessary data'
            })
        
        return findings
    
    def _analyze_sec_compliance(self, audit_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze SEC filing compliance requirements."""
        findings = []
        
        # Check for proper documentation of analysis procedures
        undocumented_analyses = [
            entry for entry in audit_data 
            if 'ANALYSIS' in entry['action_type'] and len(entry['action_description']) < 50
        ]
        
        if undocumented_analyses:
            findings.append({
                'type': 'SEC_DOCUMENTATION_INSUFFICIENT',
                'severity': 'MEDIUM',
                'description': f'{len(undocumented_analyses)} analyses lack detailed documentation',
                'recommendation': 'Provide comprehensive documentation for all analysis procedures'
            })
        
        # Check for verification of data sources
        unverified_sources = []
        for entry in audit_data:
            metadata = entry.get('metadata')
            if metadata is None:
                unverified_sources.append(entry)
            elif not metadata.get('source_verified', False):
                unverified_sources.append(entry)
        
        if unverified_sources:
            findings.append({
                'type': 'SEC_SOURCE_VERIFICATION',
                'severity': 'HIGH',
                'description': f'{len(unverified_sources)} actions use unverified data sources',
                'recommendation': 'Implement source verification procedures'
            })
        
        return findings
    
    def _analyze_internal_controls(self, audit_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze internal control effectiveness."""
        findings = []
        
        # Check error rates by agent
        agent_errors = {}
        agent_totals = {}
        
        for entry in audit_data:
            agent_id = entry['agent_id']
            if agent_id not in agent_totals:
                agent_totals[agent_id] = 0
                agent_errors[agent_id] = 0
            
            agent_totals[agent_id] += 1
            if entry['status'] == 'ERROR':
                agent_errors[agent_id] += 1
        
        # Flag agents with high error rates
        for agent_id in agent_totals:
            error_rate = agent_errors[agent_id] / agent_totals[agent_id]
            if error_rate > 0.05:  # More than 5% error rate
                findings.append({
                    'type': 'INTERNAL_HIGH_ERROR_RATE',
                    'severity': 'MEDIUM',
                    'description': f'Agent {agent_id} has {error_rate:.1%} error rate',
                    'recommendation': 'Review and improve agent error handling'
                })
        
        return findings
    
    def _generate_recommendations(self, report_type: str, findings: List[Dict[str, Any]], compliance_score: float) -> List[str]:
        """Generate recommendations based on findings and compliance score."""
        recommendations = []
        
        # General recommendations based on compliance score
        if compliance_score < 95:
            recommendations.append("Improve overall system reliability to achieve >95% success rate")
        
        if compliance_score < 90:
            recommendations.append("Conduct immediate review of failed operations and implement corrective measures")
        
        # Specific recommendations based on findings
        high_severity_findings = [f for f in findings if f.get('severity') == 'HIGH']
        if high_severity_findings:
            recommendations.append("Address all high-severity compliance issues immediately")
        
        # Report-type specific recommendations
        if report_type == 'sox_compliance':
            recommendations.append("Implement quarterly SOX compliance reviews")
            recommendations.append("Enhance segregation of duties controls")
        elif report_type == 'gdpr_compliance':
            recommendations.append("Conduct annual GDPR compliance assessment")
            recommendations.append("Implement data minimization practices")
        
        return recommendations
    
    def export_report(self, report: ComplianceReport, output_path: str, format: str = 'json') -> str:
        """
        Export compliance report in specified format.
        
        Args:
            report: ComplianceReport to export
            output_path: Output file path
            format: Export format (json, xml, csv, html)
            
        Returns:
            str: Path to exported file
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        if format.lower() == 'json':
            return self._export_json(report, output_file)
        elif format.lower() == 'xml':
            return self._export_xml(report, output_file)
        elif format.lower() == 'csv':
            return self._export_csv(report, output_file)
        elif format.lower() == 'html':
            return self._export_html(report, output_file)
        else:
            raise ValueError(f"Unsupported export format: {format}")
    
    def _export_json(self, report: ComplianceReport, output_file: Path) -> str:
        """Export report as JSON."""
        report_dict = {
            'report_id': report.report_id,
            'report_type': report.report_type,
            'generated_at': report.generated_at.isoformat(),
            'period_start': report.period_start.isoformat(),
            'period_end': report.period_end.isoformat(),
            'metrics': {
                'total_actions': report.total_actions,
                'successful_actions': report.successful_actions,
                'failed_actions': report.failed_actions,
                'compliance_score': report.compliance_score
            },
            'scope': {
                'agents_involved': report.agents_involved,
                'deals_analyzed': report.deals_analyzed
            },
            'findings': report.findings,
            'recommendations': report.recommendations
        }
        
        with open(output_file.with_suffix('.json'), 'w') as f:
            json.dump(report_dict, f, indent=2)
        
        return str(output_file.with_suffix('.json'))
    
    def _export_xml(self, report: ComplianceReport, output_file: Path) -> str:
        """Export report as XML."""
        root = ET.Element('ComplianceReport')
        root.set('id', report.report_id)
        root.set('type', report.report_type)
        root.set('generated', report.generated_at.isoformat())
        
        # Period
        period = ET.SubElement(root, 'Period')
        period.set('start', report.period_start.isoformat())
        period.set('end', report.period_end.isoformat())
        
        # Metrics
        metrics = ET.SubElement(root, 'Metrics')
        ET.SubElement(metrics, 'TotalActions').text = str(report.total_actions)
        ET.SubElement(metrics, 'SuccessfulActions').text = str(report.successful_actions)
        ET.SubElement(metrics, 'FailedActions').text = str(report.failed_actions)
        ET.SubElement(metrics, 'ComplianceScore').text = str(report.compliance_score)
        
        # Findings
        findings_elem = ET.SubElement(root, 'Findings')
        for finding in report.findings:
            finding_elem = ET.SubElement(findings_elem, 'Finding')
            finding_elem.set('type', finding.get('type', ''))
            finding_elem.set('severity', finding.get('severity', ''))
            ET.SubElement(finding_elem, 'Description').text = finding.get('description', '')
            ET.SubElement(finding_elem, 'Recommendation').text = finding.get('recommendation', '')
        
        # Recommendations
        recommendations_elem = ET.SubElement(root, 'Recommendations')
        for rec in report.recommendations:
            ET.SubElement(recommendations_elem, 'Recommendation').text = rec
        
        tree = ET.ElementTree(root)
        xml_file = output_file.with_suffix('.xml')
        tree.write(xml_file, encoding='utf-8', xml_declaration=True)
        
        return str(xml_file)
    
    def _export_csv(self, report: ComplianceReport, output_file: Path) -> str:
        """Export report as CSV (findings summary)."""
        csv_file = output_file.with_suffix('.csv')
        
        with open(csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            
            # Header
            writer.writerow(['Report ID', 'Type', 'Generated', 'Period Start', 'Period End', 
                           'Total Actions', 'Successful', 'Failed', 'Compliance Score'])
            
            # Summary row
            writer.writerow([
                report.report_id, report.report_type, report.generated_at.isoformat(),
                report.period_start.isoformat(), report.period_end.isoformat(),
                report.total_actions, report.successful_actions, report.failed_actions,
                f"{report.compliance_score:.2f}%"
            ])
            
            # Empty row
            writer.writerow([])
            
            # Findings header
            writer.writerow(['Finding Type', 'Severity', 'Description', 'Recommendation'])
            
            # Findings
            for finding in report.findings:
                writer.writerow([
                    finding.get('type', ''),
                    finding.get('severity', ''),
                    finding.get('description', ''),
                    finding.get('recommendation', '')
                ])
        
        return str(csv_file)
    
    def _export_html(self, report: ComplianceReport, output_file: Path) -> str:
        """Export report as HTML."""
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Compliance Report - {report.report_id}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .header {{ background-color: #f0f0f0; padding: 20px; border-radius: 5px; }}
                .metrics {{ display: flex; justify-content: space-around; margin: 20px 0; }}
                .metric {{ text-align: center; padding: 15px; background-color: #e8f4f8; border-radius: 5px; }}
                .findings {{ margin: 20px 0; }}
                .finding {{ margin: 10px 0; padding: 15px; border-left: 4px solid #ccc; }}
                .finding.high {{ border-left-color: #ff4444; }}
                .finding.medium {{ border-left-color: #ffaa00; }}
                .finding.low {{ border-left-color: #44ff44; }}
                .recommendations {{ background-color: #f9f9f9; padding: 20px; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Compliance Report</h1>
                <p><strong>Report ID:</strong> {report.report_id}</p>
                <p><strong>Type:</strong> {report.report_type}</p>
                <p><strong>Generated:</strong> {report.generated_at.strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p><strong>Period:</strong> {report.period_start.strftime('%Y-%m-%d')} to {report.period_end.strftime('%Y-%m-%d')}</p>
            </div>
            
            <div class="metrics">
                <div class="metric">
                    <h3>{report.total_actions}</h3>
                    <p>Total Actions</p>
                </div>
                <div class="metric">
                    <h3>{report.successful_actions}</h3>
                    <p>Successful</p>
                </div>
                <div class="metric">
                    <h3>{report.failed_actions}</h3>
                    <p>Failed</p>
                </div>
                <div class="metric">
                    <h3>{report.compliance_score:.1f}%</h3>
                    <p>Compliance Score</p>
                </div>
            </div>
            
            <h2>Findings</h2>
            <div class="findings">
        """
        
        for finding in report.findings:
            severity_class = finding.get('severity', 'low').lower()
            html_content += f"""
                <div class="finding {severity_class}">
                    <h4>{finding.get('type', 'Unknown')}</h4>
                    <p><strong>Severity:</strong> {finding.get('severity', 'Unknown')}</p>
                    <p><strong>Description:</strong> {finding.get('description', '')}</p>
                    <p><strong>Recommendation:</strong> {finding.get('recommendation', '')}</p>
                </div>
            """
        
        html_content += """
            </div>
            
            <h2>Recommendations</h2>
            <div class="recommendations">
                <ul>
        """
        
        for rec in report.recommendations:
            html_content += f"<li>{rec}</li>"
        
        html_content += """
                </ul>
            </div>
        </body>
        </html>
        """
        
        html_file = output_file.with_suffix('.html')
        with open(html_file, 'w') as f:
            f.write(html_content)
        
        return str(html_file)
    
    def generate_regulatory_summary(self, report: ComplianceReport) -> Dict[str, Any]:
        """
        Generate a regulatory summary suitable for external reporting.
        
        Args:
            report: ComplianceReport to summarize
            
        Returns:
            Dict containing regulatory summary
        """
        return {
            'executive_summary': {
                'report_period': f"{report.period_start.strftime('%Y-%m-%d')} to {report.period_end.strftime('%Y-%m-%d')}",
                'overall_compliance_score': f"{report.compliance_score:.1f}%",
                'total_transactions_reviewed': report.total_actions,
                'success_rate': f"{(report.successful_actions / report.total_actions * 100):.1f}%" if report.total_actions > 0 else "N/A",
                'critical_findings': len([f for f in report.findings if f.get('severity') == 'HIGH'])
            },
            'scope_of_review': {
                'deals_analyzed': len(report.deals_analyzed),
                'agents_involved': len(report.agents_involved),
                'review_methodology': 'Automated audit trail analysis with manual validation'
            },
            'key_findings': [
                {
                    'category': finding.get('type', ''),
                    'risk_level': finding.get('severity', ''),
                    'description': finding.get('description', ''),
                    'management_action': finding.get('recommendation', '')
                }
                for finding in report.findings[:10]  # Top 10 findings
            ],
            'management_response': {
                'action_plan': report.recommendations,
                'target_completion': (datetime.now() + timedelta(days=90)).strftime('%Y-%m-%d'),
                'responsible_party': 'Compliance Team'
            }
        }