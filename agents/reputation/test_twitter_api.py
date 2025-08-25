"""
Quick test for Twitter API connectivity
"""

import sys
import os

# Add the agents directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from reputation.social_media_collector import SocialMediaCollector

def test_twitter_api():
    """Test Twitter API connection"""
    print("Testing Twitter API Connection...")
    
    collector = SocialMediaCollector()
    
    if not collector.twitter_client:
        print("❌ Twitter client not initialized - check TWITTER_BEARER_TOKEN")
        return False
    
    try:
        # Test with a simple search
        mentions = collector.collect_twitter_mentions("Tesla", max_results=10)
        
        if mentions:
            print(f"✅ Twitter API working! Collected {len(mentions)} mentions")
            print(f"Sample tweet: {mentions[0].get('text', 'No text')[:100]}...")
            return True
        else:
            print("⚠️ Twitter API connected but no results returned")
            return True  # Still counts as working
            
    except Exception as e:
        print(f"❌ Twitter API error: {e}")
        return False

if __name__ == "__main__":
    success = test_twitter_api()
    print(f"\nTwitter API Test: {'PASS' if success else 'FAIL'}")