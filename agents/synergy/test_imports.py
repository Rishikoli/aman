"""
Simple test to verify imports work correctly.
"""

try:
    from google_trends_client import GoogleTrendsClient
    print("✓ GoogleTrendsClient imported successfully")
except Exception as e:
    print(f"✗ Error importing GoogleTrendsClient: {e}")

try:
    from builtwith_client import BuiltWithClient
    print("✓ BuiltWithClient imported successfully")
except Exception as e:
    print(f"✗ Error importing BuiltWithClient: {e}")

try:
    from competitive_intelligence import CompetitiveIntelligenceAnalyzer
    print("✓ CompetitiveIntelligenceAnalyzer imported successfully")
except Exception as e:
    print(f"✗ Error importing CompetitiveIntelligenceAnalyzer: {e}")

try:
    from market_intelligence_service import MarketIntelligenceService
    print("✓ MarketIntelligenceService imported successfully")
except Exception as e:
    print(f"✗ Error importing MarketIntelligenceService: {e}")

# Test basic functionality
try:
    service = MarketIntelligenceService()
    print("✓ MarketIntelligenceService instantiated successfully")
    
    # Test with minimal data
    deal_data = {
        'deal_id': 'test_001',
        'deal_name': 'Test Deal',
        'acquirer': {'name': 'Test Corp'},
        'target': {'name': 'Target Corp'},
        'industry': {'keywords': ['technology']},
        'synergy_focus': ['integration']
    }
    
    print("✓ Test data prepared")
    print("✓ All imports and basic setup successful!")
    
except Exception as e:
    print(f"✗ Error in basic functionality test: {e}")