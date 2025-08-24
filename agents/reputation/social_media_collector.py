"""
Social Media Data Collection Module
Handles gathering social media mentions and discussions for reputation analysis
"""

import os
import sys
import logging
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import tweepy

# Add the agents directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import CONFIG

logger = logging.getLogger(__name__)

class SocialMediaCollector:
    """
    Collects social media mentions and discussions for reputation analysis
    """
    
    def __init__(self):
        """Initialize the Social Media Collector"""
        self.twitter_bearer_token = CONFIG['api_keys']['twitter']
        self.twitter_client = None
        
        if self.twitter_bearer_token:
            try:
                self.twitter_client = tweepy.Client(bearer_token=self.twitter_bearer_token)
                logger.info("Twitter API client initialized successfully")
            except Exception as e:
                logger.warning(f"Failed to initialize Twitter API client: {e}")
        else:
            logger.warning("TWITTER_BEARER_TOKEN not found in environment variables")
    
    def collect_twitter_mentions(self, company_name: str, max_results: int = 100) -> List[Dict[str, Any]]:
        """
        Collect Twitter mentions of a company
        
        Args:
            company_name: Name of the company to search for
            max_results: Maximum number of tweets to collect
            
        Returns:
            List of tweets with metadata
        """
        tweets = []
        
        if not self.twitter_client:
            logger.warning("Twitter client not available, skipping Twitter collection")
            return tweets
        
        try:
            # Search for recent tweets mentioning the company
            query = f'"{company_name}" -is:retweet lang:en'
            
            response = self.twitter_client.search_recent_tweets(
                query=query,
                max_results=min(max_results, 100),  # API limit
                tweet_fields=['created_at', 'author_id', 'public_metrics', 'context_annotations', 'lang'],
                user_fields=['username', 'verified', 'public_metrics']
            )
            
            if response.data:
                for tweet in response.data:
                    formatted_tweet = {
                        'id': tweet.id,
                        'text': tweet.text,
                        'created_at': tweet.created_at.isoformat() if tweet.created_at else '',
                        'author_id': tweet.author_id,
                        'retweet_count': tweet.public_metrics.get('retweet_count', 0) if tweet.public_metrics else 0,
                        'like_count': tweet.public_metrics.get('like_count', 0) if tweet.public_metrics else 0,
                        'reply_count': tweet.public_metrics.get('reply_count', 0) if tweet.public_metrics else 0,
                        'quote_count': tweet.public_metrics.get('quote_count', 0) if tweet.public_metrics else 0,
                        'lang': tweet.lang,
                        'data_source': 'Twitter',
                        'company_name': company_name,
                        'collected_at': datetime.now().isoformat()
                    }
                    tweets.append(formatted_tweet)
            
            logger.info(f"Collected {len(tweets)} Twitter mentions for {company_name}")
            
        except Exception as e:
            logger.error(f"Error collecting Twitter mentions for {company_name}: {e}")
        
        return tweets
    
    def collect_reddit_discussions(self, company_name: str, subreddits: List[str] = None) -> List[Dict[str, Any]]:
        """
        Collect Reddit discussions about a company (using web scraping)
        
        Args:
            company_name: Name of the company to search for
            subreddits: List of subreddits to search in
            
        Returns:
            List of Reddit posts and comments
        """
        discussions = []
        
        if subreddits is None:
            subreddits = ['investing', 'stocks', 'SecurityAnalysis', 'ValueInvesting', 'business']
        
        try:
            # Use Reddit's JSON API (no authentication required for public posts)
            for subreddit in subreddits:
                try:
                    # Search for posts mentioning the company
                    search_url = f"https://www.reddit.com/r/{subreddit}/search.json"
                    params = {
                        'q': company_name,
                        'restrict_sr': 'on',
                        'sort': 'relevance',
                        'limit': 25
                    }
                    
                    headers = {
                        'User-Agent': 'AMAN-ReputationAgent/1.0'
                    }
                    
                    response = requests.get(search_url, params=params, headers=headers)
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        for post in data.get('data', {}).get('children', []):
                            post_data = post.get('data', {})
                            
                            formatted_post = {
                                'id': post_data.get('id', ''),
                                'title': post_data.get('title', ''),
                                'text': post_data.get('selftext', ''),
                                'score': post_data.get('score', 0),
                                'upvote_ratio': post_data.get('upvote_ratio', 0),
                                'num_comments': post_data.get('num_comments', 0),
                                'created_utc': post_data.get('created_utc', 0),
                                'subreddit': subreddit,
                                'author': post_data.get('author', ''),
                                'url': f"https://reddit.com{post_data.get('permalink', '')}",
                                'data_source': 'Reddit',
                                'company_name': company_name,
                                'collected_at': datetime.now().isoformat()
                            }
                            discussions.append(formatted_post)
                    
                    # Rate limiting - be respectful to Reddit's servers
                    import time
                    time.sleep(1)
                
                except Exception as e:
                    logger.warning(f"Error collecting from subreddit {subreddit}: {e}")
                    continue
            
            logger.info(f"Collected {len(discussions)} Reddit discussions for {company_name}")
            
        except Exception as e:
            logger.error(f"Error collecting Reddit discussions for {company_name}: {e}")
        
        return discussions
    
    def collect_linkedin_mentions(self, company_name: str) -> List[Dict[str, Any]]:
        """
        Collect LinkedIn mentions (limited due to API restrictions)
        
        Args:
            company_name: Name of the company to search for
            
        Returns:
            List of LinkedIn mentions (may be empty due to API limitations)
        """
        mentions = []
        
        # LinkedIn has strict API access requirements
        # For now, we'll return empty and log a warning
        logger.warning("LinkedIn data collection requires special API access - skipping for now")
        
        # In a production environment, you would need:
        # 1. LinkedIn Marketing Developer Platform access
        # 2. Proper authentication and permissions
        # 3. Company page access or partnership agreements
        
        return mentions
    
    def collect_youtube_mentions(self, company_name: str, max_results: int = 50) -> List[Dict[str, Any]]:
        """
        Collect YouTube video mentions using web scraping
        
        Args:
            company_name: Name of the company to search for
            max_results: Maximum number of videos to collect
            
        Returns:
            List of YouTube videos mentioning the company
        """
        videos = []
        
        try:
            # Use YouTube's RSS feed for search results (no API key required)
            search_query = company_name.replace(' ', '+')
            
            # Note: This is a simplified approach. In production, you might want to use:
            # 1. YouTube Data API v3 (requires API key)
            # 2. More sophisticated web scraping with selenium
            # 3. Third-party services that aggregate YouTube data
            
            logger.info(f"YouTube data collection would require API key or advanced scraping - placeholder implementation")
            
            # Placeholder for YouTube data structure
            placeholder_video = {
                'id': 'placeholder',
                'title': f'Sample video mentioning {company_name}',
                'description': 'Placeholder description',
                'channel': 'Sample Channel',
                'published_at': datetime.now().isoformat(),
                'view_count': 0,
                'like_count': 0,
                'comment_count': 0,
                'data_source': 'YouTube',
                'company_name': company_name,
                'collected_at': datetime.now().isoformat()
            }
            
            # In a real implementation, this would contain actual scraped data
            # videos.append(placeholder_video)
            
        except Exception as e:
            logger.error(f"Error collecting YouTube mentions for {company_name}: {e}")
        
        return videos
    
    def aggregate_social_mentions(self, company_name: str) -> Dict[str, Any]:
        """
        Aggregate mentions from all social media platforms
        
        Args:
            company_name: Name of the company to search for
            
        Returns:
            Dictionary containing all social media mentions
        """
        try:
            logger.info(f"Collecting social media mentions for {company_name}")
            
            # Collect from all platforms
            twitter_mentions = self.collect_twitter_mentions(company_name)
            reddit_discussions = self.collect_reddit_discussions(company_name)
            linkedin_mentions = self.collect_linkedin_mentions(company_name)
            youtube_mentions = self.collect_youtube_mentions(company_name)
            
            # Aggregate results
            aggregated_data = {
                'company_name': company_name,
                'collection_timestamp': datetime.now().isoformat(),
                'twitter': {
                    'count': len(twitter_mentions),
                    'mentions': twitter_mentions
                },
                'reddit': {
                    'count': len(reddit_discussions),
                    'discussions': reddit_discussions
                },
                'linkedin': {
                    'count': len(linkedin_mentions),
                    'mentions': linkedin_mentions
                },
                'youtube': {
                    'count': len(youtube_mentions),
                    'videos': youtube_mentions
                },
                'total_mentions': len(twitter_mentions) + len(reddit_discussions) + len(linkedin_mentions) + len(youtube_mentions)
            }
            
            logger.info(f"Collected {aggregated_data['total_mentions']} total social media mentions for {company_name}")
            
            return aggregated_data
            
        except Exception as e:
            logger.error(f"Error aggregating social mentions for {company_name}: {e}")
            return {
                'company_name': company_name,
                'collection_timestamp': datetime.now().isoformat(),
                'error': str(e),
                'total_mentions': 0
            }