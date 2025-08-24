"""
Simple NLP utilities to replace Hugging Face transformers.
Cross-platform compatible using built-in Python libraries and basic NLP techniques.
"""

import re
import logging
from typing import Dict, List, Any, Optional, Tuple
from collections import Counter
import string
import json
from pathlib import Path

logger = logging.getLogger(__name__)

class SimpleNLP:
    """
    Simple NLP processor using rule-based and statistical methods.
    No external ML dependencies required.
    """
    
    def __init__(self):
        """Initialize the simple NLP processor."""
        self.legal_keywords = self._load_legal_keywords()
        self.risk_keywords = self._load_risk_keywords()
        self.entity_patterns = self._load_entity_patterns()
        
    def _load_legal_keywords(self) -> Dict[str, List[str]]:
        """Load legal domain keywords for classification."""
        return {
            'litigation': [
                'lawsuit', 'litigation', 'court', 'plaintiff', 'defendant', 'complaint',
                'motion', 'brief', 'trial', 'settlement', 'damages', 'injunction',
                'appeal', 'judgment', 'verdict', 'arbitration', 'mediation'
            ],
            'contract': [
                'agreement', 'contract', 'terms', 'conditions', 'whereas', 'party',
                'consideration', 'breach', 'performance', 'obligation', 'covenant',
                'warranty', 'indemnification', 'termination', 'renewal'
            ],
            'regulatory': [
                'regulation', 'compliance', 'sec', 'fda', 'ftc', 'antitrust',
                'securities', 'disclosure', 'filing', 'violation', 'penalty',
                'enforcement', 'investigation', 'audit', 'inspection'
            ],
            'intellectual_property': [
                'patent', 'trademark', 'copyright', 'trade secret', 'invention',
                'claims', 'infringement', 'licensing', 'royalty', 'prior art',
                'novelty', 'obviousness', 'prosecution', 'maintenance'
            ],
            'corporate': [
                'incorporation', 'bylaws', 'board', 'directors', 'shareholders',
                'merger', 'acquisition', 'dissolution', 'governance', 'fiduciary',
                'proxy', 'voting', 'dividend', 'capital', 'equity'
            ]
        }
    
    def _load_risk_keywords(self) -> Dict[str, List[str]]:
        """Load risk-related keywords for sentiment analysis."""
        return {
            'high_risk': [
                'material adverse', 'significant risk', 'substantial doubt', 'going concern',
                'default', 'bankruptcy', 'insolvency', 'violation', 'breach', 'penalty',
                'investigation', 'enforcement', 'litigation', 'lawsuit', 'claim',
                'contingent liability', 'material weakness', 'deficiency'
            ],
            'medium_risk': [
                'uncertainty', 'may result', 'could impact', 'potential', 'possible',
                'risk factor', 'challenge', 'difficulty', 'adverse', 'negative',
                'decline', 'decrease', 'loss', 'impairment', 'contingency'
            ],
            'low_risk': [
                'mitigate', 'manage', 'control', 'monitor', 'adequate', 'sufficient',
                'effective', 'compliance', 'improvement', 'strengthen', 'enhance',
                'favorable', 'positive', 'growth', 'increase', 'benefit'
            ]
        }
    
    def _load_entity_patterns(self) -> Dict[str, str]:
        """Load regex patterns for entity extraction."""
        return {
            'money': r'\$[\d,]+(?:\.\d{2})?(?:\s*(?:million|billion|thousand|M|B|K))?',
            'percentage': r'\d+(?:\.\d+)?%',
            'date': r'\b(?:\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\w+\s+\d{1,2},?\s+\d{4})\b',
            'company': r'\b[A-Z][a-zA-Z\s&]+(?:Inc\.?|Corp\.?|LLC|Ltd\.?|Co\.?|Company)\b',
            'case_citation': r'\b\d+\s+[A-Z][a-z]+\.?\s+\d+\b',
            'statute': r'\b\d+\s+U\.?S\.?C\.?\s+§?\s*\d+\b',
            'regulation': r'\b\d+\s+C\.?F\.?R\.?\s+§?\s*\d+(?:\.\d+)?\b'
        }
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """
        Extract named entities from text using regex patterns.
        
        Args:
            text: Input text
            
        Returns:
            Dictionary of entity types and their matches
        """
        entities = {}
        
        for entity_type, pattern in self.entity_patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                # Remove duplicates and limit to top 10
                entities[entity_type] = list(set(matches))[:10]
        
        return entities
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """
        Analyze legal risk sentiment using keyword-based approach.
        
        Args:
            text: Input text
            
        Returns:
            Sentiment analysis results
        """
        text_lower = text.lower()
        
        # Count risk keywords
        high_risk_count = sum(1 for keyword in self.risk_keywords['high_risk'] 
                             if keyword in text_lower)
        medium_risk_count = sum(1 for keyword in self.risk_keywords['medium_risk'] 
                               if keyword in text_lower)
        low_risk_count = sum(1 for keyword in self.risk_keywords['low_risk'] 
                            if keyword in text_lower)
        
        total_risk_keywords = high_risk_count + medium_risk_count + low_risk_count
        
        if total_risk_keywords == 0:
            risk_level = 'neutral'
            risk_score = 0.5
        else:
            # Calculate weighted risk score
            risk_score = (high_risk_count * 1.0 + medium_risk_count * 0.5 + low_risk_count * 0.1) / total_risk_keywords
            
            if risk_score >= 0.7:
                risk_level = 'high'
            elif risk_score >= 0.4:
                risk_level = 'medium'
            else:
                risk_level = 'low'
        
        return {
            'risk_level': risk_level,
            'risk_score': risk_score,
            'high_risk_indicators': high_risk_count,
            'medium_risk_indicators': medium_risk_count,
            'low_risk_indicators': low_risk_count,
            'total_risk_keywords': total_risk_keywords
        }
    
    def classify_document_type(self, text: str) -> Dict[str, Any]:
        """
        Classify legal document type using keyword matching.
        
        Args:
            text: Document text
            
        Returns:
            Document classification results
        """
        text_lower = text.lower()
        
        # Count keywords for each category
        category_scores = {}
        for category, keywords in self.legal_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                category_scores[category] = score
        
        if not category_scores:
            return {
                'document_type': 'unknown',
                'confidence': 0.0,
                'category_scores': {}
            }
        
        # Find the category with the highest score
        best_category = max(category_scores, key=category_scores.get)
        max_score = category_scores[best_category]
        total_keywords = sum(len(keywords) for keywords in self.legal_keywords.values())
        
        # Calculate confidence based on keyword density
        confidence = min(1.0, max_score / 10.0)  # Normalize to 0-1 range
        
        return {
            'document_type': best_category,
            'confidence': confidence,
            'category_scores': category_scores,
            'keyword_matches': max_score
        }
    
    def extract_key_phrases(self, text: str, max_phrases: int = 10) -> List[Dict[str, Any]]:
        """
        Extract key phrases using simple statistical methods.
        
        Args:
            text: Input text
            max_phrases: Maximum number of phrases to return
            
        Returns:
            List of key phrases with scores
        """
        # Clean and tokenize text
        text = re.sub(r'[^\w\s]', ' ', text.lower())
        words = text.split()
        
        # Remove common stop words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have',
            'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
            'may', 'might', 'can', 'shall', 'must', 'this', 'that', 'these', 'those'
        }
        
        # Filter words
        filtered_words = [word for word in words if word not in stop_words and len(word) > 2]
        
        # Generate n-grams (1-3 words)
        phrases = []
        
        # Unigrams
        phrases.extend(filtered_words)
        
        # Bigrams
        for i in range(len(filtered_words) - 1):
            phrases.append(f"{filtered_words[i]} {filtered_words[i+1]}")
        
        # Trigrams
        for i in range(len(filtered_words) - 2):
            phrases.append(f"{filtered_words[i]} {filtered_words[i+1]} {filtered_words[i+2]}")
        
        # Count phrase frequencies
        phrase_counts = Counter(phrases)
        
        # Score phrases (frequency * length bonus)
        scored_phrases = []
        for phrase, count in phrase_counts.most_common():
            word_count = len(phrase.split())
            score = count * (1 + 0.1 * word_count)  # Slight bonus for longer phrases
            
            scored_phrases.append({
                'phrase': phrase,
                'frequency': count,
                'score': score,
                'word_count': word_count
            })
        
        # Return top phrases
        return sorted(scored_phrases, key=lambda x: x['score'], reverse=True)[:max_phrases]
    
    def summarize_text(self, text: str, max_sentences: int = 3) -> str:
        """
        Create a simple extractive summary.
        
        Args:
            text: Input text
            max_sentences: Maximum number of sentences in summary
            
        Returns:
            Summary text
        """
        # Split into sentences
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
        
        if len(sentences) <= max_sentences:
            return '. '.join(sentences) + '.'
        
        # Score sentences based on keyword density
        sentence_scores = []
        
        for i, sentence in enumerate(sentences):
            score = 0
            sentence_lower = sentence.lower()
            
            # Score based on legal keywords
            for category, keywords in self.legal_keywords.items():
                for keyword in keywords:
                    if keyword in sentence_lower:
                        score += 1
            
            # Score based on risk keywords
            for category, keywords in self.risk_keywords.items():
                for keyword in keywords:
                    if keyword in sentence_lower:
                        score += 1
            
            # Bonus for sentence position (first and last sentences often important)
            if i == 0 or i == len(sentences) - 1:
                score += 2
            
            sentence_scores.append((score, i, sentence))
        
        # Select top sentences
        top_sentences = sorted(sentence_scores, key=lambda x: x[0], reverse=True)[:max_sentences]
        
        # Sort by original order
        top_sentences = sorted(top_sentences, key=lambda x: x[1])
        
        # Create summary
        summary_sentences = [sentence for _, _, sentence in top_sentences]
        return '. '.join(summary_sentences) + '.'
    
    def analyze_legal_text(self, text: str) -> Dict[str, Any]:
        """
        Comprehensive legal text analysis.
        
        Args:
            text: Legal document text
            
        Returns:
            Complete analysis results
        """
        return {
            'entities': self.extract_entities(text),
            'sentiment': self.analyze_sentiment(text),
            'document_type': self.classify_document_type(text),
            'key_phrases': self.extract_key_phrases(text),
            'summary': self.summarize_text(text),
            'text_length': len(text),
            'word_count': len(text.split()),
            'sentence_count': len(re.split(r'[.!?]+', text))
        }

# Global NLP instance
_nlp_instance = None

def get_nlp() -> SimpleNLP:
    """Get the global NLP instance."""
    global _nlp_instance
    
    if _nlp_instance is None:
        _nlp_instance = SimpleNLP()
    
    return _nlp_instance

# Convenience functions
def extract_entities(text: str) -> Dict[str, List[str]]:
    """Extract entities from text."""
    return get_nlp().extract_entities(text)

def analyze_sentiment(text: str) -> Dict[str, Any]:
    """Analyze sentiment of text."""
    return get_nlp().analyze_sentiment(text)

def classify_document(text: str) -> Dict[str, Any]:
    """Classify document type."""
    return get_nlp().classify_document_type(text)

def extract_key_phrases(text: str, max_phrases: int = 10) -> List[Dict[str, Any]]:
    """Extract key phrases from text."""
    return get_nlp().extract_key_phrases(text, max_phrases)

def summarize_text(text: str, max_sentences: int = 3) -> str:
    """Summarize text."""
    return get_nlp().summarize_text(text, max_sentences)

def analyze_legal_text(text: str) -> Dict[str, Any]:
    """Perform comprehensive legal text analysis."""
    return get_nlp().analyze_legal_text(text)