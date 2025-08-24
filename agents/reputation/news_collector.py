"""
News Data Collection Module
Handles gathering news articles from multiple sources for reputation analysis
"""

import os
import sys
import logging
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from newsapi import NewsApiClient

# Add the agents directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import CONFIG

logger = logging.getLogger(__name__)

class NewsCollector:
    """
    Collects news articles from multiple sources for reputation analysis
    """
    
    def __init__(self):
        """Initialize the News Collector"""
        self.news_api_key = CONFIG['api_keys']['news']
        self.newsapi = None
        
        if self.news_api_key:
            try:
                self.newsapi = NewsApiClient(api_key=self.news_api_key)
                logger.info("NewsAPI client initialized successfully")
            except Exception as e:
                logger.warning(f"Failed to initialize NewsAPI client: {e}")
        else:
            logger.warning("NEWS_API_KEY not found in environment variables")
    
    def collect_company_news(self, company_name: str, days_back: int = 30) -> List[Dict[str, Any]]:
        """
        Collect news articles about a specific company
        
        Args:
            company_name: Name of the company to search for
            days_back: Number of days to look back for news
            
        Returns:
            List of news articles with metadata
        """
        articles = []
        
        try:
            # Calculate date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days_back)
            
            # Search for company news using NewsAPI
            if self.newsapi:
                articles.extend(self._fetch_newsapi_articles(company_name, start_date, end_date))
            
            # Add RSS feed sources as fallback
            articles.extend(self._fetch_rss_articles(company_name, days_back))
            
            logger.info(f"Collected {len(articles)} news articles for {company_name}")
            return articles
            
        except Exception as e:
            logger.error(f"Error collecting news for {company_name}: {e}")
            return []
    
    def _fetch_newsapi_articles(self, company_name: str, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """
        Fetch articles from NewsAPI
        
        Args:
            company_name: Company name to search for
            start_date: Start date for search
            end_date: End date for search
            
        Returns:
            List of formatted articles
        """
        articles = []
        
        try:
            # Search everything endpoint
            response = self.newsapi.get_everything(
                q=company_name,
                from_param=start_date.strftime('%Y-%m-%d'),
                to=end_date.strftime('%Y-%m-%d'),
                language='en',
                sort_by='relevancy',
                page_size=100
            )
            
            if response['status'] == 'ok':
                for article in response['articles']:
                    formatted_article = {
                        'title': article.get('title', ''),
                        'description': article.get('description', ''),
                        'content': article.get('content', ''),
                        'url': article.get('url', ''),
                        'source': article.get('source', {}).get('name', 'Unknown'),
                        'published_at': article.get('publishedAt', ''),
                        'author': article.get('author', ''),
                        'data_source': 'NewsAPI',
                        'company_name': company_name,
                        'collected_at': datetime.now().isoformat()
                    }
                    articles.append(formatted_article)
            
        except Exception as e:
            logger.error(f"Error fetching NewsAPI articles: {e}")
        
        return articles
    
    def _fetch_rss_articles(self, company_name: str, days_back: int) -> List[Dict[str, Any]]:
        """
        Fetch articles from RSS feeds as fallback
        
        Args:
            company_name: Company name to search for
            days_back: Number of days to look back
            
        Returns:
            List of formatted articles
        """
        articles = []
        
        # RSS feeds for financial news
        rss_feeds = [
            'https://feeds.reuters.com/reuters/businessNews',
            'https://feeds.bloomberg.com/markets/news.rss',
            'https://rss.cnn.com/rss/money_latest.rss'
        ]
        
        try:
            import feedparser
            
            for feed_url in rss_feeds:
                try:
                    feed = feedparser.parse(feed_url)
                    
                    for entry in feed.entries:
                        # Simple keyword matching for company name
                        title = entry.get('title', '').lower()
                        summary = entry.get('summary', '').lower()
                        
                        if company_name.lower() in title or company_name.lower() in summary:
                            # Check if article is within date range
                            published = entry.get('published_parsed')
                            if published:
                                pub_date = datetime(*published[:6])
                                if pub_date >= datetime.now() - timedelta(days=days_back):
                                    formatted_article = {
                                        'title': entry.get('title', ''),
                                        'description': entry.get('summary', ''),
                                        'content': entry.get('summary', ''),
                                        'url': entry.get('link', ''),
                                        'source': feed.feed.get('title', 'RSS Feed'),
                                        'published_at': entry.get('published', ''),
                                        'author': entry.get('author', ''),
                                        'data_source': 'RSS',
                                        'company_name': company_name,
                                        'collected_at': datetime.now().isoformat()
                                    }
                                    articles.append(formatted_article)
                
                except Exception as e:
                    logger.warning(f"Error parsing RSS feed {feed_url}: {e}")
                    continue
        
        except ImportError:
            logger.warning("feedparser not available, skipping RSS feeds")
        except Exception as e:
            logger.error(f"Error fetching RSS articles: {e}")
        
        return articles
    
    def collect_industry_news(self, industry: str, days_back: int = 7) -> List[Dict[str, Any]]:
        """
        Collect general industry news for context
        
        Args:
            industry: Industry sector to search for
            days_back: Number of days to look back
            
        Returns:
            List of industry news articles
        """
        articles = []
        
        try:
            if self.newsapi:
                end_date = datetime.now()
                start_date = end_date - timedelta(days=days_back)
                
                response = self.newsapi.get_everything(
                    q=industry,
                    from_param=start_date.strftime('%Y-%m-%d'),
                    to=end_date.strftime('%Y-%m-%d'),
                    language='en',
                    sort_by='relevancy',
                    page_size=50
                )
                
                if response['status'] == 'ok':
                    for article in response['articles']:
                        formatted_article = {
                            'title': article.get('title', ''),
                            'description': article.get('description', ''),
                            'content': article.get('content', ''),
                            'url': article.get('url', ''),
                            'source': article.get('source', {}).get('name', 'Unknown'),
                            'published_at': article.get('publishedAt', ''),
                            'author': article.get('author', ''),
                            'data_source': 'NewsAPI',
                            'industry': industry,
                            'collected_at': datetime.now().isoformat()
                        }
                        articles.append(formatted_article)
            
            logger.info(f"Collected {len(articles)} industry news articles for {industry}")
            
        except Exception as e:
            logger.error(f"Error collecting industry news for {industry}: {e}")
        
        return articles