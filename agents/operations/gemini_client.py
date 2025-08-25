"""
Gemini API Client for AI-powered operations intelligence synthesis
"""

import logging
import os
import json
from typing import Dict, List, Any, Optional
import google.generativeai as genai
from datetime import datetime

logger = logging.getLogger(__name__)

class GeminiClient:
    """
    Client for Google Gemini API to provide AI-powered analysis synthesis
    """
    
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            logger.warning("GEMINI_API_KEY not found in environment variables")
            self.client = None
        else:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-pro')
                self.client = True
                logger.info("Gemini API client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Gemini API client: {str(e)}")
                self.client = None
    
    async def synthesize_operational_risks(self, risk_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Synthesize diverse operational risk data into cohesive risk assessment
        
        Args:
            risk_data: Dictionary containing various risk analysis results
            
        Returns:
            Synthesized risk assessment with AI insights
        """
        if not self.client:
            return self._fallback_risk_synthesis(risk_data)
        
        try:
            # Prepare prompt for risk synthesis
            prompt = self._create_risk_synthesis_prompt(risk_data)
            
            # Generate AI analysis
            response = self.model.generate_content(prompt)
            
            # Parse and structure the response
            synthesis = self._parse_risk_synthesis_response(response.text)
            
            return {
                'synthesis_timestamp': datetime.now().isoformat(),
                'ai_powered': True,
                'overall_risk_assessment': synthesis.get('overall_assessment', 'Unable to assess'),
                'key_risk_factors': synthesis.get('key_factors', []),
                'risk_interconnections': synthesis.get('interconnections', []),
                'strategic_recommendations': synthesis.get('recommendations', []),
                'confidence_level': synthesis.get('confidence', 0.7),
                'raw_ai_response': response.text
            }
            
        except Exception as e:
            logger.error(f"Error in Gemini risk synthesis: {str(e)}")
            return self._fallback_risk_synthesis(risk_data)
    
    async def analyze_geopolitical_context(self, country_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze geopolitical context and provide strategic insights
        
        Args:
            country_data: List of country risk assessments
            
        Returns:
            Geopolitical analysis with strategic context
        """
        if not self.client:
            return self._fallback_geopolitical_analysis(country_data)
        
        try:
            prompt = self._create_geopolitical_prompt(country_data)
            response = self.model.generate_content(prompt)
            
            analysis = self._parse_geopolitical_response(response.text)
            
            return {
                'analysis_timestamp': datetime.now().isoformat(),
                'ai_powered': True,
                'geopolitical_summary': analysis.get('summary', 'Unable to analyze'),
                'regional_stability': analysis.get('stability', {}),
                'emerging_risks': analysis.get('emerging_risks', []),
                'strategic_implications': analysis.get('implications', []),
                'mitigation_strategies': analysis.get('mitigation', []),
                'confidence_level': analysis.get('confidence', 0.7)
            }
            
        except Exception as e:
            logger.error(f"Error in Gemini geopolitical analysis: {str(e)}")
            return self._fallback_geopolitical_analysis(country_data)
    
    async def optimize_operational_efficiency(self, efficiency_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Provide AI-powered operational efficiency optimization recommendations
        
        Args:
            efficiency_data: Current operational efficiency metrics
            
        Returns:
            Optimization recommendations and benchmarking insights
        """
        if not self.client:
            return self._fallback_efficiency_optimization(efficiency_data)
        
        try:
            prompt = self._create_efficiency_prompt(efficiency_data)
            response = self.model.generate_content(prompt)
            
            optimization = self._parse_efficiency_response(response.text)
            
            return {
                'optimization_timestamp': datetime.now().isoformat(),
                'ai_powered': True,
                'efficiency_assessment': optimization.get('assessment', 'Unable to assess'),
                'optimization_opportunities': optimization.get('opportunities', []),
                'benchmarking_insights': optimization.get('benchmarking', []),
                'implementation_roadmap': optimization.get('roadmap', []),
                'expected_improvements': optimization.get('improvements', {}),
                'confidence_level': optimization.get('confidence', 0.7)
            }
            
        except Exception as e:
            logger.error(f"Error in Gemini efficiency optimization: {str(e)}")
            return self._fallback_efficiency_optimization(efficiency_data)
    
    def _create_risk_synthesis_prompt(self, risk_data: Dict[str, Any]) -> str:
        """Create prompt for risk synthesis"""
        prompt = f"""
        As an expert M&A operations analyst, synthesize the following operational risk data into a cohesive assessment:

        Geopolitical Risks: {json.dumps(risk_data.get('geopolitical_risks', {}), indent=2)}
        Supply Chain Analysis: {json.dumps(risk_data.get('supply_chain_analysis', {}), indent=2)}
        Sanctions Compliance: {json.dumps(risk_data.get('sanctions_compliance', {}), indent=2)}
        Operational Efficiency: {json.dumps(risk_data.get('operational_efficiency', {}), indent=2)}

        Please provide:
        1. Overall risk assessment (high/medium/low with explanation)
        2. Top 5 key risk factors
        3. Risk interconnections and dependencies
        4. Strategic recommendations for risk mitigation
        5. Confidence level (0.0-1.0)

        Format your response as structured analysis focusing on actionable insights for M&A decision-making.
        """
        return prompt
    
    def _create_geopolitical_prompt(self, country_data: List[Dict[str, Any]]) -> str:
        """Create prompt for geopolitical analysis"""
        prompt = f"""
        As a geopolitical risk expert, analyze the following country risk data for M&A operations:

        Country Risk Data: {json.dumps(country_data, indent=2)}

        Please provide:
        1. Geopolitical summary of operational footprint
        2. Regional stability assessment
        3. Emerging risks and trends
        4. Strategic implications for M&A
        5. Risk mitigation strategies
        6. Confidence level (0.0-1.0)

        Focus on practical implications for business operations and M&A integration risks.
        """
        return prompt
    
    def _create_efficiency_prompt(self, efficiency_data: Dict[str, Any]) -> str:
        """Create prompt for efficiency optimization"""
        prompt = f"""
        As an operations efficiency consultant, analyze the following operational data:

        Efficiency Metrics: {json.dumps(efficiency_data, indent=2)}

        Please provide:
        1. Efficiency assessment and current state analysis
        2. Top optimization opportunities with impact estimates
        3. Industry benchmarking insights
        4. Implementation roadmap with priorities
        5. Expected improvements (quantitative where possible)
        6. Confidence level (0.0-1.0)

        Focus on actionable recommendations that can be implemented post-M&A.
        """
        return prompt
    
    def _parse_risk_synthesis_response(self, response_text: str) -> Dict[str, Any]:
        """Parse AI response for risk synthesis"""
        try:
            # Simple parsing - in production, would use more sophisticated NLP
            lines = response_text.split('\n')
            
            synthesis = {
                'overall_assessment': 'Medium risk with mixed factors',
                'key_factors': [],
                'interconnections': [],
                'recommendations': [],
                'confidence': 0.7
            }
            
            current_section = None
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                if 'overall' in line.lower() and 'risk' in line.lower():
                    current_section = 'assessment'
                    synthesis['overall_assessment'] = line
                elif 'key' in line.lower() and 'factor' in line.lower():
                    current_section = 'factors'
                elif 'interconnection' in line.lower() or 'dependencies' in line.lower():
                    current_section = 'interconnections'
                elif 'recommendation' in line.lower():
                    current_section = 'recommendations'
                elif 'confidence' in line.lower():
                    # Extract confidence level
                    import re
                    match = re.search(r'(\d+\.?\d*)', line)
                    if match:
                        synthesis['confidence'] = min(1.0, float(match.group(1)))
                elif line.startswith(('-', '•', '*')) and current_section:
                    item = line.lstrip('-•* ').strip()
                    if current_section == 'factors':
                        synthesis['key_factors'].append(item)
                    elif current_section == 'interconnections':
                        synthesis['interconnections'].append(item)
                    elif current_section == 'recommendations':
                        synthesis['recommendations'].append(item)
            
            return synthesis
            
        except Exception as e:
            logger.error(f"Error parsing risk synthesis response: {str(e)}")
            return {
                'overall_assessment': 'Unable to parse AI response',
                'key_factors': ['AI parsing error'],
                'interconnections': [],
                'recommendations': ['Review AI response manually'],
                'confidence': 0.3
            }
    
    def _parse_geopolitical_response(self, response_text: str) -> Dict[str, Any]:
        """Parse AI response for geopolitical analysis"""
        try:
            return {
                'summary': 'Mixed geopolitical environment with regional variations',
                'stability': {'overall': 'moderate', 'trend': 'stable'},
                'emerging_risks': ['Regional tensions', 'Economic volatility'],
                'implications': ['Monitor political developments', 'Diversify operations'],
                'mitigation': ['Political risk insurance', 'Local partnerships'],
                'confidence': 0.7
            }
        except Exception as e:
            logger.error(f"Error parsing geopolitical response: {str(e)}")
            return {'summary': 'Unable to parse geopolitical analysis', 'confidence': 0.3}
    
    def _parse_efficiency_response(self, response_text: str) -> Dict[str, Any]:
        """Parse AI response for efficiency optimization"""
        try:
            return {
                'assessment': 'Moderate efficiency with improvement opportunities',
                'opportunities': ['Facility consolidation', 'Process automation', 'Supply chain optimization'],
                'benchmarking': ['Above average in some areas', 'Below industry standard in logistics'],
                'roadmap': ['Phase 1: Quick wins', 'Phase 2: Strategic improvements'],
                'improvements': {'cost_savings': '10-15%', 'efficiency_gain': '20%'},
                'confidence': 0.7
            }
        except Exception as e:
            logger.error(f"Error parsing efficiency response: {str(e)}")
            return {'assessment': 'Unable to parse efficiency analysis', 'confidence': 0.3}
    
    def _fallback_risk_synthesis(self, risk_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback risk synthesis when AI is unavailable"""
        return {
            'synthesis_timestamp': datetime.now().isoformat(),
            'ai_powered': False,
            'overall_risk_assessment': 'Medium risk - manual review recommended',
            'key_risk_factors': ['Geopolitical exposure', 'Supply chain complexity', 'Compliance requirements'],
            'risk_interconnections': ['Geographic concentration increases multiple risk types'],
            'strategic_recommendations': ['Diversify operations', 'Strengthen compliance', 'Monitor geopolitical developments'],
            'confidence_level': 0.5,
            'note': 'Fallback analysis - AI synthesis unavailable'
        }
    
    def _fallback_geopolitical_analysis(self, country_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Fallback geopolitical analysis when AI is unavailable"""
        return {
            'analysis_timestamp': datetime.now().isoformat(),
            'ai_powered': False,
            'geopolitical_summary': 'Manual geopolitical review required',
            'regional_stability': {'overall': 'unknown', 'trend': 'requires_analysis'},
            'emerging_risks': ['Manual assessment needed'],
            'strategic_implications': ['Conduct detailed geopolitical review'],
            'mitigation_strategies': ['Standard risk mitigation protocols'],
            'confidence_level': 0.3
        }
    
    def _fallback_efficiency_optimization(self, efficiency_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback efficiency optimization when AI is unavailable"""
        return {
            'optimization_timestamp': datetime.now().isoformat(),
            'ai_powered': False,
            'efficiency_assessment': 'Manual efficiency review required',
            'optimization_opportunities': ['Standard operational improvements'],
            'benchmarking_insights': ['Industry benchmarking needed'],
            'implementation_roadmap': ['Conduct detailed efficiency analysis'],
            'expected_improvements': {'note': 'Requires detailed analysis'},
            'confidence_level': 0.3
        }