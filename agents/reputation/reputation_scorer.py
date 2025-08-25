"""
Comprehensive Reputation Scoring System
Combines multiple data sources and sentiment analysis to generate reputation scores
"""

import os
import sys
import logging
import statistics
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

# Add the agents directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logger = logging.getLogger(__name__)

class ReputationScorer:
    """
    Advanced reputation scoring system that combines multiple data sources
    """
    
    def __init__(self):
        """Initialize the Reputation Scorer"""
        
        # Scoring weights for different data sources
        self.source_weights = {
            'news': 0.35,           # News articles have high impact
            'social_media': 0.25,   # Social media reflects public opinion
            'employee_reviews': 0.20, # Employee sentiment is important
            'customer_reviews': 0.15, # Customer feedback matters
            'web_sources': 0.05     # Other web sources provide context
        }
        
        # Platform-specific weights within social media
        self.social_platform_weights = {
            'reddit': 0.4,
            'hackernews': 0.3,
            'linkedin': 0.2,
            'youtube': 0.1
        }
        
        # Scoring parameters
        self.base_score = 50  # Neutral starting point (0-100 scale)
        self.max_score = 100
        self.min_score = 0
        
        logger.info("Reputation Scorer initialized with weighted scoring system")
    
    def calculate_comprehensive_score(self, reputation_data: Dict[str, Any], 
                                    sentiment_analysis: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Calculate comprehensive reputation score from all data sources
        
        Args:
            reputation_data: Complete reputation data from all sources
            sentiment_analysis: Optional pre-computed sentiment analysis
            
        Returns:
            Dictionary containing comprehensive reputation scores and breakdown
        """
        try:
            company_name = reputation_data.get('company_name', 'Unknown Company')
            
            # Initialize scoring components
            score_components = {}
            weighted_scores = []
            
            # 1. News Sentiment Score
            news_score = self._calculate_news_score(reputation_data.get('data_sources', {}).get('news', {}))
            if news_score is not None:
                score_components['news'] = news_score
                weighted_scores.append(news_score * self.source_weights['news'])
            
            # 2. Social Media Score
            social_score = self._calculate_social_media_score(reputation_data.get('data_sources', {}).get('social_media', {}))
            if social_score is not None:
                score_components['social_media'] = social_score
                weighted_scores.append(social_score * self.source_weights['social_media'])
            
            # 3. Employee Reviews Score
            employee_score = self._calculate_employee_review_score(reputation_data.get('data_sources', {}).get('web_sources', {}))
            if employee_score is not None:
                score_components['employee_reviews'] = employee_score
                weighted_scores.append(employee_score * self.source_weights['employee_reviews'])
            
            # 4. Customer Reviews Score
            customer_score = self._calculate_customer_review_score(reputation_data.get('data_sources', {}).get('web_sources', {}))
            if customer_score is not None:
                score_components['customer_reviews'] = customer_score
                weighted_scores.append(customer_score * self.source_weights['customer_reviews'])
            
            # 5. Web Sources Score
            web_score = self._calculate_web_sources_score(reputation_data.get('data_sources', {}).get('web_sources', {}))
            if web_score is not None:
                score_components['web_sources'] = web_score
                weighted_scores.append(web_score * self.source_weights['web_sources'])
            
            # Calculate overall score
            if weighted_scores:
                # Normalize weights based on available data
                total_weight = sum(self.source_weights[component] for component in score_components.keys())
                overall_score = sum(weighted_scores) / total_weight * 100
            else:
                overall_score = self.base_score
            
            # Ensure score is within bounds
            overall_score = max(self.min_score, min(self.max_score, overall_score))
            
            # Calculate confidence level
            confidence = self._calculate_confidence(score_components, reputation_data)
            
            # Generate score interpretation
            interpretation = self._interpret_score(overall_score)
            
            # Calculate trend if historical data is available
            trend = self._calculate_trend(reputation_data)
            
            return {
                'company_name': company_name,
                'overall_score': round(overall_score, 2),
                'score_components': score_components,
                'confidence_level': confidence,
                'interpretation': interpretation,
                'trend': trend,
                'scoring_metadata': {
                    'scorer_version': '1.0.0',
                    'calculation_timestamp': datetime.now().isoformat(),
                    'data_sources_used': list(score_components.keys()),
                    'source_weights': self.source_weights
                }
            }
            
        except Exception as e:
            logger.error(f"Error calculating comprehensive reputation score: {e}")
            return {
                'company_name': reputation_data.get('company_name', 'Unknown'),
                'overall_score': self.base_score,
                'error': str(e),
                'confidence_level': 'low'
            }
    
    def calculate_esg_scores(self, reputation_data: Dict[str, Any], 
                           esg_analysis: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Calculate ESG-specific reputation scores
        
        Args:
            reputation_data: Complete reputation data
            esg_analysis: Optional ESG analysis from Gemini
            
        Returns:
            Dictionary containing ESG scores
        """
        try:
            esg_scores = {
                'environmental': self.base_score,
                'social': self.base_score,
                'governance': self.base_score
            }
            
            # Use Gemini ESG analysis if available
            if esg_analysis and not esg_analysis.get('error'):
                esg_scores['environmental'] = esg_analysis.get('environmental', {}).get('score', self.base_score)
                esg_scores['social'] = esg_analysis.get('social', {}).get('score', self.base_score)
                esg_scores['governance'] = esg_analysis.get('governance', {}).get('score', self.base_score)
            else:
                # Fallback ESG scoring based on available data
                esg_scores = self._calculate_fallback_esg_scores(reputation_data)
            
            # Calculate overall ESG score
            overall_esg = statistics.mean(esg_scores.values())
            
            return {
                'overall_esg_score': round(overall_esg, 2),
                'environmental_score': round(esg_scores['environmental'], 2),
                'social_score': round(esg_scores['social'], 2),
                'governance_score': round(esg_scores['governance'], 2),
                'esg_interpretation': self._interpret_esg_score(overall_esg),
                'calculation_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error calculating ESG scores: {e}")
            return {
                'overall_esg_score': self.base_score,
                'error': str(e)
            }
    
    def _calculate_news_score(self, news_data: Dict[str, Any]) -> Optional[float]:
        """Calculate reputation score from news data"""
        try:
            if not news_data or news_data.get('total_articles', 0) == 0:
                return None
            
            # Base score on article count and recency
            article_count = news_data.get('total_articles', 0)
            
            # Score based on volume (more coverage = more visibility, but not necessarily better)
            volume_score = min(100, (article_count / 50) * 50 + 50)  # Normalize around 50 articles
            
            # This would be enhanced with actual sentiment analysis
            # For now, assume neutral sentiment
            sentiment_score = 50
            
            # Combine volume and sentiment
            news_score = (volume_score * 0.3) + (sentiment_score * 0.7)
            
            return news_score
            
        except Exception as e:
            logger.error(f"Error calculating news score: {e}")
            return None
    
    def _calculate_social_media_score(self, social_data: Dict[str, Any]) -> Optional[float]:
        """Calculate reputation score from social media data"""
        try:
            if not social_data or social_data.get('total_mentions', 0) == 0:
                return None
            
            platform_scores = []
            
            # Reddit score
            reddit_data = social_data.get('reddit', {})
            if reddit_data.get('count', 0) > 0:
                reddit_score = self._score_social_platform(reddit_data)
                platform_scores.append(reddit_score * self.social_platform_weights['reddit'])
            
            # Hacker News score
            hackernews_data = social_data.get('hackernews', {})
            if hackernews_data.get('count', 0) > 0:
                hackernews_score = self._score_social_platform(hackernews_data)
                platform_scores.append(hackernews_score * self.social_platform_weights['hackernews'])
            
            # LinkedIn score
            linkedin_data = social_data.get('linkedin', {})
            if linkedin_data.get('count', 0) > 0:
                linkedin_score = self._score_social_platform(linkedin_data)
                platform_scores.append(linkedin_score * self.social_platform_weights['linkedin'])
            
            if platform_scores:
                active_platforms = [p for p in ['reddit', 'hackernews', 'linkedin', 'youtube'] if social_data.get(p, {}).get('count', 0) > 0]
                total_weight = sum(self.social_platform_weights[p] for p in active_platforms)
                return sum(platform_scores) / total_weight * 100
            
            return None
            
        except Exception as e:
            logger.error(f"Error calculating social media score: {e}")
            return None
    
    def _calculate_employee_review_score(self, web_data: Dict[str, Any]) -> Optional[float]:
        """Calculate score from employee reviews (Glassdoor, etc.)"""
        try:
            glassdoor_data = web_data.get('glassdoor', {})
            if not glassdoor_data or glassdoor_data.get('count', 0) == 0:
                return None
            
            # This would use actual review sentiment and ratings
            # For now, return a placeholder score
            return 65  # Slightly positive placeholder
            
        except Exception as e:
            logger.error(f"Error calculating employee review score: {e}")
            return None
    
    def _calculate_customer_review_score(self, web_data: Dict[str, Any]) -> Optional[float]:
        """Calculate score from customer reviews (Trustpilot, etc.)"""
        try:
            trustpilot_data = web_data.get('trustpilot', {})
            if not trustpilot_data or trustpilot_data.get('count', 0) == 0:
                return None
            
            # This would use actual review sentiment and ratings
            # For now, return a placeholder score
            return 70  # Positive placeholder
            
        except Exception as e:
            logger.error(f"Error calculating customer review score: {e}")
            return None
    
    def _calculate_web_sources_score(self, web_data: Dict[str, Any]) -> Optional[float]:
        """Calculate score from other web sources"""
        try:
            if not web_data:
                return None
            
            # BBB rating contribution
            bbb_data = web_data.get('bbb', {})
            bbb_score = 50  # Default neutral
            
            if bbb_data and bbb_data.get('rating'):
                rating = bbb_data.get('rating', 'C')
                rating_scores = {
                    'A+': 95, 'A': 90, 'A-': 85,
                    'B+': 80, 'B': 75, 'B-': 70,
                    'C+': 65, 'C': 60, 'C-': 55,
                    'D+': 50, 'D': 45, 'D-': 40,
                    'F': 30
                }
                bbb_score = rating_scores.get(rating, 50)
            
            return bbb_score
            
        except Exception as e:
            logger.error(f"Error calculating web sources score: {e}")
            return None
    
    def _score_social_platform(self, platform_data: Dict[str, Any]) -> float:
        """Score individual social media platform"""
        try:
            mention_count = platform_data.get('count', 0)
            
            # Base score on engagement and volume
            if mention_count == 0:
                return 50
            
            # Volume scoring (logarithmic scale)
            import math
            volume_score = min(100, 50 + (math.log10(mention_count + 1) * 10))
            
            # This would incorporate actual sentiment analysis
            sentiment_score = 50  # Placeholder neutral sentiment
            
            # Combine volume and sentiment
            platform_score = (volume_score * 0.4) + (sentiment_score * 0.6)
            
            return platform_score
            
        except Exception as e:
            logger.error(f"Error scoring social platform: {e}")
            return 50
    
    def _calculate_fallback_esg_scores(self, reputation_data: Dict[str, Any]) -> Dict[str, float]:
        """Calculate fallback ESG scores when AI analysis is unavailable"""
        try:
            # Simple heuristic-based ESG scoring
            esg_scores = {
                'environmental': 50,
                'social': 50,
                'governance': 50
            }
            
            # Adjust based on available data patterns
            # This is a simplified approach - in production, you'd use more sophisticated analysis
            
            return esg_scores
            
        except Exception as e:
            logger.error(f"Error calculating fallback ESG scores: {e}")
            return {'environmental': 50, 'social': 50, 'governance': 50}
    
    def _calculate_confidence(self, score_components: Dict[str, float], 
                            reputation_data: Dict[str, Any]) -> str:
        """Calculate confidence level in the reputation score"""
        try:
            # Factors affecting confidence
            data_source_count = len(score_components)
            
            # Check data volume
            total_data_points = reputation_data.get('summary', {}).get('total_data_points', 0)
            
            # Calculate confidence
            if data_source_count >= 3 and total_data_points >= 50:
                return 'high'
            elif data_source_count >= 2 and total_data_points >= 20:
                return 'medium'
            else:
                return 'low'
                
        except Exception as e:
            logger.error(f"Error calculating confidence: {e}")
            return 'low'
    
    def _interpret_score(self, score: float) -> Dict[str, str]:
        """Interpret the reputation score"""
        try:
            if score >= 80:
                category = 'excellent'
                description = 'Strong positive reputation with minimal negative sentiment'
            elif score >= 70:
                category = 'good'
                description = 'Generally positive reputation with some areas for improvement'
            elif score >= 60:
                category = 'fair'
                description = 'Mixed reputation with both positive and negative aspects'
            elif score >= 40:
                category = 'poor'
                description = 'Predominantly negative reputation requiring attention'
            else:
                category = 'critical'
                description = 'Severely damaged reputation requiring immediate action'
            
            return {
                'category': category,
                'description': description
            }
            
        except Exception as e:
            logger.error(f"Error interpreting score: {e}")
            return {
                'category': 'unknown',
                'description': 'Unable to interpret reputation score'
            }
    
    def _interpret_esg_score(self, esg_score: float) -> Dict[str, str]:
        """Interpret the ESG score"""
        try:
            if esg_score >= 80:
                return {
                    'category': 'leader',
                    'description': 'Strong ESG performance across all dimensions'
                }
            elif esg_score >= 60:
                return {
                    'category': 'good',
                    'description': 'Solid ESG performance with room for improvement'
                }
            elif esg_score >= 40:
                return {
                    'category': 'developing',
                    'description': 'ESG practices need significant improvement'
                }
            else:
                return {
                    'category': 'lagging',
                    'description': 'Poor ESG performance requiring immediate attention'
                }
                
        except Exception as e:
            logger.error(f"Error interpreting ESG score: {e}")
            return {
                'category': 'unknown',
                'description': 'Unable to interpret ESG score'
            }
    
    def _calculate_trend(self, reputation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate reputation trend (placeholder for historical comparison)"""
        try:
            # This would compare with historical data
            # For now, return neutral trend
            return {
                'direction': 'stable',
                'change_percentage': 0,
                'description': 'No historical data available for trend analysis'
            }
            
        except Exception as e:
            logger.error(f"Error calculating trend: {e}")
            return {
                'direction': 'unknown',
                'change_percentage': 0,
                'description': 'Unable to calculate trend'
            }