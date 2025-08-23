"""
Finance Agent with ML-Powered Analysis
Integrates financial data retrieval, ML analysis, and AI-powered insights.
"""

import sys
import os
import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

# Add the agents directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from finance.financial_analysis_engine import FinancialAnalysisEngine
from finance.gemini_financial_analyzer import GeminiFinancialAnalyzer
from finance.intelligent_financial_integration import IntelligentFinancialIntegration

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FinanceAgent:
    """
    Advanced Finance Agent with ML-powered analysis capabilities
    """
    
    def __init__(self):
        """Initialize the Finance Agent"""
        self.analysis_engine = FinancialAnalysisEngine()
        self.gemini_analyzer = GeminiFinancialAnalyzer()
        self.intelligent_financial = IntelligentFinancialIntegration()
        self.agent_id = "finance_agent"
        self.version = "2.1.0"
        
        logger.info(f"Finance Agent {self.version} initialized with intelligent financial intelligence")
    
    def analyze_company_financials(self, financial_data: Dict, options: Dict = None) -> Dict[str, Any]:
        """
        Perform comprehensive financial analysis of a company
        
        Args:
            financial_data: Raw financial data from data sources
            options: Analysis options and preferences
            
        Returns:
            Dictionary containing comprehensive financial analysis
        """
        try:
            logger.info(f"Starting comprehensive financial analysis...")
            
            if not options:
                options = {}
            
            analysis_results = {
                'agent_id': self.agent_id,
                'analysis_date': datetime.now().isoformat(),
                'company_symbol': financial_data.get('metadata', {}).get('symbol', 'Unknown'),
                'data_source': financial_data.get('dataSource', 'Unknown')
            }
            
            # Step 1: Calculate Financial Ratios
            logger.info("Calculating financial ratios...")
            try:
                ratios = self.analysis_engine.calculate_financial_ratios(financial_data)
                analysis_results['financial_ratios'] = ratios
                logger.info("Financial ratios calculated successfully")
            except Exception as e:
                logger.error(f"Error calculating financial ratios: {str(e)}")
                analysis_results['financial_ratios'] = {'error': str(e)}
            
            # Step 2: Detect Financial Anomalies
            logger.info("Detecting financial anomalies...")
            try:
                anomalies = self.analysis_engine.detect_financial_anomalies(financial_data)
                analysis_results['anomaly_detection'] = anomalies
                
                # If anomalies found, get AI explanation
                if anomalies.get('anomalies') and len(anomalies['anomalies']) > 0:
                    logger.info("Explaining anomalies with AI...")
                    anomaly_explanation = self.gemini_analyzer.explain_financial_anomaly(anomalies)
                    analysis_results['anomaly_explanation'] = anomaly_explanation
                
                logger.info(f"Anomaly detection completed - found {len(anomalies.get('anomalies', []))} anomalies")
            except Exception as e:
                logger.error(f"Error detecting financial anomalies: {str(e)}")
                analysis_results['anomaly_detection'] = {'error': str(e)}
            
            # Step 3: Create Financial Forecasts
            logger.info("Creating financial forecasts...")
            try:
                forecast_years = options.get('forecast_years', 3)
                forecasts = self.analysis_engine.create_financial_forecasts(financial_data, forecast_years)
                analysis_results['financial_forecasts'] = forecasts
                
                # Get AI validation of forecasts
                if forecasts.get('forecasts'):
                    logger.info("Validating forecasts with AI...")
                    forecast_validation = self.gemini_analyzer.validate_financial_forecasts(forecasts)
                    analysis_results['forecast_validation'] = forecast_validation
                
                logger.info("Financial forecasts created successfully")
            except Exception as e:
                logger.error(f"Error creating financial forecasts: {str(e)}")
                analysis_results['financial_forecasts'] = {'error': str(e)}
            
            # Step 4: Analyze MD&A if available
            if options.get('include_narrative_analysis', True):
                mda_text = self._extract_mda_text(financial_data)
                if mda_text:
                    logger.info("Analyzing MD&A section...")
                    try:
                        mda_analysis = self.gemini_analyzer.analyze_mda_section(mda_text)
                        analysis_results['mda_analysis'] = mda_analysis
                        logger.info("MD&A analysis completed")
                    except Exception as e:
                        logger.error(f"Error analyzing MD&A: {str(e)}")
                        analysis_results['mda_analysis'] = {'error': str(e)}
            
            # Step 5: Generate Risk Assessment
            logger.info("Generating risk assessment...")
            try:
                risk_assessment = self._generate_risk_assessment(analysis_results)
                analysis_results['risk_assessment'] = risk_assessment
                logger.info("Risk assessment completed")
            except Exception as e:
                logger.error(f"Error generating risk assessment: {str(e)}")
                analysis_results['risk_assessment'] = {'error': str(e)}
            
            # Step 6: Create Executive Summary
            logger.info("Creating executive summary...")
            try:
                executive_summary = self._create_executive_summary(analysis_results)
                analysis_results['executive_summary'] = executive_summary
                logger.info("Executive summary created")
            except Exception as e:
                logger.error(f"Error creating executive summary: {str(e)}")
                analysis_results['executive_summary'] = {'error': str(e)}
            
            # Add analysis metadata
            analysis_results['metadata'] = {
                'analysis_duration': 'completed',
                'components_analyzed': list(analysis_results.keys()),
                'data_quality_score': self._assess_overall_data_quality(analysis_results),
                'confidence_level': self._calculate_confidence_level(analysis_results)
            }
            
            logger.info("Comprehensive financial analysis completed successfully")
            return analysis_results
            
        except Exception as e:
            logger.error(f"Error in comprehensive financial analysis: {str(e)}")
            return {
                'agent_id': self.agent_id,
                'error': str(e),
                'analysis_date': datetime.now().isoformat(),
                'status': 'failed'
            }
    
    def quick_financial_health_check(self, financial_data: Dict) -> Dict[str, Any]:
        """
        Perform a quick financial health assessment
        
        Args:
            financial_data: Raw financial data
            
        Returns:
            Dictionary containing quick health assessment
        """
        try:
            logger.info("Performing quick financial health check...")
            
            # Calculate key ratios only
            ratios = self.analysis_engine.calculate_financial_ratios(financial_data)
            
            # Assess financial health based on key metrics
            health_score = self._calculate_health_score(ratios)
            
            # Quick anomaly check
            anomalies = self.analysis_engine.detect_financial_anomalies(financial_data)
            
            result = {
                'agent_id': self.agent_id,
                'analysis_type': 'quick_health_check',
                'analysis_date': datetime.now().isoformat(),
                'company_symbol': financial_data.get('metadata', {}).get('symbol', 'Unknown'),
                'health_score': health_score,
                'key_ratios': self._extract_key_ratios(ratios),
                'anomaly_count': len(anomalies.get('anomalies', [])),
                'recommendation': self._get_health_recommendation(health_score, anomalies)
            }
            
            logger.info(f"Quick health check completed - Health Score: {health_score['overall_score']}")
            return result
            
        except Exception as e:
            logger.error(f"Error in quick financial health check: {str(e)}")
            return {
                'agent_id': self.agent_id,
                'error': str(e),
                'analysis_type': 'quick_health_check',
                'analysis_date': datetime.now().isoformat(),
                'status': 'failed'
            }
    
    def compare_companies(self, company_data_list: List[Dict]) -> Dict[str, Any]:
        """
        Compare financial metrics across multiple companies
        
        Args:
            company_data_list: List of company financial data
            
        Returns:
            Dictionary containing comparative analysis
        """
        try:
            logger.info(f"Comparing {len(company_data_list)} companies...")
            
            if len(company_data_list) < 2:
                raise ValueError("At least 2 companies required for comparison")
            
            comparison_results = {
                'agent_id': self.agent_id,
                'analysis_type': 'company_comparison',
                'analysis_date': datetime.now().isoformat(),
                'companies_compared': len(company_data_list)
            }
            
            # Calculate ratios for each company
            company_ratios = []
            for i, company_data in enumerate(company_data_list):
                try:
                    ratios = self.analysis_engine.calculate_financial_ratios(company_data)
                    company_ratios.append({
                        'symbol': company_data.get('metadata', {}).get('symbol', f'Company_{i+1}'),
                        'ratios': ratios
                    })
                except Exception as e:
                    logger.warning(f"Failed to calculate ratios for company {i+1}: {str(e)}")
            
            # Perform comparative analysis
            if len(company_ratios) >= 2:
                comparison_results['comparative_analysis'] = self._perform_comparative_analysis(company_ratios)
                comparison_results['rankings'] = self._rank_companies(company_ratios)
                comparison_results['peer_analysis'] = self._generate_peer_analysis(company_ratios)
            
            logger.info("Company comparison completed successfully")
            return comparison_results
            
        except Exception as e:
            logger.error(f"Error in company comparison: {str(e)}")
            return {
                'agent_id': self.agent_id,
                'error': str(e),
                'analysis_type': 'company_comparison',
                'analysis_date': datetime.now().isoformat(),
                'status': 'failed'
            }
    
    def _extract_mda_text(self, financial_data: Dict) -> Optional[str]:
        """Extract MD&A text from financial data if available"""
        # This would typically extract from SEC filings or annual reports
        # For now, return None as we don't have MD&A text in our current data structure
        return None
    
    def _generate_risk_assessment(self, analysis_results: Dict) -> Dict[str, Any]:
        """Generate comprehensive risk assessment"""
        risk_factors = []
        risk_score = 0
        
        # Analyze financial ratios for risks
        ratios = analysis_results.get('financial_ratios', {})
        if 'leverage' in ratios:
            debt_ratios = ratios['leverage']
            if 'debt_to_equity' in debt_ratios:
                avg_de_ratio = sum(debt_ratios['debt_to_equity']) / len(debt_ratios['debt_to_equity']) if debt_ratios['debt_to_equity'] else 0
                if avg_de_ratio > 2.0:
                    risk_factors.append("High debt-to-equity ratio indicates elevated financial risk")
                    risk_score += 20
        
        # Analyze anomalies for risks
        anomalies = analysis_results.get('anomaly_detection', {})
        anomaly_count = len(anomalies.get('anomalies', []))
        if anomaly_count > 0:
            risk_factors.append(f"{anomaly_count} financial anomalies detected requiring investigation")
            risk_score += min(anomaly_count * 10, 30)
        
        # Analyze profitability trends
        if 'profitability' in ratios:
            profit_ratios = ratios['profitability']
            if 'net_margin' in profit_ratios and profit_ratios['net_margin']:
                recent_margin = profit_ratios['net_margin'][0] if profit_ratios['net_margin'] else 0
                if recent_margin < 0:
                    risk_factors.append("Negative profit margins indicate profitability concerns")
                    risk_score += 25
        
        # Classify overall risk level
        if risk_score >= 50:
            risk_level = "High"
        elif risk_score >= 25:
            risk_level = "Medium"
        else:
            risk_level = "Low"
        
        return {
            'overall_risk_level': risk_level,
            'risk_score': min(risk_score, 100),
            'risk_factors': risk_factors,
            'mitigation_recommendations': self._get_risk_mitigation_recommendations(risk_factors)
        }
    
    def _create_executive_summary(self, analysis_results: Dict) -> Dict[str, Any]:
        """Create executive summary of financial analysis"""
        summary = {
            'company_symbol': analysis_results.get('company_symbol', 'Unknown'),
            'analysis_date': analysis_results.get('analysis_date'),
            'key_findings': [],
            'recommendations': [],
            'overall_assessment': 'Neutral'
        }
        
        # Analyze key findings
        ratios = analysis_results.get('financial_ratios', {})
        if 'profitability' in ratios and 'net_margin' in ratios['profitability']:
            net_margins = ratios['profitability']['net_margin']
            if net_margins:
                recent_margin = net_margins[0]
                if recent_margin > 10:
                    summary['key_findings'].append("Strong profitability with healthy net margins")
                elif recent_margin < 0:
                    summary['key_findings'].append("Profitability concerns with negative net margins")
        
        # Analyze anomalies
        anomalies = analysis_results.get('anomaly_detection', {})
        if anomalies.get('anomalies'):
            summary['key_findings'].append(f"{len(anomalies['anomalies'])} financial anomalies require attention")
        
        # Risk assessment
        risk_assessment = analysis_results.get('risk_assessment', {})
        risk_level = risk_assessment.get('overall_risk_level', 'Unknown')
        summary['key_findings'].append(f"Overall financial risk level: {risk_level}")
        
        # Generate recommendations
        if risk_level == "High":
            summary['recommendations'].append("Immediate financial review and risk mitigation required")
            summary['overall_assessment'] = 'Caution'
        elif risk_level == "Medium":
            summary['recommendations'].append("Monitor key financial metrics closely")
            summary['overall_assessment'] = 'Neutral'
        else:
            summary['recommendations'].append("Continue current financial management practices")
            summary['overall_assessment'] = 'Positive'
        
        return summary
    
    def _assess_overall_data_quality(self, analysis_results: Dict) -> float:
        """Assess overall data quality of the analysis"""
        quality_scores = []
        
        # Check financial ratios quality
        ratios = analysis_results.get('financial_ratios', {})
        if 'metadata' in ratios:
            quality_scores.append(ratios['metadata'].get('data_quality_score', 0.5))
        
        # Check if key components completed successfully
        key_components = ['financial_ratios', 'anomaly_detection', 'financial_forecasts']
        successful_components = sum(1 for comp in key_components if comp in analysis_results and 'error' not in analysis_results[comp])
        component_score = successful_components / len(key_components)
        quality_scores.append(component_score)
        
        return sum(quality_scores) / len(quality_scores) if quality_scores else 0.5
    
    def _calculate_confidence_level(self, analysis_results: Dict) -> str:
        """Calculate confidence level of the analysis"""
        data_quality = self._assess_overall_data_quality(analysis_results)
        
        if data_quality >= 0.8:
            return "High"
        elif data_quality >= 0.6:
            return "Medium"
        else:
            return "Low"
    
    def _calculate_health_score(self, ratios: Dict) -> Dict[str, Any]:
        """Calculate financial health score"""
        scores = []
        
        # Profitability score
        if 'profitability' in ratios and 'net_margin' in ratios['profitability']:
            net_margins = ratios['profitability']['net_margin']
            if net_margins:
                recent_margin = net_margins[0]
                if recent_margin > 15:
                    scores.append(90)
                elif recent_margin > 5:
                    scores.append(70)
                elif recent_margin > 0:
                    scores.append(50)
                else:
                    scores.append(20)
        
        # Liquidity score
        if 'liquidity' in ratios and 'current_ratio' in ratios['liquidity']:
            current_ratios = ratios['liquidity']['current_ratio']
            if current_ratios:
                recent_ratio = current_ratios[0]
                if recent_ratio > 2:
                    scores.append(80)
                elif recent_ratio > 1.5:
                    scores.append(70)
                elif recent_ratio > 1:
                    scores.append(60)
                else:
                    scores.append(30)
        
        # Leverage score
        if 'leverage' in ratios and 'debt_to_equity' in ratios['leverage']:
            de_ratios = ratios['leverage']['debt_to_equity']
            if de_ratios:
                recent_ratio = de_ratios[0]
                if recent_ratio < 0.5:
                    scores.append(90)
                elif recent_ratio < 1:
                    scores.append(70)
                elif recent_ratio < 2:
                    scores.append(50)
                else:
                    scores.append(20)
        
        overall_score = sum(scores) / len(scores) if scores else 50
        
        return {
            'overall_score': round(overall_score, 1),
            'component_scores': {
                'profitability': scores[0] if len(scores) > 0 else None,
                'liquidity': scores[1] if len(scores) > 1 else None,
                'leverage': scores[2] if len(scores) > 2 else None
            },
            'grade': self._score_to_grade(overall_score)
        }
    
    def _score_to_grade(self, score: float) -> str:
        """Convert numeric score to letter grade"""
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F"
    
    def _extract_key_ratios(self, ratios: Dict) -> Dict[str, Any]:
        """Extract key ratios for quick display"""
        key_ratios = {}
        
        if 'profitability' in ratios:
            prof = ratios['profitability']
            if 'net_margin' in prof and prof['net_margin']:
                key_ratios['net_margin'] = prof['net_margin'][0]
            if 'roe' in prof and prof['roe']:
                key_ratios['roe'] = prof['roe'][0]
        
        if 'liquidity' in ratios:
            liq = ratios['liquidity']
            if 'current_ratio' in liq and liq['current_ratio']:
                key_ratios['current_ratio'] = liq['current_ratio'][0]
        
        if 'leverage' in ratios:
            lev = ratios['leverage']
            if 'debt_to_equity' in lev and lev['debt_to_equity']:
                key_ratios['debt_to_equity'] = lev['debt_to_equity'][0]
        
        return key_ratios
    
    def _get_health_recommendation(self, health_score: Dict, anomalies: Dict) -> str:
        """Get recommendation based on health score and anomalies"""
        score = health_score['overall_score']
        anomaly_count = len(anomalies.get('anomalies', []))
        
        if score >= 80 and anomaly_count == 0:
            return "Strong financial position - continue current strategy"
        elif score >= 60 and anomaly_count <= 1:
            return "Stable financial position - monitor key metrics"
        elif score >= 40:
            return "Financial concerns identified - detailed review recommended"
        else:
            return "Significant financial risks - immediate attention required"
    
    def _perform_comparative_analysis(self, company_ratios: List[Dict]) -> Dict[str, Any]:
        """Perform comparative analysis across companies"""
        # This is a simplified implementation
        return {
            'companies_analyzed': len(company_ratios),
            'comparison_metrics': ['profitability', 'liquidity', 'leverage'],
            'analysis_note': 'Detailed comparative analysis implementation pending'
        }
    
    def _rank_companies(self, company_ratios: List[Dict]) -> List[Dict]:
        """Rank companies based on financial performance"""
        # Simplified ranking implementation
        rankings = []
        for i, company in enumerate(company_ratios):
            rankings.append({
                'rank': i + 1,
                'symbol': company['symbol'],
                'score': 75 - (i * 5)  # Placeholder scoring
            })
        return rankings
    
    def _generate_peer_analysis(self, company_ratios: List[Dict]) -> Dict[str, Any]:
        """Generate peer analysis"""
        return {
            'peer_group_size': len(company_ratios),
            'analysis_note': 'Peer analysis implementation pending'
        }
    
    def _get_risk_mitigation_recommendations(self, risk_factors: List[str]) -> List[str]:
        """Get risk mitigation recommendations"""
        recommendations = []
        
        for risk in risk_factors:
            if "debt" in risk.lower():
                recommendations.append("Consider debt reduction strategies and refinancing options")
            elif "anomal" in risk.lower():
                recommendations.append("Conduct detailed investigation of financial anomalies")
            elif "margin" in risk.lower():
                recommendations.append("Focus on cost reduction and revenue optimization")
        
        if not recommendations:
            recommendations.append("Continue monitoring financial performance")
        
        return recommendations
    
    def analyze_company_with_intelligence(self, company_identifier: str, options: Dict = None) -> Dict[str, Any]:
        """
        Perform comprehensive financial analysis enhanced with intelligent insights
        
        Args:
            company_identifier: Company name, ticker, or partial identifier
            options: Analysis options and preferences
            
        Returns:
            Dictionary containing comprehensive financial analysis with intelligent insights
        """
        try:
            logger.info(f"Starting intelligent financial analysis for: {company_identifier}")
            
            if not options:
                options = {}
            
            analysis_results = {
                'agent_id': self.agent_id,
                'analysis_type': 'intelligent_comprehensive',
                'analysis_date': datetime.now().isoformat(),
                'company_identifier': company_identifier,
                'version': self.version
            }
            
            # Step 1: Smart company lookup to get accurate company data
            logger.info("Performing smart company lookup...")
            try:
                lookup_result = self.intelligent_financial.smart_company_lookup(company_identifier, {
                    'includeFinancials': True,
                    'includeRiskScore': False,
                    'maxResults': 1
                })
                
                if lookup_result['totalResults'] == 0:
                    return {
                        'agent_id': self.agent_id,
                        'error': f'No company found matching "{company_identifier}"',
                        'analysis_date': datetime.now().isoformat(),
                        'status': 'failed'
                    }
                
                primary_company = lookup_result['results'][0]
                analysis_results['company_info'] = {
                    'symbol': primary_company['symbol'],
                    'name': primary_company['name'],
                    'industry': primary_company.get('industry'),
                    'sector': primary_company.get('sector'),
                    'lookup_confidence': lookup_result['confidence']
                }
                
                logger.info(f"Company identified: {primary_company['name']} ({primary_company['symbol']})")
                
            except Exception as e:
                logger.error(f"Smart company lookup failed: {str(e)}")
                analysis_results['company_lookup_error'] = str(e)
                # Continue with traditional analysis using the original identifier
                analysis_results['company_info'] = {
                    'symbol': company_identifier,
                    'name': 'Unknown',
                    'lookup_confidence': 0.0
                }
            
            company_symbol = analysis_results['company_info']['symbol']
            
            # Step 2: Get financial data for traditional analysis
            logger.info("Retrieving financial data...")
            try:
                # This would typically call the financial data service
                # For now, we'll create a placeholder that would integrate with existing services
                financial_data = self._get_financial_data_for_analysis(company_symbol)
                
                if financial_data:
                    # Step 3: Perform traditional financial analysis
                    logger.info("Performing traditional financial analysis...")
                    traditional_analysis = self.analyze_company_financials(financial_data, options)
                    analysis_results['traditional_analysis'] = traditional_analysis
                else:
                    logger.warning("No financial data available for traditional analysis")
                    analysis_results['traditional_analysis'] = {
                        'error': 'No financial data available',
                        'available': False
                    }
                    
            except Exception as e:
                logger.error(f"Traditional financial analysis failed: {str(e)}")
                analysis_results['traditional_analysis'] = {
                    'error': str(e),
                    'available': False
                }
            
            # Step 4: Get intelligent insights
            logger.info("Gathering intelligent financial insights...")
            try:
                # Peer analysis
                peer_analysis = self.intelligent_financial.identify_peer_companies(company_symbol, {
                    'maxPeers': options.get('max_peers', 5),
                    'includeFinancials': False,
                    'similarityThreshold': options.get('similarity_threshold', 0.7)
                })
                analysis_results['peer_analysis'] = peer_analysis
                logger.info(f"Peer analysis completed: {peer_analysis['peersFound']} peers found")
                
            except Exception as e:
                logger.warning(f"Peer analysis failed: {str(e)}")
                analysis_results['peer_analysis'] = {
                    'error': str(e),
                    'available': False
                }
            
            try:
                # Risk scoring
                risk_assessment = self.intelligent_financial.build_comprehensive_risk_score(company_symbol, {
                    'includePeerComparison': True,
                    'includeHistoricalTrends': True,
                    'riskHorizon': options.get('risk_horizon', '1year')
                })
                analysis_results['intelligent_risk_assessment'] = risk_assessment
                logger.info(f"Risk assessment completed: {risk_assessment['riskLevel']} ({risk_assessment['overallRiskScore']}/100)")
                
            except Exception as e:
                logger.warning(f"Intelligent risk assessment failed: {str(e)}")
                analysis_results['intelligent_risk_assessment'] = {
                    'error': str(e),
                    'available': False
                }
            
            # Step 5: Generate integrated insights
            logger.info("Generating integrated insights...")
            analysis_results['integrated_insights'] = self._generate_integrated_insights(analysis_results)
            
            # Step 6: Create comprehensive executive summary
            analysis_results['comprehensive_summary'] = self._create_comprehensive_summary(analysis_results)
            
            # Step 7: Add analysis metadata
            analysis_results['metadata'] = {
                'analysis_duration': 'completed',
                'components_analyzed': list(analysis_results.keys()),
                'intelligent_features_used': [
                    'smart_company_lookup',
                    'peer_identification',
                    'ml_risk_scoring'
                ],
                'confidence_level': self._calculate_overall_confidence(analysis_results)
            }
            
            logger.info("Intelligent comprehensive financial analysis completed successfully")
            return analysis_results
            
        except Exception as e:
            logger.error(f"Error in intelligent financial analysis: {str(e)}")
            return {
                'agent_id': self.agent_id,
                'error': str(e),
                'analysis_type': 'intelligent_comprehensive',
                'analysis_date': datetime.now().isoformat(),
                'status': 'failed'
            }
    
    def _get_financial_data_for_analysis(self, symbol: str) -> Optional[Dict]:
        """
        Get financial data for traditional analysis
        This is a placeholder that would integrate with existing financial data services
        """
        try:
            # This would typically call the existing financial data service
            # For now, return dummy data for testing
            return self._create_dummy_financial_data()
        except Exception as e:
            logger.error(f"Failed to get financial data for {symbol}: {str(e)}")
            return None
    
    def _generate_integrated_insights(self, analysis_results: Dict) -> List[str]:
        """Generate insights that combine traditional and intelligent analysis"""
        insights = []
        
        # Company identification insights
        company_info = analysis_results.get('company_info', {})
        if company_info.get('lookup_confidence', 0) > 0.8:
            insights.append(f"High confidence company identification: {company_info.get('name')} ({company_info.get('symbol')})")
        
        # Traditional vs intelligent risk comparison
        traditional_risk = analysis_results.get('traditional_analysis', {}).get('risk_assessment', {})
        intelligent_risk = analysis_results.get('intelligent_risk_assessment', {})
        
        if not traditional_risk.get('error') and not intelligent_risk.get('error'):
            trad_level = traditional_risk.get('overall_risk_level', 'Unknown')
            intel_level = intelligent_risk.get('riskLevel', 'Unknown')
            
            if trad_level == intel_level:
                insights.append(f"Risk assessment consensus: Both traditional and ML-based analysis indicate {trad_level} risk")
            else:
                insights.append(f"Risk assessment divergence: Traditional analysis shows {trad_level} risk, ML-based shows {intel_level} risk")
        
        # Peer analysis insights
        peer_analysis = analysis_results.get('peer_analysis', {})
        if not peer_analysis.get('error') and peer_analysis.get('peersFound', 0) > 0:
            insights.append(f"Peer analysis available: {peer_analysis['peersFound']} similar companies identified for benchmarking")
            
            # Add top peer insight
            if peer_analysis.get('peers'):
                top_peer = peer_analysis['peers'][0]
                similarity = top_peer.get('similarityScore', 0) * 100
                insights.append(f"Most similar peer: {top_peer.get('name')} with {similarity:.1f}% financial similarity")
        
        # ML-based risk insights
        if not intelligent_risk.get('error'):
            risk_components = intelligent_risk.get('riskComponents', {})
            high_risk_areas = [name for name, data in risk_components.items() if data.get('level') == 'High']
            
            if high_risk_areas:
                insights.append(f"ML-identified high risk areas: {', '.join(high_risk_areas)}")
            
            # Peer risk comparison
            peer_comparison = intelligent_risk.get('peerComparison', {})
            if peer_comparison.get('available'):
                insights.append(f"Risk vs peers: {peer_comparison.get('comparison', 'Unknown')}")
        
        return insights
    
    def _create_comprehensive_summary(self, analysis_results: Dict) -> Dict[str, Any]:
        """Create comprehensive executive summary combining all analysis components"""
        summary = {
            'company': analysis_results.get('company_info', {}),
            'analysis_date': analysis_results.get('analysis_date'),
            'key_findings': [],
            'risk_assessment': {},
            'peer_insights': [],
            'recommendations': [],
            'overall_assessment': 'Neutral'
        }
        
        # Combine key findings from all sources
        traditional_summary = analysis_results.get('traditional_analysis', {}).get('executive_summary', {})
        if traditional_summary and not traditional_summary.get('error'):
            summary['key_findings'].extend(traditional_summary.get('key_findings', []))
        
        # Add intelligent insights
        integrated_insights = analysis_results.get('integrated_insights', [])
        summary['key_findings'].extend(integrated_insights)
        
        # Risk assessment summary
        intelligent_risk = analysis_results.get('intelligent_risk_assessment', {})
        if not intelligent_risk.get('error'):
            summary['risk_assessment'] = {
                'overall_level': intelligent_risk.get('riskLevel'),
                'score': intelligent_risk.get('overallRiskScore'),
                'confidence': intelligent_risk.get('confidence', {}).get('level'),
                'peer_comparison': intelligent_risk.get('peerComparison', {}).get('comparison')
            }
        
        # Peer insights
        peer_analysis = analysis_results.get('peer_analysis', {})
        if not peer_analysis.get('error') and peer_analysis.get('peersFound', 0) > 0:
            summary['peer_insights'] = [
                f"{peer_analysis['peersFound']} peer companies identified",
                f"Industry focus: {analysis_results.get('company_info', {}).get('industry', 'Unknown')}"
            ]
            
            if peer_analysis.get('insights'):
                summary['peer_insights'].extend(peer_analysis['insights'][:2])
        
        # Combine recommendations
        if traditional_summary and traditional_summary.get('recommendations'):
            summary['recommendations'].extend(traditional_summary['recommendations'])
        
        if not intelligent_risk.get('error') and intelligent_risk.get('recommendations'):
            summary['recommendations'].extend(intelligent_risk['recommendations'][:2])
        
        # Overall assessment
        risk_level = summary['risk_assessment'].get('overall_level', 'Unknown')
        if risk_level == 'Low':
            summary['overall_assessment'] = 'Positive'
        elif risk_level == 'High':
            summary['overall_assessment'] = 'Caution'
        else:
            summary['overall_assessment'] = 'Neutral'
        
        return summary
    
    def _calculate_overall_confidence(self, analysis_results: Dict) -> str:
        """Calculate overall confidence level for the comprehensive analysis"""
        confidence_scores = []
        
        # Company lookup confidence
        company_confidence = analysis_results.get('company_info', {}).get('lookup_confidence', 0)
        confidence_scores.append(company_confidence)
        
        # Traditional analysis confidence
        traditional_analysis = analysis_results.get('traditional_analysis', {})
        if not traditional_analysis.get('error'):
            trad_confidence = traditional_analysis.get('metadata', {}).get('confidence_level', 'Medium')
            confidence_map = {'High': 0.9, 'Medium': 0.7, 'Low': 0.5}
            confidence_scores.append(confidence_map.get(trad_confidence, 0.5))
        
        # Intelligent risk assessment confidence
        intelligent_risk = analysis_results.get('intelligent_risk_assessment', {})
        if not intelligent_risk.get('error'):
            risk_confidence = intelligent_risk.get('confidence', {}).get('overall', 0.5)
            confidence_scores.append(risk_confidence)
        
        # Calculate average confidence
        if confidence_scores:
            avg_confidence = sum(confidence_scores) / len(confidence_scores)
            if avg_confidence >= 0.8:
                return 'High'
            elif avg_confidence >= 0.6:
                return 'Medium'
            else:
                return 'Low'
        
        return 'Low'

    def test_agent_capabilities(self) -> Dict[str, Any]:
        """
        Test all agent capabilities
        
        Returns:
            Dictionary containing test results
        """
        try:
            logger.info("Testing Finance Agent capabilities...")
            
            test_results = {
                'agent_id': self.agent_id,
                'version': self.version,
                'test_date': datetime.now().isoformat(),
                'capabilities': {}
            }
            
            # Test financial analysis engine
            try:
                # Create dummy financial data for testing
                dummy_data = self._create_dummy_financial_data()
                ratios = self.analysis_engine.calculate_financial_ratios(dummy_data)
                test_results['capabilities']['financial_ratios'] = {
                    'status': 'working',
                    'ratios_calculated': len(ratios)
                }
            except Exception as e:
                test_results['capabilities']['financial_ratios'] = {
                    'status': 'error',
                    'error': str(e)
                }
            
            # Test Gemini integration
            gemini_test = self.gemini_analyzer.test_connection()
            test_results['capabilities']['gemini_integration'] = gemini_test
            
            # Test Intelligent Financial Integration
            try:
                intelligent_test = self.intelligent_financial.test_service_connection()
                test_results['capabilities']['intelligent_financial'] = {
                    'status': 'working' if intelligent_test.get('overallStatus') == 'operational' else 'error',
                    'capabilities': intelligent_test.get('workingCapabilities', '0/0'),
                    'service_available': intelligent_test.get('overallStatus') == 'operational'
                }
            except Exception as e:
                test_results['capabilities']['intelligent_financial'] = {
                    'status': 'error',
                    'error': str(e),
                    'service_available': False
                }
            
            # Test anomaly detection
            try:
                dummy_data = self._create_dummy_financial_data()
                anomalies = self.analysis_engine.detect_financial_anomalies(dummy_data)
                test_results['capabilities']['anomaly_detection'] = {
                    'status': 'working',
                    'test_anomalies': len(anomalies.get('anomalies', []))
                }
            except Exception as e:
                test_results['capabilities']['anomaly_detection'] = {
                    'status': 'error',
                    'error': str(e)
                }
            
            # Test forecasting
            try:
                dummy_data = self._create_dummy_financial_data()
                forecasts = self.analysis_engine.create_financial_forecasts(dummy_data, 2)
                test_results['capabilities']['forecasting'] = {
                    'status': 'working',
                    'metrics_forecasted': len(forecasts.get('forecasts', {}))
                }
            except Exception as e:
                test_results['capabilities']['forecasting'] = {
                    'status': 'error',
                    'error': str(e)
                }
            
            # Overall status
            working_capabilities = sum(1 for cap in test_results['capabilities'].values() 
                                     if isinstance(cap, dict) and cap.get('status') == 'working')
            total_capabilities = len([cap for cap in test_results['capabilities'].values() 
                                    if isinstance(cap, dict) and 'status' in cap])
            
            test_results['overall_status'] = 'operational' if working_capabilities > 0 else 'failed'
            test_results['capabilities_working'] = f"{working_capabilities}/{total_capabilities}"
            
            logger.info(f"Finance Agent test completed - {working_capabilities}/{total_capabilities} capabilities working")
            return test_results
            
        except Exception as e:
            logger.error(f"Error testing Finance Agent capabilities: {str(e)}")
            return {
                'agent_id': self.agent_id,
                'error': str(e),
                'test_date': datetime.now().isoformat(),
                'overall_status': 'failed'
            }
    
    def _create_dummy_financial_data(self) -> Dict[str, Any]:
        """Create dummy financial data for testing"""
        return {
            'statements': {
                'incomeStatement': [
                    {
                        'date': '2023-12-31',
                        'revenue': 100000000,
                        'netIncome': 10000000,
                        'grossProfit': 40000000,
                        'operatingIncome': 15000000
                    },
                    {
                        'date': '2022-12-31',
                        'revenue': 90000000,
                        'netIncome': 8000000,
                        'grossProfit': 36000000,
                        'operatingIncome': 12000000
                    },
                    {
                        'date': '2021-12-31',
                        'revenue': 80000000,
                        'netIncome': 6000000,
                        'grossProfit': 32000000,
                        'operatingIncome': 10000000
                    }
                ],
                'balanceSheet': [
                    {
                        'date': '2023-12-31',
                        'totalAssets': 200000000,
                        'totalLiabilities': 120000000,
                        'totalStockholdersEquity': 80000000,
                        'cashAndCashEquivalents': 20000000,
                        'totalDebt': 50000000,
                        'totalCurrentAssets': 60000000,
                        'totalCurrentLiabilities': 30000000
                    },
                    {
                        'date': '2022-12-31',
                        'totalAssets': 180000000,
                        'totalLiabilities': 110000000,
                        'totalStockholdersEquity': 70000000,
                        'cashAndCashEquivalents': 15000000,
                        'totalDebt': 45000000,
                        'totalCurrentAssets': 50000000,
                        'totalCurrentLiabilities': 25000000
                    }
                ],
                'cashFlow': [
                    {
                        'date': '2023-12-31',
                        'operatingCashFlow': 12000000,
                        'freeCashFlow': 8000000,
                        'capitalExpenditure': 4000000
                    },
                    {
                        'date': '2022-12-31',
                        'operatingCashFlow': 10000000,
                        'freeCashFlow': 6000000,
                        'capitalExpenditure': 4000000
                    }
                ]
            },
            'metadata': {
                'symbol': 'TEST',
                'source': 'dummy_data'
            }
        }


if __name__ == "__main__":
    # Test the Finance Agent
    agent = FinanceAgent()
    test_results = agent.test_agent_capabilities()
    print(json.dumps(test_results, indent=2))