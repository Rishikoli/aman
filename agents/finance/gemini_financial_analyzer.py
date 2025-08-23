"""
Gemini API Integration for Financial Narrative Analysis
Provides AI-powered analysis of MD&A sections and complex financial narratives.
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any
import requests
from datetime import datetime

# Load environment variables from backend
try:
    from .env_loader import load_backend_env
    load_backend_env()
except ImportError:
    pass  # Fallback if env_loader is not available

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiFinancialAnalyzer:
    """
    Gemini API client for financial narrative analysis
    """
    
    def __init__(self):
        """Initialize the Gemini financial analyzer"""
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            logger.warning("GEMINI_API_KEY not found in environment variables")
        
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        self.headers = {
            'Content-Type': 'application/json'
        }
        
        # Financial analysis prompts
        self.prompts = {
            'mda_summary': """
            Analyze the following Management Discussion & Analysis (MD&A) section and provide:
            1. Key business highlights and challenges
            2. Management's outlook and strategy
            3. Risk factors mentioned
            4. Financial performance insights
            5. Forward-looking statements and guidance
            
            Please structure your response as a JSON object with these sections:
            - "key_highlights": list of main business highlights
            - "challenges": list of key challenges identified
            - "management_outlook": summary of management's perspective
            - "risk_factors": list of risk factors mentioned
            - "financial_insights": key financial performance insights
            - "forward_guidance": any forward-looking statements or guidance
            - "overall_sentiment": "positive", "neutral", or "negative"
            
            MD&A Text:
            {text}
            """,
            
            'financial_narrative': """
            Analyze the following financial narrative and provide insights on:
            1. Financial performance trends
            2. Business strategy implications
            3. Competitive positioning
            4. Operational efficiency indicators
            5. Capital allocation decisions
            
            Structure your response as JSON:
            - "performance_trends": analysis of financial trends
            - "strategy_implications": business strategy insights
            - "competitive_position": competitive analysis
            - "operational_efficiency": efficiency indicators
            - "capital_allocation": capital allocation insights
            - "key_concerns": any red flags or concerns
            - "confidence_level": "high", "medium", or "low"
            
            Financial Narrative:
            {text}
            """,
            
            'anomaly_explanation': """
            Based on the following financial anomaly data, provide a detailed explanation of:
            1. Possible business reasons for the anomaly
            2. Industry context that might explain the deviation
            3. Potential impact on future performance
            4. Recommended areas for further investigation
            
            Structure as JSON:
            - "business_reasons": likely business explanations
            - "industry_context": relevant industry factors
            - "future_impact": potential impact on future performance
            - "investigation_areas": areas requiring further analysis
            - "severity_assessment": "low", "medium", "high", or "critical"
            
            Anomaly Data:
            {anomaly_data}
            """,
            
            'forecast_validation': """
            Review the following financial forecasts and provide:
            1. Reasonableness assessment of the projections
            2. Key assumptions that should be validated
            3. Potential risks to the forecast
            4. Alternative scenarios to consider
            
            Structure as JSON:
            - "reasonableness": assessment of forecast reasonableness
            - "key_assumptions": critical assumptions to validate
            - "forecast_risks": risks that could impact projections
            - "alternative_scenarios": other scenarios to consider
            - "confidence_rating": 1-10 scale confidence in forecasts
            
            Forecast Data:
            {forecast_data}
            """
        }
    
    def analyze_mda_section(self, mda_text: str) -> Dict[str, Any]:
        """
        Analyze Management Discussion & Analysis section
        
        Args:
            mda_text: MD&A text content
            
        Returns:
            Dictionary containing structured analysis
        """
        try:
            logger.info("Analyzing MD&A section with Gemini...")
            
            if not self.api_key:
                return self._create_fallback_mda_analysis(mda_text)
            
            prompt = self.prompts['mda_summary'].format(text=mda_text[:8000])  # Limit text length
            
            response = self._make_gemini_request(prompt)
            
            if response and 'candidates' in response:
                content = response['candidates'][0]['content']['parts'][0]['text']
                
                # Try to parse JSON response
                try:
                    analysis = json.loads(content)
                    analysis['metadata'] = {
                        'analysis_date': datetime.now().isoformat(),
                        'text_length': len(mda_text),
                        'ai_model': 'gemini-pro'
                    }
                    return analysis
                except json.JSONDecodeError:
                    # If JSON parsing fails, return structured fallback
                    return {
                        'raw_analysis': content,
                        'parsing_error': 'Could not parse JSON response',
                        'metadata': {
                            'analysis_date': datetime.now().isoformat(),
                            'text_length': len(mda_text),
                            'ai_model': 'gemini-pro'
                        }
                    }
            else:
                return self._create_fallback_mda_analysis(mda_text)
                
        except Exception as e:
            logger.error(f"Error analyzing MD&A section: {str(e)}")
            return self._create_fallback_mda_analysis(mda_text, error=str(e))
    
    def analyze_financial_narrative(self, narrative_text: str, financial_context: Dict = None) -> Dict[str, Any]:
        """
        Analyze complex financial narratives
        
        Args:
            narrative_text: Financial narrative text
            financial_context: Additional financial context data
            
        Returns:
            Dictionary containing narrative analysis
        """
        try:
            logger.info("Analyzing financial narrative with Gemini...")
            
            if not self.api_key:
                return self._create_fallback_narrative_analysis(narrative_text)
            
            # Enhance prompt with financial context if available
            enhanced_text = narrative_text
            if financial_context:
                context_summary = f"Financial Context: {json.dumps(financial_context, indent=2)}\n\n"
                enhanced_text = context_summary + narrative_text
            
            prompt = self.prompts['financial_narrative'].format(text=enhanced_text[:8000])
            
            response = self._make_gemini_request(prompt)
            
            if response and 'candidates' in response:
                content = response['candidates'][0]['content']['parts'][0]['text']
                
                try:
                    analysis = json.loads(content)
                    analysis['metadata'] = {
                        'analysis_date': datetime.now().isoformat(),
                        'text_length': len(narrative_text),
                        'has_financial_context': financial_context is not None,
                        'ai_model': 'gemini-pro'
                    }
                    return analysis
                except json.JSONDecodeError:
                    return {
                        'raw_analysis': content,
                        'parsing_error': 'Could not parse JSON response',
                        'metadata': {
                            'analysis_date': datetime.now().isoformat(),
                            'text_length': len(narrative_text),
                            'ai_model': 'gemini-pro'
                        }
                    }
            else:
                return self._create_fallback_narrative_analysis(narrative_text)
                
        except Exception as e:
            logger.error(f"Error analyzing financial narrative: {str(e)}")
            return self._create_fallback_narrative_analysis(narrative_text, error=str(e))
    
    def explain_financial_anomaly(self, anomaly_data: Dict) -> Dict[str, Any]:
        """
        Provide AI-powered explanation of financial anomalies
        
        Args:
            anomaly_data: Anomaly detection results
            
        Returns:
            Dictionary containing anomaly explanation
        """
        try:
            logger.info("Explaining financial anomaly with Gemini...")
            
            if not self.api_key:
                return self._create_fallback_anomaly_explanation(anomaly_data)
            
            # Format anomaly data for analysis
            anomaly_summary = json.dumps(anomaly_data, indent=2)
            prompt = self.prompts['anomaly_explanation'].format(anomaly_data=anomaly_summary)
            
            response = self._make_gemini_request(prompt)
            
            if response and 'candidates' in response:
                content = response['candidates'][0]['content']['parts'][0]['text']
                
                try:
                    explanation = json.loads(content)
                    explanation['metadata'] = {
                        'analysis_date': datetime.now().isoformat(),
                        'anomaly_count': len(anomaly_data.get('anomalies', [])),
                        'ai_model': 'gemini-pro'
                    }
                    return explanation
                except json.JSONDecodeError:
                    return {
                        'raw_explanation': content,
                        'parsing_error': 'Could not parse JSON response',
                        'metadata': {
                            'analysis_date': datetime.now().isoformat(),
                            'ai_model': 'gemini-pro'
                        }
                    }
            else:
                return self._create_fallback_anomaly_explanation(anomaly_data)
                
        except Exception as e:
            logger.error(f"Error explaining financial anomaly: {str(e)}")
            return self._create_fallback_anomaly_explanation(anomaly_data, error=str(e))
    
    def validate_financial_forecasts(self, forecast_data: Dict) -> Dict[str, Any]:
        """
        Validate and provide insights on financial forecasts
        
        Args:
            forecast_data: Financial forecast results
            
        Returns:
            Dictionary containing forecast validation
        """
        try:
            logger.info("Validating financial forecasts with Gemini...")
            
            if not self.api_key:
                return self._create_fallback_forecast_validation(forecast_data)
            
            # Format forecast data for analysis
            forecast_summary = json.dumps(forecast_data, indent=2)
            prompt = self.prompts['forecast_validation'].format(forecast_data=forecast_summary)
            
            response = self._make_gemini_request(prompt)
            
            if response and 'candidates' in response:
                content = response['candidates'][0]['content']['parts'][0]['text']
                
                try:
                    validation = json.loads(content)
                    validation['metadata'] = {
                        'analysis_date': datetime.now().isoformat(),
                        'forecasted_metrics': len(forecast_data.get('forecasts', {})),
                        'ai_model': 'gemini-pro'
                    }
                    return validation
                except json.JSONDecodeError:
                    return {
                        'raw_validation': content,
                        'parsing_error': 'Could not parse JSON response',
                        'metadata': {
                            'analysis_date': datetime.now().isoformat(),
                            'ai_model': 'gemini-pro'
                        }
                    }
            else:
                return self._create_fallback_forecast_validation(forecast_data)
                
        except Exception as e:
            logger.error(f"Error validating financial forecasts: {str(e)}")
            return self._create_fallback_forecast_validation(forecast_data, error=str(e))
    
    def _make_gemini_request(self, prompt: str) -> Optional[Dict]:
        """
        Make request to Gemini API
        
        Args:
            prompt: The prompt to send to Gemini
            
        Returns:
            API response or None if failed
        """
        try:
            payload = {
                "contents": [{
                    "parts": [{
                        "text": prompt
                    }]
                }],
                "generationConfig": {
                    "temperature": 0.3,
                    "topK": 40,
                    "topP": 0.95,
                    "maxOutputTokens": 2048,
                }
            }
            
            url = f"{self.base_url}?key={self.api_key}"
            
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Gemini API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error making Gemini request: {str(e)}")
            return None
    
    def _create_fallback_mda_analysis(self, mda_text: str, error: str = None) -> Dict[str, Any]:
        """Create fallback MD&A analysis when Gemini is unavailable"""
        return {
            'key_highlights': ['AI analysis unavailable - manual review required'],
            'challenges': ['Unable to identify challenges automatically'],
            'management_outlook': 'AI analysis unavailable',
            'risk_factors': ['Manual risk assessment required'],
            'financial_insights': ['Detailed financial analysis needed'],
            'forward_guidance': 'No AI-generated guidance available',
            'overall_sentiment': 'neutral',
            'fallback_mode': True,
            'error': error,
            'metadata': {
                'analysis_date': datetime.now().isoformat(),
                'text_length': len(mda_text),
                'ai_model': 'fallback'
            }
        }
    
    def _create_fallback_narrative_analysis(self, narrative_text: str, error: str = None) -> Dict[str, Any]:
        """Create fallback narrative analysis when Gemini is unavailable"""
        return {
            'performance_trends': 'AI analysis unavailable - manual review required',
            'strategy_implications': 'Manual strategy analysis needed',
            'competitive_position': 'Competitive analysis unavailable',
            'operational_efficiency': 'Efficiency analysis required',
            'capital_allocation': 'Manual capital allocation review needed',
            'key_concerns': ['AI analysis unavailable'],
            'confidence_level': 'low',
            'fallback_mode': True,
            'error': error,
            'metadata': {
                'analysis_date': datetime.now().isoformat(),
                'text_length': len(narrative_text),
                'ai_model': 'fallback'
            }
        }
    
    def _create_fallback_anomaly_explanation(self, anomaly_data: Dict, error: str = None) -> Dict[str, Any]:
        """Create fallback anomaly explanation when Gemini is unavailable"""
        return {
            'business_reasons': ['AI explanation unavailable - manual analysis required'],
            'industry_context': 'Industry analysis unavailable',
            'future_impact': 'Impact assessment requires manual review',
            'investigation_areas': ['All anomalies require manual investigation'],
            'severity_assessment': 'medium',
            'fallback_mode': True,
            'error': error,
            'metadata': {
                'analysis_date': datetime.now().isoformat(),
                'anomaly_count': len(anomaly_data.get('anomalies', [])),
                'ai_model': 'fallback'
            }
        }
    
    def _create_fallback_forecast_validation(self, forecast_data: Dict, error: str = None) -> Dict[str, Any]:
        """Create fallback forecast validation when Gemini is unavailable"""
        return {
            'reasonableness': 'AI validation unavailable - manual review required',
            'key_assumptions': ['All assumptions require manual validation'],
            'forecast_risks': ['Risk assessment unavailable'],
            'alternative_scenarios': ['Scenario analysis required'],
            'confidence_rating': 5,
            'fallback_mode': True,
            'error': error,
            'metadata': {
                'analysis_date': datetime.now().isoformat(),
                'forecasted_metrics': len(forecast_data.get('forecasts', {})),
                'ai_model': 'fallback'
            }
        }
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Test Gemini API connection
        
        Returns:
            Dictionary containing connection test results
        """
        try:
            if not self.api_key:
                return {
                    'success': False,
                    'message': 'Gemini API key not configured',
                    'fallback_available': True
                }
            
            # Simple test prompt
            test_prompt = "Respond with 'Connection successful' if you can read this message."
            response = self._make_gemini_request(test_prompt)
            
            if response and 'candidates' in response:
                return {
                    'success': True,
                    'message': 'Gemini API connection successful',
                    'model': 'gemini-pro'
                }
            else:
                return {
                    'success': False,
                    'message': 'Gemini API connection failed',
                    'fallback_available': True
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Gemini API test failed: {str(e)}',
                'fallback_available': True
            }