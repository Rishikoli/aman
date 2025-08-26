"""
Comprehensive test for the Legal Agent
Tests the complete legal analysis workflow
"""

import sys
import logging
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from legal.legal_agent import LegalAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def test_legal_agent_comprehensive():
    """Test comprehensive legal analysis"""
    print("\n" + "="*80)
    print("TESTING COMPREHENSIVE LEGAL AGENT ANALYSIS")
    print("="*80)
    
    agent = LegalAgent()
    
    # Test with a well-known public company
    test_ticker = "AAPL"
    test_company_name = "Apple Inc"
    
    try:
        print(f"\nTesting comprehensive legal analysis for {test_ticker}...")
        
        results = agent.analyze_company_legal_profile(
            test_ticker, 
            test_company_name, 
            include_ai_analysis=True
        )
        
        if results and not results.get('error'):
            print("✅ Comprehensive legal analysis successful!")
            
            # Display key results
            print(f"\nAnalysis Components: {', '.join(results.get('analysis_components', []))}")
            
            # Overall assessment
            overall_assessment = results.get('overall_assessment', {})
            print(f"Overall Score: {overall_assessment.get('overall_score', 0)}/100")
            print(f"Assessment Level: {overall_assessment.get('assessment_level', 'unknown')}")
            print(f"Recommendation: {overall_assessment.get('recommendation', 'unknown')}")
            
            # Risk assessment
            risk_assessment = results.get('risk_assessment', {})
            print(f"Risk Level: {risk_assessment.get('risk_level', 'unknown')}")
            print(f"Critical Risks: {len(risk_assessment.get('critical_risks', []))}")
            
            # Compliance status
            compliance_status = results.get('compliance_status', {})
            print(f"Compliance Status: {compliance_status.get('overall_status', 'unknown')}")
            print(f"Compliance Score: {compliance_status.get('compliance_score', 0)}/100")
            
            # Data sources
            legal_intelligence = results.get('legal_intelligence', {})
            data_sources = legal_intelligence.get('data_sources', [])
            print(f"Data Sources Used: {', '.join(data_sources) if data_sources else 'None'}")
            
            # Document analysis
            document_analysis = results.get('document_analysis', {})
            if document_analysis and not document_analysis.get('error'):
                docs_analyzed = document_analysis.get('documents_analyzed', 0)
                print(f"Documents Analyzed with AI: {docs_analyzed}")
            
            # Recommendations
            recommendations = results.get('recommendations', [])
            print(f"\nTop Recommendations ({len(recommendations)}):")
            for i, rec in enumerate(recommendations[:5], 1):
                print(f"  {i}. {rec}")
            
        else:
            print(f"❌ Comprehensive legal analysis failed: {results.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Legal agent test error: {e}")

def test_legal_risk_summary():
    """Test legal risk summary functionality"""
    print("\n" + "="*80)
    print("TESTING LEGAL RISK SUMMARY")
    print("="*80)
    
    agent = LegalAgent()
    
    test_ticker = "MSFT"
    test_company_name = "Microsoft Corporation"
    
    try:
        print(f"\nTesting legal risk summary for {test_ticker}...")
        
        summary = agent.get_legal_risk_summary(test_ticker, test_company_name)
        
        if summary and not summary.get('error'):
            print("✅ Legal risk summary generation successful!")
            
            print(f"Overall Score: {summary.get('overall_score', 0)}/100")
            print(f"Assessment Level: {summary.get('assessment_level', 'unknown')}")
            print(f"Risk Level: {summary.get('risk_level', 'unknown')}")
            print(f"Compliance Status: {summary.get('compliance_status', 'unknown')}")
            print(f"Critical Risks: {summary.get('critical_risks', 0)}")
            print(f"Data Sources: {summary.get('data_sources', 0)}")
            print(f"Requires Immediate Attention: {summary.get('requires_immediate_attention', False)}")
            
            top_recommendations = summary.get('top_recommendations', [])
            if top_recommendations:
                print(f"\nTop Recommendations:")
                for i, rec in enumerate(top_recommendations, 1):
                    print(f"  {i}. {rec}")
            
        else:
            print(f"❌ Legal risk summary failed: {summary.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Legal risk summary test error: {e}")

def test_ai_document_analysis():
    """Test AI document analysis with sample legal text"""
    print("\n" + "="*80)
    print("TESTING AI DOCUMENT ANALYSIS")
    print("="*80)
    
    agent = LegalAgent()
    
    # Sample legal text for testing
    sample_legal_text = """
    LEGAL PROCEEDINGS
    
    The Company is subject to various legal proceedings and claims that arise in the ordinary course of business. 
    These matters include intellectual property disputes, employment-related claims, and regulatory investigations.
    
    In March 2023, the Company received a subpoena from the Securities and Exchange Commission requesting documents 
    related to certain accounting practices. The Company is cooperating fully with this investigation.
    
    The Company is also defending against a patent infringement lawsuit filed by TechCorp Inc. in the U.S. District 
    Court for the Northern District of California. The plaintiff seeks damages of approximately $50 million and 
    injunctive relief. The Company believes the claims are without merit and intends to defend vigorously.
    
    Additionally, the Company has been named as a defendant in a class action lawsuit alleging violations of 
    federal securities laws. The lawsuit seeks unspecified monetary damages and is in the early stages of litigation.
    
    While the Company believes it has meritorious defenses to these claims, litigation is inherently uncertain, 
    and adverse outcomes could have a material adverse effect on the Company's financial condition and results of operations.
    """
    
    try:
        print("\nTesting AI analysis on sample legal text...")
        
        # Use the AI analyzer directly for testing
        analysis = agent.ai_analyzer.analyze_legal_document_comprehensive(
            sample_legal_text,
            document_type="Legal Proceedings Section"
        )
        
        if analysis and not analysis.get('error'):
            print("✅ AI document analysis successful!")
            
            # Display analysis results
            doc_analysis = analysis.get('document_analysis', {})
            print(f"Document Type: {doc_analysis.get('document_type', 'Unknown')}")
            
            # Risk analysis
            risk_analysis = analysis.get('risk_analysis', {})
            if risk_analysis:
                print(f"Weighted Risk Score: {risk_analysis.get('weighted_overall_score', 0)}/100")
                print(f"Risk Level: {risk_analysis.get('risk_level', 'unknown')}")
                
                top_risks = risk_analysis.get('top_risk_categories', [])
                if top_risks:
                    print(f"Top Risk Categories: {', '.join(top_risks)}")
            
            # Litigation risk
            litigation_risk = analysis.get('litigation_risk', {})
            if litigation_risk:
                print(f"Litigation Risk Score: {litigation_risk.get('litigation_score', 0)}/100")
                print(f"Requires Legal Review: {litigation_risk.get('requires_legal_review', False)}")
                print(f"Litigation Indicators: {litigation_risk.get('total_litigation_indicators', 0)}")
            
            # Compliance analysis
            compliance_analysis = analysis.get('compliance_analysis', {})
            if compliance_analysis:
                print(f"Compliance Score: {compliance_analysis.get('compliance_score', 0)}/100")
                print(f"Compliance Level: {compliance_analysis.get('compliance_level', 'unknown')}")
                print(f"High-Risk Gaps: {compliance_analysis.get('high_risk_gaps', 0)}")
            
            # Overall risk score
            overall_risk = analysis.get('overall_risk_score', {})
            if overall_risk:
                print(f"Overall Risk Score: {overall_risk.get('overall_score', 0)}/100")
                print(f"Overall Risk Level: {overall_risk.get('risk_level', 'unknown')}")
            
            # Recommendations
            recommendations = analysis.get('recommendations', [])
            if recommendations:
                print(f"\nAI Recommendations ({len(recommendations)}):")
                for i, rec in enumerate(recommendations[:3], 1):
                    print(f"  {i}. {rec}")
            
            # AI insights (if available)
            ai_insights = analysis.get('ai_insights', {})
            if ai_insights.get('available'):
                print(f"\n🤖 AI Insights Available: {ai_insights.get('model', 'Unknown model')}")
                insights_text = ai_insights.get('insights', '')
                if insights_text:
                    print(f"Insights Preview: {insights_text[:200]}...")
            else:
                print(f"\n🤖 AI Insights: {ai_insights.get('reason', 'Not available')}")
            
        else:
            print(f"❌ AI document analysis failed: {analysis.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ AI document analysis test error: {e}")

def test_nlp_pipeline():
    """Test basic NLP pipeline functionality"""
    print("\n" + "="*80)
    print("TESTING NLP PIPELINE")
    print("="*80)
    
    agent = LegalAgent()
    
    # Sample contract text
    sample_contract = """
    CONFIDENTIALITY AGREEMENT
    
    This Confidentiality Agreement ("Agreement") is entered into on January 1, 2024, between Company A and Company B.
    
    1. CONFIDENTIAL INFORMATION
    Each party agrees to hold in confidence all proprietary information disclosed by the other party.
    
    2. LIMITATION OF LIABILITY
    In no event shall either party be liable for any indirect, incidental, or consequential damages.
    
    3. TERMINATION
    This Agreement shall terminate automatically after two (2) years unless terminated earlier by mutual consent.
    
    4. GOVERNING LAW
    This Agreement shall be governed by the laws of the State of Delaware.
    """
    
    try:
        print("\nTesting NLP pipeline on sample contract...")
        
        # Test basic NLP analysis
        nlp_analysis = agent.nlp_pipeline.analyze_legal_document(sample_contract)
        
        if nlp_analysis:
            print("✅ NLP pipeline analysis successful!")
            
            # Document classification
            doc_classification = nlp_analysis.get('document_classification', {})
            print(f"Document Type: {doc_classification.get('predicted_type', 'Unknown')}")
            
            # Entities
            entities = nlp_analysis.get('entities', {})
            if entities:
                print(f"Entities Found: {len(entities)} categories")
                for entity_type, entity_list in entities.items():
                    if entity_list:
                        print(f"  {entity_type}: {len(entity_list)} items")
            
            # Legal clauses
            legal_clauses = nlp_analysis.get('legal_clauses', [])
            print(f"Legal Clauses Identified: {len(legal_clauses)}")
            for clause in legal_clauses[:3]:  # Show first 3
                print(f"  - {clause.get('clause_type', 'Unknown')}: {clause.get('matched_text', '')}")
            
            # Contract analysis
            contract_analysis = nlp_analysis.get('contract_analysis', {})
            if contract_analysis:
                print(f"Contract Type: {contract_analysis.get('contract_type', 'Unknown')}")
                print(f"Key Terms: {len(contract_analysis.get('key_terms', []))}")
                print(f"Obligations: {len(contract_analysis.get('obligations', []))}")
            
            # Risk analysis
            risk_analysis = nlp_analysis.get('risk_analysis', [])
            print(f"Risks Identified: {len(risk_analysis)}")
            for risk in risk_analysis[:2]:  # Show first 2
                print(f"  - {risk.get('risk_category', 'Unknown')}: {risk.get('severity', 'Unknown')} severity")
            
            # Text statistics
            text_stats = nlp_analysis.get('text_statistics', {})
            if text_stats:
                print(f"Text Statistics: {text_stats.get('word_count', 0)} words, {text_stats.get('sentence_count', 0)} sentences")
            
        else:
            print("❌ NLP pipeline analysis failed")
            
    except Exception as e:
        print(f"❌ NLP pipeline test error: {e}")

def main():
    """Run all legal agent tests"""
    print("LEGAL AGENT COMPREHENSIVE TEST SUITE")
    print("="*80)
    
    # Test individual components
    test_nlp_pipeline()
    test_ai_document_analysis()
    
    # Test integrated functionality
    test_legal_agent_comprehensive()
    test_legal_risk_summary()
    
    print("\n" + "="*80)
    print("LEGAL AGENT TESTS COMPLETED")
    print("="*80)
    print("\nNote: Some tests may show limited results due to API limitations")
    print("or missing external data sources. This is expected for the demo environment.")
    print("The legal agent handles these scenarios gracefully and provides")
    print("analysis based on available data sources.")

if __name__ == "__main__":
    main()