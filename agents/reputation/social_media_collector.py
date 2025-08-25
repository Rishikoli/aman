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
        logger.info("Social Media Collector initialized with Reddit and Hacker News")
    

    
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
    
    def collect_hackernews_mentions(self, company_name: str, max_results: int = 50) -> List[Dict[str, Any]]:
        """
        Collect Hacker News mentions of a company
        
        Args:
            company_name: Name of the company to search for
            max_results: Maximum number of posts to collect
            
        Returns:
            List of Hacker News posts mentioning the company
        """
        mentions = []
        
        try:
            # Hacker News Algolia API (no authentication required)
            search_url = "https://hn.algolia.com/api/v1/search"
            params = {
                'query': company_name,
                'tags': 'story',
                'hitsPerPage': min(max_results, 50),
                'numericFilters': f'created_at_i>{int((datetime.now() - timedelta(days=30)).timestamp())}'
            }
            
            headers = {
                'User-Agent': 'AMAN-ReputationAgent/1.0'
            }
            
            response = requests.get(search_url, params=params, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                
                for hit in data.get('hits', []):
                    formatted_mention = {
                        'id': hit.get('objectID', ''),
                        'title': hit.get('title', ''),
                        'url': hit.get('url', ''),
                        'hn_url': f"https://news.ycombinator.com/item?id={hit.get('objectID', '')}",
                        'score': hit.get('points', 0),
                        'num_comments': hit.get('num_comments', 0),
                        'author': hit.get('author', ''),
                        'created_at': hit.get('created_at', ''),
                        'tags': hit.get('_tags', []),
                        'data_source': 'HackerNews',
                        'company_name': company_name,
                        'collected_at': datetime.now().isoformat()
                    }
                    mentions.append(formatted_mention)
            
            logger.info(f"Collected {len(mentions)} Hacker News mentions for {company_name}")
            
        except Exception as e:
            logger.error(f"Error collecting Hacker News mentions for {company_name}: {e}")
        
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
            reddit_discussions = self.collect_reddit_discussions(company_name)
            hackernews_mentions = self.collect_hackernews_mentions(company_name)
            linkedin_mentions = self.collect_linkedin_mentions(company_name)
            youtube_mentions = self.collect_youtube_mentions(company_name)
            
            # Aggregate results
            aggregated_data = {
                'company_name': company_name,
                'collection_timestamp': datetime.now().isoformat(),
                'reddit': {
                    'count': len(reddit_discussions),
                    'discussions': reddit_discussions
                },
                'hackernews': {
                    'count': len(hackernews_mentions),
                    'mentions': hackernews_mentions
                },
                'linkedin': {
                    'count': len(linkedin_mentions),
                    'mentions': linkedin_mentions
                },
                'youtube': {
                    'count': len(youtube_mentions),
                    'videos': youtube_mentions
                },
                'total_mentions': len(reddit_discussions) + len(hackernews_mentions) + len(linkedin_mentions) + len(youtube_mentions)
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