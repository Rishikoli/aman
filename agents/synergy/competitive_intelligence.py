"""
Competitive Intelligence analyzer for market positioning and competitive analysis.
Combines multiple data sources to provide comprehensive competitive insights for M&A synergies.
"""

import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import pandas as pd
import requests
from google_trends_client import GoogleTrendsClient
from builtwith_client import BuiltWithClient

logger = logging.getLogger(__name__)

class CompetitiveIntelligenceAnalyzer:
    """Analyzer for competitive positioning and market intelligence."""
    
    def __init__(self, builtwith_api_key: Optional[str] = None):
        """
        Initialize the competitive intelligence analyzer.
        
        Args:
            builtwith_api_key: Optional BuiltWith API key for enhanced features
        """
        self.trends_client = GoogleTrendsClient()
        self.builtwith_client = BuiltWithClient(builtwith_api_key)
        
    def analyze_competitive_position(self, 
                                   company1: Dict, 
                                   company2: Dict, 
                                   industry_keywords: List[str]) -> Dict:
        """
        Analyze competitive positioning between two companies.
        
        Args:
            company1: First company data (name, domain, keywords)
            company2: Second company data (name, domain, keywords)
            industry_keywords: Industry-specific keywords for analysis
            
        Returns:
            Dictionary containing competitive analysis results
        """
        try:
            analysis_results = {
                'company1': company1.get('name', 'Company 1'),
                'company2': company2.get('name', 'Company 2'),
                'analysis_timestamp': datetime.now().isoformat(),
                'market_positioning': {},
                'technology_positioning': {},
                'competitive_advantages': {},
                'synergy_opportunities': {},
                'risk_assessment': {}
            }
            
            # Analyze market positioning using Google Trends
            market_analysis = self._analyze_market_positioning(company1, company2, industry_keywords)
            analysis_results['market_positioning'] = market_analysis
            
            # Analyze technology positioning using BuiltWith
            tech_analysis = self._analyze_technology_positioning(company1, company2)
            analysis_results['technology_positioning'] = tech_analysis
            
            # Identify competitive advantages
            competitive_advantages = self._identify_competitive_advantages(market_analysis, tech_analysis)
            analysis_results['competitive_advantages'] = competitive_advantages
            
            # Identify synergy opportunities
            synergy_opportunities = self._identify_synergy_opportunities(market_analysis, tech_analysis)
            analysis_results['synergy_opportunities'] = synergy_opportunities
            
            # Assess integration risks
            risk_assessment = self._assess_integration_risks(market_analysis, tech_analysis)
            analysis_results['risk_assessment'] = risk_assessment
            
            return analysis_results
            
        except Exception as e:
            logger.error(f"Error in competitive analysis: {str(e)}")
            return {
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def _analyze_market_positioning(self, company1: Dict, company2: Dict, industry_keywords: List[str]) -> Dict:
        """Analyze market positioning using trend data."""
        try:
            # Prepare keywords for analysis
            company1_keywords = [company1.get('name', '')] + company1.get('keywords', [])
            company2_keywords = [company2.get('name', '')] + company2.get('keywords', [])
            
            # Get trend data for both companies
            company1_trends = self.trends_client.get_market_interest(company1_keywords[:5])
            company2_trends = self.trends_client.get_market_interest(company2_keywords[:5])
            industry_trends = self.trends_client.get_market_interest(industry_keywords[:5])
            
            # Compare market presence
            market_comparison = self._compare_market_presence(company1_trends, company2_trends)
            
            # Analyze industry positioning
            industry_positioning = self._analyze_industry_positioning(
                company1_trends, company2_trends, industry_trends
            )
            
            return {
                'company1_trends': company1_trends,
                'company2_trends': company2_trends,
                'industry_trends': industry_trends,
                'market_comparison': market_comparison,
                'industry_positioning': industry_positioning
            }
            
        except Exception as e:
            logger.error(f"Error analyzing market positioning: {str(e)}")
            return {'error': str(e)}
    
    def _analyze_technology_positioning(self, company1: Dict, company2: Dict) -> Dict:
        """Analyze technology positioning using tech stack data."""
        try:
            domain1 = company1.get('domain', '')
            domain2 = company2.get('domain', '')
            
            if not domain1 or not domain2:
                return {'error': 'Missing domain information for technology analysis'}
            
            # Get technology stack comparison
            tech_comparison = self.builtwith_client.compare_tech_stacks(domain1, domain2)
            
            # Analyze technology maturity
            tech_maturity = self._analyze_technology_maturity(tech_comparison)
            
            return {
                'tech_stack_comparison': tech_comparison,
                'technology_maturity': tech_maturity
            }
            
        except Exception as e:
            logger.error(f"Error analyzing technology positioning: {str(e)}")
            return {'error': str(e)}
    
    def _compare_market_presence(self, trends1: Dict, trends2: Dict) -> Dict:
        """Compare market presence between two companies."""
        try:
            analysis1 = trends1.get('trend_analysis', {})
            analysis2 = trends2.get('trend_analysis', {})
            
            if not analysis1 or not analysis2:
                return {'error': 'Insufficient trend data for comparison'}
            
            # Calculate average interest scores
            avg_interest1 = self._calculate_average_interest(analysis1)
            avg_interest2 = self._calculate_average_interest(analysis2)
            
            # Determine market leader
            if avg_interest1 > avg_interest2 * 1.2:
                market_leader = 'company1'
                leadership_strength = 'strong'
            elif avg_interest2 > avg_interest1 * 1.2:
                market_leader = 'company2'
                leadership_strength = 'strong'
            elif abs(avg_interest1 - avg_interest2) < 10:
                market_leader = 'balanced'
                leadership_strength = 'equal'
            else:
                market_leader = 'company1' if avg_interest1 > avg_interest2 else 'company2'
                leadership_strength = 'moderate'
            
            return {
                'company1_avg_interest': avg_interest1,
                'company2_avg_interest': avg_interest2,
                'market_leader': market_leader,
                'leadership_strength': leadership_strength,
                'interest_ratio': avg_interest1 / max(avg_interest2, 1)
            }
            
        except Exception as e:
            logger.error(f"Error comparing market presence: {str(e)}")
            return {'error': str(e)}
    
    def _calculate_average_interest(self, trend_analysis: Dict) -> float:
        """Calculate average interest score from trend analysis."""
        interests = []
        for keyword, data in trend_analysis.items():
            if isinstance(data, dict) and 'current_interest' in data:
                interests.append(data['current_interest'])
        
        return sum(interests) / len(interests) if interests else 0
    
    def _analyze_industry_positioning(self, trends1: Dict, trends2: Dict, industry_trends: Dict) -> Dict:
        """Analyze how companies position within their industry."""
        try:
            industry_analysis = industry_trends.get('trend_analysis', {})
            
            if not industry_analysis:
                return {'error': 'No industry trend data available'}
            
            # Calculate industry average interest
            industry_avg = self._calculate_average_interest(industry_analysis)
            
            # Compare companies to industry average
            company1_avg = self._calculate_average_interest(trends1.get('trend_analysis', {}))
            company2_avg = self._calculate_average_interest(trends2.get('trend_analysis', {}))
            
            positioning = {
                'industry_average': industry_avg,
                'company1_vs_industry': company1_avg / max(industry_avg, 1),
                'company2_vs_industry': company2_avg / max(industry_avg, 1),
                'industry_momentum': self._assess_industry_momentum(industry_analysis)
            }
            
            # Classify positioning
            positioning['company1_position'] = self._classify_market_position(positioning['company1_vs_industry'])
            positioning['company2_position'] = self._classify_market_position(positioning['company2_vs_industry'])
            
            return positioning
            
        except Exception as e:
            logger.error(f"Error analyzing industry positioning: {str(e)}")
            return {'error': str(e)}
    
    def _classify_market_position(self, ratio: float) -> str:
        """Classify market position based on industry ratio."""
        if ratio > 1.5:
            return 'market_leader'
        elif ratio > 1.1:
            return 'above_average'
        elif ratio > 0.9:
            return 'average'
        elif ratio > 0.5:
            return 'below_average'
        else:
            return 'niche_player'
    
    def _assess_industry_momentum(self, industry_analysis: Dict) -> str:
        """Assess overall industry momentum."""
        positive_trends = 0
        total_trends = 0
        
        for keyword, data in industry_analysis.items():
            if isinstance(data, dict) and 'market_momentum' in data:
                total_trends += 1
                momentum = data['market_momentum']
                if momentum in ['strong_positive', 'moderate_positive']:
                    positive_trends += 1
        
        if total_trends == 0:
            return 'unknown'
        
        positive_ratio = positive_trends / total_trends
        
        if positive_ratio > 0.7:
            return 'strong_growth'
        elif positive_ratio > 0.5:
            return 'moderate_growth'
        elif positive_ratio > 0.3:
            return 'stable'
        else:
            return 'declining'
    
    def _analyze_technology_maturity(self, tech_comparison: Dict) -> Dict:
        """Analyze technology maturity from comparison data."""
        try:
            stack1 = tech_comparison.get('stack1', {}).get('analysis', {})
            stack2 = tech_comparison.get('stack2', {}).get('analysis', {})
            
            if not stack1 or not stack2:
                return {'error': 'Insufficient technology data'}
            
            maturity_analysis = {
                'company1_maturity': self._assess_tech_maturity(stack1),
                'company2_maturity': self._assess_tech_maturity(stack2),
                'integration_complexity': tech_comparison.get('comparison', {}).get('integration_complexity', 'unknown'),
                'technology_gap': self._calculate_technology_gap(stack1, stack2)
            }
            
            return maturity_analysis
            
        except Exception as e:
            logger.error(f"Error analyzing technology maturity: {str(e)}")
            return {'error': str(e)}
    
    def _assess_tech_maturity(self, tech_analysis: Dict) -> Dict:
        """Assess technology maturity for a single company."""
        modernization = tech_analysis.get('modernization_level', 'unknown')
        cloud_adoption = tech_analysis.get('cloud_adoption', 'unknown')
        complexity = tech_analysis.get('tech_complexity', 'unknown')
        
        # Calculate maturity score
        maturity_score = 0
        
        if modernization == 'modern':
            maturity_score += 40
        elif modernization == 'mixed':
            maturity_score += 20
        
        if cloud_adoption == 'high':
            maturity_score += 30
        elif cloud_adoption == 'medium':
            maturity_score += 15
        
        if complexity == 'high':
            maturity_score += 20
        elif complexity == 'medium':
            maturity_score += 10
        
        # Determine maturity level
        if maturity_score >= 70:
            maturity_level = 'advanced'
        elif maturity_score >= 40:
            maturity_level = 'intermediate'
        else:
            maturity_level = 'basic'
        
        return {
            'maturity_score': maturity_score,
            'maturity_level': maturity_level,
            'modernization_level': modernization,
            'cloud_adoption': cloud_adoption,
            'complexity': complexity
        }
    
    def _calculate_technology_gap(self, tech1: Dict, tech2: Dict) -> Dict:
        """Calculate technology gap between two companies."""
        maturity1 = self._assess_tech_maturity(tech1)
        maturity2 = self._assess_tech_maturity(tech2)
        
        score_gap = abs(maturity1['maturity_score'] - maturity2['maturity_score'])
        
        if score_gap < 10:
            gap_level = 'minimal'
        elif score_gap < 30:
            gap_level = 'moderate'
        else:
            gap_level = 'significant'
        
        return {
            'gap_score': score_gap,
            'gap_level': gap_level,
            'leader': 'company1' if maturity1['maturity_score'] > maturity2['maturity_score'] else 'company2'
        }
    
    def _identify_competitive_advantages(self, market_analysis: Dict, tech_analysis: Dict) -> Dict:
        """Identify competitive advantages for each company."""
        advantages = {
            'company1_advantages': [],
            'company2_advantages': [],
            'shared_strengths': []
        }
        
        try:
            # Market-based advantages
            market_comparison = market_analysis.get('market_comparison', {})
            market_leader = market_comparison.get('market_leader', 'balanced')
            
            if market_leader == 'company1':
                advantages['company1_advantages'].append('Stronger market presence and brand recognition')
            elif market_leader == 'company2':
                advantages['company2_advantages'].append('Stronger market presence and brand recognition')
            else:
                advantages['shared_strengths'].append('Balanced market presence')
            
            # Technology-based advantages
            tech_maturity = tech_analysis.get('technology_maturity', {})
            tech_gap = tech_maturity.get('technology_gap', {})
            
            if tech_gap.get('leader') == 'company1' and tech_gap.get('gap_level') != 'minimal':
                advantages['company1_advantages'].append('More advanced technology infrastructure')
            elif tech_gap.get('leader') == 'company2' and tech_gap.get('gap_level') != 'minimal':
                advantages['company2_advantages'].append('More advanced technology infrastructure')
            
            # Industry positioning advantages
            industry_positioning = market_analysis.get('industry_positioning', {})
            
            company1_position = industry_positioning.get('company1_position', 'average')
            company2_position = industry_positioning.get('company2_position', 'average')
            
            if company1_position in ['market_leader', 'above_average']:
                advantages['company1_advantages'].append(f'Strong industry position ({company1_position})')
            
            if company2_position in ['market_leader', 'above_average']:
                advantages['company2_advantages'].append(f'Strong industry position ({company2_position})')
            
        except Exception as e:
            logger.error(f"Error identifying competitive advantages: {str(e)}")
            advantages['error'] = str(e)
        
        return advantages
    
    def _identify_synergy_opportunities(self, market_analysis: Dict, tech_analysis: Dict) -> Dict:
        """Identify synergy opportunities based on competitive analysis."""
        synergies = {
            'market_synergies': [],
            'technology_synergies': [],
            'strategic_synergies': [],
            'risk_mitigation_synergies': []
        }
        
        try:
            # Market synergies
            market_comparison = market_analysis.get('market_comparison', {})
            if market_comparison.get('market_leader') == 'balanced':
                synergies['market_synergies'].append('Combined market presence creates stronger competitive position')
            
            industry_momentum = market_analysis.get('industry_positioning', {}).get('industry_momentum', '')
            if industry_momentum in ['strong_growth', 'moderate_growth']:
                synergies['market_synergies'].append('Favorable industry trends support revenue synergies')
            
            # Technology synergies
            tech_comparison = tech_analysis.get('tech_stack_comparison', {})
            integration_synergies = tech_comparison.get('synergy_opportunities', [])
            
            for synergy in integration_synergies:
                if synergy.get('potential_savings') in ['high', 'medium']:
                    synergies['technology_synergies'].append(synergy.get('description', ''))
            
            # Strategic synergies
            tech_gap = tech_analysis.get('technology_maturity', {}).get('technology_gap', {})
            if tech_gap.get('gap_level') == 'significant':
                synergies['strategic_synergies'].append('Technology modernization opportunity through knowledge transfer')
            
            # Risk mitigation synergies
            overlap_pct = tech_comparison.get('comparison', {}).get('overlap_percentage', 0)
            if overlap_pct > 50:
                synergies['risk_mitigation_synergies'].append('High technology compatibility reduces integration risk')
            
        except Exception as e:
            logger.error(f"Error identifying synergy opportunities: {str(e)}")
            synergies['error'] = str(e)
        
        return synergies
    
    def _assess_integration_risks(self, market_analysis: Dict, tech_analysis: Dict) -> Dict:
        """Assess integration risks based on competitive analysis."""
        risks = {
            'market_risks': [],
            'technology_risks': [],
            'competitive_risks': [],
            'overall_risk_level': 'medium'
        }
        
        try:
            # Market risks
            market_comparison = market_analysis.get('market_comparison', {})
            leadership_strength = market_comparison.get('leadership_strength', 'equal')
            
            if leadership_strength == 'strong':
                risks['market_risks'].append('Potential brand dilution from merging strong market positions')
            
            # Technology risks
            tech_maturity = tech_analysis.get('technology_maturity', {})
            integration_complexity = tech_maturity.get('integration_complexity', 'medium')
            
            if integration_complexity == 'high':
                risks['technology_risks'].append('High technology integration complexity')
            
            tech_gap = tech_maturity.get('technology_gap', {})
            if tech_gap.get('gap_level') == 'significant':
                risks['technology_risks'].append('Significant technology gap may complicate integration')
            
            # Competitive risks
            industry_momentum = market_analysis.get('industry_positioning', {}).get('industry_momentum', '')
            if industry_momentum == 'declining':
                risks['competitive_risks'].append('Declining industry trends may limit synergy realization')
            
            # Calculate overall risk level
            total_risks = len(risks['market_risks']) + len(risks['technology_risks']) + len(risks['competitive_risks'])
            
            if total_risks >= 4:
                risks['overall_risk_level'] = 'high'
            elif total_risks <= 1:
                risks['overall_risk_level'] = 'low'
            
        except Exception as e:
            logger.error(f"Error assessing integration risks: {str(e)}")
            risks['error'] = str(e)
        
        return risks