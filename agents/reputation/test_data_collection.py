"""
Test script for reputation data collection functionality
"""

import sys
import os
import json
from datetime import datetime

# Add the agents directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from reputation.reputation_data_collector import ReputationDataCollector
from reputation.news_collector import NewsCollector
from reputation.social_media_collector import SocialMediaCollector
from reputation.web_scraper import WebScraper

def test_news_collector():
    """Test the news collector functionality"""
    print("Testing News Collector...")
    
    collector = NewsCollector()
    
    # Test company news collection
    company_name = "Apple Inc"
    news_articles = collector.collect_company_news(company_name, days_back=7)
    
    print(f"Collected {len(news_articles)} news articles for {company_name}")
    
    if news_articles:
        print("Sample article:")
        print(json.dumps(news_articles[0], indent=2))
    
    # Test industry news collection
    industry_news = collector.collect_industry_news("technology", days_back=3)
    print(f"Collected {len(industry_news)} industry news articles")
    
    return len(news_articles) > 0 or len(industry_news) > 0

def test_social_media_collector():
    """Test the social media collector functionality"""
    print("\nTesting Social Media Collector...")
    
    collector = SocialMediaCollector()
    
    # Test Twitter mentions
    company_name = "Tesla"
    twitter_mentions = collector.collect_twitter_mentions(company_name, max_results=10)
    
    print(f"Collected {len(twitter_mentions)} Twitter mentions for {company_name}")
    
    if twitter_mentions:
        print("Sample tweet:")
        print(json.dumps(twitter_mentions[0], indent=2))
    
    # Test Reddit discussions
    reddit_discussions = collector.collect_reddit_discussions(company_name)
    print(f"Collected {len(reddit_discussions)} Reddit discussions")
    
    # Test aggregated social mentions
    social_data = collector.aggregate_social_mentions(company_name)
    print(f"Total social mentions: {social_data.get('total_mentions', 0)}")
    
    return social_data.get('total_mentions', 0) > 0

def test_web_scraper():
    """Test the web scraper functionality"""
    print("\nTesting Web Scraper...")
    
    scraper = WebScraper()
    
    company_name = "Microsoft"
    ticker = "MSFT"
    industry = "technology"
    
    # Test individual scraping functions
    glassdoor_reviews = scraper.scrape_glassdoor_reviews(company_name)
    print(f"Glassdoor reviews: {len(glassdoor_reviews)}")
    
    trustpilot_reviews = scraper.scrape_trustpilot_reviews(company_name)
    print(f"Trustpilot reviews: {len(trustpilot_reviews)}")
    
    bbb_data = scraper.scrape_bbb_ratings(company_name)
    print(f"BBB data collected: {bool(bbb_data)}")
    
    # Test aggregated web data
    web_data = scraper.aggregate_web_data(company_name, ticker, industry)
    print(f"Web data sources: {web_data.get('total_sources', 0)}")
    
    return bool(web_data)

def test_comprehensive_collection():
    """Test the comprehensive reputation data collection"""
    print("\nTesting Comprehensive Reputation Data Collection...")
    
    collector = ReputationDataCollector()
    
    company_name = "Amazon"
    ticker = "AMZN"
    industry = "e-commerce"
    
    # Test comprehensive collection
    reputation_data = collector.collect_comprehensive_reputation_data(
        company_name=company_name,
        ticker=ticker,
        industry=industry,
        days_back=7
    )
    
    print(f"Collection completed for {company_name}")
    print(f"Summary: {json.dumps(reputation_data.get('summary', {}), indent=2)}")
    
    # Test saving data
    try:
        output_path = collector.save_reputation_data(reputation_data)
        print(f"Data saved to: {output_path}")
        
        # Test loading data
        loaded_data = collector.load_reputation_data(output_path)
        print(f"Data loaded successfully: {loaded_data.get('company_name') == company_name}")
        
        return True
        
    except Exception as e:
        print(f"Error in save/load test: {e}")
        return False

def test_targeted_collection():
    """Test targeted data collection from specific sources"""
    print("\nTesting Targeted Data Collection...")
    
    collector = ReputationDataCollector()
    
    company_name = "Google"
    
    # Test collecting only from news sources
    news_only_data = collector.collect_targeted_reputation_data(
        company_name=company_name,
        sources=['news'],
        days_back=5
    )
    
    print(f"News-only collection: {bool(news_only_data.get('data_sources', {}).get('news'))}")
    
    # Test collecting from multiple specific sources
    multi_source_data = collector.collect_targeted_reputation_data(
        company_name=company_name,
        sources=['news', 'social'],
        days_back=3,
        ticker='GOOGL',
        industry='technology'
    )
    
    print(f"Multi-source collection sources: {list(multi_source_data.get('data_sources', {}).keys())}")
    
    return bool(news_only_data) and bool(multi_source_data)

def main():
    """Run all tests"""
    print("Starting Reputation Data Collection Tests")
    print("=" * 50)
    
    test_results = []
    
    # Run individual component tests
    test_results.append(("News Collector", test_news_collector()))
    test_results.append(("Social Media Collector", test_social_media_collector()))
    test_results.append(("Web Scraper", test_web_scraper()))
    
    # Run integration tests
    test_results.append(("Comprehensive Collection", test_comprehensive_collection()))
    test_results.append(("Targeted Collection", test_targeted_collection()))
    
    # Print results
    print("\n" + "=" * 50)
    print("Test Results:")
    print("=" * 50)
    
    for test_name, result in test_results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name}: {status}")
    
    # Overall result
    all_passed = all(result for _, result in test_results)
    overall_status = "ALL TESTS PASSED" if all_passed else "SOME TESTS FAILED"
    print(f"\nOverall: {overall_status}")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)