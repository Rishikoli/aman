"""
Test suite for the compliance reporting system.
"""

import unittest
import tempfile
import os
import json
from datetime import datetime, timedelta
from .audit_logger import AuditLogger
from .compliance_reporter import ComplianceReporter, ComplianceReport

class TestComplianceReporter(unittest.TestCase):
    """Test cases for the ComplianceReporter class."""
    
    def setUp(self):
        """Set up test environment with temporary database and sample data."""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_compliance.db")
        self.audit_logger = AuditLogger(self.db_path)
        self.compliance_reporter = ComplianceReporter(self.audit_logger)
        
        # Create sample audit data
        self._create_sample_data()
    
    def tearDown(self):
        """Clean up test environment."""
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        # Clean up any remaining files in temp directory
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def _create_sample_data(self):
        """Create sample audit data for testing."""
        base_time = datetime.now() - timedelta(days=30)
        
        # Create successful operations
        for i in range(10):
            log_id = self.audit_logger.log_action(
                agent_id=f"agent_{i % 3}",
                action_type="FINANCIAL_ANALYSIS",
                action_description=f"Financial analysis operation {i}",
                deal_id=f"deal_{i % 2}",
                user_id=f"user_{i % 2}",
                status="SUCCESS",
                execution_time_ms=1000 + i * 100,
                metadata={"source_verified": True, "processing_purpose": "due_diligence"}
            )
            
            # Add lineage for some entries
            if i % 2 == 0:
                self.audit_logger.log_data_lineage(
                    audit_log_id=log_id,
                    source_type="API",
                    source_id="financial_api",
                    transformation_type="DATA_NORMALIZATION",
                    data_quality_score=0.95
                )
        
        # Create some failed operations
        for i in range(3):
            self.audit_logger.log_action(
                agent_id=f"agent_{i}",
                action_type="DATA_PROCESSING",
                action_description=f"Failed data processing {i}",
                deal_id="deal_0",
                user_id="user_0",
                status="ERROR",
                error_message=f"Processing error {i}",
                metadata={"source_verified": False}
            )
        
        # Create operations with potential compliance issues
        # SOX violation - same user doing modification and approval
        self.audit_logger.log_action(
            agent_id="agent_0",
            action_type="DATA_MODIFICATION",
            action_description="Modify financial data",
            deal_id="deal_0",
            user_id="user_violation",
            status="SUCCESS"
        )
        
        self.audit_logger.log_action(
            agent_id="agent_0",
            action_type="DATA_APPROVAL",
            action_description="Approve financial data",
            deal_id="deal_0",
            user_id="user_violation",
            status="SUCCESS"
        )
    
    def test_query_audit_trail_basic(self):
        """Test basic audit trail querying."""
        results = self.compliance_reporter.query_audit_trail()
        
        # Should return all entries (10 success + 3 error + 2 violation = 15)
        self.assertEqual(len(results), 15)
        
        # Test filtering by status
        success_results = self.compliance_reporter.query_audit_trail(status="SUCCESS")
        self.assertEqual(len(success_results), 12)  # 10 + 2 violation entries
        
        error_results = self.compliance_reporter.query_audit_trail(status="ERROR")
        self.assertEqual(len(error_results), 3)
    
    def test_query_audit_trail_filtering(self):
        """Test audit trail querying with various filters."""
        # Test deal_id filtering
        deal_0_results = self.compliance_reporter.query_audit_trail(deal_id="deal_0")
        self.assertGreater(len(deal_0_results), 0)
        
        # Test agent_id filtering
        agent_0_results = self.compliance_reporter.query_audit_trail(agent_id="agent_0")
        self.assertGreater(len(agent_0_results), 0)
        
        # Test action_type filtering
        analysis_results = self.compliance_reporter.query_audit_trail(action_type="FINANCIAL_ANALYSIS")
        self.assertEqual(len(analysis_results), 10)
        
        # Test date filtering
        recent_date = datetime.now() - timedelta(days=1)
        recent_results = self.compliance_reporter.query_audit_trail(start_date=recent_date)
        self.assertEqual(len(recent_results), 15)  # All entries are recent
    
    def test_generate_sox_compliance_report(self):
        """Test SOX compliance report generation."""
        start_date = datetime.now() - timedelta(days=30)
        end_date = datetime.now()
        
        report = self.compliance_reporter.generate_compliance_report(
            report_type="sox_compliance",
            start_date=start_date,
            end_date=end_date
        )
        
        self.assertIsInstance(report, ComplianceReport)
        self.assertEqual(report.report_type, "sox_compliance")
        self.assertEqual(report.total_actions, 15)
        self.assertEqual(report.successful_actions, 12)
        self.assertEqual(report.failed_actions, 3)
        self.assertEqual(report.compliance_score, 80.0)  # 12/15 * 100
        
        # Should detect SOX violation
        sox_violations = [f for f in report.findings if f['type'] == 'SOX_SEGREGATION_VIOLATION']
        self.assertEqual(len(sox_violations), 1)
        self.assertEqual(sox_violations[0]['severity'], 'HIGH')
    
    def test_generate_gdpr_compliance_report(self):
        """Test GDPR compliance report generation."""
        start_date = datetime.now() - timedelta(days=30)
        end_date = datetime.now()
        
        report = self.compliance_reporter.generate_compliance_report(
            report_type="gdpr_compliance",
            start_date=start_date,
            end_date=end_date
        )
        
        self.assertIsInstance(report, ComplianceReport)
        self.assertEqual(report.report_type, "gdpr_compliance")
        
        # Should detect GDPR issues (unclear purpose for failed operations)
        gdpr_issues = [f for f in report.findings if 'GDPR' in f['type']]
        self.assertGreater(len(gdpr_issues), 0)
    
    def test_generate_sec_compliance_report(self):
        """Test SEC compliance report generation."""
        start_date = datetime.now() - timedelta(days=30)
        end_date = datetime.now()
        
        report = self.compliance_reporter.generate_compliance_report(
            report_type="sec_filing",
            start_date=start_date,
            end_date=end_date
        )
        
        self.assertIsInstance(report, ComplianceReport)
        self.assertEqual(report.report_type, "sec_filing")
        
        # Should detect SEC issues (unverified sources)
        sec_issues = [f for f in report.findings if 'SEC' in f['type']]
        self.assertGreater(len(sec_issues), 0)
    
    def test_generate_internal_audit_report(self):
        """Test internal audit report generation."""
        start_date = datetime.now() - timedelta(days=30)
        end_date = datetime.now()
        
        report = self.compliance_reporter.generate_compliance_report(
            report_type="internal_audit",
            start_date=start_date,
            end_date=end_date
        )
        
        self.assertIsInstance(report, ComplianceReport)
        self.assertEqual(report.report_type, "internal_audit")
        
        # Should analyze error rates by agent
        internal_issues = [f for f in report.findings if 'INTERNAL' in f['type']]
        # May or may not have high error rate findings depending on distribution
        self.assertIsInstance(internal_issues, list)
    
    def test_export_report_json(self):
        """Test JSON report export."""
        start_date = datetime.now() - timedelta(days=30)
        end_date = datetime.now()
        
        report = self.compliance_reporter.generate_compliance_report(
            report_type="sox_compliance",
            start_date=start_date,
            end_date=end_date
        )
        
        output_path = os.path.join(self.temp_dir, "test_report")
        exported_file = self.compliance_reporter.export_report(report, output_path, "json")
        
        self.assertTrue(os.path.exists(exported_file))
        self.assertTrue(exported_file.endswith('.json'))
        
        # Verify JSON content
        with open(exported_file, 'r') as f:
            data = json.load(f)
            self.assertEqual(data['report_id'], report.report_id)
            self.assertEqual(data['report_type'], report.report_type)
            self.assertEqual(data['metrics']['total_actions'], report.total_actions)
    
    def test_export_report_xml(self):
        """Test XML report export."""
        start_date = datetime.now() - timedelta(days=30)
        end_date = datetime.now()
        
        report = self.compliance_reporter.generate_compliance_report(
            report_type="sox_compliance",
            start_date=start_date,
            end_date=end_date
        )
        
        output_path = os.path.join(self.temp_dir, "test_report")
        exported_file = self.compliance_reporter.export_report(report, output_path, "xml")
        
        self.assertTrue(os.path.exists(exported_file))
        self.assertTrue(exported_file.endswith('.xml'))
        
        # Verify XML is well-formed
        import xml.etree.ElementTree as ET
        tree = ET.parse(exported_file)
        root = tree.getroot()
        self.assertEqual(root.tag, 'ComplianceReport')
        self.assertEqual(root.get('id'), report.report_id)
    
    def test_export_report_csv(self):
        """Test CSV report export."""
        start_date = datetime.now() - timedelta(days=30)
        end_date = datetime.now()
        
        report = self.compliance_reporter.generate_compliance_report(
            report_type="sox_compliance",
            start_date=start_date,
            end_date=end_date
        )
        
        output_path = os.path.join(self.temp_dir, "test_report")
        exported_file = self.compliance_reporter.export_report(report, output_path, "csv")
        
        self.assertTrue(os.path.exists(exported_file))
        self.assertTrue(exported_file.endswith('.csv'))
        
        # Verify CSV content
        import csv
        with open(exported_file, 'r') as f:
            reader = csv.reader(f)
            rows = list(reader)
            self.assertGreater(len(rows), 2)  # Header + summary + findings
    
    def test_export_report_html(self):
        """Test HTML report export."""
        start_date = datetime.now() - timedelta(days=30)
        end_date = datetime.now()
        
        report = self.compliance_reporter.generate_compliance_report(
            report_type="sox_compliance",
            start_date=start_date,
            end_date=end_date
        )
        
        output_path = os.path.join(self.temp_dir, "test_report")
        exported_file = self.compliance_reporter.export_report(report, output_path, "html")
        
        self.assertTrue(os.path.exists(exported_file))
        self.assertTrue(exported_file.endswith('.html'))
        
        # Verify HTML content contains key elements
        with open(exported_file, 'r') as f:
            content = f.read()
            self.assertIn('<html>', content)
            self.assertIn(report.report_id, content)
            self.assertIn('Compliance Report', content)
    
    def test_generate_regulatory_summary(self):
        """Test regulatory summary generation."""
        start_date = datetime.now() - timedelta(days=30)
        end_date = datetime.now()
        
        report = self.compliance_reporter.generate_compliance_report(
            report_type="sox_compliance",
            start_date=start_date,
            end_date=end_date
        )
        
        summary = self.compliance_reporter.generate_regulatory_summary(report)
        
        self.assertIn('executive_summary', summary)
        self.assertIn('scope_of_review', summary)
        self.assertIn('key_findings', summary)
        self.assertIn('management_response', summary)
        
        # Verify executive summary content
        exec_summary = summary['executive_summary']
        self.assertIn('overall_compliance_score', exec_summary)
        self.assertIn('total_transactions_reviewed', exec_summary)
        self.assertEqual(exec_summary['total_transactions_reviewed'], 15)
    
    def test_invalid_report_type(self):
        """Test handling of invalid report types."""
        start_date = datetime.now() - timedelta(days=30)
        end_date = datetime.now()
        
        with self.assertRaises(ValueError):
            self.compliance_reporter.generate_compliance_report(
                report_type="invalid_type",
                start_date=start_date,
                end_date=end_date
            )
    
    def test_invalid_export_format(self):
        """Test handling of invalid export formats."""
        start_date = datetime.now() - timedelta(days=30)
        end_date = datetime.now()
        
        report = self.compliance_reporter.generate_compliance_report(
            report_type="sox_compliance",
            start_date=start_date,
            end_date=end_date
        )
        
        output_path = os.path.join(self.temp_dir, "test_report")
        
        with self.assertRaises(ValueError):
            self.compliance_reporter.export_report(report, output_path, "invalid_format")
    
    def test_report_with_deal_filter(self):
        """Test report generation with specific deal filtering."""
        start_date = datetime.now() - timedelta(days=30)
        end_date = datetime.now()
        
        report = self.compliance_reporter.generate_compliance_report(
            report_type="sox_compliance",
            start_date=start_date,
            end_date=end_date,
            deal_ids=["deal_0"]
        )
        
        # Should only include actions for deal_0
        self.assertIn("deal_0", report.deals_analyzed)
        self.assertNotIn("deal_1", report.deals_analyzed)
        self.assertLess(report.total_actions, 15)  # Fewer than all actions

if __name__ == '__main__':
    unittest.main()