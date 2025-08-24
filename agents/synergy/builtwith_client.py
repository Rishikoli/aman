"""
BuiltWith API client for website traffic and tech stack overlap analysis.
Provides technology stack intelligence for M&A synergy identification.
"""

import logging
from typing import Dict, List, Optional, Set
import requests
import builtwith
from datetime import datetime
import time

logger = logging.getLogger(__name__)

class BuiltWithClient:
    """Client for accessing BuiltWith technology profiling data."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the BuiltWith client.
        
        Args:
            api_key: Optional BuiltWith API key for enhanced features
        """
        self.api_key = api_key
        self.rate_limit_delay = 2  # Seconds between requests for free tier
        
    def _rate_limit(self):
        """Apply rate limiting to avoid being blocked."""
        time.sleep(self.rate_limit_delay)
    
    def get_tech_stack(self, domain: str) -> Dict:
        """
        Get technology stack information for a domain.
        
        Args:
            domain: Domain name to analyze (e.g., 'example.com')
            
        Returns:
            Dictionary containing technology stack information
        """
        try:
            self._rate_limit()
            
            # Use builtwith library for basic tech stack detection
            tech_data = builtwith.parse(f"https://{domain}")
            
            # Organize technology data by categories
            organized_tech = self._organize_technologies(tech_data)
            
            return {
                'domain': domain,
                'technologies': organized_tech,
                'raw_data': tech_data,
                'analysis': self._analyze_tech_stack(organized_tech),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error fetching tech stack for {domain}: {str(e)}")
            return {
                'domain': domain,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def _organize_technologies(self, tech_data: Dict) -> Dict:
        """
        Organize raw technology data into categories.
        
        Args:
            tech_data: Raw technology data from BuiltWith
            
        Returns:
            Organized technology data by category
        """
        organized = {
            'web_servers': [],
            'programming_languages': [],
            'frameworks': [],
            'databases': [],
            'analytics': [],
            'advertising': [],
            'cdn': [],
            'cms': [],
            'ecommerce': [],
            'payment_processors': [],
            'security': [],
            'hosting': [],
            'other': []
        }
        
        # Category mappings for common technologies
        category_mappings = {
            'web-servers': 'web_servers',
            'programming-languages-and-frameworks': 'programming_languages',
            'javascript-frameworks': 'frameworks',
            'databases': 'databases',
            'analytics-and-tracking': 'analytics',
            'advertising-networks': 'advertising',
            'cdn': 'cdn',
            'cms': 'cms',
            'ecommerce': 'ecommerce',
            'payment-processors': 'payment_processors',
            'ssl-certificates': 'security',
            'hosting': 'hosting'
        }
        
        for category, technologies in tech_data.items():
            mapped_category = category_mappings.get(category, 'other')
            if isinstance(technologies, list):
                organized[mapped_category].extend(technologies)
            else:
                organized[mapped_category].append(technologies)
        
        return organized
    
    def _analyze_tech_stack(self, tech_stack: Dict) -> Dict:
        """
        Analyze technology stack for insights.
        
        Args:
            tech_stack: Organized technology stack data
            
        Returns:
            Analysis insights about the technology stack
        """
        analysis = {
            'tech_complexity': 'low',
            'modernization_level': 'unknown',
            'cloud_adoption': 'unknown',
            'security_posture': 'unknown',
            'integration_difficulty': 'medium',
            'key_technologies': [],
            'potential_synergies': []
        }
        
        try:
            # Count total technologies
            total_tech_count = sum(len(techs) for techs in tech_stack.values() if isinstance(techs, list))
            
            # Determine complexity
            if total_tech_count > 20:
                analysis['tech_complexity'] = 'high'
            elif total_tech_count > 10:
                analysis['tech_complexity'] = 'medium'
            
            # Analyze modernization level
            modern_indicators = ['react', 'angular', 'vue', 'node.js', 'python', 'docker', 'kubernetes']
            legacy_indicators = ['jquery', 'php', 'asp.net', 'coldfusion']
            
            modern_count = self._count_tech_indicators(tech_stack, modern_indicators)
            legacy_count = self._count_tech_indicators(tech_stack, legacy_indicators)
            
            if modern_count > legacy_count:
                analysis['modernization_level'] = 'modern'
            elif legacy_count > modern_count:
                analysis['modernization_level'] = 'legacy'
            else:
                analysis['modernization_level'] = 'mixed'
            
            # Analyze cloud adoption
            cloud_indicators = ['aws', 'azure', 'google cloud', 'cloudflare', 'heroku']
            cloud_count = self._count_tech_indicators(tech_stack, cloud_indicators)
            
            if cloud_count > 0:
                analysis['cloud_adoption'] = 'high' if cloud_count > 2 else 'medium'
            else:
                analysis['cloud_adoption'] = 'low'
            
            # Analyze security posture
            security_indicators = ['ssl', 'https', 'cloudflare', 'security headers']
            security_count = self._count_tech_indicators(tech_stack, security_indicators)
            
            if security_count > 2:
                analysis['security_posture'] = 'strong'
            elif security_count > 0:
                analysis['security_posture'] = 'moderate'
            else:
                analysis['security_posture'] = 'weak'
            
            # Determine integration difficulty
            if analysis['tech_complexity'] == 'high' and analysis['modernization_level'] == 'legacy':
                analysis['integration_difficulty'] = 'high'
            elif analysis['modernization_level'] == 'modern' and analysis['cloud_adoption'] == 'high':
                analysis['integration_difficulty'] = 'low'
            
            # Extract key technologies
            analysis['key_technologies'] = self._extract_key_technologies(tech_stack)
            
            # Identify potential synergies
            analysis['potential_synergies'] = self._identify_tech_synergies(tech_stack)
            
        except Exception as e:
            logger.error(f"Error analyzing tech stack: {str(e)}")
            analysis['error'] = str(e)
        
        return analysis
    
    def _count_tech_indicators(self, tech_stack: Dict, indicators: List[str]) -> int:
        """Count how many indicator technologies are present."""
        count = 0
        for category, technologies in tech_stack.items():
            if isinstance(technologies, list):
                for tech in technologies:
                    tech_name = str(tech).lower() if tech else ''
                    for indicator in indicators:
                        if indicator.lower() in tech_name:
                            count += 1
                            break
        return count
    
    def _extract_key_technologies(self, tech_stack: Dict) -> List[str]:
        """Extract key technologies from the stack."""
        key_techs = []
        
        # Priority categories for key technologies
        priority_categories = ['programming_languages', 'frameworks', 'databases', 'web_servers']
        
        for category in priority_categories:
            if category in tech_stack and tech_stack[category]:
                # Take first few technologies from each priority category
                key_techs.extend(tech_stack[category][:2])
        
        return key_techs[:10]  # Limit to top 10
    
    def _identify_tech_synergies(self, tech_stack: Dict) -> List[str]:
        """Identify potential technology synergies."""
        synergies = []
        
        # Common synergy patterns
        if tech_stack.get('databases'):
            synergies.append("Database consolidation opportunities")
        
        if tech_stack.get('analytics'):
            synergies.append("Analytics platform unification potential")
        
        if tech_stack.get('cdn'):
            synergies.append("CDN and hosting optimization opportunities")
        
        if tech_stack.get('payment_processors'):
            synergies.append("Payment processing consolidation benefits")
        
        if len(tech_stack.get('frameworks', [])) > 3:
            synergies.append("Framework standardization opportunities")
        
        return synergies
    
    def compare_tech_stacks(self, domain1: str, domain2: str) -> Dict:
        """
        Compare technology stacks of two domains for synergy analysis.
        
        Args:
            domain1: First domain to compare
            domain2: Second domain to compare
            
        Returns:
            Dictionary containing comparison results and synergy opportunities
        """
        try:
            # Get tech stacks for both domains
            stack1 = self.get_tech_stack(domain1)
            stack2 = self.get_tech_stack(domain2)
            
            if 'error' in stack1 or 'error' in stack2:
                return {
                    'error': 'Failed to retrieve tech stacks for comparison',
                    'domain1_error': stack1.get('error'),
                    'domain2_error': stack2.get('error'),
                    'timestamp': datetime.now().isoformat()
                }
            
            # Perform comparison analysis
            comparison = self._analyze_stack_overlap(
                stack1.get('technologies', {}),
                stack2.get('technologies', {})
            )
            
            return {
                'domain1': domain1,
                'domain2': domain2,
                'stack1': stack1,
                'stack2': stack2,
                'comparison': comparison,
                'synergy_opportunities': self._identify_integration_synergies(comparison),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error comparing tech stacks: {str(e)}")
            return {
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def _analyze_stack_overlap(self, stack1: Dict, stack2: Dict) -> Dict:
        """Analyze overlap between two technology stacks."""
        overlap_analysis = {
            'common_technologies': {},
            'unique_to_stack1': {},
            'unique_to_stack2': {},
            'overlap_percentage': 0,
            'integration_complexity': 'medium'
        }
        
        try:
            all_categories = set(stack1.keys()) | set(stack2.keys())
            total_overlap = 0
            total_technologies = 0
            
            for category in all_categories:
                techs1 = set(str(t).lower() for t in stack1.get(category, []) if t)
                techs2 = set(str(t).lower() for t in stack2.get(category, []) if t)
                
                common = techs1 & techs2
                unique1 = techs1 - techs2
                unique2 = techs2 - techs1
                
                if common or unique1 or unique2:
                    overlap_analysis['common_technologies'][category] = list(common)
                    overlap_analysis['unique_to_stack1'][category] = list(unique1)
                    overlap_analysis['unique_to_stack2'][category] = list(unique2)
                
                total_overlap += len(common)
                total_technologies += len(techs1 | techs2)
            
            # Calculate overlap percentage
            if total_technologies > 0:
                overlap_analysis['overlap_percentage'] = (total_overlap / total_technologies) * 100
            
            # Determine integration complexity
            if overlap_analysis['overlap_percentage'] > 60:
                overlap_analysis['integration_complexity'] = 'low'
            elif overlap_analysis['overlap_percentage'] < 30:
                overlap_analysis['integration_complexity'] = 'high'
            
        except Exception as e:
            logger.error(f"Error analyzing stack overlap: {str(e)}")
            overlap_analysis['error'] = str(e)
        
        return overlap_analysis
    
    def _identify_integration_synergies(self, comparison: Dict) -> List[Dict]:
        """Identify specific integration synergies based on tech stack comparison."""
        synergies = []
        
        try:
            common_techs = comparison.get('common_technologies', {})
            unique1 = comparison.get('unique_to_stack1', {})
            unique2 = comparison.get('unique_to_stack2', {})
            overlap_pct = comparison.get('overlap_percentage', 0)
            
            # Common technology synergies
            for category, technologies in common_techs.items():
                if technologies:
                    synergies.append({
                        'type': 'consolidation',
                        'category': category,
                        'description': f"Consolidate {category} - both companies use {', '.join(technologies[:3])}",
                        'potential_savings': 'medium',
                        'implementation_effort': 'low'
                    })
            
            # Complementary technology synergies
            for category in unique1.keys() | unique2.keys():
                if category in unique1 and category in unique2:
                    synergies.append({
                        'type': 'standardization',
                        'category': category,
                        'description': f"Standardize {category} technologies across organizations",
                        'potential_savings': 'high',
                        'implementation_effort': 'medium'
                    })
            
            # Overall integration assessment
            if overlap_pct > 50:
                synergies.append({
                    'type': 'integration',
                    'category': 'overall',
                    'description': f"High technology compatibility ({overlap_pct:.1f}% overlap) enables smooth integration",
                    'potential_savings': 'high',
                    'implementation_effort': 'low'
                })
            elif overlap_pct < 25:
                synergies.append({
                    'type': 'modernization',
                    'category': 'overall',
                    'description': f"Low overlap ({overlap_pct:.1f}%) suggests opportunity for technology modernization",
                    'potential_savings': 'high',
                    'implementation_effort': 'high'
                })
            
        except Exception as e:
            logger.error(f"Error identifying integration synergies: {str(e)}")
            synergies.append({
                'type': 'error',
                'description': f"Unable to analyze synergies: {str(e)}",
                'potential_savings': 'unknown',
                'implementation_effort': 'unknown'
            })
        
        return synergies