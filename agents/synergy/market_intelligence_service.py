"""
Market Intelligence Service for the Synergy Agent.
Integrates Google Trends, BuiltWith, and competitive analysis for comprehensive market intelligence.
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime
import os
from google_trends_client import GoogleTrendsClient
from builtwith_client import BuiltWithClient
from competitive_intelligence import CompetitiveIntelligenceAnalyzer

logger = logging.getLogger(__name__)

class MarketIntelligenceService:
    """Service for comprehensive market intelligence and competitive analysis."""
    
    def __init__(self):
        """Initialize the market intelligence service."""
        self.trends_client = GoogleTrendsClient()
        self.builtwith_client = BuiltWithClient(
            api_key=os.getenv('BUILTWITH_API_KEY')  # Optional API key
        )
        self.competitive_analyzer = CompetitiveIntelligenceAnalyzer(
            builtwith_api_key=os.getenv('BUILTWITH_API_KEY')
        )
        
    def analyze_market_synergies(self, deal_data: Dict) -> Dict:
        """
        Analyze market synergies for an M&A deal.
        
        Args:
            deal_data: Dictionary containing deal information including:
                - acquirer: Company information (name, domain, keywords)
                - target: Company information (name, domain, keywords)
                - industry: Industry information and keywords
                - synergy_focus: Areas of synergy focus
                
        Returns:
            Dictionary containing comprehensive market intelligence analysis
        """
        try:
            logger.info(f"Starting market synergy analysis for deal: {deal_data.get('deal_name', 'Unknown')}")
            
            analysis_results = {
                'deal_id': deal_data.get('deal_id'),
                'deal_name': deal_data.get('deal_name'),
                'analysis_timestamp': datetime.now().isoformat(),
                'market_trends': {},
                'competitive_positioning': {},
                'synergy_validation': {},
                'technology_overlap': {},
                'recommendations': [],
                'risk_assessment': {}
            }
            
            # Extract company and industry data
            acquirer = deal_data.get('acquirer', {})
            target = deal_data.get('target', {})
            industry_keywords = deal_data.get('industry', {}).get('keywords', [])
            synergy_keywords = deal_data.get('synergy_focus', [])
            
            # 1. Analyze market trends for revenue synergy validation
            market_trends = self._analyze_market_trends(acquirer, target, industry_keywords, synergy_keywords)
            analysis_results['market_trends'] = market_trends
            
            # 2. Perform competitive positioning analysis
            competitive_analysis = self.competitive_analyzer.analyze_competitive_position(
                acquirer, target, industry_keywords
            )
            analysis_results['competitive_positioning'] = competitive_analysis
            
            # 3. Validate synergy opportunities using market data
            synergy_validation = self._validate_synergy_opportunities(
                market_trends, competitive_analysis, synergy_keywords
            )
            analysis_results['synergy_validation'] = synergy_validation
            
            # 4. Analyze technology overlap for cost synergies
            if acquirer.get('domain') and target.get('domain'):
                tech_overlap = self.builtwith_client.compare_tech_stacks(
                    acquirer['domain'], target['domain']
                )
                analysis_results['technology_overlap'] = tech_overlap
            
            # 5. Generate recommendations
            recommendations = self._generate_market_recommendations(
                market_trends, competitive_analysis, synergy_validation
            )
            analysis_results['recommendations'] = recommendations
            
            # 6. Assess market-related risks
            risk_assessment = self._assess_market_risks(
                market_trends, competitive_analysis
            )
            analysis_results['risk_assessment'] = risk_assessment
            
            logger.info("Market synergy analysis completed successfully")
            return analysis_results
            
        except Exception as e:
            logger.error(f"Error in market synergy analysis: {str(e)}")
            return {
                'error': str(e),
                'timestamp': datetime.now().isoformat(),
                'deal_id': deal_data.get('deal_id')
            }
    
    def _analyze_market_trends(self, acquirer: Dict, target: Dict, 
                             industry_keywords: List[str], synergy_keywords: List[str]) -> Dict:
        """Analyze market trends for all relevant keywords."""
        try:
            trends_analysis = {
                'acquirer_trends': {},
                'target_trends': {},
                'industry_trends': {},
                'synergy_trends': {},
                'market_momentum': 'unknown'
            }
            
            # Get trends for acquirer
            acquirer_keywords = [acquirer.get('name', '')] + acquirer.get('keywords', [])
            if acquirer_keywords[0]:  # Only if name is provided
                trends_analysis['acquirer_trends'] = self.trends_client.get_market_interest(
                    acquirer_keywords[:5]
                )
            
            # Get trends for target
            target_keywords = [target.get('name', '')] + target.get('keywords', [])
            if target_keywords[0]:  # Only if name is provided
                trends_analysis['target_trends'] = self.trends_client.get_market_interest(
                    target_keywords[:5]
                )
            
            # Get industry trends
            if industry_keywords:
                trends_analysis['industry_trends'] = self.trends_client.get_market_interest(
                    industry_keywords[:5]
                )
            
            # Get synergy-specific trends
            if synergy_keywords:
                trends_analysis['synergy_trends'] = self.trends_client.get_market_interest(
                    synergy_keywords[:5]
                )
            
            # Assess overall market momentum
            trends_analysis['market_momentum'] = self._assess_overall_momentum(trends_analysis)
            
            return trends_analysis
            
        except Exception as e:
            logger.error(f"Error analyzing market trends: {str(e)}")
            return {'error': str(e)}
    
    def _assess_overall_momentum(self, trends_analysis: Dict) -> str:
        """Assess overall market momentum from all trend data."""
        try:
            positive_signals = 0
            total_signals = 0
            
            # Check each trend category
            for category, trend_data in trends_analysis.items():
                if category == 'market_momentum':
                    continue
                
                if isinstance(trend_data, dict) and 'trend_analysis' in trend_data:
                    analysis = trend_data['trend_analysis']
                    for keyword, data in analysis.items():
                        if isinstance(data, dict) and 'market_momentum' in data:
                            total_signals += 1
                            momentum = data['market_momentum']
                            if momentum in ['strong_positive', 'moderate_positive']:
                                positive_signals += 1
            
            if total_signals == 0:
                return 'insufficient_data'
            
            positive_ratio = positive_signals / total_signals
            
            if positive_ratio >= 0.7:
                return 'strong_positive'
            elif positive_ratio >= 0.5:
                return 'moderate_positive'
            elif positive_ratio >= 0.3:
                return 'stable'
            else:
                return 'negative'
                
        except Exception as e:
            logger.error(f"Error assessing market momentum: {str(e)}")
            return 'unknown'
    
    def _validate_synergy_opportunities(self, market_trends: Dict, 
                                      competitive_analysis: Dict, 
                                      synergy_keywords: List[str]) -> Dict:
        """Validate synergy opportunities using market intelligence."""
        try:
            validation = {
                'revenue_synergies': {},
                'market_expansion': {},
                'cross_selling': {},
                'validation_score': 0,
                'confidence_level': 'low'
            }
            
            # Validate revenue synergies using trend data
            if synergy_keywords and market_trends.get('synergy_trends'):
                synergy_validation = self.trends_client.validate_revenue_synergies(
                    synergy_keywords, 
                    [competitive_analysis.get('company1', ''), competitive_analysis.get('company2', '')]
                )
                validation['revenue_synergies'] = synergy_validation
            
            # Analyze market expansion opportunities
            market_expansion = self._analyze_market_expansion_potential(
                market_trends, competitive_analysis
            )
            validation['market_expansion'] = market_expansion
            
            # Analyze cross-selling potential
            cross_selling = self._analyze_cross_selling_potential(
                market_trends, competitive_analysis
            )
            validation['cross_selling'] = cross_selling
            
            # Calculate overall validation score
            validation_score = self._calculate_validation_score(validation)
            validation['validation_score'] = validation_score
            
            # Determine confidence level
            if validation_score >= 70:
                validation['confidence_level'] = 'high'
            elif validation_score >= 40:
                validation['confidence_level'] = 'medium'
            else:
                validation['confidence_level'] = 'low'
            
            return validation
            
        except Exception as e:
            logger.error(f"Error validating synergy opportunities: {str(e)}")
            return {'error': str(e)}
    
    def _analyze_market_expansion_potential(self, market_trends: Dict, competitive_analysis: Dict) -> Dict:
        """Analyze market expansion potential based on trends and competitive position."""
        try:
            expansion_analysis = {
                'geographic_expansion': 'unknown',
                'product_expansion': 'unknown',
                'market_size_opportunity': 'unknown',
                'expansion_score': 0
            }
            
            # Analyze geographic expansion using regional interest data
            industry_trends = market_trends.get('industry_trends', {})
            regional_interest = industry_trends.get('regional_interest', {})
            
            if regional_interest:
                # Count regions with significant interest
                high_interest_regions = sum(1 for region, interest in regional_interest.items() 
                                          if isinstance(interest, (int, float)) and interest > 50)
                
                if high_interest_regions > 5:
                    expansion_analysis['geographic_expansion'] = 'high_potential'
                    expansion_analysis['expansion_score'] += 30
                elif high_interest_regions > 2:
                    expansion_analysis['geographic_expansion'] = 'moderate_potential'
                    expansion_analysis['expansion_score'] += 15
                else:
                    expansion_analysis['geographic_expansion'] = 'limited_potential'
            
            # Analyze product expansion using trend momentum
            market_momentum = market_trends.get('market_momentum', 'unknown')
            if market_momentum in ['strong_positive', 'moderate_positive']:
                expansion_analysis['product_expansion'] = 'favorable'
                expansion_analysis['expansion_score'] += 25
            elif market_momentum == 'stable':
                expansion_analysis['product_expansion'] = 'moderate'
                expansion_analysis['expansion_score'] += 10
            else:
                expansion_analysis['product_expansion'] = 'challenging'
            
            # Assess market size opportunity
            competitive_positioning = competitive_analysis.get('market_positioning', {})
            industry_positioning = competitive_positioning.get('industry_positioning', {})
            industry_momentum = industry_positioning.get('industry_momentum', 'unknown')
            
            if industry_momentum in ['strong_growth', 'moderate_growth']:
                expansion_analysis['market_size_opportunity'] = 'growing_market'
                expansion_analysis['expansion_score'] += 20
            elif industry_momentum == 'stable':
                expansion_analysis['market_size_opportunity'] = 'stable_market'
                expansion_analysis['expansion_score'] += 10
            else:
                expansion_analysis['market_size_opportunity'] = 'declining_market'
            
            return expansion_analysis
            
        except Exception as e:
            logger.error(f"Error analyzing market expansion potential: {str(e)}")
            return {'error': str(e)}
    
    def _analyze_cross_selling_potential(self, market_trends: Dict, competitive_analysis: Dict) -> Dict:
        """Analyze cross-selling potential based on market data."""
        try:
            cross_selling_analysis = {
                'customer_overlap': 'unknown',
                'product_complementarity': 'unknown',
                'market_receptivity': 'unknown',
                'cross_selling_score': 0
            }
            
            # Analyze customer overlap using market presence data
            market_comparison = competitive_analysis.get('market_positioning', {}).get('market_comparison', {})
            market_leader = market_comparison.get('market_leader', 'balanced')
            
            if market_leader == 'balanced':
                cross_selling_analysis['customer_overlap'] = 'high_potential'
                cross_selling_analysis['cross_selling_score'] += 30
            else:
                cross_selling_analysis['customer_overlap'] = 'moderate_potential'
                cross_selling_analysis['cross_selling_score'] += 15
            
            # Analyze product complementarity using trend correlation
            acquirer_trends = market_trends.get('acquirer_trends', {})
            target_trends = market_trends.get('target_trends', {})
            
            if acquirer_trends and target_trends:
                # Simple correlation analysis based on trend patterns
                correlation_score = self._calculate_trend_correlation(acquirer_trends, target_trends)
                
                if correlation_score > 0.7:
                    cross_selling_analysis['product_complementarity'] = 'highly_complementary'
                    cross_selling_analysis['cross_selling_score'] += 25
                elif correlation_score > 0.4:
                    cross_selling_analysis['product_complementarity'] = 'moderately_complementary'
                    cross_selling_analysis['cross_selling_score'] += 15
                else:
                    cross_selling_analysis['product_complementarity'] = 'limited_complementarity'
                    cross_selling_analysis['cross_selling_score'] += 5
            
            # Assess market receptivity
            market_momentum = market_trends.get('market_momentum', 'unknown')
            if market_momentum in ['strong_positive', 'moderate_positive']:
                cross_selling_analysis['market_receptivity'] = 'high'
                cross_selling_analysis['cross_selling_score'] += 20
            elif market_momentum == 'stable':
                cross_selling_analysis['market_receptivity'] = 'moderate'
                cross_selling_analysis['cross_selling_score'] += 10
            else:
                cross_selling_analysis['market_receptivity'] = 'low'
            
            return cross_selling_analysis
            
        except Exception as e:
            logger.error(f"Error analyzing cross-selling potential: {str(e)}")
            return {'error': str(e)}
    
    def _calculate_trend_correlation(self, trends1: Dict, trends2: Dict) -> float:
        """Calculate simple correlation between two trend datasets."""
        try:
            # Extract interest values from both trend datasets
            values1 = []
            values2 = []
            
            analysis1 = trends1.get('trend_analysis', {})
            analysis2 = trends2.get('trend_analysis', {})
            
            # Get average interest values
            for keyword, data in analysis1.items():
                if isinstance(data, dict) and 'current_interest' in data:
                    values1.append(data['current_interest'])
            
            for keyword, data in analysis2.items():
                if isinstance(data, dict) and 'current_interest' in data:
                    values2.append(data['current_interest'])
            
            if not values1 or not values2:
                return 0.5  # Neutral correlation if no data
            
            # Simple correlation calculation
            avg1 = sum(values1) / len(values1)
            avg2 = sum(values2) / len(values2)
            
            # If both are above average interest (>30), consider them correlated
            if avg1 > 30 and avg2 > 30:
                return 0.8
            elif avg1 > 15 and avg2 > 15:
                return 0.6
            else:
                return 0.3
                
        except Exception as e:
            logger.error(f"Error calculating trend correlation: {str(e)}")
            return 0.5
    
    def _calculate_validation_score(self, validation: Dict) -> float:
        """Calculate overall validation score for synergy opportunities."""
        try:
            total_score = 0
            
            # Revenue synergies score
            revenue_synergies = validation.get('revenue_synergies', {})
            if 'synergy_score' in revenue_synergies:
                synergy_score_data = revenue_synergies['synergy_score']
                if isinstance(synergy_score_data, dict):
                    total_score += synergy_score_data.get('score', 0) * 0.4
            
            # Market expansion score
            market_expansion = validation.get('market_expansion', {})
            expansion_score = market_expansion.get('expansion_score', 0)
            total_score += expansion_score * 0.3
            
            # Cross-selling score
            cross_selling = validation.get('cross_selling', {})
            cross_selling_score = cross_selling.get('cross_selling_score', 0)
            total_score += cross_selling_score * 0.3
            
            return min(100, total_score)  # Cap at 100
            
        except Exception as e:
            logger.error(f"Error calculating validation score: {str(e)}")
            return 0
    
    def _generate_market_recommendations(self, market_trends: Dict, 
                                       competitive_analysis: Dict, 
                                       synergy_validation: Dict) -> List[str]:
        """Generate market-based recommendations for the M&A deal."""
        recommendations = []
        
        try:
            # Market momentum recommendations
            market_momentum = market_trends.get('market_momentum', 'unknown')
            if market_momentum in ['strong_positive', 'moderate_positive']:
                recommendations.append("Favorable market trends support revenue synergy realization")
            elif market_momentum == 'negative':
                recommendations.append("Declining market trends may limit synergy potential - focus on cost synergies")
            
            # Competitive positioning recommendations
            competitive_advantages = competitive_analysis.get('competitive_advantages', {})
            shared_strengths = competitive_advantages.get('shared_strengths', [])
            
            if shared_strengths:
                recommendations.append("Balanced competitive positions enable collaborative market approach")
            
            # Technology recommendations
            tech_positioning = competitive_analysis.get('technology_positioning', {})
            tech_comparison = tech_positioning.get('tech_stack_comparison', {})
            overlap_pct = tech_comparison.get('comparison', {}).get('overlap_percentage', 0)
            
            if overlap_pct > 60:
                recommendations.append("High technology overlap enables rapid integration and cost synergies")
            elif overlap_pct < 30:
                recommendations.append("Low technology overlap suggests modernization opportunity but higher integration risk")
            
            # Synergy validation recommendations
            validation_score = synergy_validation.get('validation_score', 0)
            confidence_level = synergy_validation.get('confidence_level', 'low')
            
            if validation_score > 70 and confidence_level == 'high':
                recommendations.append("Strong market validation supports aggressive synergy targets")
            elif validation_score < 40:
                recommendations.append("Limited market validation suggests conservative synergy estimates")
            
            # Default recommendation if none generated
            if not recommendations:
                recommendations.append("Proceed with standard market analysis and synergy validation")
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {str(e)}")
            recommendations.append("Unable to generate market-based recommendations - conduct manual analysis")
        
        return recommendations
    
    def _assess_market_risks(self, market_trends: Dict, competitive_analysis: Dict) -> Dict:
        """Assess market-related risks for the M&A deal."""
        try:
            risk_assessment = {
                'market_risks': [],
                'competitive_risks': [],
                'technology_risks': [],
                'overall_risk_level': 'medium',
                'risk_score': 50
            }
            
            # Market trend risks
            market_momentum = market_trends.get('market_momentum', 'unknown')
            if market_momentum == 'negative':
                risk_assessment['market_risks'].append("Declining market trends may impact synergy realization")
                risk_assessment['risk_score'] += 20
            
            # Competitive risks
            market_comparison = competitive_analysis.get('market_positioning', {}).get('market_comparison', {})
            leadership_strength = market_comparison.get('leadership_strength', 'equal')
            
            if leadership_strength == 'strong':
                risk_assessment['competitive_risks'].append("Strong market leader position may face integration challenges")
                risk_assessment['risk_score'] += 15
            
            # Technology integration risks
            tech_positioning = competitive_analysis.get('technology_positioning', {})
            integration_complexity = tech_positioning.get('tech_stack_comparison', {}).get('comparison', {}).get('integration_complexity', 'medium')
            
            if integration_complexity == 'high':
                risk_assessment['technology_risks'].append("High technology integration complexity")
                risk_assessment['risk_score'] += 25
            
            # Determine overall risk level
            if risk_assessment['risk_score'] > 80:
                risk_assessment['overall_risk_level'] = 'high'
            elif risk_assessment['risk_score'] < 40:
                risk_assessment['overall_risk_level'] = 'low'
            
            return risk_assessment
            
        except Exception as e:
            logger.error(f"Error assessing market risks: {str(e)}")
            return {
                'error': str(e),
                'overall_risk_level': 'unknown',
                'risk_score': 50
            }