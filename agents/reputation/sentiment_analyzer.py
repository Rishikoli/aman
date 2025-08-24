"""
Sentiment Analysis Engine
Implements VADER sentiment analysis and other sentiment scoring methods
"""

import os
import sys
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import statistics

# Add the agents directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob

logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    """
    Advanced sentiment analysis using multiple methods
    """
    
    def __init__(self):
        """Initialize the Sentiment Analyzer"""
        self.vader_analyzer = SentimentIntensityAnalyzer()
        
        # Sentiment thresholds
        self.sentiment_thresholds = {
            'very_positive': 0.6,
            'positive': 0.2,
            'neutral': -0.2,
            'negative': -0.6,
            'very_negative': -1.0
        }
        
        logger.info("Sentiment Analyzer initialized with VADER and TextBlob")
    
    def analyze_text_sentiment(self, text: str) -> Dict[str, Any]:
        """
        Analyze sentiment of a single text using multiple methods
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary containing sentiment scores and classifications
        """
        if not text or not text.strip():
            return {
                'text': text,
                'vader_scores': {'compound': 0, 'pos': 0, 'neu': 1, 'neg': 0},
                'textblob_polarity': 0,
                'textblob_subjectivity': 0,
                'combined_sentiment': 0,
                'sentiment_label': 'neutral',
                'confidence': 0
            }
        
        try:
            # VADER sentiment analysis
            vader_scores = self.vader_analyzer.polarity_scores(text)
            
            # TextBlob sentiment analysis
            blob = TextBlob(text)
            textblob_polarity = blob.sentiment.polarity
            textblob_subjectivity = blob.sentiment.subjectivity
            
            # Combine scores (weighted average)
            combined_sentiment = (vader_scores['compound'] * 0.7) + (textblob_polarity * 0.3)
            
            # Classify sentiment
            sentiment_label = self._classify_sentiment(combined_sentiment)
            
            # Calculate confidence based on agreement between methods
            confidence = self._calculate_confidence(vader_scores['compound'], textblob_polarity)
            
            return {
                'text': text[:200] + '...' if len(text) > 200 else text,  # Truncate for storage
                'vader_scores': vader_scores,
                'textblob_polarity': textblob_polarity,
                'textblob_subjectivity': textblob_subjectivity,
                'combined_sentiment': combined_sentiment,
                'sentiment_label': sentiment_label,
                'confidence': confidence,
                'analysis_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error analyzing text sentiment: {e}")
            return {
                'text': text[:200] + '...' if len(text) > 200 else text,
                'error': str(e),
                'combined_sentiment': 0,
                'sentiment_label': 'neutral',
                'confidence': 0
            }
    
    def analyze_batch_sentiment(self, texts: List[str]) -> List[Dict[str, Any]]:
        """
        Analyze sentiment for a batch of texts
        
        Args:
            texts: List of texts to analyze
            
        Returns:
            List of sentiment analysis results
        """
        results = []
        
        for text in texts:
            result = self.analyze_text_sentiment(text)
            results.append(result)
        
        logger.info(f"Analyzed sentiment for {len(texts)} texts")
        return results
    
    def analyze_news_sentiment(self, news_articles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze sentiment of news articles
        
        Args:
            news_articles: List of news article dictionaries
            
        Returns:
            Dictionary containing aggregated news sentiment analysis
        """
        if not news_articles:
            return {
                'total_articles': 0,
                'sentiment_distribution': {},
                'average_sentiment': 0,
                'sentiment_trend': 'neutral'
            }
        
        try:
            sentiments = []
            sentiment_details = []
            
            for article in news_articles:
                # Combine title and description for analysis
                text_to_analyze = f"{article.get('title', '')} {article.get('description', '')}"
                
                sentiment_result = self.analyze_text_sentiment(text_to_analyze)
                sentiments.append(sentiment_result['combined_sentiment'])
                
                # Add article metadata to sentiment result
                sentiment_result.update({
                    'article_title': article.get('title', ''),
                    'article_source': article.get('source', ''),
                    'article_url': article.get('url', ''),
                    'published_at': article.get('published_at', '')
                })
                
                sentiment_details.append(sentiment_result)
            
            # Calculate aggregated metrics
            average_sentiment = statistics.mean(sentiments) if sentiments else 0
            sentiment_distribution = self._calculate_sentiment_distribution(sentiments)
            sentiment_trend = self._determine_sentiment_trend(sentiments)
            
            return {
                'total_articles': len(news_articles),
                'sentiment_distribution': sentiment_distribution,
                'average_sentiment': average_sentiment,
                'sentiment_trend': sentiment_trend,
                'sentiment_details': sentiment_details,
                'analysis_metadata': {
                    'analyzer_version': '1.0.0',
                    'analysis_timestamp': datetime.now().isoformat(),
                    'methods_used': ['VADER', 'TextBlob']
                }
            }
            
        except Exception as e:
            logger.error(f"Error analyzing news sentiment: {e}")
            return {
                'total_articles': len(news_articles),
                'error': str(e),
                'average_sentiment': 0,
                'sentiment_trend': 'neutral'
            }
    
    def analyze_social_sentiment(self, social_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze sentiment of social media mentions
        
        Args:
            social_data: Dictionary containing social media data
            
        Returns:
            Dictionary containing aggregated social sentiment analysis
        """
        try:
            platform_sentiments = {}
            all_sentiments = []
            
            # Analyze Twitter mentions
            twitter_data = social_data.get('twitter', {})
            if twitter_data.get('mentions'):
                twitter_sentiments = []
                for mention in twitter_data['mentions']:
                    sentiment = self.analyze_text_sentiment(mention.get('text', ''))
                    twitter_sentiments.append(sentiment['combined_sentiment'])
                
                platform_sentiments['twitter'] = {
                    'count': len(twitter_sentiments),
                    'average_sentiment': statistics.mean(twitter_sentiments) if twitter_sentiments else 0,
                    'sentiment_distribution': self._calculate_sentiment_distribution(twitter_sentiments)
                }
                all_sentiments.extend(twitter_sentiments)
            
            # Analyze Reddit discussions
            reddit_data = social_data.get('reddit', {})
            if reddit_data.get('discussions'):
                reddit_sentiments = []
                for discussion in reddit_data['discussions']:
                    text = f"{discussion.get('title', '')} {discussion.get('text', '')}"
                    sentiment = self.analyze_text_sentiment(text)
                    reddit_sentiments.append(sentiment['combined_sentiment'])
                
                platform_sentiments['reddit'] = {
                    'count': len(reddit_sentiments),
                    'average_sentiment': statistics.mean(reddit_sentiments) if reddit_sentiments else 0,
                    'sentiment_distribution': self._calculate_sentiment_distribution(reddit_sentiments)
                }
                all_sentiments.extend(reddit_sentiments)
            
            # Calculate overall social sentiment
            overall_sentiment = statistics.mean(all_sentiments) if all_sentiments else 0
            overall_distribution = self._calculate_sentiment_distribution(all_sentiments)
            
            return {
                'platform_sentiments': platform_sentiments,
                'overall_sentiment': overall_sentiment,
                'overall_distribution': overall_distribution,
                'total_mentions_analyzed': len(all_sentiments),
                'sentiment_trend': self._determine_sentiment_trend(all_sentiments),
                'analysis_metadata': {
                    'analyzer_version': '1.0.0',
                    'analysis_timestamp': datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            logger.error(f"Error analyzing social sentiment: {e}")
            return {
                'error': str(e),
                'overall_sentiment': 0,
                'total_mentions_analyzed': 0
            }
    
    def analyze_review_sentiment(self, reviews: List[Dict[str, Any]], review_type: str = 'general') -> Dict[str, Any]:
        """
        Analyze sentiment of customer/employee reviews
        
        Args:
            reviews: List of review dictionaries
            review_type: Type of reviews ('customer', 'employee', 'general')
            
        Returns:
            Dictionary containing review sentiment analysis
        """
        if not reviews:
            return {
                'review_type': review_type,
                'total_reviews': 0,
                'average_sentiment': 0,
                'sentiment_distribution': {}
            }
        
        try:
            sentiments = []
            detailed_analysis = []
            
            for review in reviews:
                # Extract review text (different fields for different review types)
                if review_type == 'employee':
                    text = f"{review.get('pros', '')} {review.get('cons', '')} {review.get('advice', '')}"
                else:
                    text = review.get('content', '') or review.get('text', '')
                
                sentiment_result = self.analyze_text_sentiment(text)
                sentiments.append(sentiment_result['combined_sentiment'])
                
                # Add review metadata
                sentiment_result.update({
                    'review_rating': review.get('rating'),
                    'review_date': review.get('date'),
                    'review_source': review.get('data_source')
                })
                
                detailed_analysis.append(sentiment_result)
            
            # Calculate metrics
            average_sentiment = statistics.mean(sentiments) if sentiments else 0
            sentiment_distribution = self._calculate_sentiment_distribution(sentiments)
            
            return {
                'review_type': review_type,
                'total_reviews': len(reviews),
                'average_sentiment': average_sentiment,
                'sentiment_distribution': sentiment_distribution,
                'detailed_analysis': detailed_analysis,
                'sentiment_trend': self._determine_sentiment_trend(sentiments),
                'analysis_metadata': {
                    'analyzer_version': '1.0.0',
                    'analysis_timestamp': datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            logger.error(f"Error analyzing review sentiment: {e}")
            return {
                'review_type': review_type,
                'total_reviews': len(reviews),
                'error': str(e),
                'average_sentiment': 0
            }
    
    def _classify_sentiment(self, score: float) -> str:
        """
        Classify sentiment score into categories
        
        Args:
            score: Sentiment score (-1 to 1)
            
        Returns:
            Sentiment label
        """
        if score >= self.sentiment_thresholds['very_positive']:
            return 'very_positive'
        elif score >= self.sentiment_thresholds['positive']:
            return 'positive'
        elif score >= self.sentiment_thresholds['neutral']:
            return 'neutral'
        elif score >= self.sentiment_thresholds['negative']:
            return 'negative'
        else:
            return 'very_negative'
    
    def _calculate_confidence(self, vader_score: float, textblob_score: float) -> float:
        """
        Calculate confidence based on agreement between sentiment methods
        
        Args:
            vader_score: VADER compound score
            textblob_score: TextBlob polarity score
            
        Returns:
            Confidence score (0 to 1)
        """
        # Calculate agreement between methods
        difference = abs(vader_score - textblob_score)
        
        # Convert difference to confidence (lower difference = higher confidence)
        confidence = max(0, 1 - (difference / 2))
        
        return round(confidence, 3)
    
    def _calculate_sentiment_distribution(self, sentiments: List[float]) -> Dict[str, float]:
        """
        Calculate distribution of sentiments across categories
        
        Args:
            sentiments: List of sentiment scores
            
        Returns:
            Dictionary with sentiment category percentages
        """
        if not sentiments:
            return {}
        
        distribution = {
            'very_positive': 0,
            'positive': 0,
            'neutral': 0,
            'negative': 0,
            'very_negative': 0
        }
        
        for sentiment in sentiments:
            label = self._classify_sentiment(sentiment)
            distribution[label] += 1
        
        # Convert to percentages
        total = len(sentiments)
        for key in distribution:
            distribution[key] = round((distribution[key] / total) * 100, 2)
        
        return distribution
    
    def _determine_sentiment_trend(self, sentiments: List[float]) -> str:
        """
        Determine overall sentiment trend
        
        Args:
            sentiments: List of sentiment scores
            
        Returns:
            Trend description
        """
        if not sentiments:
            return 'neutral'
        
        average = statistics.mean(sentiments)
        
        if average >= 0.3:
            return 'positive'
        elif average <= -0.3:
            return 'negative'
        else:
            return 'neutral'