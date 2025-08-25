"""
Test script for sentiment analysis and reputation scoring functionality
"""

import sys
import os
import json
from datetime import datetime

# Add the agents directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from reputation.sentiment_analyzer import SentimentAnalyzer
from reputation.reputation_scorer import ReputationScorer
from reputation.gemini_reputation_analyzer import GeminiReputationAnalyzer
from reputation.reputation_agent import ReputationAgent

def test_sentiment_analyzer():
    """Test the sentiment analyzer functionality"""
    print("Testing Sentiment Analyzer...")
    
    analyzer = SentimentAnalyzer()
    
    # Test individual text sentiment analysis
    test_texts = [
        "This company has excellent customer service and innovative products!",
        "Terrible experience with their support team, very disappointed.",
        "The company is okay, nothing special but not bad either.",
        "Outstanding leadership and great work environment for employees.",
        "Major data breach concerns and poor security practices."
    ]
    
    print("\nTesting individual text sentiment analysis:")
    for i, text in enumerate(test_texts, 1):
        result = analyzer.analyze_text_sentiment(text)
        print(f"{i}. Text: {text[:50]}...")
        print(f"   Sentiment: {result['sentiment_label']} ({result['combined_sentiment']:.3f})")
        print(f"   Confidence: {result['confidence']:.3f}")
    
    # Test batch sentiment analysis
    batch_results = analyzer.analyze_batch_sentiment(test_texts)
    print(f"\nBatch analysis completed for {len(batch_results)} texts")
    
    # Test news sentiment analysis
    sample_news = [
        {
            'title': 'Company Reports Record Quarterly Profits',
            'description': 'Strong performance across all business segments',
            'source': 'Financial Times'
        },
        {
            'title': 'Regulatory Investigation Launched',
            'description': 'Authorities examining potential compliance violations',
            'source': 'Reuters'
        }
    ]
    
    news_sentiment = analyzer.analyze_news_sentiment(sample_news)
    print(f"\nNews sentiment analysis:")
    print(f"Average sentiment: {news_sentiment.get('average_sentiment', 0):.3f}")
    print(f"Sentiment trend: {news_sentiment.get('sentiment_trend', 'neutral')}")
    
    return True

def test_reputation_scorer():
    """Test the reputation scorer functionality"""
    print("\nTesting Reputation Scorer...")
    
    scorer = ReputationScorer()
    
    # Create sample reputation data
    sample_reputation_data = {
        'company_name': 'Test Company',
        'data_sources': {
            'news': {
                'total_articles': 25,
                'company_articles': [
                    {'title': 'Positive news about company', 'description': 'Great performance'},
                    {'title': 'Company wins award', 'description': 'Excellence in innovation'}
                ]
            },
            'social_media': {
                'total_mentions': 150,
                'twitter': {'count': 75, 'mentions': []},
                'reddit': {'count': 50, 'discussions': []},
                'linkedin': {'count': 25, 'mentions': []}
            },
            'web_sources': {
                'bbb': {'rating': 'A+', 'accredited': True},
                'glassdoor': {'count': 10, 'reviews': []},
                'trustpilot': {'count': 15, 'reviews': []}
            }
        },
        'summary': {
            'total_data_points': 200,
            'success_rate': 0.85
        }
    }
    
    # Test comprehensive scoring
    reputation_scores = scorer.calculate_comprehensive_score(sample_reputation_data)
    
    print(f"Overall reputation score: {reputation_scores.get('overall_score', 0):.2f}")
    print(f"Score interpretation: {reputation_scores.get('interpretation', {}).get('category', 'unknown')}")
    print(f"Confidence level: {reputation_scores.get('confidence_level', 'unknown')}")
    print(f"Score components: {json.dumps(reputation_scores.get('score_components', {}), indent=2)}")
    
    # Test ESG scoring
    esg_scores = scorer.calculate_esg_scores(sample_reputation_data)
    print(f"\nESG Scores:")
    print(f"Overall ESG: {esg_scores.get('overall_esg_score', 0):.2f}")
    print(f"Environmental: {esg_scores.get('environmental_score', 0):.2f}")
    print(f"Social: {esg_scores.get('social_score', 0):.2f}")
    print(f"Governance: {esg_scores.get('governance_score', 0):.2f}")
    
    return True

def test_gemini_analyzer():
    """Test the Gemini AI analyzer functionality"""
    print("\nTesting Gemini Reputation Analyzer...")
    
    analyzer = GeminiReputationAnalyzer()
    
    # Create sample data for AI analysis
    sample_data = {
        'company_name': 'AI Test Company',
        'data_sources': {
            'news': {'total_articles': 20},
            'social_media': {'total_mentions': 100},
            'web_sources': {'total_sources': 5}
        }
    }
    
    # Test reputation summary (will use fallback if no API key)
    reputation_summary = analyzer.analyze_reputation_summary(sample_data)
    print(f"AI reputation summary available: {not reputation_summary.get('error')}")
    
    if not reputation_summary.get('error'):
        print(f"AI sentiment score: {reputation_summary.get('overall_sentiment', 0)}")
        print(f"Key themes: {reputation_summary.get('key_themes', [])}")
    else:
        print(f"AI analysis unavailable: {reputation_summary.get('error', 'Unknown error')}")
    
    # Test ESG assessment
    esg_assessment = analyzer.generate_esg_assessment(sample_data)
    print(f"AI ESG assessment available: {not esg_assessment.get('error')}")
    
    # Test sentiment nuances
    sample_texts = [
        "Great company with innovative products",
        "Poor customer service experience",
        "Average performance, nothing special"
    ]
    
    nuanced_analysis = analyzer.analyze_sentiment_nuances(sample_texts, "Customer feedback")
    print(f"Nuanced sentiment analysis available: {not nuanced_analysis.get('error')}")
    
    return True

def test_reputation_agent():
    """Test the main reputation agent functionality"""
    print("\nTesting Reputation Agent...")
    
    agent = ReputationAgent()
    
    # Test comprehensive analysis (with limited data due to API constraints)
    company_name = "Microsoft"
    
    print(f"Running comprehensive reputation analysis for {company_name}...")
    
    try:
        # Run analysis with AI disabled to avoid API issues in testing
        analysis = agent.analyze_company_reputation(
            company_name=company_name,
            ticker="MSFT",
            industry="technology",
            days_back=7,  # Short period for testing
            include_ai_analysis=False  # Disable AI for testing
        )
        
        print(f"Analysis completed successfully: {not analysis.get('error')}")
        
        if not analysis.get('error'):
            # Print key results
            reputation_scores = analysis.get('reputation_scores', {})
            print(f"Overall reputation score: {reputation_scores.get('overall_score', 0):.2f}")
            print(f"Confidence level: {reputation_scores.get('confidence_level', 'unknown')}")
            
            # Print summary
            summary = analysis.get('summary', {})
            print(f"Overall assessment: {summary.get('overall_assessment', 'unknown')}")
            print(f"Key findings: {len(summary.get('key_findings', []))}")
            
            # Print alerts
            alerts = analysis.get('alerts', [])
            print(f"Total alerts generated: {len(alerts)}")
            
            if alerts:
                print("Sample alerts:")
                for alert in alerts[:3]:  # Show first 3 alerts
                    print(f"  - {alert.get('severity', 'unknown').upper()}: {alert.get('title', 'No title')}")
        
        else:
            print(f"Analysis error: {analysis.get('error')}")
        
        # Test report generation
        if not analysis.get('error'):
            report = agent.generate_reputation_report(analysis)
            print(f"\nReport generated successfully: {not report.get('error')}")
            
            if not report.get('error'):
                key_metrics = report.get('key_metrics', {})
                print(f"Report key metrics:")
                print(f"  - Overall score: {key_metrics.get('overall_reputation_score', 0)}")
                print(f"  - Category: {key_metrics.get('reputation_category', 'unknown')}")
                print(f"  - ESG score: {key_metrics.get('overall_esg_score', 0)}")
                print(f"  - Confidence: {key_metrics.get('confidence_level', 'unknown')}")
        
        return not analysis.get('error')
        
    except Exception as e:
        print(f"Error in reputation agent test: {e}")
        return False

def test_integration():
    """Test integration between all components"""
    print("\nTesting Component Integration...")
    
    try:
        # Test data flow between components
        analyzer = SentimentAnalyzer()
        scorer = ReputationScorer()
        
        # Create sample data that flows through the system
        sample_texts = [
            "Excellent company performance and leadership",
            "Concerns about environmental impact",
            "Strong financial results this quarter"
        ]
        
        # Test sentiment analysis
        sentiment_results = analyzer.analyze_batch_sentiment(sample_texts)
        print(f"Sentiment analysis: {len(sentiment_results)} results")
        
        # Create mock reputation data
        mock_data = {
            'company_name': 'Integration Test Co',
            'data_sources': {
                'news': {'total_articles': len(sentiment_results)},
                'social_media': {'total_mentions': 50}
            },
            'summary': {'total_data_points': 75, 'success_rate': 1.0}
        }
        
        # Test scoring
        scores = scorer.calculate_comprehensive_score(mock_data)
        print(f"Scoring integration: Score = {scores.get('overall_score', 0):.2f}")
        
        return True
        
    except Exception as e:
        print(f"Integration test error: {e}")
        return False

def main():
    """Run all sentiment analysis and reputation scoring tests"""
    print("Starting Sentiment Analysis and Reputation Scoring Tests")
    print("=" * 60)
    
    test_results = []
    
    # Run individual component tests
    test_results.append(("Sentiment Analyzer", test_sentiment_analyzer()))
    test_results.append(("Reputation Scorer", test_reputation_scorer()))
    test_results.append(("Gemini Analyzer", test_gemini_analyzer()))
    test_results.append(("Reputation Agent", test_reputation_agent()))
    test_results.append(("Integration Test", test_integration()))
    
    # Print results
    print("\n" + "=" * 60)
    print("Test Results:")
    print("=" * 60)
    
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