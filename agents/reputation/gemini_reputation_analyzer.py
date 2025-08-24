"""
Gemini AI-Powered Reputation Analyzer
Provides nuanced sentiment analysis and reputation insights using Google's Gemini API
"""

import os
import sys
import logging
import json
from typing import Dict, List, Optional, Any
from datetime import datetime

# Add the agents directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import CONFIG

logger = logging.getLogger(__name__)

class GeminiReputationAnalyzer:
    """
    Advanced reputation analysis using Google's Gemini AI
    """
    
    def __init__(self):
        """Initialize the Gemini Reputation Analyzer"""
        self.api_key = CONFIG['api_keys']['gemini']
        self.client = None
        
        if self.api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                self.client = genai.GenerativeModel('gemini-pro')
                logger.info("Gemini AI client initialized successfully")
            except ImportError:
                logger.warning("Google GenerativeAI library not installed. Install with: pip install google-generativeai")
            except Exception as e:
                logger.warning(f"Failed to initialize Gemini client: {e}")
        else:
            logger.warning("GEMINI_API_KEY not found in environment variables")
    
    def analyze_reputation_summary(self, reputation_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate comprehensive reputation summary using Gemini AI
        
        Args:
            reputation_data: Complete reputation data from all sources
            
        Returns:
            Dictionary containing AI-generated reputation insights
        """
        if not self.client:
            return {
                'error': 'Gemini client not available',
                'summary': 'AI analysis unavailable - using fallback analysis',
                'sentiment_score': 0,
                'key_themes': [],
                'recommendations': []
            }
        
        try:
            company_name = reputation_data.get('company_name', 'Unknown Company')
            
            # Prepare data summary for AI analysis
            data_summary = self._prepare_data_summary(reputation_data)
            
            # Create prompt for comprehensive analysis
            prompt = f"""
            Analyze the reputation data for {company_name} and provide a comprehensive assessment.
            
            Data Summary:
            {data_summary}
            
            Please provide:
            1. Overall reputation sentiment (score from -1 to 1)
            2. Key reputation themes and trends
            3. Strengths and weaknesses in public perception
            4. ESG (Environmental, Social, Governance) factors mentioned
            5. Risk factors and potential reputation threats
            6. Strategic recommendations for reputation management
            
            Format your response as JSON with the following structure:
            {{
                "overall_sentiment": <score>,
                "sentiment_explanation": "<explanation>",
                "key_themes": ["theme1", "theme2", ...],
                "strengths": ["strength1", "strength2", ...],
                "weaknesses": ["weakness1", "weakness2", ...],
                "esg_factors": {{
                    "environmental": ["factor1", ...],
                    "social": ["factor1", ...],
                    "governance": ["factor1", ...]
                }},
                "risk_factors": ["risk1", "risk2", ...],
                "recommendations": ["rec1", "rec2", ...],
                "confidence_level": "<high/medium/low>"
            }}
            """
            
            response = self.client.generate_content(prompt)
            
            # Parse AI response
            try:
                ai_analysis = json.loads(response.text)
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails
                ai_analysis = {
                    'overall_sentiment': 0,
                    'sentiment_explanation': response.text[:500],
                    'key_themes': [],
                    'strengths': [],
                    'weaknesses': [],
                    'esg_factors': {'environmental': [], 'social': [], 'governance': []},
                    'risk_factors': [],
                    'recommendations': [],
                    'confidence_level': 'low'
                }
            
            # Add metadata
            ai_analysis.update({
                'company_name': company_name,
                'analysis_timestamp': datetime.now().isoformat(),
                'analyzer_version': '1.0.0',
                'data_sources_analyzed': list(reputation_data.get('data_sources', {}).keys())
            })
            
            return ai_analysis
            
        except Exception as e:
            logger.error(f"Error in Gemini reputation analysis: {e}")
            return {
                'error': str(e),
                'company_name': reputation_data.get('company_name', 'Unknown'),
                'analysis_timestamp': datetime.now().isoformat()
            }
    
    def analyze_sentiment_nuances(self, texts: List[str], context: str = '') -> Dict[str, Any]:
        """
        Perform nuanced sentiment analysis on a collection of texts
        
        Args:
            texts: List of texts to analyze
            context: Additional context for analysis
            
        Returns:
            Dictionary containing nuanced sentiment insights
        """
        if not self.client or not texts:
            return {
                'error': 'Gemini client not available or no texts provided',
                'nuanced_sentiment': 0,
                'emotional_tone': 'neutral',
                'key_concerns': [],
                'positive_aspects': []
            }
        
        try:
            # Limit texts for API efficiency
            sample_texts = texts[:20] if len(texts) > 20 else texts
            
            prompt = f"""
            Analyze the sentiment and emotional nuances in the following texts about a company.
            Context: {context}
            
            Texts to analyze:
            {json.dumps(sample_texts[:10], indent=2)}
            
            Provide a nuanced analysis including:
            1. Overall sentiment score (-1 to 1)
            2. Dominant emotional tone
            3. Key concerns or criticisms mentioned
            4. Positive aspects highlighted
            5. Underlying themes and patterns
            6. Credibility assessment of the sources
            
            Format as JSON:
            {{
                "nuanced_sentiment": <score>,
                "emotional_tone": "<tone>",
                "key_concerns": ["concern1", ...],
                "positive_aspects": ["aspect1", ...],
                "underlying_themes": ["theme1", ...],
                "credibility_assessment": "<high/medium/low>",
                "analysis_confidence": "<high/medium/low>"
            }}
            """
            
            response = self.client.generate_content(prompt)
            
            try:
                analysis = json.loads(response.text)
            except json.JSONDecodeError:
                analysis = {
                    'nuanced_sentiment': 0,
                    'emotional_tone': 'neutral',
                    'key_concerns': [],
                    'positive_aspects': [],
                    'underlying_themes': [],
                    'credibility_assessment': 'medium',
                    'analysis_confidence': 'low',
                    'raw_response': response.text[:500]
                }
            
            analysis.update({
                'texts_analyzed': len(sample_texts),
                'total_texts_available': len(texts),
                'analysis_timestamp': datetime.now().isoformat()
            })
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error in nuanced sentiment analysis: {e}")
            return {
                'error': str(e),
                'nuanced_sentiment': 0,
                'emotional_tone': 'neutral'
            }
    
    def generate_esg_assessment(self, reputation_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate ESG (Environmental, Social, Governance) assessment
        
        Args:
            reputation_data: Complete reputation data
            
        Returns:
            Dictionary containing ESG assessment
        """
        if not self.client:
            return {
                'error': 'Gemini client not available',
                'esg_score': 0,
                'environmental_score': 0,
                'social_score': 0,
                'governance_score': 0
            }
        
        try:
            company_name = reputation_data.get('company_name', 'Unknown Company')
            data_summary = self._prepare_data_summary(reputation_data)
            
            prompt = f"""
            Analyze the ESG (Environmental, Social, Governance) factors for {company_name} based on the reputation data.
            
            Data Summary:
            {data_summary}
            
            Provide scores (0-100) and analysis for:
            1. Environmental factors (sustainability, climate impact, green initiatives)
            2. Social factors (employee relations, community impact, diversity)
            3. Governance factors (leadership, transparency, ethics, compliance)
            
            Format as JSON:
            {{
                "overall_esg_score": <0-100>,
                "environmental": {{
                    "score": <0-100>,
                    "factors": ["factor1", ...],
                    "strengths": ["strength1", ...],
                    "concerns": ["concern1", ...]
                }},
                "social": {{
                    "score": <0-100>,
                    "factors": ["factor1", ...],
                    "strengths": ["strength1", ...],
                    "concerns": ["concern1", ...]
                }},
                "governance": {{
                    "score": <0-100>,
                    "factors": ["factor1", ...],
                    "strengths": ["strength1", ...],
                    "concerns": ["concern1", ...]
                }},
                "key_recommendations": ["rec1", "rec2", ...],
                "risk_level": "<low/medium/high>"
            }}
            """
            
            response = self.client.generate_content(prompt)
            
            try:
                esg_analysis = json.loads(response.text)
            except json.JSONDecodeError:
                esg_analysis = {
                    'overall_esg_score': 50,
                    'environmental': {'score': 50, 'factors': [], 'strengths': [], 'concerns': []},
                    'social': {'score': 50, 'factors': [], 'strengths': [], 'concerns': []},
                    'governance': {'score': 50, 'factors': [], 'strengths': [], 'concerns': []},
                    'key_recommendations': [],
                    'risk_level': 'medium',
                    'raw_response': response.text[:500]
                }
            
            esg_analysis.update({
                'company_name': company_name,
                'analysis_timestamp': datetime.now().isoformat(),
                'analyzer_version': '1.0.0'
            })
            
            return esg_analysis
            
        except Exception as e:
            logger.error(f"Error in ESG assessment: {e}")
            return {
                'error': str(e),
                'overall_esg_score': 0,
                'company_name': reputation_data.get('company_name', 'Unknown')
            }
    
    def generate_reputation_alerts(self, reputation_data: Dict[str, Any], 
                                 previous_analysis: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Generate reputation alerts and trend analysis
        
        Args:
            reputation_data: Current reputation data
            previous_analysis: Previous analysis for trend comparison
            
        Returns:
            List of reputation alerts
        """
        alerts = []
        
        if not self.client:
            return [{
                'type': 'system',
                'severity': 'info',
                'message': 'AI-powered alerts unavailable - Gemini client not configured',
                'timestamp': datetime.now().isoformat()
            }]
        
        try:
            company_name = reputation_data.get('company_name', 'Unknown Company')
            
            # Analyze current data for potential issues
            current_summary = self._prepare_data_summary(reputation_data)
            
            prompt = f"""
            Analyze the reputation data for {company_name} and identify any alerts or concerning trends.
            
            Current Data:
            {current_summary}
            
            Identify:
            1. Negative sentiment spikes
            2. Emerging reputation risks
            3. Unusual patterns in mentions
            4. Potential crisis indicators
            5. Positive opportunities
            
            Format each alert as JSON:
            {{
                "type": "<negative_sentiment/risk/crisis/opportunity/trend>",
                "severity": "<low/medium/high/critical>",
                "title": "<alert title>",
                "description": "<detailed description>",
                "recommended_action": "<action to take>",
                "urgency": "<immediate/soon/monitor>"
            }}
            
            Return as a JSON array of alerts.
            """
            
            response = self.client.generate_content(prompt)
            
            try:
                ai_alerts = json.loads(response.text)
                if isinstance(ai_alerts, list):
                    for alert in ai_alerts:
                        alert.update({
                            'company_name': company_name,
                            'timestamp': datetime.now().isoformat(),
                            'source': 'gemini_ai'
                        })
                    alerts.extend(ai_alerts)
            except json.JSONDecodeError:
                # Fallback alert if parsing fails
                alerts.append({
                    'type': 'system',
                    'severity': 'medium',
                    'title': 'AI Analysis Available',
                    'description': response.text[:200],
                    'company_name': company_name,
                    'timestamp': datetime.now().isoformat(),
                    'source': 'gemini_ai'
                })
            
        except Exception as e:
            logger.error(f"Error generating reputation alerts: {e}")
            alerts.append({
                'type': 'error',
                'severity': 'low',
                'title': 'Alert Generation Error',
                'description': f'Error generating AI alerts: {str(e)}',
                'timestamp': datetime.now().isoformat(),
                'source': 'system'
            })
        
        return alerts
    
    def _prepare_data_summary(self, reputation_data: Dict[str, Any]) -> str:
        """
        Prepare a concise summary of reputation data for AI analysis
        
        Args:
            reputation_data: Complete reputation data
            
        Returns:
            String summary of the data
        """
        try:
            summary_parts = []
            
            # News data summary
            news_data = reputation_data.get('data_sources', {}).get('news', {})
            if news_data and news_data.get('total_articles', 0) > 0:
                summary_parts.append(f"News Articles: {news_data['total_articles']} articles collected")
            
            # Social media summary
            social_data = reputation_data.get('data_sources', {}).get('social_media', {})
            if social_data and social_data.get('total_mentions', 0) > 0:
                summary_parts.append(f"Social Media: {social_data['total_mentions']} mentions across platforms")
            
            # Web sources summary
            web_data = reputation_data.get('data_sources', {}).get('web_sources', {})
            if web_data:
                summary_parts.append(f"Web Sources: Multiple reputation sources analyzed")
            
            # Collection summary
            collection_summary = reputation_data.get('summary', {})
            if collection_summary:
                summary_parts.append(f"Data Quality: {collection_summary.get('success_rate', 0):.1%} collection success rate")
            
            return "; ".join(summary_parts) if summary_parts else "Limited reputation data available"
            
        except Exception as e:
            logger.error(f"Error preparing data summary: {e}")
            return "Error preparing data summary for AI analysis"