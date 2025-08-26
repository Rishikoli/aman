"""
Legal & Compliance Agent
Main agent that orchestrates legal analysis using multiple data sources and AI
"""

import logging
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path

from .legal_data_integration import LegalDataIntegration
from .ai_legal_analyzer import AILegalAnalyzer
from .legal_nlp_pipeline import LegalNLPPipeline

logger = logging.getLogger(__name__)

class LegalAgent:
    """
    Main Legal & Compliance Agent for M&A due diligence
    Combines data integration, AI analysis, and NLP processing
    """
    
    def __init__(self):
        """Initialize the Legal Agent with all components"""
        self.data_integration = LegalDataIntegration()
        self.ai_analyzer = AILegalAnalyzer()
        self.nlp_pipeline = LegalNLPPipeline()
        
        # Initialize NLP pipeline
        self.nlp_pipeline.initialize()
        
        # Results cache
        self.cache_dir = Path("temp/legal_agent_results")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info("Legal Agent initialized successfully")
    
    def analyze_company_legal_profile(self, company_identifier: str, 
                                    company_name: Optional[str] = None,
                                    include_ai_analysis: bool = True) -> Dict[str, Any]:
        """
        Comprehensive legal analysis of a company for M&A due diligence
        
        Args:
            company_identifier: Ticker symbol, CIK, or company name
            company_name: Optional company name for better matching
            include_ai_analysis: Whether to include AI-powered analysis
            
        Returns:
            Comprehensive legal profile and risk assessment
        """
        try:
            logger.info(f"Starting comprehensive legal analysis for: {company_identifier}")
            
            # Initialize results structure
            results = {
                'company_identifier': company_identifier,
                'company_name': company_name,
                'analysis_timestamp': datetime.now().isoformat(),
                'analysis_components': [],
                'legal_intelligence': {},
                'document_analysis': {},
                'risk_assessment': {},
                'compliance_status': {},
                'recommendations': [],
                'overall_assessment': {}
            }
            
            # 1. Get comprehensive legal intelligence from multiple sources
            logger.info("Gathering legal intelligence from multiple sources...")
            try:
                legal_intelligence = self.data_integration.get_comprehensive_legal_intelligence(
                    company_identifier, company_name
                )
                results['legal_intelligence'] = legal_intelligence
                results['analysis_components'].append('legal_intelligence')
                logger.info("✅ Legal intelligence gathering completed")
            except Exception as e:
                logger.error(f"Legal intelligence gathering failed: {e}")
                results['legal_intelligence'] = {'error': str(e)}
            
            # 2. Analyze any available legal documents with AI
            if include_ai_analysis:
                logger.info("Performing AI-powered document analysis...")
                try:
                    document_analysis = self._analyze_available_documents(legal_intelligence)
                    results['document_analysis'] = document_analysis
                    results['analysis_components'].append('ai_document_analysis')
                    logger.info("✅ AI document analysis completed")
                except Exception as e:
                    logger.error(f"AI document analysis failed: {e}")
                    results['document_analysis'] = {'error': str(e)}
            
            # 3. Comprehensive risk assessment
            logger.info("Performing comprehensive risk assessment...")
            try:
                risk_assessment = self._perform_comprehensive_risk_assessment(results)
                results['risk_assessment'] = risk_assessment
                results['analysis_components'].append('risk_assessment')
                logger.info("✅ Risk assessment completed")
            except Exception as e:
                logger.error(f"Risk assessment failed: {e}")
                results['risk_assessment'] = {'error': str(e)}
            
            # 4. Compliance status evaluation
            logger.info("Evaluating compliance status...")
            try:
                compliance_status = self._evaluate_compliance_status(results)
                results['compliance_status'] = compliance_status
                results['analysis_components'].append('compliance_evaluation')
                logger.info("✅ Compliance evaluation completed")
            except Exception as e:
                logger.error(f"Compliance evaluation failed: {e}")
                results['compliance_status'] = {'error': str(e)}
            
            # 5. Generate comprehensive recommendations
            logger.info("Generating recommendations...")
            try:
                recommendations = self._generate_comprehensive_recommendations(results)
                results['recommendations'] = recommendations
                logger.info("✅ Recommendations generated")
            except Exception as e:
                logger.error(f"Recommendation generation failed: {e}")
                results['recommendations'] = [f"Error generating recommendations: {str(e)}"]
            
            # 6. Overall assessment and scoring
            logger.info("Calculating overall assessment...")
            try:
                overall_assessment = self._calculate_overall_assessment(results)
                results['overall_assessment'] = overall_assessment
                logger.info("✅ Overall assessment completed")
            except Exception as e:
                logger.error(f"Overall assessment failed: {e}")
                results['overall_assessment'] = {'error': str(e)}
            
            # 7. Cache results
            self._cache_results(company_identifier, results)
            
            logger.info("✅ Comprehensive legal analysis completed successfully")
            return results
            
        except Exception as e:
            logger.error(f"Error in comprehensive legal analysis: {e}")
            return {
                'company_identifier': company_identifier,
                'error': str(e),
                'analysis_timestamp': datetime.now().isoformat()
            }
    
    def _analyze_available_documents(self, legal_intelligence: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze available legal documents using AI
        
        Args:
            legal_intelligence: Legal intelligence data
            
        Returns:
            Document analysis results
        """
        document_analyses = []
        
        # Analyze SEC filing content if available
        sec_analysis = legal_intelligence.get('sec_analysis', {})
        if sec_analysis and not sec_analysis.get('error'):
            legal_analysis = sec_analysis.get('legal_analysis', {})
            
            # Analyze legal proceedings section
            legal_proceedings = legal_analysis.get('legal_proceedings', {})
            if legal_proceedings.get('found') and legal_proceedings.get('content'):
                logger.info("Analyzing legal proceedings section with AI...")
                
                proceedings_analysis = self.ai_analyzer.analyze_legal_document_comprehensive(
                    legal_proceedings['content'],
                    document_type='SEC Legal Proceedings'
                )
                
                document_analyses.append({
                    'document_type': 'SEC Legal Proceedings',
                    'source': 'SEC EDGAR',
                    'analysis': proceedings_analysis,
                    'original_content_length': len(legal_proceedings['content'])
                })
            
            # Analyze risk factors section
            risk_factors = legal_analysis.get('risk_factors', {})
            if risk_factors.get('found') and risk_factors.get('content'):
                logger.info("Analyzing risk factors section with AI...")
                
                risk_analysis = self.ai_analyzer.analyze_legal_document_comprehensive(
                    risk_factors['content'],
                    document_type='SEC Risk Factors'
                )
                
                document_analyses.append({
                    'document_type': 'SEC Risk Factors',
                    'source': 'SEC EDGAR',
                    'analysis': risk_analysis,
                    'original_content_length': len(risk_factors['content'])
                })
        
        # Analyze corporate structure documents if available
        corporate_structure = legal_intelligence.get('corporate_structure', {})
        if corporate_structure.get('found'):
            # Create summary document for analysis
            company_details = corporate_structure.get('company_details', {})
            officers = corporate_structure.get('officers', [])
            
            if company_details or officers:
                # Create a text summary for AI analysis
                summary_text = self._create_corporate_summary_text(company_details, officers)
                
                if summary_text:
                    logger.info("Analyzing corporate structure with AI...")
                    
                    corporate_analysis = self.ai_analyzer.analyze_legal_document_comprehensive(
                        summary_text,
                        document_type='Corporate Structure Summary'
                    )
                    
                    document_analyses.append({
                        'document_type': 'Corporate Structure Summary',
                        'source': 'OpenCorporates',
                        'analysis': corporate_analysis,
                        'original_content_length': len(summary_text)
                    })
        
        return {
            'documents_analyzed': len(document_analyses),
            'document_analyses': document_analyses,
            'analysis_timestamp': datetime.now().isoformat()
        }
    
    def _create_corporate_summary_text(self, company_details: Dict, officers: List[Dict]) -> str:
        """Create a text summary of corporate structure for AI analysis"""
        summary_parts = []
        
        if company_details:
            basic_info = company_details.get('basic_info', {})
            
            summary_parts.append(f"Company: {basic_info.get('name', 'Unknown')}")
            summary_parts.append(f"Status: {basic_info.get('current_status', 'Unknown')}")
            summary_parts.append(f"Jurisdiction: {basic_info.get('jurisdiction_code', 'Unknown')}")
            summary_parts.append(f"Company Type: {basic_info.get('company_type', 'Unknown')}")
            
            if basic_info.get('incorporation_date'):
                summary_parts.append(f"Incorporation Date: {basic_info['incorporation_date']}")
            
            if basic_info.get('registered_address'):
                summary_parts.append(f"Registered Address: {basic_info['registered_address']}")
        
        if officers:
            summary_parts.append("\nOfficers and Directors:")
            for officer in officers[:10]:  # Limit to 10 officers
                officer_info = f"- {officer.get('name', 'Unknown')}"
                if officer.get('position'):
                    officer_info += f" ({officer['position']})"
                if officer.get('start_date'):
                    officer_info += f" since {officer['start_date']}"
                if officer.get('inactive'):
                    officer_info += " [INACTIVE]"
                summary_parts.append(officer_info)
        
        return "\n".join(summary_parts)
    
    def _perform_comprehensive_risk_assessment(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform comprehensive risk assessment combining all analysis components
        
        Args:
            results: Combined analysis results
            
        Returns:
            Comprehensive risk assessment
        """
        risk_assessment = {
            'risk_categories': {},
            'overall_risk_score': 0,
            'risk_level': 'low',
            'critical_risks': [],
            'risk_factors': []
        }
        
        # 1. Extract risks from legal intelligence
        legal_intelligence = results.get('legal_intelligence', {})
        if legal_intelligence and not legal_intelligence.get('error'):
            integrated_risks = legal_intelligence.get('integrated_risks', [])
            overall_risk_score = legal_intelligence.get('overall_risk_score', {})
            
            risk_assessment['legal_intelligence_risks'] = {
                'total_risks': len(integrated_risks),
                'high_severity_risks': len([r for r in integrated_risks if r['severity'] == 'high']),
                'risk_score': overall_risk_score.get('score', 0),
                'risk_level': overall_risk_score.get('risk_level', 'low')
            }
            
            # Add to overall risk factors
            risk_assessment['risk_factors'].extend([
                {
                    'source': 'legal_intelligence',
                    'category': risk['risk_type'],
                    'severity': risk['severity'],
                    'description': risk['description']
                }
                for risk in integrated_risks
            ])
        
        # 2. Extract risks from AI document analysis
        document_analysis = results.get('document_analysis', {})
        if document_analysis and not document_analysis.get('error'):
            document_analyses = document_analysis.get('document_analyses', [])
            
            ai_risks = []
            for doc_analysis in document_analyses:
                analysis = doc_analysis.get('analysis', {})
                if analysis and not analysis.get('error'):
                    # Extract risk analysis
                    risk_analysis = analysis.get('risk_analysis', {})
                    if risk_analysis:
                        overall_score = risk_analysis.get('weighted_overall_score', 0)
                        ai_risks.append({
                            'document_type': doc_analysis['document_type'],
                            'risk_score': overall_score,
                            'risk_level': analysis.get('overall_risk_score', {}).get('risk_level', 'low')
                        })
                    
                    # Extract specific risks
                    litigation_risk = analysis.get('litigation_risk', {})
                    if litigation_risk.get('requires_legal_review'):
                        risk_assessment['critical_risks'].append({
                            'type': 'litigation',
                            'source': doc_analysis['document_type'],
                            'description': 'Litigation indicators require legal review',
                            'severity': 'high'
                        })
            
            risk_assessment['ai_analysis_risks'] = {
                'documents_with_risks': len(ai_risks),
                'document_risk_scores': ai_risks
            }
        
        # 3. Calculate overall risk score
        risk_scores = []
        
        # Legal intelligence risk score
        legal_risk_score = risk_assessment.get('legal_intelligence_risks', {}).get('risk_score', 0)
        if legal_risk_score > 0:
            risk_scores.append(legal_risk_score)
        
        # AI analysis risk scores
        ai_risk_data = risk_assessment.get('ai_analysis_risks', {})
        ai_risk_scores = [doc['risk_score'] for doc in ai_risk_data.get('document_risk_scores', [])]
        if ai_risk_scores:
            avg_ai_risk = sum(ai_risk_scores) / len(ai_risk_scores)
            risk_scores.append(avg_ai_risk)
        
        # Calculate weighted overall risk score
        if risk_scores:
            risk_assessment['overall_risk_score'] = sum(risk_scores) / len(risk_scores)
        else:
            risk_assessment['overall_risk_score'] = 0
        
        # Determine risk level
        overall_score = risk_assessment['overall_risk_score']
        if overall_score >= 70:
            risk_assessment['risk_level'] = 'high'
        elif overall_score >= 40:
            risk_assessment['risk_level'] = 'medium'
        else:
            risk_assessment['risk_level'] = 'low'
        
        # Categorize risks
        risk_categories = {}
        for risk_factor in risk_assessment['risk_factors']:
            category = risk_factor['category']
            if category not in risk_categories:
                risk_categories[category] = []
            risk_categories[category].append(risk_factor)
        
        risk_assessment['risk_categories'] = risk_categories
        
        return risk_assessment
    
    def _evaluate_compliance_status(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate overall compliance status
        
        Args:
            results: Combined analysis results
            
        Returns:
            Compliance status evaluation
        """
        compliance_status = {
            'overall_status': 'unknown',
            'compliance_areas': {},
            'compliance_score': 0,
            'issues_identified': [],
            'recommendations': []
        }
        
        # Extract compliance information from legal intelligence
        legal_intelligence = results.get('legal_intelligence', {})
        if legal_intelligence and not legal_intelligence.get('error'):
            li_compliance = legal_intelligence.get('compliance_status', {})
            
            compliance_status['sec_compliance'] = {
                'status': li_compliance.get('sec_compliance', 'unknown'),
                'filing_currency': li_compliance.get('filing_currency', 'unknown'),
                'last_filing_date': li_compliance.get('last_filing_date')
            }
            
            compliance_status['corporate_compliance'] = {
                'status': li_compliance.get('corporate_compliance', 'unknown')
            }
            
            # Add issues
            compliance_status['issues_identified'].extend(
                li_compliance.get('issues_found', [])
            )
        
        # Extract compliance information from AI document analysis
        document_analysis = results.get('document_analysis', {})
        if document_analysis and not document_analysis.get('error'):
            document_analyses = document_analysis.get('document_analyses', [])
            
            compliance_issues = []
            for doc_analysis in document_analyses:
                analysis = doc_analysis.get('analysis', {})
                if analysis and not analysis.get('error'):
                    comp_analysis = analysis.get('compliance_analysis', {})
                    if comp_analysis:
                        issues = comp_analysis.get('compliance_issues', [])
                        compliance_issues.extend([
                            {
                                'source': doc_analysis['document_type'],
                                'area': issue['compliance_area'],
                                'risk_level': issue['risk_level'],
                                'description': issue['description']
                            }
                            for issue in issues
                        ])
            
            compliance_status['document_compliance_issues'] = compliance_issues
            compliance_status['issues_identified'].extend([
                f"{issue['area']}: {issue['description']}" for issue in compliance_issues
            ])
        
        # Calculate overall compliance score
        sec_status = compliance_status.get('sec_compliance', {}).get('status', 'unknown')
        corp_status = compliance_status.get('corporate_compliance', {}).get('status', 'unknown')
        
        score = 50  # Start neutral
        
        if sec_status == 'good':
            score += 25
        elif sec_status == 'poor':
            score -= 25
        
        if corp_status == 'good':
            score += 25
        elif corp_status == 'poor':
            score -= 25
        
        # Adjust for issues
        high_risk_issues = len([i for i in compliance_status.get('document_compliance_issues', []) 
                               if i.get('risk_level') == 'high'])
        score -= high_risk_issues * 10
        
        compliance_status['compliance_score'] = max(0, min(100, score))
        
        # Determine overall status
        if compliance_status['compliance_score'] >= 80:
            compliance_status['overall_status'] = 'good'
        elif compliance_status['compliance_score'] >= 60:
            compliance_status['overall_status'] = 'acceptable'
        else:
            compliance_status['overall_status'] = 'poor'
        
        return compliance_status
    
    def _generate_comprehensive_recommendations(self, results: Dict[str, Any]) -> List[str]:
        """
        Generate comprehensive recommendations based on all analysis components
        
        Args:
            results: Combined analysis results
            
        Returns:
            List of prioritized recommendations
        """
        recommendations = []
        
        # Risk-based recommendations
        risk_assessment = results.get('risk_assessment', {})
        overall_risk_level = risk_assessment.get('risk_level', 'low')
        
        if overall_risk_level == 'high':
            recommendations.append("🚨 CRITICAL: High legal risk identified - immediate comprehensive legal review required")
        elif overall_risk_level == 'medium':
            recommendations.append("⚠️ MODERATE: Elevated legal risk - enhanced due diligence recommended")
        
        # Critical risks
        critical_risks = risk_assessment.get('critical_risks', [])
        if critical_risks:
            recommendations.append(f"Address {len(critical_risks)} critical legal risks immediately")
        
        # Compliance recommendations
        compliance_status = results.get('compliance_status', {})
        overall_compliance = compliance_status.get('overall_status', 'unknown')
        
        if overall_compliance == 'poor':
            recommendations.append("🚨 URGENT: Poor compliance status - address compliance gaps before proceeding")
        elif overall_compliance == 'acceptable':
            recommendations.append("⚠️ Monitor compliance status and address identified gaps")
        
        # Data source recommendations
        legal_intelligence = results.get('legal_intelligence', {})
        data_sources = legal_intelligence.get('data_sources', [])
        
        if len(data_sources) < 2:
            recommendations.append("Limited legal data sources - supplement with additional research")
        
        if legal_intelligence.get('sec_analysis', {}).get('error'):
            recommendations.append("SEC data unavailable - verify public company status and filing requirements")
        
        # AI analysis recommendations
        document_analysis = results.get('document_analysis', {})
        if document_analysis and not document_analysis.get('error'):
            docs_analyzed = document_analysis.get('documents_analyzed', 0)
            if docs_analyzed > 0:
                recommendations.append(f"AI analysis completed on {docs_analyzed} documents - review detailed findings")
            else:
                recommendations.append("No documents available for AI analysis - obtain key legal documents")
        
        # Specific risk category recommendations
        risk_categories = risk_assessment.get('risk_categories', {})
        
        if 'litigation' in risk_categories:
            recommendations.append("Litigation risks identified - engage litigation counsel for detailed assessment")
        
        if 'regulatory' in risk_categories:
            recommendations.append("Regulatory risks found - conduct comprehensive regulatory compliance review")
        
        if 'corporate_governance' in risk_categories:
            recommendations.append("Corporate governance issues - review board structure and governance practices")
        
        # Default recommendations
        if not recommendations:
            recommendations.append("✅ No immediate legal red flags - proceed with standard due diligence")
            recommendations.append("Continue monitoring for legal developments during transaction process")
        
        # Add general best practices
        recommendations.extend([
            "Obtain legal opinions from target company's counsel on key legal matters",
            "Review all material contracts and agreements",
            "Verify insurance coverage and claims history",
            "Conduct final legal review before transaction closing"
        ])
        
        return recommendations[:15]  # Limit to 15 recommendations
    
    def _calculate_overall_assessment(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate overall legal assessment and scoring
        
        Args:
            results: Combined analysis results
            
        Returns:
            Overall assessment
        """
        assessment = {
            'overall_score': 0,
            'assessment_level': 'unknown',
            'key_findings': [],
            'decision_factors': {},
            'recommendation': 'unknown'
        }
        
        # Component scores
        risk_score = results.get('risk_assessment', {}).get('overall_risk_score', 0)
        compliance_score = results.get('compliance_status', {}).get('compliance_score', 50)
        
        # Calculate overall score (lower risk score is better, higher compliance score is better)
        # Invert risk score so higher overall score is better
        inverted_risk_score = 100 - risk_score
        
        # Weight the components
        overall_score = (inverted_risk_score * 0.6) + (compliance_score * 0.4)
        assessment['overall_score'] = round(overall_score, 2)
        
        # Determine assessment level
        if overall_score >= 80:
            assessment['assessment_level'] = 'low_risk'
            assessment['recommendation'] = 'proceed_with_standard_diligence'
        elif overall_score >= 60:
            assessment['assessment_level'] = 'moderate_risk'
            assessment['recommendation'] = 'proceed_with_enhanced_diligence'
        elif overall_score >= 40:
            assessment['assessment_level'] = 'high_risk'
            assessment['recommendation'] = 'proceed_with_caution'
        else:
            assessment['assessment_level'] = 'very_high_risk'
            assessment['recommendation'] = 'consider_transaction_risks_carefully'
        
        # Key findings
        risk_assessment = results.get('risk_assessment', {})
        critical_risks = risk_assessment.get('critical_risks', [])
        
        if critical_risks:
            assessment['key_findings'].append(f"{len(critical_risks)} critical legal risks identified")
        
        compliance_status = results.get('compliance_status', {})
        if compliance_status.get('overall_status') == 'poor':
            assessment['key_findings'].append("Poor compliance status")
        
        legal_intelligence = results.get('legal_intelligence', {})
        data_sources = len(legal_intelligence.get('data_sources', []))
        assessment['key_findings'].append(f"Analysis based on {data_sources} data sources")
        
        # Decision factors
        assessment['decision_factors'] = {
            'risk_score': risk_score,
            'compliance_score': compliance_score,
            'data_completeness': min(data_sources / 2 * 100, 100),  # Assume 2 sources is complete
            'critical_issues': len(critical_risks)
        }
        
        return assessment
    
    def _cache_results(self, company_identifier: str, results: Dict[str, Any]):
        """Cache analysis results for future reference"""
        try:
            cache_file = self.cache_dir / f"{company_identifier}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            with open(cache_file, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            
            logger.info(f"Results cached to: {cache_file}")
            
        except Exception as e:
            logger.warning(f"Failed to cache results: {e}")
    
    def get_legal_risk_summary(self, company_identifier: str, 
                              company_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Get a concise legal risk summary for quick decision making
        
        Args:
            company_identifier: Company identifier
            company_name: Optional company name
            
        Returns:
            Concise legal risk summary
        """
        try:
            # Get full analysis
            full_analysis = self.analyze_company_legal_profile(
                company_identifier, company_name, include_ai_analysis=False
            )
            
            # Extract key information for summary
            overall_assessment = full_analysis.get('overall_assessment', {})
            risk_assessment = full_analysis.get('risk_assessment', {})
            compliance_status = full_analysis.get('compliance_status', {})
            
            summary = {
                'company_identifier': company_identifier,
                'analysis_timestamp': full_analysis.get('analysis_timestamp'),
                'overall_score': overall_assessment.get('overall_score', 0),
                'assessment_level': overall_assessment.get('assessment_level', 'unknown'),
                'recommendation': overall_assessment.get('recommendation', 'unknown'),
                'risk_level': risk_assessment.get('risk_level', 'unknown'),
                'compliance_status': compliance_status.get('overall_status', 'unknown'),
                'critical_risks': len(risk_assessment.get('critical_risks', [])),
                'data_sources': len(full_analysis.get('legal_intelligence', {}).get('data_sources', [])),
                'top_recommendations': full_analysis.get('recommendations', [])[:5],
                'requires_immediate_attention': overall_assessment.get('assessment_level') in ['high_risk', 'very_high_risk']
            }
            
            return summary
            
        except Exception as e:
            logger.error(f"Error generating legal risk summary: {e}")
            return {
                'company_identifier': company_identifier,
                'error': str(e),
                'analysis_timestamp': datetime.now().isoformat()
            }