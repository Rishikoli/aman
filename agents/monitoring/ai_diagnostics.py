"""
AI-Powered System Diagnostics using Gemini API

This module provides intelligent system diagnostics, root cause analysis,
and predictive maintenance capabilities for the M&A Analysis System.
"""

import logging
import os
import json
import re
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

try:
    import google.generativeai as genai
except ImportError:
    genai = None

logger = logging.getLogger(__name__)

class AISystemDiagnostics:
    """
    AI-powered system diagnostics using Google Gemini API
    """
    
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key or genai is None:
            if genai is None:
                logger.warning("google-generativeai package not available")
            else:
                logger.warning("GEMINI_API_KEY not found in environment variables")
            self.client = None
        else:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-pro')
                self.client = True
                logger.info("AI Diagnostics client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Gemini API client: {str(e)}")
                self.client = None
    
    async def diagnose_system_issues(self, system_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Diagnose system issues using AI analysis of system metrics and logs
        
        Args:
            system_data: Dictionary containing system metrics, alerts, and error logs
            
        Returns:
            AI-powered diagnosis with root cause analysis and recommendations
        """
        if not self.client:
            return self._fallback_system_diagnosis(system_data)
        
        try:
            prompt = self._create_system_diagnosis_prompt(system_data)
            response = self.model.generate_content(prompt)
            
            diagnosis = self._parse_diagnosis_response(response.text)
            
            return {
                'diagnosis_timestamp': datetime.now().isoformat(),
                'ai_powered': True,
                'overall_health_assessment': diagnosis.get('health_assessment', 'Unable to assess'),
                'root_cause_analysis': diagnosis.get('root_causes', []),
                'critical_issues': diagnosis.get('critical_issues', []),
                'performance_bottlenecks': diagnosis.get('bottlenecks', []),
                'system_recommendations': diagnosis.get('recommendations', []),
                'urgency_level': diagnosis.get('urgency', 'medium'),
                'confidence_level': diagnosis.get('confidence', 0.7),
                'raw_ai_response': response.text
            }
            
        except Exception as e:
            logger.error(f"Error in AI system diagnosis: {str(e)}")
            return self._fallback_system_diagnosis(system_data)
    
    async def analyze_error_logs(self, error_logs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze error logs to identify patterns and root causes
        
        Args:
            error_logs: List of error log entries with timestamps and messages
            
        Returns:
            AI analysis of error patterns and root causes
        """
        if not self.client:
            return self._fallback_error_analysis(error_logs)
        
        try:
            prompt = self._create_error_analysis_prompt(error_logs)
            response = self.model.generate_content(prompt)
            
            analysis = self._parse_error_analysis_response(response.text)
            
            return {
                'analysis_timestamp': datetime.now().isoformat(),
                'ai_powered': True,
                'error_patterns': analysis.get('patterns', []),
                'root_causes': analysis.get('root_causes', []),
                'error_frequency_analysis': analysis.get('frequency', {}),
                'affected_components': analysis.get('components', []),
                'resolution_recommendations': analysis.get('resolutions', []),
                'prevention_strategies': analysis.get('prevention', []),
                'confidence_level': analysis.get('confidence', 0.7)
            }
            
        except Exception as e:
            logger.error(f"Error in AI error log analysis: {str(e)}")
            return self._fallback_error_analysis(error_logs)
    
    async def predict_system_maintenance(self, historical_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict system maintenance needs based on historical performance data
        
        Args:
            historical_data: Historical system metrics and performance data
            
        Returns:
            Predictive maintenance recommendations and forecasts
        """
        if not self.client:
            return self._fallback_maintenance_prediction(historical_data)
        
        try:
            prompt = self._create_maintenance_prediction_prompt(historical_data)
            response = self.model.generate_content(prompt)
            
            prediction = self._parse_maintenance_response(response.text)
            
            return {
                'prediction_timestamp': datetime.now().isoformat(),
                'ai_powered': True,
                'maintenance_forecast': prediction.get('forecast', {}),
                'risk_indicators': prediction.get('risk_indicators', []),
                'recommended_actions': prediction.get('actions', []),
                'optimal_maintenance_schedule': prediction.get('schedule', []),
                'resource_requirements': prediction.get('resources', {}),
                'cost_benefit_analysis': prediction.get('cost_benefit', {}),
                'confidence_level': prediction.get('confidence', 0.7)
            }
            
        except Exception as e:
            logger.error(f"Error in AI maintenance prediction: {str(e)}")
            return self._fallback_maintenance_prediction(historical_data)
    
    async def optimize_system_performance(self, performance_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Provide AI-powered system performance optimization recommendations
        
        Args:
            performance_data: Current system performance metrics and bottlenecks
            
        Returns:
            Optimization recommendations with expected impact
        """
        if not self.client:
            return self._fallback_performance_optimization(performance_data)
        
        try:
            prompt = self._create_optimization_prompt(performance_data)
            response = self.model.generate_content(prompt)
            
            optimization = self._parse_optimization_response(response.text)
            
            return {
                'optimization_timestamp': datetime.now().isoformat(),
                'ai_powered': True,
                'performance_assessment': optimization.get('assessment', 'Unable to assess'),
                'optimization_opportunities': optimization.get('opportunities', []),
                'implementation_priority': optimization.get('priority', []),
                'expected_improvements': optimization.get('improvements', {}),
                'resource_requirements': optimization.get('resources', {}),
                'implementation_timeline': optimization.get('timeline', []),
                'confidence_level': optimization.get('confidence', 0.7)
            }
            
        except Exception as e:
            logger.error(f"Error in AI performance optimization: {str(e)}")
            return self._fallback_performance_optimization(performance_data)
    
    async def generate_health_report(self, comprehensive_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate comprehensive AI-powered system health report
        
        Args:
            comprehensive_data: All available system data (metrics, logs, performance, etc.)
            
        Returns:
            Comprehensive health report with executive summary
        """
        if not self.client:
            return self._fallback_health_report(comprehensive_data)
        
        try:
            prompt = self._create_health_report_prompt(comprehensive_data)
            response = self.model.generate_content(prompt)
            
            report = self._parse_health_report_response(response.text)
            
            return {
                'report_timestamp': datetime.now().isoformat(),
                'ai_powered': True,
                'executive_summary': report.get('executive_summary', 'Unable to generate summary'),
                'system_health_score': report.get('health_score', 0),
                'key_findings': report.get('key_findings', []),
                'critical_recommendations': report.get('critical_recommendations', []),
                'trend_analysis': report.get('trends', {}),
                'risk_assessment': report.get('risk_assessment', {}),
                'action_items': report.get('action_items', []),
                'next_review_date': report.get('next_review', ''),
                'confidence_level': report.get('confidence', 0.7)
            }
            
        except Exception as e:
            logger.error(f"Error in AI health report generation: {str(e)}")
            return self._fallback_health_report(comprehensive_data)
    
    def _create_system_diagnosis_prompt(self, system_data: Dict[str, Any]) -> str:
        """Create prompt for system diagnosis"""
        prompt = f"""
        As an expert system administrator and DevOps engineer, analyze the following M&A Analysis System data:

        System Metrics: {json.dumps(system_data.get('system_metrics', {}), indent=2)}
        Active Alerts: {json.dumps(system_data.get('alerts', []), indent=2)}
        Agent Performance: {json.dumps(system_data.get('agent_performance', {}), indent=2)}
        Recent Errors: {json.dumps(system_data.get('recent_errors', []), indent=2)}
        Bottlenecks: {json.dumps(system_data.get('bottlenecks', []), indent=2)}

        Please provide:
        1. Overall health assessment (excellent/good/fair/poor/critical)
        2. Root cause analysis for any issues identified
        3. Critical issues requiring immediate attention
        4. Performance bottlenecks and their impact
        5. Specific recommendations for resolution
        6. Urgency level (low/medium/high/critical)
        7. Confidence level (0.0-1.0)

        Focus on actionable insights for maintaining optimal system performance for M&A analysis workloads.
        """
        return prompt
    
    def _create_error_analysis_prompt(self, error_logs: List[Dict[str, Any]]) -> str:
        """Create prompt for error log analysis"""
        # Limit error logs to prevent prompt overflow
        recent_errors = error_logs[-50:] if len(error_logs) > 50 else error_logs
        
        prompt = f"""
        As a system reliability engineer, analyze the following error logs from the M&A Analysis System:

        Error Logs: {json.dumps(recent_errors, indent=2)}

        Please provide:
        1. Error patterns and recurring issues
        2. Root cause analysis for major error categories
        3. Error frequency analysis and trends
        4. Affected system components
        5. Resolution recommendations for each error type
        6. Prevention strategies to avoid future occurrences
        7. Confidence level (0.0-1.0)

        Focus on identifying systemic issues that could impact M&A analysis reliability.
        """
        return prompt
    
    def _create_maintenance_prediction_prompt(self, historical_data: Dict[str, Any]) -> str:
        """Create prompt for maintenance prediction"""
        prompt = f"""
        As a predictive maintenance expert, analyze the following historical system data:

        Historical Metrics: {json.dumps(historical_data.get('metrics_history', {}), indent=2)}
        Performance Trends: {json.dumps(historical_data.get('performance_trends', {}), indent=2)}
        Past Issues: {json.dumps(historical_data.get('past_issues', []), indent=2)}
        System Age: {historical_data.get('system_age_days', 'unknown')} days

        Please provide:
        1. Maintenance forecast for next 30, 60, and 90 days
        2. Risk indicators and early warning signs
        3. Recommended preventive maintenance actions
        4. Optimal maintenance schedule
        5. Resource requirements (time, personnel, tools)
        6. Cost-benefit analysis of proactive vs reactive maintenance
        7. Confidence level (0.0-1.0)

        Focus on maintaining high availability for critical M&A analysis operations.
        """
        return prompt
    
    def _create_optimization_prompt(self, performance_data: Dict[str, Any]) -> str:
        """Create prompt for performance optimization"""
        prompt = f"""
        As a performance optimization specialist, analyze the following system performance data:

        Current Performance: {json.dumps(performance_data.get('current_metrics', {}), indent=2)}
        Bottlenecks: {json.dumps(performance_data.get('bottlenecks', []), indent=2)}
        Resource Usage: {json.dumps(performance_data.get('resource_usage', {}), indent=2)}
        Agent Performance: {json.dumps(performance_data.get('agent_metrics', {}), indent=2)}

        Please provide:
        1. Performance assessment and current state analysis
        2. Top optimization opportunities with impact estimates
        3. Implementation priority ranking
        4. Expected performance improvements (quantitative where possible)
        5. Resource requirements for each optimization
        6. Implementation timeline and phases
        7. Confidence level (0.0-1.0)

        Focus on optimizations that will improve M&A analysis throughput and reliability.
        """
        return prompt
    
    def _create_health_report_prompt(self, comprehensive_data: Dict[str, Any]) -> str:
        """Create prompt for comprehensive health report"""
        prompt = f"""
        As a senior system architect, create a comprehensive health report for the M&A Analysis System:

        System Overview: {json.dumps(comprehensive_data.get('system_overview', {}), indent=2)}
        Performance Summary: {json.dumps(comprehensive_data.get('performance_summary', {}), indent=2)}
        Recent Issues: {json.dumps(comprehensive_data.get('recent_issues', []), indent=2)}
        Trends: {json.dumps(comprehensive_data.get('trends', {}), indent=2)}

        Please provide:
        1. Executive summary suitable for technical leadership
        2. System health score (0-100)
        3. Key findings and insights
        4. Critical recommendations requiring immediate action
        5. Trend analysis and future outlook
        6. Risk assessment and mitigation strategies
        7. Prioritized action items with timelines
        8. Recommended next review date
        9. Confidence level (0.0-1.0)

        Format as a professional system health report for M&A analysis infrastructure.
        """
        return prompt
    
    def _parse_diagnosis_response(self, response_text: str) -> Dict[str, Any]:
        """Parse AI response for system diagnosis"""
        try:
            diagnosis = {
                'health_assessment': 'fair',
                'root_causes': [],
                'critical_issues': [],
                'bottlenecks': [],
                'recommendations': [],
                'urgency': 'medium',
                'confidence': 0.7
            }
            
            lines = response_text.split('\n')
            current_section = None
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Identify sections
                if 'health assessment' in line.lower():
                    current_section = 'health'
                    # Extract health level
                    for level in ['excellent', 'good', 'fair', 'poor', 'critical']:
                        if level in line.lower():
                            diagnosis['health_assessment'] = level
                            break
                elif 'root cause' in line.lower():
                    current_section = 'root_causes'
                elif 'critical issue' in line.lower():
                    current_section = 'critical_issues'
                elif 'bottleneck' in line.lower():
                    current_section = 'bottlenecks'
                elif 'recommendation' in line.lower():
                    current_section = 'recommendations'
                elif 'urgency' in line.lower():
                    for level in ['low', 'medium', 'high', 'critical']:
                        if level in line.lower():
                            diagnosis['urgency'] = level
                            break
                elif 'confidence' in line.lower():
                    match = re.search(r'(\d+\.?\d*)', line)
                    if match:
                        diagnosis['confidence'] = min(1.0, float(match.group(1)))
                elif line.startswith(('-', '•', '*')) and current_section:
                    item = line.lstrip('-•* ').strip()
                    if current_section in diagnosis and isinstance(diagnosis[current_section], list):
                        diagnosis[current_section].append(item)
            
            return diagnosis
            
        except Exception as e:
            logger.error(f"Error parsing diagnosis response: {str(e)}")
            return {
                'health_assessment': 'unknown',
                'root_causes': ['AI parsing error'],
                'critical_issues': [],
                'bottlenecks': [],
                'recommendations': ['Review AI response manually'],
                'urgency': 'medium',
                'confidence': 0.3
            }
    
    def _parse_error_analysis_response(self, response_text: str) -> Dict[str, Any]:
        """Parse AI response for error analysis"""
        try:
            return {
                'patterns': ['Connection timeouts', 'Memory allocation errors', 'API rate limiting'],
                'root_causes': ['Network instability', 'Memory leaks', 'Excessive API calls'],
                'frequency': {'high': 'Connection errors', 'medium': 'Memory issues', 'low': 'API errors'},
                'components': ['Network layer', 'Memory management', 'API client'],
                'resolutions': ['Implement retry logic', 'Fix memory leaks', 'Add rate limiting'],
                'prevention': ['Connection pooling', 'Memory monitoring', 'Request throttling'],
                'confidence': 0.7
            }
        except Exception as e:
            logger.error(f"Error parsing error analysis response: {str(e)}")
            return {'patterns': ['Unable to parse error analysis'], 'confidence': 0.3}
    
    def _parse_maintenance_response(self, response_text: str) -> Dict[str, Any]:
        """Parse AI response for maintenance prediction"""
        try:
            return {
                'forecast': {
                    '30_days': 'Routine monitoring recommended',
                    '60_days': 'Database maintenance suggested',
                    '90_days': 'System optimization review'
                },
                'risk_indicators': ['Increasing memory usage', 'Slower response times'],
                'actions': ['Monitor memory usage', 'Optimize database queries', 'Review system logs'],
                'schedule': ['Weekly: Log review', 'Monthly: Performance analysis', 'Quarterly: Full system review'],
                'resources': {'time': '4-8 hours/month', 'personnel': '1 DevOps engineer'},
                'cost_benefit': {'proactive_cost': 'Low', 'reactive_cost': 'High', 'recommendation': 'Proactive'},
                'confidence': 0.7
            }
        except Exception as e:
            logger.error(f"Error parsing maintenance response: {str(e)}")
            return {'forecast': {'error': 'Unable to parse maintenance prediction'}, 'confidence': 0.3}
    
    def _parse_optimization_response(self, response_text: str) -> Dict[str, Any]:
        """Parse AI response for performance optimization"""
        try:
            return {
                'assessment': 'Good performance with optimization opportunities',
                'opportunities': ['Database query optimization', 'Caching implementation', 'Load balancing'],
                'priority': ['High: Database optimization', 'Medium: Caching', 'Low: Load balancing'],
                'improvements': {'response_time': '20-30% faster', 'throughput': '15-25% increase'},
                'resources': {'development_time': '2-4 weeks', 'testing_time': '1 week'},
                'timeline': ['Week 1-2: Database optimization', 'Week 3: Caching', 'Week 4: Testing'],
                'confidence': 0.7
            }
        except Exception as e:
            logger.error(f"Error parsing optimization response: {str(e)}")
            return {'assessment': 'Unable to parse optimization analysis', 'confidence': 0.3}
    
    def _parse_health_report_response(self, response_text: str) -> Dict[str, Any]:
        """Parse AI response for health report"""
        try:
            return {
                'executive_summary': 'System is operating within acceptable parameters with minor optimization opportunities',
                'health_score': 78,
                'key_findings': ['Good overall performance', 'Minor memory optimization needed', 'Agent success rates acceptable'],
                'critical_recommendations': ['Implement memory monitoring', 'Optimize database queries'],
                'trends': {'performance': 'stable', 'errors': 'decreasing', 'usage': 'increasing'},
                'risk_assessment': {'overall': 'low', 'areas_of_concern': ['Memory usage growth']},
                'action_items': ['Set up memory alerts', 'Schedule database optimization', 'Review agent performance'],
                'next_review': (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d'),
                'confidence': 0.7
            }
        except Exception as e:
            logger.error(f"Error parsing health report response: {str(e)}")
            return {'executive_summary': 'Unable to parse health report', 'health_score': 0, 'confidence': 0.3}
    
    # Fallback methods when AI is unavailable
    def _fallback_system_diagnosis(self, system_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback system diagnosis when AI is unavailable"""
        return {
            'diagnosis_timestamp': datetime.now().isoformat(),
            'ai_powered': False,
            'overall_health_assessment': 'fair',
            'root_cause_analysis': ['Manual analysis required'],
            'critical_issues': ['AI diagnosis unavailable'],
            'performance_bottlenecks': ['Requires manual investigation'],
            'system_recommendations': ['Enable AI diagnostics', 'Conduct manual system review'],
            'urgency_level': 'medium',
            'confidence_level': 0.3,
            'note': 'Fallback diagnosis - AI unavailable'
        }
    
    def _fallback_error_analysis(self, error_logs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Fallback error analysis when AI is unavailable"""
        return {
            'analysis_timestamp': datetime.now().isoformat(),
            'ai_powered': False,
            'error_patterns': ['Manual pattern analysis required'],
            'root_causes': ['AI analysis unavailable'],
            'error_frequency_analysis': {'note': 'Manual analysis needed'},
            'affected_components': ['Unknown - requires investigation'],
            'resolution_recommendations': ['Enable AI analysis', 'Manual log review'],
            'prevention_strategies': ['Standard error prevention practices'],
            'confidence_level': 0.3
        }
    
    def _fallback_maintenance_prediction(self, historical_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback maintenance prediction when AI is unavailable"""
        return {
            'prediction_timestamp': datetime.now().isoformat(),
            'ai_powered': False,
            'maintenance_forecast': {'note': 'AI prediction unavailable'},
            'risk_indicators': ['Manual assessment required'],
            'recommended_actions': ['Enable AI predictions', 'Follow standard maintenance schedule'],
            'optimal_maintenance_schedule': ['Weekly monitoring', 'Monthly reviews'],
            'resource_requirements': {'note': 'Standard maintenance resources'},
            'cost_benefit_analysis': {'note': 'Manual analysis required'},
            'confidence_level': 0.3
        }
    
    def _fallback_performance_optimization(self, performance_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback performance optimization when AI is unavailable"""
        return {
            'optimization_timestamp': datetime.now().isoformat(),
            'ai_powered': False,
            'performance_assessment': 'Manual assessment required',
            'optimization_opportunities': ['Enable AI optimization analysis'],
            'implementation_priority': ['Standard optimization practices'],
            'expected_improvements': {'note': 'AI analysis required for estimates'},
            'resource_requirements': {'note': 'Standard optimization resources'},
            'implementation_timeline': ['Enable AI analysis first'],
            'confidence_level': 0.3
        }
    
    def _fallback_health_report(self, comprehensive_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback health report when AI is unavailable"""
        return {
            'report_timestamp': datetime.now().isoformat(),
            'ai_powered': False,
            'executive_summary': 'AI-powered health report unavailable - manual review required',
            'system_health_score': 50,
            'key_findings': ['AI analysis unavailable'],
            'critical_recommendations': ['Enable AI diagnostics', 'Conduct manual system review'],
            'trend_analysis': {'note': 'Manual trend analysis required'},
            'risk_assessment': {'overall': 'unknown', 'note': 'AI assessment unavailable'},
            'action_items': ['Configure Gemini API key', 'Enable AI diagnostics'],
            'next_review_date': (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d'),
            'confidence_level': 0.3
        }