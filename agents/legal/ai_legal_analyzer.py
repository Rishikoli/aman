"""
AI-Powered Legal Analysis Engine
Combines spaCy NLP pipeline with Gemini API for advanced legal reasoning
"""

import logging
import re
import json
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import os
import sys
from pathlib import Path

# Add utils directory to path
sys.path.append(str(Path(__file__).parent.parent / 'utils'))

from .legal_nlp_pipeline import LegalNLPPipeline

logger = logging.getLogger(__name__)

class AILegalAnalyzer:
    """
    AI-powered legal analysis engine combining NLP and LLM capabilities
    """
    
    def __init__(self, gemini_api_key: Optional[str] = None):
        """
        Initialize AI legal analyzer
        
        Args:
            gemini_api_key: Optional Gemini API key
        """
        self.gemini_api_key = gemini_api_key or os.getenv('GEMINI_API_KEY')
        self.nlp_pipeline = LegalNLPPipeline()
        
        # Initialize NLP pipeline
        self.nlp_initialized = self.nlp_pipeline.initialize()
        
        # Gemini client (will be initialized when needed)
        self.gemini_client = None
        
        # Legal risk categories and scoring
        self.risk_categories = {
            'litigation': {
                'weight': 0.3,
                'keywords': ['lawsuit', 'litigation', 'court', 'plaintiff', 'defendant', 'settlement']
            },
            'regulatory': {
                'weight': 0.25,
                'keywords': ['violation', 'compliance', 'regulatory', 'investigation', 'enforcement']
            },
            'contractual': {
                'weight': 0.2,
                'keywords': ['breach', 'default', 'termination', 'penalty', 'damages']
            },
            'intellectual_property': {
                'weight': 0.15,
                'keywords': ['patent', 'trademark', 'copyright', 'infringement', 'licensing']
            },
            'corporate_governance': {
                'weight': 0.1,
                'keywords': ['governance', 'board', 'director', 'shareholder', 'fiduciary']
            }
        }
        
        logger.info("AI Legal Analyzer initialized")
    
    def _init_gemini_client(self):
        """Initialize Gemini API client if available"""
        if self.gemini_client is None and self.gemini_api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.gemini_api_key)
                self.gemini_client = genai.GenerativeModel('gemini-pro')
                logger.info("Gemini API client initialized")
            except ImportError:
                logger.warning("Google Generative AI library not available")
            except Exception as e:
                logger.error(f"Failed to initialize Gemini client: {e}")
    
    def analyze_legal_document_comprehensive(self, text: str, 
                                           document_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Comprehensive AI-powered legal document analysis
        
        Args:
            text: Legal document text
            document_type: Optional document type hint
            
        Returns:
            Comprehensive analysis results
        """
        try:
            logger.info("Starting comprehensive legal document analysis")
            
            # 1. Basic NLP analysis
            nlp_analysis = self.nlp_pipeline.analyze_legal_document(text)
            
            # 2. Advanced risk scoring
            risk_analysis = self._advanced_risk_scoring(text, nlp_analysis)
            
            # 3. Legal clause extraction and analysis
            clause_analysis = self._analyze_legal_clauses_advanced(text)
            
            # 4. Compliance gap detection
            compliance_analysis = self._detect_compliance_gaps(text, nlp_analysis)
            
            # 5. AI-powered insights (if Gemini available)
            ai_insights = self._generate_ai_insights(text, document_type)
            
            # 6. Litigation risk assessment
            litigation_risk = self._assess_litigation_risk(text, nlp_analysis)
            
            # 7. Generate recommendations
            recommendations = self._generate_legal_recommendations(
                nlp_analysis, risk_analysis, compliance_analysis, litigation_risk
            )
            
            return {
                'document_analysis': {
                    'document_type': document_type or nlp_analysis.get('document_classification', {}).get('predicted_type', 'unknown'),
                    'text_statistics': nlp_analysis.get('text_statistics', {}),
                    'analysis_timestamp': datetime.now().isoformat()
                },
                'nlp_analysis': nlp_analysis,
                'risk_analysis': risk_analysis,
                'clause_analysis': clause_analysis,
                'compliance_analysis': compliance_analysis,
                'litigation_risk': litigation_risk,
                'ai_insights': ai_insights,
                'recommendations': recommendations,
                'overall_risk_score': self._calculate_overall_legal_risk_score(
                    risk_analysis, compliance_analysis, litigation_risk
                )
            }
            
        except Exception as e:
            logger.error(f"Error in comprehensive legal analysis: {e}")
            return {
                'error': str(e),
                'analysis_timestamp': datetime.now().isoformat()
            }
    
    def _advanced_risk_scoring(self, text: str, nlp_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Advanced risk scoring using multiple factors
        
        Args:
            text: Document text
            nlp_analysis: Basic NLP analysis results
            
        Returns:
            Advanced risk scoring results
        """
        risk_scores = {}
        text_lower = text.lower()
        
        # Calculate risk scores for each category
        for category, config in self.risk_categories.items():
            keyword_matches = 0
            context_matches = []
            
            for keyword in config['keywords']:
                matches = list(re.finditer(r'\b' + re.escape(keyword) + r'\b', text_lower))
                keyword_matches += len(matches)
                
                # Extract context for each match
                for match in matches:
                    start = max(0, match.start() - 100)
                    end = min(len(text), match.end() + 100)
                    context = text[start:end].strip()
                    context_matches.append({
                        'keyword': keyword,
                        'context': context,
                        'position': match.start()
                    })
            
            # Calculate category risk score
            base_score = min(keyword_matches * 10, 100)  # Cap at 100
            
            # Adjust based on context severity
            severity_multiplier = self._assess_context_severity(context_matches)
            final_score = min(base_score * severity_multiplier, 100)
            
            risk_scores[category] = {
                'score': final_score,
                'keyword_matches': keyword_matches,
                'context_matches': context_matches[:5],  # Top 5 contexts
                'severity_multiplier': severity_multiplier
            }
        
        # Calculate weighted overall risk
        weighted_score = sum(
            scores['score'] * config['weight'] 
            for category, (scores, config) in 
            zip(risk_scores.keys(), zip(risk_scores.values(), self.risk_categories.values()))
        )
        
        return {
            'category_scores': risk_scores,
            'weighted_overall_score': weighted_score,
            'risk_level': self._score_to_risk_level(weighted_score),
            'top_risk_categories': self._get_top_risk_categories(risk_scores)
        }
    
    def _assess_context_severity(self, context_matches: List[Dict]) -> float:
        """Assess severity based on context around risk keywords"""
        if not context_matches:
            return 1.0
        
        severity_indicators = {
            'high': ['material', 'significant', 'substantial', 'major', 'critical', 'severe'],
            'medium': ['potential', 'possible', 'may', 'could', 'might'],
            'low': ['minor', 'minimal', 'limited', 'unlikely', 'remote']
        }
        
        high_count = 0
        medium_count = 0
        low_count = 0
        
        for match in context_matches:
            context_lower = match['context'].lower()
            
            for indicator in severity_indicators['high']:
                if indicator in context_lower:
                    high_count += 1
                    break
            
            for indicator in severity_indicators['medium']:
                if indicator in context_lower:
                    medium_count += 1
                    break
            
            for indicator in severity_indicators['low']:
                if indicator in context_lower:
                    low_count += 1
                    break
        
        # Calculate severity multiplier
        total_contexts = len(context_matches)
        if total_contexts == 0:
            return 1.0
        
        high_ratio = high_count / total_contexts
        low_ratio = low_count / total_contexts
        
        if high_ratio > 0.3:
            return 1.5  # Increase risk
        elif low_ratio > 0.3:
            return 0.7  # Decrease risk
        else:
            return 1.0  # Neutral
    
    def _analyze_legal_clauses_advanced(self, text: str) -> Dict[str, Any]:
        """
        Advanced legal clause analysis with risk assessment
        
        Args:
            text: Document text
            
        Returns:
            Advanced clause analysis
        """
        # Get basic clause extraction
        basic_clauses = self.nlp_pipeline.extract_legal_clauses(text)
        
        # Enhanced clause analysis
        clause_risks = []
        
        # Define problematic clause patterns
        problematic_patterns = {
            'unlimited_liability': {
                'patterns': [r'unlimited liability', r'without limitation', r'in no event.*limited'],
                'risk_level': 'high',
                'description': 'Unlimited liability exposure'
            },
            'broad_indemnification': {
                'patterns': [r'indemnify.*against.*all', r'hold.*harmless.*from.*any'],
                'risk_level': 'high',
                'description': 'Broad indemnification obligations'
            },
            'automatic_renewal': {
                'patterns': [r'automatically.*renew', r'auto.*renewal', r'unless.*terminated'],
                'risk_level': 'medium',
                'description': 'Automatic renewal clauses'
            },
            'exclusive_jurisdiction': {
                'patterns': [r'exclusive jurisdiction', r'courts of.*shall have.*jurisdiction'],
                'risk_level': 'medium',
                'description': 'Exclusive jurisdiction clauses'
            },
            'liquidated_damages': {
                'patterns': [r'liquidated damages', r'penalty.*amount', r'fixed.*damages'],
                'risk_level': 'medium',
                'description': 'Liquidated damages provisions'
            }
        }
        
        text_lower = text.lower()
        
        for clause_type, config in problematic_patterns.items():
            for pattern in config['patterns']:
                matches = list(re.finditer(pattern, text_lower, re.IGNORECASE))
                
                for match in matches:
                    # Extract context
                    start = max(0, match.start() - 150)
                    end = min(len(text), match.end() + 150)
                    context = text[start:end].strip()
                    
                    clause_risks.append({
                        'clause_type': clause_type,
                        'risk_level': config['risk_level'],
                        'description': config['description'],
                        'matched_text': match.group(),
                        'context': context,
                        'position': match.start()
                    })
        
        # Analyze clause balance
        clause_balance = self._analyze_clause_balance(basic_clauses + clause_risks)
        
        return {
            'basic_clauses': basic_clauses,
            'problematic_clauses': clause_risks,
            'clause_balance': clause_balance,
            'total_clauses_analyzed': len(basic_clauses) + len(clause_risks),
            'high_risk_clauses': len([c for c in clause_risks if c['risk_level'] == 'high'])
        }
    
    def _analyze_clause_balance(self, all_clauses: List[Dict]) -> Dict[str, Any]:
        """Analyze the balance of contractual clauses"""
        clause_types = {}
        
        for clause in all_clauses:
            clause_type = clause.get('clause_type', 'unknown')
            if clause_type not in clause_types:
                clause_types[clause_type] = 0
            clause_types[clause_type] += 1
        
        # Assess balance
        total_clauses = len(all_clauses)
        balance_score = 50  # Start neutral
        
        # Check for heavily skewed clause types
        if total_clauses > 0:
            for clause_type, count in clause_types.items():
                ratio = count / total_clauses
                
                # Penalty for heavily skewed contracts
                if ratio > 0.5:
                    balance_score -= 20
                elif ratio > 0.3:
                    balance_score -= 10
        
        return {
            'clause_distribution': clause_types,
            'balance_score': max(0, balance_score),
            'is_balanced': balance_score >= 40,
            'dominant_clause_type': max(clause_types.items(), key=lambda x: x[1])[0] if clause_types else None
        }
    
    def _detect_compliance_gaps(self, text: str, nlp_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Detect potential compliance gaps and regulatory issues
        
        Args:
            text: Document text
            nlp_analysis: NLP analysis results
            
        Returns:
            Compliance gap analysis
        """
        compliance_issues = []
        
        # Define compliance requirements patterns
        compliance_patterns = {
            'data_privacy': {
                'required_terms': ['privacy policy', 'data protection', 'gdpr', 'personal data'],
                'risk_if_missing': 'high',
                'description': 'Data privacy compliance requirements'
            },
            'anti_corruption': {
                'required_terms': ['anti-corruption', 'bribery', 'fcpa', 'compliance'],
                'risk_if_missing': 'high',
                'description': 'Anti-corruption compliance'
            },
            'employment_law': {
                'required_terms': ['equal opportunity', 'discrimination', 'harassment', 'workplace'],
                'risk_if_missing': 'medium',
                'description': 'Employment law compliance'
            },
            'intellectual_property': {
                'required_terms': ['intellectual property', 'confidentiality', 'trade secrets'],
                'risk_if_missing': 'medium',
                'description': 'IP protection requirements'
            },
            'financial_regulations': {
                'required_terms': ['sox', 'sarbanes-oxley', 'financial reporting', 'audit'],
                'risk_if_missing': 'high',
                'description': 'Financial regulatory compliance'
            }
        }
        
        text_lower = text.lower()
        
        for compliance_area, config in compliance_patterns.items():
            terms_found = []
            
            for term in config['required_terms']:
                if term in text_lower:
                    terms_found.append(term)
            
            coverage_ratio = len(terms_found) / len(config['required_terms'])
            
            if coverage_ratio < 0.5:  # Less than 50% coverage
                compliance_issues.append({
                    'compliance_area': compliance_area,
                    'description': config['description'],
                    'risk_level': config['risk_if_missing'],
                    'coverage_ratio': coverage_ratio,
                    'missing_terms': [t for t in config['required_terms'] if t not in terms_found],
                    'found_terms': terms_found
                })
        
        # Calculate overall compliance score
        total_areas = len(compliance_patterns)
        issues_count = len(compliance_issues)
        compliance_score = max(0, 100 - (issues_count / total_areas * 100))
        
        return {
            'compliance_issues': compliance_issues,
            'compliance_score': compliance_score,
            'high_risk_gaps': len([i for i in compliance_issues if i['risk_level'] == 'high']),
            'total_gaps_identified': len(compliance_issues),
            'compliance_level': 'good' if compliance_score >= 80 else 'acceptable' if compliance_score >= 60 else 'poor'
        }
    
    def _assess_litigation_risk(self, text: str, nlp_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess litigation risk based on document content
        
        Args:
            text: Document text
            nlp_analysis: NLP analysis results
            
        Returns:
            Litigation risk assessment
        """
        # Extract existing legal risks from NLP analysis
        existing_risks = nlp_analysis.get('risk_analysis', [])
        
        # Additional litigation indicators
        litigation_indicators = {
            'active_litigation': [
                'pending lawsuit', 'ongoing litigation', 'court proceeding',
                'legal action', 'plaintiff', 'defendant'
            ],
            'regulatory_action': [
                'sec investigation', 'regulatory inquiry', 'enforcement action',
                'consent decree', 'settlement agreement'
            ],
            'contract_disputes': [
                'breach of contract', 'contract dispute', 'material breach',
                'default notice', 'cure period'
            ],
            'ip_disputes': [
                'patent infringement', 'trademark dispute', 'copyright violation',
                'trade secret misappropriation'
            ]
        }
        
        text_lower = text.lower()
        litigation_risks = []
        
        for risk_category, indicators in litigation_indicators.items():
            category_risks = []
            
            for indicator in indicators:
                if indicator in text_lower:
                    # Find context
                    pattern_pos = text_lower.find(indicator)
                    start = max(0, pattern_pos - 200)
                    end = min(len(text), pattern_pos + 200)
                    context = text[start:end].strip()
                    
                    category_risks.append({
                        'indicator': indicator,
                        'context': context,
                        'severity': self._assess_litigation_severity(context)
                    })
            
            if category_risks:
                litigation_risks.append({
                    'category': risk_category,
                    'risks': category_risks,
                    'risk_count': len(category_risks)
                })
        
        # Calculate litigation risk score
        total_risks = sum(len(cat['risks']) for cat in litigation_risks)
        high_severity_risks = sum(
            len([r for r in cat['risks'] if r['severity'] == 'high'])
            for cat in litigation_risks
        )
        
        litigation_score = min(total_risks * 15 + high_severity_risks * 10, 100)
        
        return {
            'litigation_risks': litigation_risks,
            'litigation_score': litigation_score,
            'risk_level': self._score_to_risk_level(litigation_score),
            'total_litigation_indicators': total_risks,
            'high_severity_indicators': high_severity_risks,
            'requires_legal_review': litigation_score >= 50
        }
    
    def _assess_litigation_severity(self, context: str) -> str:
        """Assess severity of litigation indicators"""
        context_lower = context.lower()
        
        high_severity = ['material', 'significant', 'substantial', 'major', 'critical']
        low_severity = ['minor', 'minimal', 'resolved', 'settled', 'dismissed']
        
        high_count = sum(1 for indicator in high_severity if indicator in context_lower)
        low_count = sum(1 for indicator in low_severity if indicator in context_lower)
        
        if high_count > low_count:
            return 'high'
        elif low_count > high_count:
            return 'low'
        else:
            return 'medium'
    
    def _generate_ai_insights(self, text: str, document_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate AI-powered insights using Gemini API
        
        Args:
            text: Document text
            document_type: Optional document type
            
        Returns:
            AI-generated insights
        """
        if not self.gemini_api_key:
            return {
                'available': False,
                'reason': 'Gemini API key not configured'
            }
        
        try:
            self._init_gemini_client()
            
            if not self.gemini_client:
                return {
                    'available': False,
                    'reason': 'Gemini client initialization failed'
                }
            
            # Prepare prompt for legal analysis
            prompt = self._create_legal_analysis_prompt(text, document_type)
            
            # Generate insights
            response = self.gemini_client.generate_content(prompt)
            
            if response and response.text:
                return {
                    'available': True,
                    'insights': response.text,
                    'generated_at': datetime.now().isoformat(),
                    'model': 'gemini-pro'
                }
            else:
                return {
                    'available': False,
                    'reason': 'No response from Gemini API'
                }
                
        except Exception as e:
            logger.error(f"Error generating AI insights: {e}")
            return {
                'available': False,
                'reason': f'Error: {str(e)}'
            }
    
    def _create_legal_analysis_prompt(self, text: str, document_type: Optional[str] = None) -> str:
        """Create prompt for Gemini legal analysis"""
        # Truncate text if too long (Gemini has token limits)
        max_chars = 8000
        if len(text) > max_chars:
            text = text[:max_chars] + "... [truncated]"
        
        prompt = f"""
As a legal expert, analyze the following legal document and provide insights on:

1. Key legal risks and red flags
2. Unusual or problematic clauses
3. Compliance considerations
4. Recommendations for risk mitigation
5. Overall assessment of legal exposure

Document Type: {document_type or 'Unknown'}

Document Text:
{text}

Please provide a structured analysis focusing on practical legal risks and actionable recommendations.
"""
        return prompt
    
    def _generate_legal_recommendations(self, nlp_analysis: Dict, risk_analysis: Dict,
                                     compliance_analysis: Dict, litigation_risk: Dict) -> List[str]:
        """Generate legal recommendations based on analysis results"""
        recommendations = []
        
        # Risk-based recommendations
        overall_risk_score = risk_analysis.get('weighted_overall_score', 0)
        if overall_risk_score >= 70:
            recommendations.append("URGENT: High legal risk identified - conduct immediate detailed legal review")
        elif overall_risk_score >= 40:
            recommendations.append("Moderate legal risk - recommend additional legal due diligence")
        
        # Top risk categories
        top_risks = risk_analysis.get('top_risk_categories', [])
        for risk_category in top_risks[:2]:  # Top 2 risks
            if risk_category == 'litigation':
                recommendations.append("Focus on litigation history and pending legal matters")
            elif risk_category == 'regulatory':
                recommendations.append("Conduct thorough regulatory compliance review")
            elif risk_category == 'contractual':
                recommendations.append("Review all material contracts and agreements")
        
        # Compliance recommendations
        compliance_issues = compliance_analysis.get('compliance_issues', [])
        high_risk_gaps = [i for i in compliance_issues if i['risk_level'] == 'high']
        
        if high_risk_gaps:
            recommendations.append(f"Address {len(high_risk_gaps)} high-risk compliance gaps immediately")
        
        # Litigation recommendations
        if litigation_risk.get('requires_legal_review', False):
            recommendations.append("Litigation indicators found - engage litigation counsel for assessment")
        
        # Clause-specific recommendations
        clause_analysis = nlp_analysis.get('legal_clauses', [])
        high_risk_clauses = [c for c in clause_analysis if c.get('confidence', 0) > 0.8]
        
        if len(high_risk_clauses) > 5:
            recommendations.append("Multiple concerning clauses identified - comprehensive contract review needed")
        
        # Default recommendation
        if not recommendations:
            recommendations.append("Continue with standard legal due diligence procedures")
        
        return recommendations[:10]  # Limit to 10 recommendations
    
    def _calculate_overall_legal_risk_score(self, risk_analysis: Dict, 
                                          compliance_analysis: Dict, 
                                          litigation_risk: Dict) -> Dict[str, Any]:
        """Calculate overall legal risk score"""
        # Weight different risk components
        weights = {
            'risk_analysis': 0.4,
            'compliance': 0.3,
            'litigation': 0.3
        }
        
        risk_score = risk_analysis.get('weighted_overall_score', 0)
        compliance_score = 100 - compliance_analysis.get('compliance_score', 100)  # Invert compliance score
        litigation_score = litigation_risk.get('litigation_score', 0)
        
        overall_score = (
            risk_score * weights['risk_analysis'] +
            compliance_score * weights['compliance'] +
            litigation_score * weights['litigation']
        )
        
        return {
            'overall_score': round(overall_score, 2),
            'risk_level': self._score_to_risk_level(overall_score),
            'component_scores': {
                'risk_analysis': risk_score,
                'compliance_risk': compliance_score,
                'litigation_risk': litigation_score
            },
            'weights': weights
        }
    
    def _score_to_risk_level(self, score: float) -> str:
        """Convert numeric score to risk level"""
        if score >= 70:
            return 'high'
        elif score >= 40:
            return 'medium'
        else:
            return 'low'
    
    def _get_top_risk_categories(self, risk_scores: Dict[str, Dict]) -> List[str]:
        """Get top risk categories by score"""
        sorted_categories = sorted(
            risk_scores.items(),
            key=lambda x: x[1]['score'],
            reverse=True
        )
        return [category for category, _ in sorted_categories if _['score'] > 20]