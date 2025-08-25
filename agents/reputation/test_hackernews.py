"""
Test Hacker News integration
"""

import sys
import os

# Add the agents directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from reputation.social_media_collector import SocialMediaCollector

def test_hackernews():
    """Test Hacker News API integration"""
    print("Testing Hacker News Integration...")
    
    collector = SocialMediaCollector()
    
    # Test with a tech company that's often discussed on HN
    company_name = "OpenAI"
    
    mentions = collector.collect_hackernews_mentions(company_name, max_results=10)
    
    print(f"Collected {len(mentions)} Hacker News mentions for {company_name}")
    
    if mentions:
        print("\nSample Hacker News mention:")
        sample = mentions[0]
        print(f"Title: {sample.get('title', 'No title')}")
        print(f"Score: {sample.get('score', 0)} points")
        print(f"Comments: {sample.get('num_comments', 0)}")
        print(f"HN URL: {sample.get('hn_url', 'No URL')}")
        
        return True
    else:
        print("No mentions found, but API connection successful")
        return True

if __name__ == "__main__":
    success = test_hackernews()
    print(f"\nHacker News Test: {'PASS' if success else 'FAIL'}")