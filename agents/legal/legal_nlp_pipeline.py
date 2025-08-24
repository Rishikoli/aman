"""
Legal NLP Pipeline for AI-powered legal analysis
Uses simple rule-based NLP instead of complex ML models
"""

import logging
import re
from typing import Dict, List, Optional, Any, Tuple
import sys
from pathlib import Path
from datetime import datetime

# Add utils directory to path
sys.path.append(str(Path(__file__).parent.parent / 'utils'))

from simple_nlp import SimpleNLP

logger = logging.getLogger(__name__)

class LegalNLPPipeline:
    """
    NLP pipeline specialized for legal document analysis and entity extraction
    Uses simple rule-based NLP instead of complex ML models
    """
    
    def __init__(self):
        """Initialize the legal NLP pipeline with simple processors"""
        self.nlp_processor = SimpleNLP()
        self.initialized = False
        
        # Legal entity patterns (inherited from SimpleNLP but can be extended)
        self.legal_patterns = {
            'court_cases': [
                r'\b[A-Z][a-z]+ v\.? [A-Z][a-z]+\b',
                r'\b[A-Z][a-z]+ vs\.? [A-Z][a-z]+\b',
                r'\bCase No\.? \d+[-/]\d+\b',
                r'\bCivil Action No\.? \d+[-/]\d+\b'
            ],
            'legal_citations': [
                r'\b\d+\s+[A-Z][a-z\.]+\s+\d+\b',  # e.g., "123 F.3d 456"
                r'\b\d+\s+U\.S\.C\.?\s+§?\s*\d+\b',  # USC citations
                r'\b\d+\s+C\.F\.R\.?\s+§?\s*\d+\b'   # CFR citations
            ],
            'monetary_amounts': [
                r'\$[\d,]+(?:\.\d{2})?(?:\s*(?:million|billion|thousand))?',
                r'(?:USD|dollars?)\s*[\d,]+(?:\.\d{2})?(?:\s*(?:million|billion|thousand))?'
            ],
            'dates': [
                r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b',
                r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b'
            ],
            'percentages': [
                r'\d+(?:\.\d+)?%'
            ]
        }
    
    def initialize(self) -> bool:
        """
        Initialize simple NLP processors
        
        Returns:
            True if initialization successful, False otherwise
        """
        try:
            logger.info("Initializing Simple Legal NLP Pipeline...")
            
            # Initialize simple NLP processor (no external dependencies)
            if self.nlp_processor:
                logger.info("✅ Simple NLP processor initialized successfully")
                self.initialized = True
                return True
            else:
                logger.error("❌ Failed to initialize simple NLP processor")
                return False
                
        except Exception as e:
            logger.error(f"Failed to initialize Legal NLP Pipeline: {e}")
            return False
    
    def extract_legal_entities(self, text: str) -> Dict[str, List[str]]:
        """
        Extract legal entities from text using simple pattern matching
        
        Args:
            text: Legal text to analyze
            
        Returns:
            Dictionary of extracted entities by category
        """
        # Use the simple NLP processor for entity extraction
        return self.nlp_processor.extract_entities(text)
    
    def analyze_legal_risk_sentiment(self, text: str) -> Dict[str, Any]:
        """
        Analyze sentiment and risk indicators in legal text using simple methods
        
        Args:
            text: Legal text to analyze
            
        Returns:
            Sentiment and risk analysis results
        """
        # Use the simple NLP processor for sentiment analysis
        return self.nlp_processor.analyze_sentiment(text)
    
    def classify_legal_document_type(self, text: str) -> Dict[str, Any]:
        """
        Classify the type of legal document using simple methods
        
        Args:
            text: Document text to classify
            
        Returns:
            Document classification results
        """
        # Use the simple NLP processor for document classification
        return self.nlp_processor.classify_document_type(text)
    
    def extract_legal_clauses(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract specific legal clauses and provisions using simple pattern matching
        
        Args:
            text: Legal document text
            
        Returns:
            List of extracted clauses
        """
        clauses = []
        
        # Common legal clause patterns
        clause_patterns = {
            'limitation_of_liability': [
                r'limitation of liability',
                r'shall not be liable',
                r'in no event shall.*be liable'
            ],
            'indemnification': [
                r'indemnify.*against',
                r'hold harmless',
                r'defend.*indemnify'
            ],
            'termination': [
                r'terminate.*agreement',
                r'upon termination',
                r'end this agreement'
            ],
            'governing_law': [
                r'governed by.*law',
                r'laws of.*shall govern',
                r'jurisdiction.*courts'
            ],
            'confidentiality': [
                r'confidential information',
                r'non-disclosure',
                r'proprietary information'
            ]
        }
        
        text_lower = text.lower()
        
        for clause_type, patterns in clause_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, text_lower, re.IGNORECASE)
                for match in matches:
                    # Extract context around the match
                    start = max(0, match.start() - 100)
                    end = min(len(text), match.end() + 100)
                    context = text[start:end].strip()
                    
                    clauses.append({
                        'clause_type': clause_type,
                        'matched_text': match.group(),
                        'context': context,
                        'start_position': match.start(),
                        'end_position': match.end(),
                        'confidence': 0.7
                    })
        
        return clauses
    
    def analyze_contract_terms(self, text: str) -> Dict[str, Any]:
        """
        Analyze contract terms and conditions
        
        Args:
            text: Contract text
            
        Returns:
            Contract analysis results
        """
        analysis = {
            'contract_type': 'unknown',
            'key_terms': [],
            'obligations': [],
            'rights': [],
            'risks': [],
            'duration': None
        }
        
        text_lower = text.lower()
        
        # Identify contract type
        contract_types = {
            'employment': ['employment', 'employee', 'employer', 'salary', 'benefits'],
            'service': ['services', 'provider', 'client', 'deliverables'],
            'purchase': ['purchase', 'sale', 'buyer', 'seller', 'goods'],
            'license': ['license', 'licensor', 'licensee', 'intellectual property'],
            'lease': ['lease', 'lessor', 'lessee', 'rent', 'premises']
        }
        
        for contract_type, keywords in contract_types.items():
            if sum(1 for keyword in keywords if keyword in text_lower) >= 2:
                analysis['contract_type'] = contract_type
                break
        
        # Extract key terms using simple patterns
        key_term_patterns = [
            r'payment.*\$[\d,]+',
            r'term.*\d+.*(?:year|month|day)',
            r'penalty.*\$[\d,]+',
            r'interest.*\d+%'
        ]
        
        for pattern in key_term_patterns:
            matches = re.findall(pattern, text_lower)
            analysis['key_terms'].extend(matches)
        
        # Extract obligations and rights
        obligation_patterns = [
            r'shall.*(?:provide|deliver|pay|perform)',
            r'must.*(?:comply|adhere|follow)',
            r'required to.*(?:maintain|ensure|complete)'
        ]
        
        for pattern in obligation_patterns:
            matches = re.findall(pattern, text_lower)
            analysis['obligations'].extend(matches[:5])  # Limit to 5
        
        return analysis
    
    def extract_legal_risks(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract legal risks and red flags from text
        
        Args:
            text: Legal text to analyze
            
        Returns:
            List of identified risks
        """
        risks = []
        
        # Risk indicator patterns
        risk_patterns = {
            'litigation_risk': [
                r'lawsuit', r'litigation', r'legal proceeding', r'court action',
                r'plaintiff', r'defendant', r'complaint filed'
            ],
            'regulatory_risk': [
                r'investigation', r'violation', r'non-compliance', r'penalty',
                r'regulatory action', r'enforcement', r'sanctions'
            ],
            'financial_risk': [
                r'material adverse', r'going concern', r'default', r'bankruptcy',
                r'insolvency', r'financial distress', r'covenant breach'
            ],
            'operational_risk': [
                r'business interruption', r'key personnel', r'system failure',
                r'data breach', r'cybersecurity', r'operational failure'
            ]
        }
        
        text_lower = text.lower()
        
        for risk_category, patterns in risk_patterns.items():
            for pattern in patterns:
                if pattern in text_lower:
                    # Find context around the risk indicator
                    pattern_pos = text_lower.find(pattern)
                    start = max(0, pattern_pos - 150)
                    end = min(len(text), pattern_pos + 150)
                    context = text[start:end].strip()
                    
                    risks.append({
                        'risk_category': risk_category,
                        'risk_indicator': pattern,
                        'context': context,
                        'severity': self._assess_risk_severity(context),
                        'position': pattern_pos
                    })
        
        # Remove duplicates and sort by severity
        unique_risks = []
        seen_contexts = set()
        
        for risk in risks:
            context_key = risk['context'][:100]  # Use first 100 chars as key
            if context_key not in seen_contexts:
                seen_contexts.add(context_key)
                unique_risks.append(risk)
        
        # Sort by severity (high first)
        severity_order = {'high': 3, 'medium': 2, 'low': 1}
        unique_risks.sort(key=lambda x: severity_order.get(x['severity'], 0), reverse=True)
        
        return unique_risks[:10]  # Return top 10 risks
    
    def _assess_risk_severity(self, context: str) -> str:
        """
        Assess the severity of a risk based on context
        
        Args:
            context: Text context around the risk indicator
            
        Returns:
            Risk severity level
        """
        context_lower = context.lower()
        
        # High severity indicators
        high_severity = [
            'material', 'significant', 'substantial', 'major', 'critical',
            'immediate', 'urgent', 'severe', 'serious', 'adverse'
        ]
        
        # Low severity indicators
        low_severity = [
            'minor', 'minimal', 'limited', 'potential', 'possible',
            'unlikely', 'remote', 'manageable', 'mitigated'
        ]
        
        high_count = sum(1 for indicator in high_severity if indicator in context_lower)
        low_count = sum(1 for indicator in low_severity if indicator in context_lower)
        
        if high_count > low_count and high_count > 0:
            return 'high'
        elif low_count > high_count and low_count > 0:
            return 'low'
        else:
            return 'medium'
    
    def generate_legal_summary(self, text: str) -> str:
        """
        Generate a summary of legal text
        
        Args:
            text: Legal text to summarize
            
        Returns:
            Summary text
        """
        # Use the simple NLP processor for summarization
        return self.nlp_processor.summarize_text(text, max_sentences=5)
    
    def analyze_legal_document(self, text: str) -> Dict[str, Any]:
        """
        Comprehensive legal document analysis
        
        Args:
            text: Legal document text
            
        Returns:
            Complete analysis results
        """
        if not self.initialized:
            logger.warning("NLP pipeline not initialized, using basic analysis")
        
        return {
            'document_classification': self.classify_legal_document_type(text),
            'entities': self.extract_legal_entities(text),
            'sentiment_analysis': self.analyze_legal_risk_sentiment(text),
            'legal_clauses': self.extract_legal_clauses(text),
            'contract_analysis': self.analyze_contract_terms(text),
            'risk_analysis': self.extract_legal_risks(text),
            'summary': self.generate_legal_summary(text),
            'analysis_timestamp': datetime.now().isoformat(),
            'text_statistics': {
                'character_count': len(text),
                'word_count': len(text.split()),
                'sentence_count': len(re.split(r'[.!?]+', text))
            }
        }