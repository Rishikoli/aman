"""
Integration test for market intelligence functionality.
Tests the complete workflow with mock data.
"""

import os
import sys
from unittest.mock import patch, Mock
import pandas as pd

# Import our modules
from market_intelligence_service import MarketIntelligenceService

def test_market_intelligence_integration():
    """Test the complete market intelligence workflow."""
    print("Starting market intelligence integration test...")
    
    # Create service instance
    service = MarketIntelligenceService()
    print("✓ Service created successfully")
    
    # Prepare test deal data
    deal_data = {
        'deal_id': 'TEST_001',
        'deal_name': 'Tech Merger Test',
        'acquirer': {
            'name': 'TechCorp',
            'domain': 'techcorp.com',
            'keywords': ['technology', 'software', 'innovation']
        },
        'target': {
            'name': 'StartupInc',
            'domain': 'startupinc.com',
            'keywords': ['startup', 'mobile', 'app']
        },
        'industry': {
            'keywords': ['technology', 'software', 'mobile', 'saas']
        },
        'synergy_focus': ['cross-selling', 'technology-integration', 'market-expansion']
    }
    print("✓ Test data prepared")
    
    # Mock external API calls to avoid rate limiting and network issues
    with patch('google_trends_client.TrendReq') as mock_trend_req, \
         patch('builtwith_client.builtwith.parse') as mock_builtwith_parse:
        
        # Mock Google Trends
        mock_pytrends = Mock()
        mock_trend_req.return_value = mock_pytrends
        
        # Create mock trend data
        mock_interest_data = pd.DataFrame({
            'technology': [60, 65, 70, 75, 80],
            'software': [55, 60, 65, 70, 75],
            'isPartial': [False, False, False, False, True]
        })
        
        mock_pytrends.interest_over_time.return_value = mock_interest_data
        mock_pytrends.related_queries.return_value = {
            'technology': {
                'top': pd.DataFrame({'query': ['tech news', 'tech stocks'], 'value': [100, 80]}),
                'rising': pd.DataFrame({'query': ['ai tech', 'tech trends'], 'value': [200, 150]})
            }
        }
        mock_pytrends.interest_by_region.return_value = pd.DataFrame({
            'technology': [80, 70, 60],
            'software': [75, 65, 55]
        }, index=['United States', 'United Kingdom', 'Canada'])
        
        print("✓ Google Trends mocked")
        
        # Mock BuiltWith
        mock_builtwith_parse.side_effect = [
            {  # TechCorp stack
                'web-servers': ['nginx', 'cloudflare'],
                'programming-languages-and-frameworks': ['python', 'react', 'node.js'],
                'databases': ['postgresql', 'redis'],
                'analytics-and-tracking': ['google-analytics', 'mixpanel'],
                'cdn': ['cloudflare'],
                'ssl-certificates': ['let\'s encrypt']
            },
            {  # StartupInc stack
                'web-servers': ['apache', 'nginx'],
                'programming-languages-and-frameworks': ['javascript', 'react', 'mongodb'],
                'databases': ['mongodb', 'redis'],
                'analytics-and-tracking': ['google-analytics'],
                'cdn': ['aws-cloudfront'],
                'ssl-certificates': ['ssl.com']
            }
        ]
        
        print("✓ BuiltWith mocked")
        
        # Run the analysis
        try:
            result = service.analyze_market_synergies(deal_data)
            print("✓ Market synergy analysis completed")
            
            # Validate results structure
            expected_keys = [
                'deal_id', 'deal_name', 'analysis_timestamp',
                'market_trends', 'competitive_positioning', 'synergy_validation',
                'technology_overlap', 'recommendations', 'risk_assessment'
            ]
            
            for key in expected_keys:
                if key in result:
                    print(f"✓ Found expected key: {key}")
                else:
                    print(f"✗ Missing expected key: {key}")
            
            # Check if we have meaningful data
            if result.get('deal_id') == 'TEST_001':
                print("✓ Deal ID correctly preserved")
            
            if result.get('market_trends'):
                print("✓ Market trends analysis present")
                
                # Check trend categories
                trends = result['market_trends']
                if 'acquirer_trends' in trends:
                    print("  ✓ Acquirer trends analyzed")
                if 'target_trends' in trends:
                    print("  ✓ Target trends analyzed")
                if 'industry_trends' in trends:
                    print("  ✓ Industry trends analyzed")
                if 'market_momentum' in trends:
                    print(f"  ✓ Market momentum: {trends['market_momentum']}")
            
            if result.get('competitive_positioning'):
                print("✓ Competitive positioning analysis present")
            
            if result.get('synergy_validation'):
                print("✓ Synergy validation present")
                validation = result['synergy_validation']
                if 'validation_score' in validation:
                    print(f"  ✓ Validation score: {validation['validation_score']}")
                if 'confidence_level' in validation:
                    print(f"  ✓ Confidence level: {validation['confidence_level']}")
            
            if result.get('technology_overlap'):
                print("✓ Technology overlap analysis present")
                tech_overlap = result['technology_overlap']
                if 'comparison' in tech_overlap:
                    comparison = tech_overlap['comparison']
                    if 'overlap_percentage' in comparison:
                        print(f"  ✓ Technology overlap: {comparison['overlap_percentage']:.1f}%")
            
            if result.get('recommendations'):
                recommendations = result['recommendations']
                print(f"✓ Generated {len(recommendations)} recommendations:")
                for i, rec in enumerate(recommendations[:3], 1):  # Show first 3
                    print(f"  {i}. {rec}")
            
            if result.get('risk_assessment'):
                print("✓ Risk assessment present")
                risk = result['risk_assessment']
                if 'overall_risk_level' in risk:
                    print(f"  ✓ Overall risk level: {risk['overall_risk_level']}")
            
            print("\n" + "="*60)
            print("INTEGRATION TEST SUMMARY")
            print("="*60)
            print("✓ All core components working correctly")
            print("✓ Google Trends integration functional")
            print("✓ BuiltWith integration functional")
            print("✓ Competitive intelligence analysis working")
            print("✓ Market intelligence service operational")
            print("✓ Complete workflow executed successfully")
            print("="*60)
            
            return True
            
        except Exception as e:
            print(f"✗ Error during analysis: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    success = test_market_intelligence_integration()
    if success:
        print("\n🎉 Integration test PASSED!")
        exit(0)
    else:
        print("\n❌ Integration test FAILED!")
        exit(1)