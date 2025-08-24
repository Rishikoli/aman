"""
Google Trends API client for market interest validation of revenue synergies.
Provides market trend analysis and interest validation for M&A synergy opportunities.
"""

import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import pandas as pd
from pytrends.request import TrendReq
import time
import random

logger = logging.getLogger(__name__)

class GoogleTrendsClient:
    """Client for accessing Google Trends data for market intelligence."""
    
    def __init__(self):
        """Initialize the Google Trends client."""
        self.pytrends = TrendReq(hl='en-US', tz=360)
        self.rate_limit_delay = 1  # Seconds between requests
        
    def _rate_limit(self):
        """Apply rate limiting to avoid being blocked."""
        time.sleep(self.rate_limit_delay + random.uniform(0, 1))
    
    def get_market_interest(self, keywords: List[str], timeframe: str = 'today 12-m') -> Dict:
        """
        Get market interest trends for given keywords.
        
        Args:
            keywords: List of keywords to analyze (max 5)
            timeframe: Time period for analysis (default: last 12 months)
            
        Returns:
            Dictionary containing trend data and analysis
        """
        try:
            # Limit to 5 keywords per request (Google Trends limitation)
            if len(keywords) > 5:
                keywords = keywords[:5]
                logger.warning(f"Limited keywords to first 5: {keywords}")
            
            self._rate_limit()
            
            # Build payload and get interest over time
            self.pytrends.build_payload(keywords, cat=0, timeframe=timeframe, geo='', gprop='')
            
            # Get interest over time
            interest_over_time = self.pytrends.interest_over_time()
            
            # Get related queries
            related_queries = self.pytrends.related_queries()
            
            # Get regional interest
            regional_interest = self.pytrends.interest_by_region(resolution='COUNTRY', inc_low_vol=True, inc_geo_code=False)
            
            # Calculate trend metrics
            trend_analysis = self._analyze_trends(interest_over_time, keywords)
            
            return {
                'keywords': keywords,
                'timeframe': timeframe,
                'interest_over_time': interest_over_time.to_dict() if not interest_over_time.empty else {},
                'regional_interest': regional_interest.to_dict() if not regional_interest.empty else {},
                'related_queries': related_queries,
                'trend_analysis': trend_analysis,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error fetching Google Trends data: {str(e)}")
            return {
                'error': str(e),
                'keywords': keywords,
                'timestamp': datetime.now().isoformat()
            }
    
    def _analyze_trends(self, interest_data: pd.DataFrame, keywords: List[str]) -> Dict:
        """
        Analyze trend data to extract insights.
        
        Args:
            interest_data: DataFrame with interest over time data
            keywords: List of keywords analyzed
            
        Returns:
            Dictionary with trend analysis insights
        """
        if interest_data.empty:
            return {'error': 'No trend data available'}
        
        analysis = {}
        
        for keyword in keywords:
            if keyword in interest_data.columns:
                series = interest_data[keyword]
                
                # Calculate trend metrics
                current_value = series.iloc[-1] if len(series) > 0 else 0
                max_value = series.max()
                min_value = series.min()
                mean_value = series.mean()
                
                # Calculate trend direction (last 4 weeks vs previous 4 weeks)
                if len(series) >= 8:
                    recent_avg = series.iloc[-4:].mean()
                    previous_avg = series.iloc[-8:-4].mean()
                    trend_direction = 'increasing' if recent_avg > previous_avg else 'decreasing'
                    trend_strength = abs(recent_avg - previous_avg) / max(previous_avg, 1)
                else:
                    trend_direction = 'insufficient_data'
                    trend_strength = 0
                
                # Calculate volatility
                volatility = series.std() / max(mean_value, 1)
                
                analysis[keyword] = {
                    'current_interest': current_value,
                    'max_interest': max_value,
                    'min_interest': min_value,
                    'average_interest': mean_value,
                    'trend_direction': trend_direction,
                    'trend_strength': trend_strength,
                    'volatility': volatility,
                    'market_momentum': self._calculate_momentum(series)
                }
        
        return analysis
    
    def _calculate_momentum(self, series: pd.Series) -> str:
        """Calculate market momentum based on trend data."""
        if len(series) < 4:
            return 'insufficient_data'
        
        recent_trend = series.iloc[-4:].mean()
        overall_avg = series.mean()
        
        if recent_trend > overall_avg * 1.2:
            return 'strong_positive'
        elif recent_trend > overall_avg * 1.1:
            return 'moderate_positive'
        elif recent_trend < overall_avg * 0.8:
            return 'strong_negative'
        elif recent_trend < overall_avg * 0.9:
            return 'moderate_negative'
        else:
            return 'stable'
    
    def validate_revenue_synergies(self, synergy_keywords: List[str], company_keywords: List[str]) -> Dict:
        """
        Validate revenue synergy opportunities using market interest data.
        
        Args:
            synergy_keywords: Keywords related to potential synergies
            company_keywords: Keywords related to the companies involved
            
        Returns:
            Dictionary with synergy validation results
        """
        try:
            # Get trends for synergy-related keywords
            synergy_trends = self.get_market_interest(synergy_keywords)
            
            # Get trends for company-related keywords
            company_trends = self.get_market_interest(company_keywords)
            
            # Analyze synergy potential
            validation_results = {
                'synergy_market_interest': synergy_trends,
                'company_market_interest': company_trends,
                'synergy_score': self._calculate_synergy_score(synergy_trends, company_trends),
                'recommendations': self._generate_synergy_recommendations(synergy_trends, company_trends),
                'timestamp': datetime.now().isoformat()
            }
            
            return validation_results
            
        except Exception as e:
            logger.error(f"Error validating revenue synergies: {str(e)}")
            return {
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def _calculate_synergy_score(self, synergy_trends: Dict, company_trends: Dict) -> Dict:
        """Calculate a synergy opportunity score based on market trends."""
        try:
            synergy_analysis = synergy_trends.get('trend_analysis', {})
            company_analysis = company_trends.get('trend_analysis', {})
            
            if not synergy_analysis or not company_analysis:
                return {'score': 0, 'confidence': 'low', 'reason': 'insufficient_data'}
            
            # Calculate average momentum and interest
            synergy_momentum = []
            company_momentum = []
            
            for keyword, data in synergy_analysis.items():
                if isinstance(data, dict) and 'current_interest' in data:
                    synergy_momentum.append(data.get('current_interest', 0))
            
            for keyword, data in company_analysis.items():
                if isinstance(data, dict) and 'current_interest' in data:
                    company_momentum.append(data.get('current_interest', 0))
            
            avg_synergy_interest = sum(synergy_momentum) / len(synergy_momentum) if synergy_momentum else 0
            avg_company_interest = sum(company_momentum) / len(company_momentum) if company_momentum else 0
            
            # Calculate combined score (0-100)
            combined_score = min(100, (avg_synergy_interest + avg_company_interest) / 2)
            
            # Determine confidence level
            if combined_score >= 70:
                confidence = 'high'
            elif combined_score >= 40:
                confidence = 'medium'
            else:
                confidence = 'low'
            
            return {
                'score': combined_score,
                'confidence': confidence,
                'synergy_interest': avg_synergy_interest,
                'company_interest': avg_company_interest
            }
            
        except Exception as e:
            logger.error(f"Error calculating synergy score: {str(e)}")
            return {'score': 0, 'confidence': 'low', 'reason': 'calculation_error'}
    
    def _generate_synergy_recommendations(self, synergy_trends: Dict, company_trends: Dict) -> List[str]:
        """Generate recommendations based on trend analysis."""
        recommendations = []
        
        try:
            synergy_analysis = synergy_trends.get('trend_analysis', {})
            
            for keyword, data in synergy_analysis.items():
                if isinstance(data, dict):
                    momentum = data.get('market_momentum', '')
                    trend_direction = data.get('trend_direction', '')
                    
                    if momentum in ['strong_positive', 'moderate_positive']:
                        recommendations.append(f"Strong market interest in '{keyword}' - favorable for revenue synergies")
                    elif momentum in ['strong_negative', 'moderate_negative']:
                        recommendations.append(f"Declining market interest in '{keyword}' - consider alternative synergy approaches")
                    elif trend_direction == 'increasing':
                        recommendations.append(f"Growing trend for '{keyword}' - potential timing advantage for synergies")
            
            if not recommendations:
                recommendations.append("Market trends are stable - proceed with standard synergy analysis")
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {str(e)}")
            recommendations.append("Unable to generate trend-based recommendations - rely on fundamental analysis")
        
        return recommendations