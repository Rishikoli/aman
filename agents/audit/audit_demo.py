"""
Demonstration of the Audit Trail and Compliance System
Shows how to integrate audit logging into M&A due diligence operations.
"""

import os
import json
from datetime import datetime, timedelta
from .audit_logger import AuditLogger
from .audit_context import AuditContext, get_audit_context
from .compliance_reporter import ComplianceReporter

def demo_audit_integration():
    """Demonstrate audit logging integration with M&A operations."""
    print("=== M&A Due Diligence Audit Trail Demo ===\n")
    
    # Initialize audit system
    audit_context = get_audit_context()
    audit_logger = audit_context.audit_logger
    compliance_reporter = ComplianceReporter(audit_logger)
    
    print("1. Simulating M&A Due Diligence Operations with Audit Logging\n")
    
    # Simulate Finance Agent operations
    print("Finance Agent: Analyzing target company financials...")
    with audit_context.log_operation(
        agent_id="finance_agent",
        action_type="FINANCIAL_ANALYSIS",
        action_description="Comprehensive financial analysis of target company",
        deal_id="deal_abc_corp_acquisition",
        user_id="analyst_john",
        session_id="session_20241201_001",
        input_data={
            "company_ticker": "ABC",
            "analysis_type": "comprehensive",
            "data_sources": ["10-K", "10-Q", "earnings_calls"]
        },
        metadata={
            "model_version": "v2.1",
            "confidence_threshold": 0.85,
            "regulatory_framework": "SEC"
        }
    ) as audit_log:
        # Simulate financial analysis
        financial_results = {
            "debt_to_equity": 0.45,
            "current_ratio": 1.8,
            "roe": 0.12,
            "revenue_growth": 0.08,
            "risk_score": 0.25,
            "anomalies_detected": []
        }
        
        audit_log.set_output(financial_results)
        audit_log.add_lineage(
            source_type="SEC_API",
            source_id="edgar_database",
            transformation_type="FINANCIAL_RATIO_CALCULATION",
            description="Calculated key financial ratios from SEC filings",
            data_quality_score=0.95
        )
        audit_log.add_decision(
            decision_type="RISK_ASSESSMENT",
            criteria="Financial ratios within industry benchmarks",
            confidence=0.92,
            alternatives=["high_risk", "medium_risk", "low_risk"],
            risk_assessment={"probability": 0.25, "impact": "medium"}
        )
    
    print("✓ Finance Agent analysis completed with full audit trail\n")
    
    # Simulate Legal Agent operations
    print("Legal Agent: Reviewing legal documents and compliance...")
    with audit_context.log_operation(
        agent_id="legal_agent",
        action_type="LEGAL_COMPLIANCE_REVIEW",
        action_description="Review target company legal documents and regulatory compliance",
        deal_id="deal_abc_corp_acquisition",
        user_id="legal_counsel_sarah",
        input_data={
            "documents": ["articles_of_incorporation", "bylaws", "material_contracts"],
            "jurisdictions": ["Delaware", "California", "New York"]
        }
    ) as audit_log:
        # Simulate legal analysis
        legal_results = {
            "compliance_score": 0.88,
            "red_flags": ["pending_litigation_case_123"],
            "regulatory_issues": [],
            "contract_risks": ["termination_clause_concern"]
        }
        
        audit_log.set_output(legal_results)
        audit_log.add_lineage(
            source_type="DOCUMENT_REPOSITORY",
            source_id="legal_docs_vault",
            transformation_type="LEGAL_ENTITY_EXTRACTION",
            description="Extracted legal entities and compliance status from documents"
        )
        audit_log.add_decision(
            decision_type="COMPLIANCE_ASSESSMENT",
            criteria="Regulatory compliance across multiple jurisdictions",
            confidence=0.88
        )
    
    print("✓ Legal Agent review completed with audit trail\n")
    
    # Simulate error scenario
    print("Operations Agent: Attempting geopolitical risk analysis...")
    try:
        with audit_context.log_operation(
            agent_id="operations_agent",
            action_type="GEOPOLITICAL_RISK_ANALYSIS",
            action_description="Analyze geopolitical risks for target company operations",
            deal_id="deal_abc_corp_acquisition",
            user_id="risk_analyst_mike",
            input_data={"regions": ["EMEA", "APAC"], "risk_factors": ["sanctions", "trade_wars"]}
        ) as audit_log:
            # Simulate an error
            raise ConnectionError("Unable to connect to World Bank API")
    except ConnectionError as e:
        print(f"✗ Operations Agent encountered error: {e}")
        print("✓ Error automatically logged in audit trail\n")
    
    # Simulate system configuration change
    print("System Administrator: Updating agent configuration...")
    audit_logger.log_system_event(
        event_type="AGENT_CONFIGURATION_UPDATE",
        event_description="Updated risk assessment thresholds for all agents",
        component="risk_assessment_engine",
        configuration_before={"high_risk_threshold": 0.7, "medium_risk_threshold": 0.4},
        configuration_after={"high_risk_threshold": 0.75, "medium_risk_threshold": 0.45},
        triggered_by="admin_alice"
    )
    print("✓ System configuration change logged\n")
    
    print("2. Querying Audit Trail\n")
    
    # Query recent audit entries
    recent_entries = compliance_reporter.query_audit_trail(
        start_date=datetime.now() - timedelta(hours=1)
    )
    
    print(f"Found {len(recent_entries)} recent audit entries:")
    for entry in recent_entries[:3]:  # Show first 3
        print(f"  - {entry['timestamp']}: {entry['agent_id']} - {entry['action_type']} ({entry['status']})")
    print()
    
    # Query by deal
    deal_entries = compliance_reporter.query_audit_trail(
        deal_id="deal_abc_corp_acquisition"
    )
    print(f"Found {len(deal_entries)} entries for deal 'deal_abc_corp_acquisition'")
    print()
    
    print("3. Generating Compliance Reports\n")
    
    # Generate SOX compliance report
    print("Generating SOX Compliance Report...")
    sox_report = compliance_reporter.generate_compliance_report(
        report_type="sox_compliance",
        start_date=datetime.now() - timedelta(days=1),
        end_date=datetime.now()
    )
    
    print(f"SOX Compliance Report Generated:")
    print(f"  - Report ID: {sox_report.report_id}")
    print(f"  - Total Actions: {sox_report.total_actions}")
    print(f"  - Success Rate: {sox_report.successful_actions}/{sox_report.total_actions}")
    print(f"  - Compliance Score: {sox_report.compliance_score:.1f}%")
    print(f"  - Findings: {len(sox_report.findings)}")
    print(f"  - Recommendations: {len(sox_report.recommendations)}")
    print()
    
    # Export report in multiple formats
    print("4. Exporting Compliance Reports\n")
    
    reports_dir = "compliance_reports"
    os.makedirs(reports_dir, exist_ok=True)
    
    # Export as JSON
    json_file = compliance_reporter.export_report(
        sox_report, 
        f"{reports_dir}/sox_compliance_report", 
        "json"
    )
    print(f"✓ JSON report exported: {json_file}")
    
    # Export as HTML
    html_file = compliance_reporter.export_report(
        sox_report, 
        f"{reports_dir}/sox_compliance_report", 
        "html"
    )
    print(f"✓ HTML report exported: {html_file}")
    
    # Export as CSV
    csv_file = compliance_reporter.export_report(
        sox_report, 
        f"{reports_dir}/sox_compliance_report", 
        "csv"
    )
    print(f"✓ CSV report exported: {csv_file}")
    print()
    
    # Generate regulatory summary
    print("5. Regulatory Summary\n")
    regulatory_summary = compliance_reporter.generate_regulatory_summary(sox_report)
    
    print("Executive Summary:")
    exec_summary = regulatory_summary['executive_summary']
    for key, value in exec_summary.items():
        print(f"  - {key.replace('_', ' ').title()}: {value}")
    print()
    
    print("Key Findings:")
    for i, finding in enumerate(regulatory_summary['key_findings'][:3], 1):
        print(f"  {i}. {finding['category']} ({finding['risk_level']})")
        print(f"     {finding['description']}")
    print()
    
    print("6. Audit Trail Integrity Verification\n")
    
    # Verify audit trail integrity
    integrity_results = audit_logger.verify_log_integrity()
    
    print("Audit Trail Integrity Check:")
    print(f"  - Total Logs: {integrity_results['total_logs']}")
    print(f"  - Verified Logs: {integrity_results['verified_logs']}")
    print(f"  - Integrity Valid: {integrity_results['is_valid']}")
    print(f"  - Violations: {len(integrity_results['integrity_violations'])}")
    
    if integrity_results['integrity_violations']:
        print("  Integrity Violations:")
        for violation in integrity_results['integrity_violations']:
            print(f"    - Log {violation['log_id']}: {violation['issue']}")
    print()
    
    print("=== Demo Complete ===")
    print("\nThe audit trail and compliance system provides:")
    print("✓ Immutable audit logging for all agent operations")
    print("✓ Data lineage tracking for transparency")
    print("✓ Agent decision logging for explainability")
    print("✓ Comprehensive compliance reporting")
    print("✓ Multiple export formats (JSON, XML, CSV, HTML)")
    print("✓ Regulatory framework adaptation")
    print("✓ Audit trail integrity verification")
    print("✓ Automated compliance analysis and recommendations")

def demo_integration_example():
    """Show how to integrate audit logging into existing agent code."""
    print("\n=== Integration Example ===\n")
    
    print("Example: Integrating audit logging into a Finance Agent function\n")
    
    code_example = '''
# Before: Regular agent function
def analyze_financial_ratios(company_data):
    ratios = calculate_ratios(company_data)
    risk_score = assess_risk(ratios)
    return {"ratios": ratios, "risk_score": risk_score}

# After: With audit logging integration
from agents.audit.audit_context import get_audit_context

def analyze_financial_ratios(company_data, deal_id=None, user_id=None):
    audit_context = get_audit_context()
    
    with audit_context.log_operation(
        agent_id="finance_agent",
        action_type="FINANCIAL_RATIO_ANALYSIS",
        action_description="Calculate and analyze financial ratios",
        deal_id=deal_id,
        user_id=user_id,
        input_data={"company_ticker": company_data.get("ticker")},
        metadata={"analysis_version": "v2.1"}
    ) as audit_log:
        
        # Original business logic
        ratios = calculate_ratios(company_data)
        risk_score = assess_risk(ratios)
        
        result = {"ratios": ratios, "risk_score": risk_score}
        
        # Add audit information
        audit_log.set_output(result)
        audit_log.add_lineage(
            source_type="API",
            source_id="financial_data_provider",
            transformation_type="RATIO_CALCULATION",
            description="Calculated financial ratios from raw financial data"
        )
        audit_log.add_decision(
            decision_type="RISK_CLASSIFICATION",
            criteria="Industry benchmark comparison",
            confidence=0.85 if risk_score < 0.5 else 0.65
        )
        
        return result
    '''
    
    print(code_example)
    print("\nKey Benefits of This Integration:")
    print("• Minimal code changes required")
    print("• Automatic timing and error handling")
    print("• Complete audit trail for compliance")
    print("• Data lineage tracking")
    print("• Decision transparency")
    print("• No impact on existing business logic")

if __name__ == "__main__":
    demo_audit_integration()
    demo_integration_example()