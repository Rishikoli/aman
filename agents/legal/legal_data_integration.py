"""
Legal Data Integration Service
Combines SEC EDGAR and OpenCorporates data for comprehensive legal intelligence
"""

import logging
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime
import json
from pathlib import Path

from .sec_edgar_client import SECEdgarClient
from .opencorporates_client import OpenCorporatesClient

logger = logging.getLogger(__name__)

class LegalDataIntegration:
    """
    Service that integrates multiple legal data sources for comprehensive analysis
    """
    
    def __init__(self):
        """Initialize legal data integration service"""
        self.sec_client = SECEdgarClient()
        self.opencorporates_client = OpenCorporatesClient()
        
        # Cache directory for integrated results
        self.cache_dir = Path("temp/legal_integration")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info("Legal Data Integration service initialized")
    
    def get_comprehensive_legal_intelligence(self, company_identifier: str, 
                                           company_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Get comprehensive legal intelligence combining all data sources
        
        Args:
            company_identifier: Ticker symbol, CIK, or company name
            company_name: Optional company name for OpenCorporates search
            
        Returns:
            Comprehensive legal intelligence report
        """
        try:
            logger.info(f"Starting comprehensive legal analysis for: {company_identifier}")
            
            # Initialize results structure
            results = {
                'company_identifier': company_identifier,
                'company_name': company_name,
                'analysis_timestamp': datetime.now().isoformat(),
                'data_sources': [],
                'sec_analysis': {},
                'corporate_structure': {},
                'integrated_risks': [],
                'compliance_status': {},
                'recommendations': []
            }
            
            # 1. Get SEC EDGAR data
            logger.info("Fetching SEC EDGAR data...")
            try:
                sec_data = self.sec_client.get_company_legal_intelligence(company_identifier)
                if sec_data and not sec_data.get('error'):
                    results['sec_analysis'] = sec_data
                    results['data_sources'].append('SEC EDGAR')
                    logger.info("✅ SEC EDGAR data retrieved successfully")
                else:
                    logger.warning(f"SEC EDGAR data retrieval failed: {sec_data.get('error', 'Unknown error')}")
                    results['sec_analysis'] = {'error': sec_data.get('error', 'Failed to retrieve SEC data')}
            except Exception as e:
                logger.error(f"SEC EDGAR integration error: {e}")
                results['sec_analysis'] = {'error': str(e)}
            
            # 2. Get OpenCorporates data
            logger.info("Fetching OpenCorporates data...")
            try:
                # Use company name if provided, otherwise use identifier
                search_name = company_name or company_identifier
                
                # Skip if identifier looks like a CIK (all digits)
                if not (company_identifier.isdigit() and len(company_identifier) >= 6):
                    corporate_data = self.opencorporates_client.verify_company_ownership(search_name)
                    if corporate_data and corporate_data.get('found'):
                        results['corporate_structure'] = corporate_data
                        results['data_sources'].append('OpenCorporates')
                        logger.info("✅ OpenCorporates data retrieved successfully")
                    else:
                        logger.warning("OpenCorporates data not found or failed")
                        results['corporate_structure'] = {'error': 'Company not found in OpenCorporates'}
                else:
                    logger.info("Skipping OpenCorporates search for CIK identifier")
                    results['corporate_structure'] = {'skipped': 'CIK identifier not suitable for OpenCorporates search'}
            except Exception as e:
                logger.error(f"OpenCorporates integration error: {e}")
                results['corporate_structure'] = {'error': str(e)}
            
            # 3. Integrate and analyze risks
            logger.info("Integrating risk analysis...")
            results['integrated_risks'] = self._integrate_risk_analysis(results)
            
            # 4. Assess compliance status
            results['compliance_status'] = self._assess_compliance_status(results)
            
            # 5. Generate recommendations
            results['recommendations'] = self._generate_recommendations(results)
            
            # 6. Calculate overall risk score
            results['overall_risk_score'] = self._calculate_overall_risk_score(results)
            
            logger.info("✅ Comprehensive legal analysis completed")
            return results
            
        except Exception as e:
            logger.error(f"Error in comprehensive legal intelligence: {e}")
            return {
                'company_identifier': company_identifier,
                'error': str(e),
                'analysis_timestamp': datetime.now().isoformat()
            }
    
    def _integrate_risk_analysis(self, results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Integrate risk analysis from all data sources
        
        Args:
            results: Combined results from all sources
            
        Returns:
            List of integrated risk factors
        """
        integrated_risks = []
        
        # Extract SEC risks
        sec_analysis = results.get('sec_analysis', {})
        if 'legal_analysis' in sec_analysis:
            legal_analysis = sec_analysis['legal_analysis']
            
            # Legal proceedings risks
            legal_proceedings = legal_analysis.get('legal_proceedings', {})
            if legal_proceedings.get('found') and legal_proceedings.get('indicators'):
                integrated_risks.append({
                    'risk_type': 'litigation',
                    'source': 'SEC EDGAR',
                    'severity': legal_proceedings.get('risk_level', 'medium'),
                    'description': f"Legal proceedings identified: {', '.join(legal_proceedings['indicators'])}",
                    'details': legal_proceedings.get('content', '')[:500],
                    'category': 'legal_proceedings'
                })
            
            # Risk factors from 10-K
            risk_factors = legal_analysis.get('risk_factors', {})
            if risk_factors.get('found') and risk_factors.get('legal_risks'):
                for risk in risk_factors['legal_risks'][:5]:  # Top 5 risks
                    integrated_risks.append({
                        'risk_type': 'regulatory',
                        'source': 'SEC EDGAR',
                        'severity': 'medium',
                        'description': f"Risk factor identified: {risk['keyword']}",
                        'details': risk['sentence'][:300],
                        'category': 'risk_factors'
                    })
        
        # Extract recent material events from 8-K filings
        recent_events = sec_analysis.get('recent_material_events', [])
        if recent_events:
            integrated_risks.append({
                'risk_type': 'material_events',
                'source': 'SEC EDGAR',
                'severity': 'medium',
                'description': f"{len(recent_events)} recent material events (8-K filings) in last 90 days",
                'details': f"Recent 8-K filings may indicate significant corporate events requiring analysis",
                'category': 'material_events',
                'count': len(recent_events)
            })
        
        # Extract corporate structure risks
        corporate_structure = results.get('corporate_structure', {})
        if corporate_structure.get('found'):
            structure_analysis = corporate_structure.get('structure_analysis', {})
            risk_factors = structure_analysis.get('risk_factors', [])
            
            for risk_factor in risk_factors:
                integrated_risks.append({
                    'risk_type': 'corporate_governance',
                    'source': 'OpenCorporates',
                    'severity': self._assess_governance_risk_severity(risk_factor),
                    'description': risk_factor,
                    'details': f"Corporate governance issue identified in company structure",
                    'category': 'governance'
                })
            
            # Low governance score is a risk
            governance_score = structure_analysis.get('governance_score', 0)
            if governance_score < 50:
                integrated_risks.append({
                    'risk_type': 'corporate_governance',
                    'source': 'OpenCorporates',
                    'severity': 'high' if governance_score < 25 else 'medium',
                    'description': f"Low corporate governance score: {governance_score}/100",
                    'details': "Poor corporate governance structure may indicate operational and compliance risks",
                    'category': 'governance',
                    'score': governance_score
                })
        
        # Sort risks by severity
        severity_order = {'high': 3, 'medium': 2, 'low': 1}
        integrated_risks.sort(key=lambda x: severity_order.get(x['severity'], 0), reverse=True)
        
        return integrated_risks
    
    def _assess_governance_risk_severity(self, risk_factor: str) -> str:
        """Assess severity of governance risk factors"""
        risk_factor_lower = risk_factor.lower()
        
        high_severity_indicators = [
            'no active officers', 'dissolved', 'inactive', 'struck off',
            'very recently incorporated'
        ]
        
        medium_severity_indicators = [
            'one active officer', 'key governance positions', 'recently incorporated'
        ]
        
        for indicator in high_severity_indicators:
            if indicator in risk_factor_lower:
                return 'high'
        
        for indicator in medium_severity_indicators:
            if indicator in risk_factor_lower:
                return 'medium'
        
        return 'low'
    
    def _assess_compliance_status(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess overall compliance status based on integrated data
        
        Args:
            results: Combined results from all sources
            
        Returns:
            Compliance status assessment
        """
        compliance_status = {
            'overall_status': 'unknown',
            'sec_compliance': 'unknown',
            'corporate_compliance': 'unknown',
            'issues_found': [],
            'last_filing_date': None,
            'filing_currency': 'unknown'
        }
        
        # Assess SEC compliance
        sec_analysis = results.get('sec_analysis', {})
        if sec_analysis and not sec_analysis.get('error'):
            recent_filings = sec_analysis.get('recent_filings', [])
            if recent_filings:
                # Check if recent filings exist
                latest_filing = recent_filings[0]
                compliance_status['last_filing_date'] = latest_filing.get('filing_date')
                
                # Check filing currency (simplified)
                filing_date = latest_filing.get('filing_date')
                if filing_date:
                    try:
                        filing_datetime = datetime.strptime(filing_date, '%Y-%m-%d')
                        days_since_filing = (datetime.now() - filing_datetime).days
                        
                        if days_since_filing <= 90:
                            compliance_status['filing_currency'] = 'current'
                            compliance_status['sec_compliance'] = 'good'
                        elif days_since_filing <= 180:
                            compliance_status['filing_currency'] = 'recent'
                            compliance_status['sec_compliance'] = 'acceptable'
                        else:
                            compliance_status['filing_currency'] = 'outdated'
                            compliance_status['sec_compliance'] = 'concerning'
                            compliance_status['issues_found'].append('SEC filings may be outdated')
                    except ValueError:
                        pass
            else:
                compliance_status['sec_compliance'] = 'poor'
                compliance_status['issues_found'].append('No recent SEC filings found')
        
        # Assess corporate compliance
        corporate_structure = results.get('corporate_structure', {})
        if corporate_structure.get('found'):
            basic_info = corporate_structure.get('company_details', {}).get('basic_info', {})
            current_status = basic_info.get('current_status', '').lower()
            
            if current_status == 'active':
                compliance_status['corporate_compliance'] = 'good'
            elif current_status in ['dissolved', 'inactive', 'struck off']:
                compliance_status['corporate_compliance'] = 'poor'
                compliance_status['issues_found'].append(f'Company status: {current_status}')
            else:
                compliance_status['corporate_compliance'] = 'unknown'
        
        # Determine overall status
        sec_status = compliance_status['sec_compliance']
        corp_status = compliance_status['corporate_compliance']
        
        if sec_status == 'good' and corp_status == 'good':
            compliance_status['overall_status'] = 'good'
        elif 'poor' in [sec_status, corp_status]:
            compliance_status['overall_status'] = 'poor'
        elif 'concerning' in [sec_status, corp_status]:
            compliance_status['overall_status'] = 'concerning'
        else:
            compliance_status['overall_status'] = 'acceptable'
        
        return compliance_status
    
    def _generate_recommendations(self, results: Dict[str, Any]) -> List[str]:
        """
        Generate recommendations based on integrated analysis
        
        Args:
            results: Combined results from all sources
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        # Analyze integrated risks
        integrated_risks = results.get('integrated_risks', [])
        high_risks = [r for r in integrated_risks if r['severity'] == 'high']
        
        if high_risks:
            recommendations.append(f"URGENT: Address {len(high_risks)} high-severity legal risks identified")
            
            # Specific recommendations based on risk types
            risk_types = set(r['risk_type'] for r in high_risks)
            
            if 'litigation' in risk_types:
                recommendations.append("Conduct detailed litigation risk assessment and consider legal reserves")
            
            if 'corporate_governance' in risk_types:
                recommendations.append("Review and strengthen corporate governance structure")
        
        # Compliance recommendations
        compliance_status = results.get('compliance_status', {})
        if compliance_status.get('overall_status') == 'poor':
            recommendations.append("Address compliance issues immediately before proceeding with M&A")
        
        if compliance_status.get('filing_currency') == 'outdated':
            recommendations.append("Verify current SEC filing status and ensure all required filings are up to date")
        
        # Data availability recommendations
        if results.get('sec_analysis', {}).get('error'):
            recommendations.append("SEC data unavailable - consider alternative sources for financial and legal analysis")
        
        if results.get('corporate_structure', {}).get('error'):
            recommendations.append("Corporate structure data limited - conduct manual verification of ownership and governance")
        
        # General recommendations
        if len(results.get('data_sources', [])) < 2:
            recommendations.append("Limited data sources available - supplement with additional due diligence")
        
        if not recommendations:
            recommendations.append("Continue with standard due diligence procedures - no immediate red flags identified")
        
        return recommendations
    
    def _calculate_overall_risk_score(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate overall risk score based on integrated analysis
        
        Args:
            results: Combined results from all sources
            
        Returns:
            Risk score analysis
        """
        risk_score = {
            'score': 0,
            'max_score': 100,
            'risk_level': 'low',
            'components': {}
        }
        
        # Risk scoring components
        integrated_risks = results.get('integrated_risks', [])
        
        # Count risks by severity
        high_risks = len([r for r in integrated_risks if r['severity'] == 'high'])
        medium_risks = len([r for r in integrated_risks if r['severity'] == 'medium'])
        low_risks = len([r for r in integrated_risks if r['severity'] == 'low'])
        
        # Calculate risk score (higher score = higher risk)
        risk_points = (high_risks * 25) + (medium_risks * 10) + (low_risks * 5)
        risk_score['score'] = min(risk_points, 100)  # Cap at 100
        
        risk_score['components'] = {
            'high_severity_risks': high_risks,
            'medium_severity_risks': medium_risks,
            'low_severity_risks': low_risks,
            'total_risks': len(integrated_risks)
        }
        
        # Determine risk level
        if risk_score['score'] >= 70:
            risk_score['risk_level'] = 'high'
        elif risk_score['score'] >= 40:
            risk_score['risk_level'] = 'medium'
        else:
            risk_score['risk_level'] = 'low'
        
        # Adjust for compliance status
        compliance_status = results.get('compliance_status', {})
        if compliance_status.get('overall_status') == 'poor':
            risk_score['score'] = min(risk_score['score'] + 20, 100)
            risk_score['risk_level'] = 'high'
        
        return risk_score
    
    def get_legal_risk_summary(self, company_identifier: str, 
                              company_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Get a concise legal risk summary for quick assessment
        
        Args:
            company_identifier: Company identifier
            company_name: Optional company name
            
        Returns:
            Concise risk summary
        """
        try:
            # Get full analysis
            full_analysis = self.get_comprehensive_legal_intelligence(company_identifier, company_name)
            
            # Extract key information for summary
            summary = {
                'company_identifier': company_identifier,
                'analysis_date': full_analysis.get('analysis_timestamp'),
                'data_sources_available': len(full_analysis.get('data_sources', [])),
                'overall_risk_score': full_analysis.get('overall_risk_score', {}),
                'compliance_status': full_analysis.get('compliance_status', {}).get('overall_status', 'unknown'),
                'high_priority_risks': len([r for r in full_analysis.get('integrated_risks', []) if r['severity'] == 'high']),
                'total_risks_identified': len(full_analysis.get('integrated_risks', [])),
                'top_recommendations': full_analysis.get('recommendations', [])[:3],
                'requires_immediate_attention': False
            }
            
            # Determine if immediate attention is required
            risk_score = summary['overall_risk_score'].get('score', 0)
            if (risk_score >= 70 or 
                summary['high_priority_risks'] > 0 or 
                summary['compliance_status'] == 'poor'):
                summary['requires_immediate_attention'] = True
            
            return summary
            
        except Exception as e:
            logger.error(f"Error generating legal risk summary: {e}")
            return {
                'company_identifier': company_identifier,
                'error': str(e),
                'analysis_date': datetime.now().isoformat()
            }