"""
AI-Powered Reputation Agent
Main orchestrator for comprehensive reputation analysis and monitoring
"""

import os
import sys
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import json

# Add the agents directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from reputation.reputation_data_collector import ReputationDataCollector
from reputation.sentiment_analyzer import SentimentAnalyzer
from reputation.gemini_reputation_analyzer import GeminiReputationAnalyzer
from reputation.reputation_scorer import ReputationScorer

logger = logging.getLogger(__name__)

class ReputationAgent:
    """
    AI-Powered Reputation Agent with comprehensive sentiment analysis
    """
    
    def __init__(self):
        """Initialize the Reputation Agent"""
        self.data_collector = ReputationDataCollector()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.gemini_analyzer = GeminiReputationAnalyzer()
        self.scorer = ReputationScorer()
        
        self.agent_id = "reputation_agent"
        self.version = "1.0.0"
        
        logger.info(f"Reputation Agent {self.version} initialized with comprehensive analysis capabilities")
    
    def analyze_company_reputation(self, 
                                 company_name: str,
                                 ticker: str = None,
                                 industry: str = None,
                                 days_back: int = 30,
                                 include_ai_analysis: bool = True) -> Dict[str, Any]:
        """
        Perform comprehensive reputation analysis for a company
        
        Args:
            company_name: Name of the company to analyze
            ticker: Stock ticker symbol if available
            industry: Industry sector if known
            days_back: Number of days to look back for data collection
            include_ai_analysis: Whether to include Gemini AI analysis
            
        Returns:
            Dictionary containing comprehensive reputation analysis
        """
        try:
            logger.info(f"Starting comprehensive reputation analysis for {company_name}")
            
            # 1. Collect reputation data from all sources
            logger.info("Collecting reputation data...")
            reputation_data = self.data_collector.collect_comprehensive_reputation_data(
                company_name=company_name,
                ticker=ticker,
                industry=industry,
                days_back=days_back
            )
            
            # 2. Perform sentiment analysis
            logger.info("Analyzing sentiment...")
            sentiment_analysis = self._perform_comprehensive_sentiment_analysis(reputation_data)
            
            # 3. Generate AI-powered insights (if enabled)
            ai_analysis = {}
            if include_ai_analysis:
                logger.info("Generating AI-powered insights...")
                ai_analysis = self._perform_ai_analysis(reputation_data)
            
            # 4. Calculate reputation scores
            logger.info("Calculating reputation scores...")
            reputation_scores = self.scorer.calculate_comprehensive_score(
                reputation_data, sentiment_analysis
            )
            
            # 5. Calculate ESG scores
            esg_scores = self.scorer.calculate_esg_scores(
                reputation_data, ai_analysis.get('esg_assessment', {})
            )
            
            # 6. Generate alerts and recommendations
            alerts = self._generate_alerts(reputation_data, ai_analysis)
            
            # 7. Compile comprehensive analysis
            comprehensive_analysis = {
                'company_name': company_name,
                'ticker': ticker,
                'industry': industry,
                'analysis_metadata': {
                    'agent_version': self.version,
                    'analysis_timestamp': datetime.now().isoformat(),
                    'days_analyzed': days_back,
                    'ai_analysis_included': include_ai_analysis
                },
                'reputation_data': reputation_data,
                'sentiment_analysis': sentiment_analysis,
                'ai_analysis': ai_analysis,
                'reputation_scores': reputation_scores,
                'esg_scores': esg_scores,
                'alerts': alerts,
                'summary': self._generate_executive_summary(
                    reputation_scores, sentiment_analysis, ai_analysis, alerts
                )
            }
            
            logger.info(f"Completed comprehensive reputation analysis for {company_name}")
            
            return comprehensive_analysis
            
        except Exception as e:
            logger.error(f"Error in comprehensive reputation analysis: {e}")
            return {
                'company_name': company_name,
                'error': str(e),
                'analysis_timestamp': datetime.now().isoformat()
            }
    
    def monitor_reputation_changes(self, 
                                 company_name: str,
                                 previous_analysis: Dict[str, Any] = None,
                                 **kwargs) -> Dict[str, Any]:
        """
        Monitor reputation changes and generate trend analysis
        
        Args:
            company_name: Name of the company to monitor
            previous_analysis: Previous analysis for comparison
            **kwargs: Additional parameters for analysis
            
        Returns:
            Dictionary containing change analysis and alerts
        """
        try:
            logger.info(f"Monitoring reputation changes for {company_name}")
            
            # Perform current analysis
            current_analysis = self.analyze_company_reputation(
                company_name=company_name,
                days_back=kwargs.get('days_back', 7),  # Shorter period for monitoring
                **kwargs
            )
            
            # Compare with previous analysis if available
            change_analysis = {}
            if previous_analysis:
                change_analysis = self._analyze_reputation_changes(
                    previous_analysis, current_analysis
                )
            
            # Generate monitoring alerts
            monitoring_alerts = self._generate_monitoring_alerts(
                current_analysis, change_analysis
            )
            
            return {
                'company_name': company_name,
                'monitoring_timestamp': datetime.now().isoformat(),
                'current_analysis': current_analysis,
                'change_analysis': change_analysis,
                'monitoring_alerts': monitoring_alerts,
                'has_significant_changes': len(monitoring_alerts) > 0
            }
            
        except Exception as e:
            logger.error(f"Error monitoring reputation changes: {e}")
            return {
                'company_name': company_name,
                'error': str(e),
                'monitoring_timestamp': datetime.now().isoformat()
            }
    
    def generate_reputation_report(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a formatted reputation report
        
        Args:
            analysis_data: Complete analysis data
            
        Returns:
            Dictionary containing formatted report
        """
        try:
            company_name = analysis_data.get('company_name', 'Unknown Company')
            
            # Extract key metrics
            reputation_scores = analysis_data.get('reputation_scores', {})
            sentiment_analysis = analysis_data.get('sentiment_analysis', {})
            esg_scores = analysis_data.get('esg_scores', {})
            alerts = analysis_data.get('alerts', [])
            
            # Generate report sections
            report = {
                'company_name': company_name,
                'report_timestamp': datetime.now().isoformat(),
                'executive_summary': analysis_data.get('summary', {}),
                'key_metrics': {
                    'overall_reputation_score': reputation_scores.get('overall_score', 0),
                    'reputation_category': reputation_scores.get('interpretation', {}).get('category', 'unknown'),
                    'overall_esg_score': esg_scores.get('overall_esg_score', 0),
                    'sentiment_trend': sentiment_analysis.get('overall_trend', 'neutral'),
                    'confidence_level': reputation_scores.get('confidence_level', 'low')
                },
                'detailed_scores': {
                    'reputation_breakdown': reputation_scores.get('score_components', {}),
                    'esg_breakdown': {
                        'environmental': esg_scores.get('environmental_score', 0),
                        'social': esg_scores.get('social_score', 0),
                        'governance': esg_scores.get('governance_score', 0)
                    }
                },
                'sentiment_insights': self._extract_sentiment_insights(sentiment_analysis),
                'alerts_summary': {
                    'total_alerts': len(alerts),
                    'critical_alerts': len([a for a in alerts if a.get('severity') == 'critical']),
                    'high_priority_alerts': len([a for a in alerts if a.get('severity') == 'high']),
                    'recent_alerts': alerts[:5]  # Most recent 5 alerts
                },
                'recommendations': self._generate_recommendations(analysis_data),
                'data_quality': {
                    'sources_analyzed': len(analysis_data.get('reputation_data', {}).get('data_sources', {})),
                    'total_data_points': analysis_data.get('reputation_data', {}).get('summary', {}).get('total_data_points', 0),
                    'collection_success_rate': analysis_data.get('reputation_data', {}).get('summary', {}).get('success_rate', 0)
                }
            }
            
            return report
            
        except Exception as e:
            logger.error(f"Error generating reputation report: {e}")
            return {
                'company_name': analysis_data.get('company_name', 'Unknown'),
                'error': str(e),
                'report_timestamp': datetime.now().isoformat()
            }
    
    def _perform_comprehensive_sentiment_analysis(self, reputation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform comprehensive sentiment analysis on all collected data"""
        try:
            sentiment_results = {}
            
            # Analyze news sentiment
            news_data = reputation_data.get('data_sources', {}).get('news', {})
            if news_data and news_data.get('company_articles'):
                sentiment_results['news'] = self.sentiment_analyzer.analyze_news_sentiment(
                    news_data['company_articles']
                )
            
            # Analyze social media sentiment
            social_data = reputation_data.get('data_sources', {}).get('social_media', {})
            if social_data:
                sentiment_results['social_media'] = self.sentiment_analyzer.analyze_social_sentiment(
                    social_data
                )
            
            # Analyze web sources sentiment (reviews, etc.)
            web_data = reputation_data.get('data_sources', {}).get('web_sources', {})
            if web_data:
                # Employee reviews
                glassdoor_reviews = web_data.get('glassdoor', {}).get('reviews', [])
                if glassdoor_reviews:
                    sentiment_results['employee_reviews'] = self.sentiment_analyzer.analyze_review_sentiment(
                        glassdoor_reviews, 'employee'
                    )
                
                # Customer reviews
                trustpilot_reviews = web_data.get('trustpilot', {}).get('reviews', [])
                if trustpilot_reviews:
                    sentiment_results['customer_reviews'] = self.sentiment_analyzer.analyze_review_sentiment(
                        trustpilot_reviews, 'customer'
                    )
            
            # Calculate overall sentiment trend
            all_sentiments = []
            for source_sentiment in sentiment_results.values():
                if isinstance(source_sentiment, dict) and 'average_sentiment' in source_sentiment:
                    all_sentiments.append(source_sentiment['average_sentiment'])
            
            overall_trend = 'neutral'
            if all_sentiments:
                import statistics
                avg_sentiment = statistics.mean(all_sentiments)
                if avg_sentiment > 0.2:
                    overall_trend = 'positive'
                elif avg_sentiment < -0.2:
                    overall_trend = 'negative'
            
            sentiment_results['overall_trend'] = overall_trend
            sentiment_results['analysis_timestamp'] = datetime.now().isoformat()
            
            return sentiment_results
            
        except Exception as e:
            logger.error(f"Error in comprehensive sentiment analysis: {e}")
            return {'error': str(e)}
    
    def _perform_ai_analysis(self, reputation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform AI-powered analysis using Gemini"""
        try:
            ai_results = {}
            
            # Generate comprehensive reputation summary
            ai_results['reputation_summary'] = self.gemini_analyzer.analyze_reputation_summary(
                reputation_data
            )
            
            # Generate ESG assessment
            ai_results['esg_assessment'] = self.gemini_analyzer.generate_esg_assessment(
                reputation_data
            )
            
            # Generate reputation alerts
            ai_results['ai_alerts'] = self.gemini_analyzer.generate_reputation_alerts(
                reputation_data
            )
            
            return ai_results
            
        except Exception as e:
            logger.error(f"Error in AI analysis: {e}")
            return {'error': str(e)}
    
    def _generate_alerts(self, reputation_data: Dict[str, Any], 
                        ai_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate comprehensive alerts from all analysis"""
        alerts = []
        
        try:
            # Add AI-generated alerts
            ai_alerts = ai_analysis.get('ai_alerts', [])
            if isinstance(ai_alerts, list):
                alerts.extend(ai_alerts)
            
            # Add system-generated alerts based on data patterns
            system_alerts = self._generate_system_alerts(reputation_data)
            alerts.extend(system_alerts)
            
            # Sort alerts by severity and timestamp
            severity_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
            alerts.sort(key=lambda x: (
                severity_order.get(x.get('severity', 'low'), 3),
                x.get('timestamp', '')
            ))
            
        except Exception as e:
            logger.error(f"Error generating alerts: {e}")
            alerts.append({
                'type': 'system_error',
                'severity': 'medium',
                'title': 'Alert Generation Error',
                'description': f'Error generating alerts: {str(e)}',
                'timestamp': datetime.now().isoformat()
            })
        
        return alerts
    
    def _generate_system_alerts(self, reputation_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate system-based alerts from data patterns"""
        alerts = []
        
        try:
            # Check data collection success rate
            success_rate = reputation_data.get('summary', {}).get('success_rate', 0)
            if success_rate < 0.5:
                alerts.append({
                    'type': 'data_quality',
                    'severity': 'medium',
                    'title': 'Low Data Collection Success Rate',
                    'description': f'Only {success_rate:.1%} of data sources were successfully collected',
                    'recommended_action': 'Check API keys and data source availability',
                    'timestamp': datetime.now().isoformat(),
                    'source': 'system'
                })
            
            # Check for insufficient data
            total_data_points = reputation_data.get('summary', {}).get('total_data_points', 0)
            if total_data_points < 10:
                alerts.append({
                    'type': 'insufficient_data',
                    'severity': 'high',
                    'title': 'Insufficient Reputation Data',
                    'description': f'Only {total_data_points} data points collected for analysis',
                    'recommended_action': 'Expand data collection timeframe or check company name spelling',
                    'timestamp': datetime.now().isoformat(),
                    'source': 'system'
                })
            
        except Exception as e:
            logger.error(f"Error generating system alerts: {e}")
        
        return alerts
    
    def _generate_executive_summary(self, reputation_scores: Dict[str, Any],
                                  sentiment_analysis: Dict[str, Any],
                                  ai_analysis: Dict[str, Any],
                                  alerts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate executive summary of the reputation analysis"""
        try:
            overall_score = reputation_scores.get('overall_score', 0)
            confidence = reputation_scores.get('confidence_level', 'low')
            interpretation = reputation_scores.get('interpretation', {})
            
            # Count critical issues
            critical_alerts = len([a for a in alerts if a.get('severity') == 'critical'])
            high_alerts = len([a for a in alerts if a.get('severity') == 'high'])
            
            summary = {
                'overall_assessment': interpretation.get('category', 'unknown'),
                'reputation_score': overall_score,
                'confidence_level': confidence,
                'key_findings': [
                    f"Overall reputation score: {overall_score}/100 ({interpretation.get('category', 'unknown')})",
                    f"Analysis confidence: {confidence}",
                    f"Sentiment trend: {sentiment_analysis.get('overall_trend', 'neutral')}"
                ],
                'immediate_concerns': critical_alerts + high_alerts,
                'recommendation_priority': 'high' if critical_alerts > 0 else 'medium' if high_alerts > 0 else 'low'
            }
            
            # Add AI insights if available
            ai_summary = ai_analysis.get('reputation_summary', {})
            if ai_summary and not ai_summary.get('error'):
                summary['ai_insights'] = ai_summary.get('sentiment_explanation', '')
            
            return summary
            
        except Exception as e:
            logger.error(f"Error generating executive summary: {e}")
            return {
                'overall_assessment': 'unknown',
                'error': str(e)
            }
    
    def _extract_sentiment_insights(self, sentiment_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Extract key sentiment insights for reporting"""
        try:
            insights = {
                'overall_trend': sentiment_analysis.get('overall_trend', 'neutral'),
                'source_breakdown': {}
            }
            
            # Extract insights from each source
            for source, data in sentiment_analysis.items():
                if isinstance(data, dict) and 'average_sentiment' in data:
                    insights['source_breakdown'][source] = {
                        'average_sentiment': data.get('average_sentiment', 0),
                        'sentiment_distribution': data.get('sentiment_distribution', {}),
                        'total_analyzed': data.get('total_articles', data.get('total_mentions_analyzed', data.get('total_reviews', 0)))
                    }
            
            return insights
            
        except Exception as e:
            logger.error(f"Error extracting sentiment insights: {e}")
            return {'error': str(e)}
    
    def _generate_recommendations(self, analysis_data: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations based on analysis"""
        recommendations = []
        
        try:
            reputation_scores = analysis_data.get('reputation_scores', {})
            overall_score = reputation_scores.get('overall_score', 0)
            
            # Score-based recommendations
            if overall_score < 40:
                recommendations.extend([
                    "Immediate crisis management response required",
                    "Engage professional reputation management services",
                    "Develop comprehensive communication strategy"
                ])
            elif overall_score < 60:
                recommendations.extend([
                    "Implement proactive reputation monitoring",
                    "Address negative sentiment sources",
                    "Enhance positive communication efforts"
                ])
            elif overall_score < 80:
                recommendations.extend([
                    "Maintain current positive momentum",
                    "Continue monitoring for emerging issues",
                    "Leverage positive sentiment for brand building"
                ])
            
            # Add AI recommendations if available
            ai_analysis = analysis_data.get('ai_analysis', {})
            ai_recommendations = ai_analysis.get('reputation_summary', {}).get('recommendations', [])
            if isinstance(ai_recommendations, list):
                recommendations.extend(ai_recommendations[:3])  # Top 3 AI recommendations
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            recommendations.append("Unable to generate specific recommendations due to analysis error")
        
        return recommendations[:5]  # Return top 5 recommendations
    
    def _analyze_reputation_changes(self, previous_analysis: Dict[str, Any], 
                                  current_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze changes between reputation analyses"""
        try:
            # Compare reputation scores
            prev_score = previous_analysis.get('reputation_scores', {}).get('overall_score', 0)
            curr_score = current_analysis.get('reputation_scores', {}).get('overall_score', 0)
            score_change = curr_score - prev_score
            
            # Compare sentiment trends
            prev_sentiment = previous_analysis.get('sentiment_analysis', {}).get('overall_trend', 'neutral')
            curr_sentiment = current_analysis.get('sentiment_analysis', {}).get('overall_trend', 'neutral')
            
            return {
                'score_change': {
                    'previous_score': prev_score,
                    'current_score': curr_score,
                    'change': score_change,
                    'change_percentage': (score_change / prev_score * 100) if prev_score > 0 else 0
                },
                'sentiment_change': {
                    'previous_trend': prev_sentiment,
                    'current_trend': curr_sentiment,
                    'trend_changed': prev_sentiment != curr_sentiment
                },
                'analysis_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error analyzing reputation changes: {e}")
            return {'error': str(e)}
    
    def _generate_monitoring_alerts(self, current_analysis: Dict[str, Any], 
                                  change_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate alerts for reputation monitoring"""
        alerts = []
        
        try:
            # Check for significant score changes
            score_change = change_analysis.get('score_change', {})
            if abs(score_change.get('change', 0)) > 10:
                severity = 'high' if abs(score_change.get('change', 0)) > 20 else 'medium'
                direction = 'improved' if score_change.get('change', 0) > 0 else 'declined'
                
                alerts.append({
                    'type': 'score_change',
                    'severity': severity,
                    'title': f'Reputation Score {direction.title()}',
                    'description': f'Reputation score {direction} by {abs(score_change.get("change", 0)):.1f} points',
                    'timestamp': datetime.now().isoformat(),
                    'source': 'monitoring'
                })
            
            # Check for sentiment trend changes
            sentiment_change = change_analysis.get('sentiment_change', {})
            if sentiment_change.get('trend_changed', False):
                alerts.append({
                    'type': 'sentiment_change',
                    'severity': 'medium',
                    'title': 'Sentiment Trend Changed',
                    'description': f'Sentiment trend changed from {sentiment_change.get("previous_trend")} to {sentiment_change.get("current_trend")}',
                    'timestamp': datetime.now().isoformat(),
                    'source': 'monitoring'
                })
            
        except Exception as e:
            logger.error(f"Error generating monitoring alerts: {e}")
        
        return alerts