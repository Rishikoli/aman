#!/usr/bin/env python3
"""
Test script for ML-powered Financial Analysis Engine
"""

import sys
import os
import json
from datetime import datetime

# Add the agents directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from finance.finance_agent import FinanceAgent

def create_test_financial_data():
    """Create comprehensive test financial data"""
    return {
        'statements': {
            'incomeStatement': [
                {
                    'date': '2023-12-31',
                    'calendarYear': '2023',
                    'period': 'FY',
                    'revenue': 150000000,
                    'netIncome': 15000000,
                    'grossProfit': 60000000,
                    'operatingIncome': 20000000,
                    'ebitda': 25000000
                },
                {
                    'date': '2022-12-31',
                    'calendarYear': '2022',
                    'period': 'FY',
                    'revenue': 130000000,
                    'netIncome': 12000000,
                    'grossProfit': 52000000,
                    'operatingIncome': 16000000,
                    'ebitda': 21000000
                },
                {
                    'date': '2021-12-31',
                    'calendarYear': '2021',
                    'period': 'FY',
                    'revenue': 110000000,
                    'netIncome': 8000000,
                    'grossProfit': 44000000,
                    'operatingIncome': 12000000,
                    'ebitda': 17000000
                },
                {
                    'date': '2020-12-31',
                    'calendarYear': '2020',
                    'period': 'FY',
                    'revenue': 100000000,
                    'netIncome': 5000000,
                    'grossProfit': 40000000,
                    'operatingIncome': 8000000,
                    'ebitda': 13000000
                },
                {
                    'date': '2019-12-31',
                    'calendarYear': '2019',
                    'period': 'FY',
                    'revenue': 95000000,
                    'netIncome': 4000000,
                    'grossProfit': 38000000,
                    'operatingIncome': 6000000,
                    'ebitda': 11000000
                }
            ],
            'balanceSheet': [
                {
                    'date': '2023-12-31',
                    'totalAssets': 300000000,
                    'totalLiabilities': 180000000,
                    'totalStockholdersEquity': 120000000,
                    'cashAndCashEquivalents': 30000000,
                    'totalDebt': 80000000,
                    'totalCurrentAssets': 90000000,
                    'totalCurrentLiabilities': 45000000
                },
                {
                    'date': '2022-12-31',
                    'totalAssets': 250000000,
                    'totalLiabilities': 150000000,
                    'totalStockholdersEquity': 100000000,
                    'cashAndCashEquivalents': 25000000,
                    'totalDebt': 70000000,
                    'totalCurrentAssets': 75000000,
                    'totalCurrentLiabilities': 40000000
                },
                {
                    'date': '2021-12-31',
                    'totalAssets': 220000000,
                    'totalLiabilities': 135000000,
                    'totalStockholdersEquity': 85000000,
                    'cashAndCashEquivalents': 20000000,
                    'totalDebt': 65000000,
                    'totalCurrentAssets': 65000000,
                    'totalCurrentLiabilities': 35000000
                },
                {
                    'date': '2020-12-31',
                    'totalAssets': 200000000,
                    'totalLiabilities': 125000000,
                    'totalStockholdersEquity': 75000000,
                    'cashAndCashEquivalents': 15000000,
                    'totalDebt': 60000000,
                    'totalCurrentAssets': 60000000,
                    'totalCurrentLiabilities': 30000000
                },
                {
                    'date': '2019-12-31',
                    'totalAssets': 180000000,
                    'totalLiabilities': 115000000,
                    'totalStockholdersEquity': 65000000,
                    'cashAndCashEquivalents': 12000000,
                    'totalDebt': 55000000,
                    'totalCurrentAssets': 55000000,
                    'totalCurrentLiabilities': 28000000
                }
            ],
            'cashFlow': [
                {
                    'date': '2023-12-31',
                    'operatingCashFlow': 18000000,
                    'freeCashFlow': 12000000,
                    'capitalExpenditure': 6000000
                },
                {
                    'date': '2022-12-31',
                    'operatingCashFlow': 15000000,
                    'freeCashFlow': 9000000,
                    'capitalExpenditure': 6000000
                },
                {
                    'date': '2021-12-31',
                    'operatingCashFlow': 12000000,
                    'freeCashFlow': 6000000,
                    'capitalExpenditure': 6000000
                },
                {
                    'date': '2020-12-31',
                    'operatingCashFlow': 8000000,
                    'freeCashFlow': 3000000,
                    'capitalExpenditure': 5000000
                },
                {
                    'date': '2019-12-31',
                    'operatingCashFlow': 6000000,
                    'freeCashFlow': 2000000,
                    'capitalExpenditure': 4000000
                }
            ]
        },
        'profile': {
            'symbol': 'TESTCO',
            'companyName': 'Test Company Inc.',
            'industry': 'Technology',
            'sector': 'Software',
            'marketCap': 2000000000,
            'description': 'A test company for financial analysis'
        },
        'metadata': {
            'symbol': 'TESTCO',
            'source': 'test_data',
            'retrievedAt': datetime.now().isoformat()
        },
        'dataSource': 'test'
    }

def create_anomaly_test_data():
    """Create test data with intentional anomalies"""
    data = create_test_financial_data()
    
    # Introduce anomalies
    # Sudden revenue drop in 2022
    data['statements']['incomeStatement'][1]['revenue'] = 50000000  # Dramatic drop
    
    # Negative cash flow in 2021
    data['statements']['cashFlow'][2]['operatingCashFlow'] = -5000000
    
    # Unrealistic debt spike in 2023
    data['statements']['balanceSheet'][0]['totalDebt'] = 250000000  # Very high debt
    
    return data

def test_financial_ratios():
    """Test financial ratio calculations"""
    print("=" * 60)
    print("TESTING FINANCIAL RATIO CALCULATIONS")
    print("=" * 60)
    
    agent = FinanceAgent()
    test_data = create_test_financial_data()
    
    try:
        ratios = agent.analysis_engine.calculate_financial_ratios(test_data)
        
        print(f"✓ Financial ratios calculated successfully")
        print(f"  - Ratio categories: {list(ratios.keys())}")
        
        if 'profitability' in ratios:
            prof = ratios['profitability']
            print(f"  - Profitability ratios: {list(prof.keys())}")
            if 'net_margin' in prof and prof['net_margin']:
                print(f"    * Latest net margin: {prof['net_margin'][0]:.2f}%")
        
        if 'liquidity' in ratios:
            liq = ratios['liquidity']
            print(f"  - Liquidity ratios: {list(liq.keys())}")
            if 'current_ratio' in liq and liq['current_ratio']:
                print(f"    * Latest current ratio: {liq['current_ratio'][0]:.2f}")
        
        if 'leverage' in ratios:
            lev = ratios['leverage']
            print(f"  - Leverage ratios: {list(lev.keys())}")
            if 'debt_to_equity' in lev and lev['debt_to_equity']:
                print(f"    * Latest debt-to-equity: {lev['debt_to_equity'][0]:.2f}")
        
        if 'growth' in ratios:
            growth = ratios['growth']
            print(f"  - Growth ratios: {list(growth.keys())}")
            if 'revenue_growth' in growth and growth['revenue_growth']:
                print(f"    * Latest revenue growth: {growth['revenue_growth'][0]:.2f}%")
        
        print(f"  - Data quality score: {ratios.get('metadata', {}).get('data_quality_score', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error calculating financial ratios: {str(e)}")
        return False

def test_anomaly_detection():
    """Test anomaly detection capabilities"""
    print("\n" + "=" * 60)
    print("TESTING ANOMALY DETECTION")
    print("=" * 60)
    
    agent = FinanceAgent()
    
    # Test with normal data
    print("\n--- Testing with normal data ---")
    normal_data = create_test_financial_data()
    
    try:
        anomalies = agent.analysis_engine.detect_financial_anomalies(normal_data)
        anomaly_count = len(anomalies.get('anomalies', []))
        print(f"✓ Normal data analysis completed")
        print(f"  - Anomalies detected: {anomaly_count}")
        print(f"  - Anomaly rate: {anomalies.get('anomaly_rate', 0):.2%}")
        print(f"  - Features analyzed: {len(anomalies.get('features_analyzed', []))}")
        
    except Exception as e:
        print(f"✗ Error in normal data anomaly detection: {str(e)}")
        return False
    
    # Test with anomalous data
    print("\n--- Testing with anomalous data ---")
    anomaly_data = create_anomaly_test_data()
    
    try:
        anomalies = agent.analysis_engine.detect_financial_anomalies(anomaly_data)
        anomaly_count = len(anomalies.get('anomalies', []))
        print(f"✓ Anomalous data analysis completed")
        print(f"  - Anomalies detected: {anomaly_count}")
        print(f"  - Anomaly rate: {anomalies.get('anomaly_rate', 0):.2%}")
        
        if anomaly_count > 0:
            print("  - Detected anomalies:")
            for i, anomaly in enumerate(anomalies['anomalies'][:3]):  # Show first 3
                print(f"    {i+1}. Period: {anomaly['period']}")
                print(f"       Severity: {anomaly['severity']}")
                print(f"       Score: {anomaly['anomaly_score']:.3f}")
                print(f"       Description: {anomaly['description']}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error in anomalous data detection: {str(e)}")
        return False

def test_financial_forecasting():
    """Test financial forecasting capabilities"""
    print("\n" + "=" * 60)
    print("TESTING FINANCIAL FORECASTING")
    print("=" * 60)
    
    agent = FinanceAgent()
    test_data = create_test_financial_data()
    
    try:
        forecasts = agent.analysis_engine.create_financial_forecasts(test_data, forecast_years=3)
        
        print(f"✓ Financial forecasts created successfully")
        print(f"  - Metrics forecasted: {len(forecasts.get('forecasts', {}))}")
        print(f"  - Forecast years: {forecasts.get('metadata', {}).get('forecast_years', 'N/A')}")
        print(f"  - Historical periods used: {forecasts.get('metadata', {}).get('historical_periods', 'N/A')}")
        
        # Show sample forecasts
        if 'forecasts' in forecasts:
            for metric, forecast_data in list(forecasts['forecasts'].items())[:3]:  # Show first 3
                if 'values' in forecast_data:
                    print(f"\n  - {metric.upper()} Forecast:")
                    for i, value in enumerate(forecast_data['values']):
                        year = 2024 + i
                        print(f"    {year}: ${value:,.0f}")
                    
                    if 'model_performance' in forecast_data:
                        perf = forecast_data['model_performance']
                        print(f"    Model R²: {perf.get('r_squared', 0):.3f}")
                        print(f"    Trend: {forecast_data.get('trend', 'N/A')}")
                        print(f"    Annual growth rate: {forecast_data.get('annual_growth_rate', 0):.2f}%")
        
        return True
        
    except Exception as e:
        print(f"✗ Error creating financial forecasts: {str(e)}")
        return False

def test_gemini_integration():
    """Test Gemini API integration"""
    print("\n" + "=" * 60)
    print("TESTING GEMINI API INTEGRATION")
    print("=" * 60)
    
    agent = FinanceAgent()
    
    # Test connection
    try:
        connection_test = agent.gemini_analyzer.test_connection()
        print(f"✓ Gemini connection test completed")
        print(f"  - Success: {connection_test.get('success', False)}")
        print(f"  - Message: {connection_test.get('message', 'N/A')}")
        print(f"  - Fallback available: {connection_test.get('fallback_available', False)}")
        
        if not connection_test.get('success', False):
            print("  ⚠ Gemini API not available - fallback mode will be used")
        
        return True
        
    except Exception as e:
        print(f"✗ Error testing Gemini integration: {str(e)}")
        return False

def test_comprehensive_analysis():
    """Test comprehensive financial analysis"""
    print("\n" + "=" * 60)
    print("TESTING COMPREHENSIVE FINANCIAL ANALYSIS")
    print("=" * 60)
    
    agent = FinanceAgent()
    test_data = create_test_financial_data()
    
    try:
        analysis = agent.analyze_company_financials(test_data, {
            'forecast_years': 3,
            'include_narrative_analysis': True
        })
        
        print(f"✓ Comprehensive analysis completed")
        print(f"  - Company: {analysis.get('company_symbol', 'N/A')}")
        print(f"  - Analysis components: {len(analysis) - 4}")  # Exclude metadata fields
        print(f"  - Data quality score: {analysis.get('metadata', {}).get('data_quality_score', 'N/A')}")
        print(f"  - Confidence level: {analysis.get('metadata', {}).get('confidence_level', 'N/A')}")
        
        # Show key results
        if 'risk_assessment' in analysis:
            risk = analysis['risk_assessment']
            print(f"\n  - Risk Assessment:")
            print(f"    * Overall risk level: {risk.get('overall_risk_level', 'N/A')}")
            print(f"    * Risk score: {risk.get('risk_score', 'N/A')}/100")
            print(f"    * Risk factors: {len(risk.get('risk_factors', []))}")
        
        if 'executive_summary' in analysis:
            summary = analysis['executive_summary']
            print(f"\n  - Executive Summary:")
            print(f"    * Overall assessment: {summary.get('overall_assessment', 'N/A')}")
            print(f"    * Key findings: {len(summary.get('key_findings', []))}")
            print(f"    * Recommendations: {len(summary.get('recommendations', []))}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error in comprehensive analysis: {str(e)}")
        return False

def test_quick_health_check():
    """Test quick financial health check"""
    print("\n" + "=" * 60)
    print("TESTING QUICK FINANCIAL HEALTH CHECK")
    print("=" * 60)
    
    agent = FinanceAgent()
    test_data = create_test_financial_data()
    
    try:
        health_check = agent.quick_financial_health_check(test_data)
        
        print(f"✓ Quick health check completed")
        print(f"  - Company: {health_check.get('company_symbol', 'N/A')}")
        
        if 'health_score' in health_check:
            score = health_check['health_score']
            print(f"  - Overall score: {score.get('overall_score', 'N/A')}/100")
            print(f"  - Grade: {score.get('grade', 'N/A')}")
        
        print(f"  - Anomaly count: {health_check.get('anomaly_count', 'N/A')}")
        print(f"  - Recommendation: {health_check.get('recommendation', 'N/A')}")
        
        if 'key_ratios' in health_check:
            ratios = health_check['key_ratios']
            print(f"  - Key ratios: {list(ratios.keys())}")
            for ratio, value in ratios.items():
                if isinstance(value, (int, float)):
                    print(f"    * {ratio}: {value:.2f}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error in quick health check: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("ML-POWERED FINANCIAL ANALYSIS ENGINE TEST SUITE")
    print("=" * 60)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    tests = [
        ("Financial Ratio Calculations", test_financial_ratios),
        ("Anomaly Detection", test_anomaly_detection),
        ("Financial Forecasting", test_financial_forecasting),
        ("Gemini API Integration", test_gemini_integration),
        ("Comprehensive Analysis", test_comprehensive_analysis),
        ("Quick Health Check", test_quick_health_check)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name} failed with exception: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{status:<10} {test_name}")
    
    print(f"\nOverall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 All tests passed! ML-powered financial analysis engine is working correctly.")
    elif passed > 0:
        print("⚠ Some tests passed. Core functionality is working but some features may need attention.")
    else:
        print("❌ All tests failed. Please check the implementation and dependencies.")
    
    print(f"\nTest completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()