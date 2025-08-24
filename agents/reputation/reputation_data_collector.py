"""
Reputation Data Collector
Main orchestrator for collecting reputation data from multiple sources
"""

import os
import sys
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import json

# Add the agents directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from reputation.news_collector import NewsCollector
from reputation.social_media_collector import SocialMediaCollector
from reputation.web_scraper import WebScraper

logger = logging.getLogger(__name__)

class ReputationDataCollector:
    """
    Main orchestrator for collecting reputation data from multiple platforms
    """
    
    def __init__(self):
        """Initialize the Reputation Data Collector"""
        self.news_collector = NewsCollector()
        self.social_collector = SocialMediaCollector()
        self.web_scraper = WebScraper()
        
        logger.info("Reputation Data Collector initialized with all collection modules")
    
    def collect_comprehensive_reputation_data(self, 
                                            company_name: str, 
                                            ticker: str = None,
                                            industry: str = None,
                                            days_back: int = 30) -> Dict[str, Any]:
        """
        Collect comprehensive reputation data from all available sources
        
        Args:
            company_name: Name of the company to analyze
            ticker: Stock ticker symbol if available
            industry: Industry sector if known
            days_back: Number of days to look back for news and social media
            
        Returns:
            Dictionary containing all collected reputation data
        """
        try:
            logger.info(f"Starting comprehensive reputation data collection for {company_name}")
            
            # Initialize results structure
            reputation_data = {
                'company_name': company_name,
                'ticker': ticker,
                'industry': industry,
                'collection_metadata': {
                    'start_time': datetime.now().isoformat(),
                    'days_back': days_back,
                    'collector_version': '1.0.0'
                },
                'data_sources': {},
                'summary': {}
            }
            
            # 1. Collect News Data
            logger.info("Collecting news articles...")
            try:
                news_data = self.news_collector.collect_company_news(company_name, days_back)
                industry_news = []
                if industry:
                    industry_news = self.news_collector.collect_industry_news(industry, days_back // 4)
                
                reputation_data['data_sources']['news'] = {
                    'company_articles': news_data,
                    'industry_articles': industry_news,
                    'total_articles': len(news_data) + len(industry_news),
                    'collection_status': 'success'
                }
                
            except Exception as e:
                logger.error(f"Error collecting news data: {e}")
                reputation_data['data_sources']['news'] = {
                    'collection_status': 'error',
                    'error': str(e)
                }
            
            # 2. Collect Social Media Data
            logger.info("Collecting social media mentions...")
            try:
                social_data = self.social_collector.aggregate_social_mentions(company_name)
                reputation_data['data_sources']['social_media'] = social_data
                reputation_data['data_sources']['social_media']['collection_status'] = 'success'
                
            except Exception as e:
                logger.error(f"Error collecting social media data: {e}")
                reputation_data['data_sources']['social_media'] = {
                    'collection_status': 'error',
                    'error': str(e)
                }
            
            # 3. Collect Web Scraping Data
            logger.info("Collecting additional web sources...")
            try:
                web_data = self.web_scraper.aggregate_web_data(company_name, ticker, industry)
                reputation_data['data_sources']['web_sources'] = web_data
                reputation_data['data_sources']['web_sources']['collection_status'] = 'success'
                
            except Exception as e:
                logger.error(f"Error collecting web data: {e}")
                reputation_data['data_sources']['web_sources'] = {
                    'collection_status': 'error',
                    'error': str(e)
                }
            
            # 4. Generate Collection Summary
            reputation_data['summary'] = self._generate_collection_summary(reputation_data)
            reputation_data['collection_metadata']['end_time'] = datetime.now().isoformat()
            
            logger.info(f"Completed reputation data collection for {company_name}")
            
            return reputation_data
            
        except Exception as e:
            logger.error(f"Error in comprehensive reputation data collection: {e}")
            return {
                'company_name': company_name,
                'collection_metadata': {
                    'start_time': datetime.now().isoformat(),
                    'end_time': datetime.now().isoformat(),
                    'error': str(e)
                },
                'error': str(e)
            }
    
    def collect_targeted_reputation_data(self, 
                                       company_name: str,
                                       sources: List[str],
                                       **kwargs) -> Dict[str, Any]:
        """
        Collect reputation data from specific sources only
        
        Args:
            company_name: Name of the company to analyze
            sources: List of sources to collect from ('news', 'social', 'web')
            **kwargs: Additional parameters for specific collectors
            
        Returns:
            Dictionary containing targeted reputation data
        """
        try:
            logger.info(f"Starting targeted reputation data collection for {company_name} from sources: {sources}")
            
            reputation_data = {
                'company_name': company_name,
                'collection_metadata': {
                    'start_time': datetime.now().isoformat(),
                    'targeted_sources': sources,
                    'collector_version': '1.0.0'
                },
                'data_sources': {}
            }
            
            # Collect from specified sources only
            if 'news' in sources:
                try:
                    days_back = kwargs.get('days_back', 30)
                    news_data = self.news_collector.collect_company_news(company_name, days_back)
                    reputation_data['data_sources']['news'] = {
                        'articles': news_data,
                        'count': len(news_data),
                        'collection_status': 'success'
                    }
                except Exception as e:
                    reputation_data['data_sources']['news'] = {
                        'collection_status': 'error',
                        'error': str(e)
                    }
            
            if 'social' in sources:
                try:
                    social_data = self.social_collector.aggregate_social_mentions(company_name)
                    reputation_data['data_sources']['social_media'] = social_data
                except Exception as e:
                    reputation_data['data_sources']['social_media'] = {
                        'collection_status': 'error',
                        'error': str(e)
                    }
            
            if 'web' in sources:
                try:
                    ticker = kwargs.get('ticker')
                    industry = kwargs.get('industry')
                    web_data = self.web_scraper.aggregate_web_data(company_name, ticker, industry)
                    reputation_data['data_sources']['web_sources'] = web_data
                except Exception as e:
                    reputation_data['data_sources']['web_sources'] = {
                        'collection_status': 'error',
                        'error': str(e)
                    }
            
            reputation_data['collection_metadata']['end_time'] = datetime.now().isoformat()
            
            logger.info(f"Completed targeted reputation data collection for {company_name}")
            
            return reputation_data
            
        except Exception as e:
            logger.error(f"Error in targeted reputation data collection: {e}")
            return {
                'company_name': company_name,
                'error': str(e)
            }
    
    def _generate_collection_summary(self, reputation_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a summary of the collected reputation data
        
        Args:
            reputation_data: The collected reputation data
            
        Returns:
            Dictionary containing collection summary
        """
        summary = {
            'total_sources_attempted': 0,
            'successful_sources': 0,
            'failed_sources': 0,
            'total_data_points': 0,
            'data_breakdown': {}
        }
        
        try:
            data_sources = reputation_data.get('data_sources', {})
            
            for source_name, source_data in data_sources.items():
                summary['total_sources_attempted'] += 1
                
                if source_data.get('collection_status') == 'success':
                    summary['successful_sources'] += 1
                else:
                    summary['failed_sources'] += 1
                
                # Count data points by source
                if source_name == 'news':
                    count = source_data.get('total_articles', 0)
                elif source_name == 'social_media':
                    count = source_data.get('total_mentions', 0)
                elif source_name == 'web_sources':
                    count = source_data.get('total_sources', 0)
                else:
                    count = 0
                
                summary['data_breakdown'][source_name] = count
                summary['total_data_points'] += count
            
            # Calculate success rate
            if summary['total_sources_attempted'] > 0:
                summary['success_rate'] = summary['successful_sources'] / summary['total_sources_attempted']
            else:
                summary['success_rate'] = 0
            
        except Exception as e:
            logger.error(f"Error generating collection summary: {e}")
            summary['error'] = str(e)
        
        return summary
    
    def save_reputation_data(self, reputation_data: Dict[str, Any], output_path: str = None) -> str:
        """
        Save collected reputation data to file
        
        Args:
            reputation_data: The collected reputation data
            output_path: Optional custom output path
            
        Returns:
            Path to the saved file
        """
        try:
            if output_path is None:
                company_name = reputation_data.get('company_name', 'unknown')
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"reputation_data_{company_name}_{timestamp}.json"
                output_path = os.path.join('temp', filename)
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Save data as JSON
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(reputation_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Reputation data saved to {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error saving reputation data: {e}")
            raise
    
    def load_reputation_data(self, file_path: str) -> Dict[str, Any]:
        """
        Load previously collected reputation data from file
        
        Args:
            file_path: Path to the saved reputation data file
            
        Returns:
            Dictionary containing the loaded reputation data
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reputation_data = json.load(f)
            
            logger.info(f"Reputation data loaded from {file_path}")
            return reputation_data
            
        except Exception as e:
            logger.error(f"Error loading reputation data from {file_path}: {e}")
            raise