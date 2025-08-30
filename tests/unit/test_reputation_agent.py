"""
Unit tests for Reputation Agent
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add agents to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'agents'))

from reputation.reputation_agent import ReputationAgent
from reputation.social_media_collector import SocialMediaCollector

class TestReputationAgent:
    
    @pytest.fixture
    def reputation_agent(self, mock_env_vars):
        """Create a Reputation Agent instance for testing"""
        return ReputationAgent()
    
    @pytest.fixture
    def sample_news_data(self):
        """Sample news data for testing"""
        return [
            {
                'title': 'Company XYZ Reports Strong Q3 Earnings',
                'content': 'Company XYZ exceeded expectations with strong revenue growth and positive outlook.',
                'source': 'Financial Times',
                'published_at': '2023-10-15T10:00:00Z',
                'sentiment': 'positive'
            },
            {
                'title': 'Regulatory Investigation into Company XYZ Practices',
                'content': 'Regulators are investigating potential compliance violations at Company XYZ.',
                'source': 'Reuters',
                'published_at': '2023-10-10T14:30:00Z',
                'sentiment': 'negative'
            }
        ]
    
    @pytest.fixture
    def sample_social_data(self):
        """Sample social media data for testing"""
        return [
            {
                'platform': 'twitter',
                'content': 'Great experience with Company XYZ products! Highly recommend.',
                'sentiment_score': 0.8,
                'engagement': 150,
                'timestamp': '2023-10-14T09:00:00Z'
            },
            {
                'platform': 'linkedin',
                'content': 'Concerned about recent layoffs at Company XYZ. Hope they recover.',
                'sentiment_score': -0.3,
                'engagement': 75,
                'timestamp': '2023-10-12T16:45:00Z'
            }
        ]
    
    @pytest.mark.unit
    def test_reputation_agent_initialization(self, reputation_agent):
        """Test Reputation Agent initialization"""
        assert reputation_agent is not None
        assert hasattr(reputation_agent, 'analyze_reputation')
    
    @pytest.mark.unit
    @patch('reputation.reputation_agent.requests.get')
    def test_news_sentiment_analysis(self, mock_get, reputation_agent, sample_news_data):
        """Test news sentiment analysis"""
        # Mock news API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'articles': sample_news_data
        }
        mock_get.return_value = mock_response
        
        sentiment_analysis = reputation_agent.analyze_news_sentiment('Company XYZ')
        
        assert 'overall_sentiment' in sentiment_analysis
        assert 'sentiment_score' in sentiment_analysis
        assert 'article_count' in sentiment_analysis
        assert sentiment_analysis['article_count'] == len(sample_news_data)
        assert -1 <= sentiment_analysis['sentiment_score'] <= 1
    
    @pytest.mark.unit
    def test_social_media_sentiment_analysis(self, reputation_agent, sample_social_data):
        """Test social media sentiment analysis"""
        with patch.object(reputation_agent, 'collect_social_media_data') as mock_collect:
            mock_collect.return_value = sample_social_data
            
            social_sentiment = reputation_agent.analyze_social_sentiment('Company XYZ')
            
            assert 'overall_sentiment' in social_sentiment
            assert 'platform_breakdown' in social_sentiment
            assert 'engagement_weighted_sentiment' in social_sentiment
            
            # Verify platform breakdown
            platforms = [item['platform'] for item in sample_social_data]
            for platform in set(platforms):
                assert platform in social_sentiment['platform_breakdown']
    
    @pytest.mark.unit
    def test_esg_assessment(self, reputation_agent):
        """Test ESG (Environmental, Social, Governance) assessment"""
        company_data = {
            'name': 'Test Corporation',
            'industry': 'Technology',
            'size': 'large',
            'public_reports': ['sustainability_report_2023.pdf', 'diversity_report_2023.pdf']
        }
        
        with patch.object(reputation_agent, 'fetch_esg_data') as mock_esg:
            mock_esg.return_value = {
                'environmental_score': 75,
                'social_score': 80,
                'governance_score': 85,
                'overall_esg_score': 80,
                'esg_rating': 'B+',
                'key_initiatives': ['carbon_neutral_2030', 'diversity_hiring']
            }
            
            esg_assessment = reputation_agent.assess_esg_factors(company_data)
            
            assert 'environmental_score' in esg_assessment
            assert 'social_score' in esg_assessment
            assert 'governance_score' in esg_assessment
            assert 'overall_esg_score' in esg_assessment
            assert 0 <= esg_assessment['overall_esg_score'] <= 100
    
    @pytest.mark.unit
    def test_stakeholder_sentiment_mapping(self, reputation_agent):
        """Test stakeholder sentiment mapping"""
        stakeholder_data = {
            'employees': {'sentiment': 0.6, 'sample_size': 500},
            'customers': {'sentiment': 0.7, 'sample_size': 1000},
            'investors': {'sentiment': 0.4, 'sample_size': 50},
            'regulators': {'sentiment': -0.2, 'sample_size': 10},
            'media': {'sentiment': 0.3, 'sample_size': 200}
        }
        
        with patch.object(reputation_agent, 'collect_stakeholder_data') as mock_stakeholder:
            mock_stakeholder.return_value = stakeholder_data
            
            stakeholder_map = reputation_agent.map_stakeholder_sentiment('Test Corp')
            
            assert 'stakeholder_groups' in stakeholder_map
            assert 'weighted_sentiment' in stakeholder_map
            assert 'risk_areas' in stakeholder_map
            
            # Verify all stakeholder groups are included
            for group in stakeholder_data.keys():
                assert group in stakeholder_map['stakeholder_groups']
    
    @pytest.mark.unit
    def test_reputation_risk_scoring(self, reputation_agent):
        """Test reputation risk scoring algorithm"""
        reputation_data = {
            'news_sentiment': 0.2,
            'social_sentiment': 0.5,
            'esg_score': 75,
            'stakeholder_sentiment': 0.4,
            'recent_controversies': 2,
            'media_coverage_volume': 'high'
        }
        
        risk_score = reputation_agent.calculate_reputation_risk(reputation_data)
        
        assert 'overall_risk_score' in risk_score
        assert 'risk_factors' in risk_score
        assert 'risk_level' in risk_score
        assert 0 <= risk_score['overall_risk_score'] <= 100
        assert risk_score['risk_level'] in ['low', 'medium', 'high', 'critical']
    
    @pytest.mark.unit
    def test_trend_analysis(self, reputation_agent):
        """Test reputation trend analysis over time"""
        historical_data = [
            {'date': '2023-07-01', 'sentiment': 0.6, 'volume': 100},
            {'date': '2023-08-01', 'sentiment': 0.4, 'volume': 150},
            {'date': '2023-09-01', 'sentiment': 0.2, 'volume': 200},
            {'date': '2023-10-01', 'sentiment': 0.5, 'volume': 120}
        ]
        
        trend_analysis = reputation_agent.analyze_reputation_trends(historical_data)
        
        assert 'trend_direction' in trend_analysis
        assert 'volatility' in trend_analysis
        assert 'momentum' in trend_analysis
        assert 'forecast' in trend_analysis
        assert trend_analysis['trend_direction'] in ['improving', 'declining', 'stable']
    
    @pytest.mark.unit
    def test_crisis_detection(self, reputation_agent):
        """Test reputation crisis detection"""
        crisis_indicators = {
            'sentiment_drop': -0.4,  # 40% drop in sentiment
            'volume_spike': 3.0,     # 3x increase in mentions
            'negative_keywords': ['scandal', 'investigation', 'lawsuit'],
            'time_window': '24_hours'
        }
        
        crisis_assessment = reputation_agent.detect_reputation_crisis(crisis_indicators)
        
        assert 'crisis_detected' in crisis_assessment
        assert 'severity_level' in crisis_assessment
        assert 'recommended_actions' in crisis_assessment
        
        if crisis_assessment['crisis_detected']:
            assert crisis_assessment['severity_level'] in ['minor', 'moderate', 'major', 'severe']
            assert len(crisis_assessment['recommended_actions']) > 0

class TestSocialMediaCollector:
    
    @pytest.fixture
    def social_collector(self):
        """Create Social Media Collector for testing"""
        return SocialMediaCollector()
    
    @pytest.mark.unit
    @patch('reputation.social_media_collector.tweepy.API')
    def test_twitter_data_collection(self, mock_twitter_api, social_collector):
        """Test Twitter data collection"""
        # Mock Twitter API response
        mock_tweet = Mock()
        mock_tweet.text = "Great product from @CompanyXYZ! Highly recommend."
        mock_tweet.created_at = "2023-10-15T10:00:00Z"
        mock_tweet.favorite_count = 25
        mock_tweet.retweet_count = 10
        
        mock_twitter_api.return_value.search_tweets.return_value = [mock_tweet]
        
        tweets = social_collector.collect_twitter_mentions('CompanyXYZ', count=10)
        
        assert len(tweets) > 0
        assert 'text' in tweets[0]
        assert 'engagement' in tweets[0]
        assert 'timestamp' in tweets[0]
    
    @pytest.mark.unit
    @patch('reputation.social_media_collector.requests.get')
    def test_reddit_data_collection(self, mock_get, social_collector):
        """Test Reddit data collection"""
        # Mock Reddit API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'data': {
                'children': [
                    {
                        'data': {
                            'title': 'Discussion about CompanyXYZ',
                            'selftext': 'What do you think about their new product?',
                            'score': 15,
                            'num_comments': 8,
                            'created_utc': 1697356800
                        }
                    }
                ]
            }
        }
        mock_get.return_value = mock_response
        
        reddit_posts = social_collector.collect_reddit_mentions('CompanyXYZ')
        
        assert len(reddit_posts) > 0
        assert 'title' in reddit_posts[0]
        assert 'score' in reddit_posts[0]
        assert 'comments' in reddit_posts[0]
    
    @pytest.mark.unit
    def test_sentiment_scoring(self, social_collector):
        """Test sentiment scoring of social media content"""
        test_content = [
            "I love this company's products! Amazing quality.",
            "Terrible customer service. Very disappointed.",
            "The product is okay, nothing special but works fine."
        ]
        
        sentiment_scores = []
        for content in test_content:
            score = social_collector.calculate_sentiment(content)
            sentiment_scores.append(score)
            assert -1 <= score <= 1
        
        # Verify sentiment ordering (positive > neutral > negative)
        assert sentiment_scores[0] > sentiment_scores[2] > sentiment_scores[1]
    
    @pytest.mark.unit
    def test_engagement_weighting(self, social_collector):
        """Test engagement-weighted sentiment calculation"""
        social_posts = [
            {'content': 'Great company!', 'sentiment': 0.8, 'engagement': 100},
            {'content': 'Not impressed', 'sentiment': -0.3, 'engagement': 50},
            {'content': 'Average product', 'sentiment': 0.1, 'engagement': 200}
        ]
        
        weighted_sentiment = social_collector.calculate_engagement_weighted_sentiment(social_posts)
        
        assert -1 <= weighted_sentiment <= 1
        # Should be different from simple average due to engagement weighting
        simple_average = sum(post['sentiment'] for post in social_posts) / len(social_posts)
        assert abs(weighted_sentiment - simple_average) > 0.01  # Should differ by at least 1%