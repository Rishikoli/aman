"""
Operational Efficiency Benchmarking System

Provides comprehensive operational efficiency analysis and benchmarking
with optimization recommendations for M&A operations intelligence
"""

import logging
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import asyncio

logger = logging.getLogger(__name__)

class OperationalEfficiencyBenchmarker:
    """
    Comprehensive operational efficiency benchmarking and optimization system
    """
    
    def __init__(self):
        # Industry benchmarks (simplified for demo - in production would use real industry data)
        self.industry_benchmarks = {
            'manufacturing': {
                'facility_utilization': 75.0,
                'geographic_efficiency': 65.0,
                'cost_per_unit': 100.0,  # Normalized baseline
                'operational_redundancy': 40.0,
                'supply_chain_efficiency': 70.0
            },
            'technology': {
                'facility_utilization': 80.0,
                'geographic_efficiency': 70.0,
                'cost_per_unit': 90.0,
                'operational_redundancy': 30.0,
                'supply_chain_efficiency': 75.0
            },
            'retail': {
                'facility_utilization': 85.0,
                'geographic_efficiency': 75.0,
                'cost_per_unit': 95.0,
                'operational_redundancy': 50.0,
                'supply_chain_efficiency': 80.0
            },
            'financial_services': {
                'facility_utilization': 90.0,
                'geographic_efficiency': 80.0,
                'cost_per_unit': 85.0,
                'operational_redundancy': 25.0,
                'supply_chain_efficiency': 60.0
            },
            'healthcare': {
                'facility_utilization': 70.0,
                'geographic_efficiency': 60.0,
                'cost_per_unit': 110.0,
                'operational_redundancy': 60.0,
                'supply_chain_efficiency': 65.0
            }
        }
        
        # Efficiency metrics weights
        self.efficiency_weights = {
            'facility_utilization': 0.25,
            'geographic_efficiency': 0.20,
            'cost_optimization': 0.20,
            'operational_redundancy': 0.15,
            'supply_chain_efficiency': 0.10,
            'technology_integration': 0.10
        }
        
        # Optimization opportunity categories
        self.optimization_categories = {
            'facility_consolidation': {
                'impact_potential': 'high',
                'implementation_complexity': 'medium',
                'typical_savings': '15-25%'
            },
            'process_automation': {
                'impact_potential': 'high',
                'implementation_complexity': 'high',
                'typical_savings': '20-30%'
            },
            'supply_chain_optimization': {
                'impact_potential': 'medium',
                'implementation_complexity': 'medium',
                'typical_savings': '10-15%'
            },
            'technology_consolidation': {
                'impact_potential': 'medium',
                'implementation_complexity': 'low',
                'typical_savings': '5-10%'
            },
            'workforce_optimization': {
                'impact_potential': 'high',
                'implementation_complexity': 'high',
                'typical_savings': '15-20%'
            }
        }
    
    async def benchmark_operational_efficiency(self, company_data: Dict[str, Any], 
                                             industry: str = 'manufacturing') -> Dict[str, Any]:
        """
        Comprehensive operational efficiency benchmarking
        
        Args:
            company_data: Company operational data
            industry: Industry sector for benchmarking
            
        Returns:
            Comprehensive efficiency benchmarking analysis
        """
        try:
            logger.info(f"Benchmarking operational efficiency for {industry} industry")
            
            # Calculate current efficiency metrics
            current_metrics = await self._calculate_efficiency_metrics(company_data)
            
            # Get industry benchmarks
            benchmarks = self._get_industry_benchmarks(industry)
            
            # Perform benchmarking analysis
            benchmark_analysis = self._perform_benchmark_analysis(current_metrics, benchmarks)
            
            # Identify optimization opportunities
            optimization_opportunities = self._identify_optimization_opportunities(
                current_metrics, benchmarks, company_data
            )
            
            # Generate efficiency recommendations
            recommendations = self._generate_efficiency_recommendations(
                benchmark_analysis, optimization_opportunities
            )
            
            # Calculate potential improvements
            potential_improvements = self._calculate_potential_improvements(
                optimization_opportunities
            )
            
            # Create implementation roadmap
            implementation_roadmap = self._create_implementation_roadmap(
                optimization_opportunities
            )
            
            return {
                'benchmarking_timestamp': datetime.now().isoformat(),
                'industry': industry,
                'current_metrics': current_metrics,
                'industry_benchmarks': benchmarks,
                'benchmark_analysis': benchmark_analysis,
                'optimization_opportunities': optimization_opportunities,
                'recommendations': recommendations,
                'potential_improvements': potential_improvements,
                'implementation_roadmap': implementation_roadmap,
                'overall_efficiency_score': benchmark_analysis.get('overall_score', 50),
                'efficiency_grade': self._calculate_efficiency_grade(
                    benchmark_analysis.get('overall_score', 50)
                )
            }
            
        except Exception as e:
            logger.error(f"Error in operational efficiency benchmarking: {str(e)}")
            return {
                'error': str(e),
                'benchmarking_timestamp': datetime.now().isoformat()
            }
    
    async def _calculate_efficiency_metrics(self, company_data: Dict[str, Any]) -> Dict[str, float]:
        """Calculate current operational efficiency metrics"""
        try:
            metrics = {}
            
            # Facility utilization
            facilities = company_data.get('facilities', [])
            if facilities:
                # Simple utilization calculation based on facility data
                total_capacity = sum(f.get('capacity', 100) for f in facilities)
                total_utilization = sum(f.get('utilization', 70) for f in facilities)
                metrics['facility_utilization'] = (total_utilization / len(facilities)) if facilities else 70.0
            else:
                metrics['facility_utilization'] = 70.0  # Default
            
            # Geographic efficiency
            locations = company_data.get('locations', [])
            if locations:
                # Calculate geographic distribution efficiency
                countries = set(loc.get('country') for loc in locations if loc.get('country'))
                regions = set(loc.get('region') for loc in locations if loc.get('region'))
                
                # More countries/regions = better distribution but potentially lower efficiency
                geo_efficiency = min(90, 50 + (len(countries) * 5) + (len(regions) * 3))
                metrics['geographic_efficiency'] = geo_efficiency
            else:
                metrics['geographic_efficiency'] = 50.0
            
            # Cost optimization score
            operational_data = company_data.get('operational_data', {})
            cost_per_unit = operational_data.get('cost_per_unit', 100)
            # Lower cost per unit = higher efficiency (inverted scale)
            metrics['cost_optimization'] = max(0, 150 - cost_per_unit)
            
            # Operational redundancy
            redundancy_score = self._calculate_redundancy_score(facilities)
            metrics['operational_redundancy'] = redundancy_score
            
            # Supply chain efficiency
            suppliers = company_data.get('suppliers', [])
            supply_chain_score = self._calculate_supply_chain_efficiency(suppliers)
            metrics['supply_chain_efficiency'] = supply_chain_score
            
            # Technology integration
            tech_data = company_data.get('technology', {})
            tech_score = self._calculate_technology_integration_score(tech_data)
            metrics['technology_integration'] = tech_score
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error calculating efficiency metrics: {str(e)}")
            return {
                'facility_utilization': 50.0,
                'geographic_efficiency': 50.0,
                'cost_optimization': 50.0,
                'operational_redundancy': 50.0,
                'supply_chain_efficiency': 50.0,
                'technology_integration': 50.0
            }
    
    def _calculate_redundancy_score(self, facilities: List[Dict[str, Any]]) -> float:
        """Calculate operational redundancy score"""
        try:
            if not facilities:
                return 0.0
            
            # Analyze facility types and functions
            facility_types = {}
            for facility in facilities:
                facility_type = facility.get('type', 'unknown')
                if facility_type not in facility_types:
                    facility_types[facility_type] = 0
                facility_types[facility_type] += 1
            
            # Calculate redundancy score based on backup facilities
            redundancy_score = 0
            for facility_type, count in facility_types.items():
                if count > 1:
                    redundancy_score += min(count - 1, 3) * 20  # Max 60 points per type
            
            return min(100, redundancy_score)
            
        except Exception as e:
            logger.error(f"Error calculating redundancy score: {str(e)}")
            return 50.0
    
    def _calculate_supply_chain_efficiency(self, suppliers: List[Dict[str, Any]]) -> float:
        """Calculate supply chain efficiency score"""
        try:
            if not suppliers:
                return 50.0
            
            # Factors affecting supply chain efficiency
            efficiency_score = 60.0  # Base score
            
            # Supplier diversification
            countries = set(s.get('country') for s in suppliers if s.get('country'))
            if len(countries) > 5:
                efficiency_score += 15  # Good diversification
            elif len(countries) > 2:
                efficiency_score += 10  # Moderate diversification
            
            # Supplier reliability (if available)
            reliable_suppliers = sum(1 for s in suppliers if s.get('reliability_score', 70) > 80)
            reliability_ratio = reliable_suppliers / len(suppliers)
            efficiency_score += reliability_ratio * 20
            
            # Supply chain complexity (fewer suppliers can be more efficient)
            if len(suppliers) < 10:
                efficiency_score += 5  # Simpler supply chain
            elif len(suppliers) > 50:
                efficiency_score -= 10  # Complex supply chain
            
            return min(100, max(0, efficiency_score))
            
        except Exception as e:
            logger.error(f"Error calculating supply chain efficiency: {str(e)}")
            return 50.0
    
    def _calculate_technology_integration_score(self, tech_data: Dict[str, Any]) -> float:
        """Calculate technology integration efficiency score"""
        try:
            if not tech_data:
                return 50.0
            
            integration_score = 50.0  # Base score
            
            # System integration level
            integration_level = tech_data.get('integration_level', 'medium')
            if integration_level == 'high':
                integration_score += 25
            elif integration_level == 'medium':
                integration_score += 10
            
            # Automation level
            automation_level = tech_data.get('automation_level', 50)
            integration_score += (automation_level - 50) * 0.5
            
            # Technology stack consolidation
            num_systems = tech_data.get('number_of_systems', 10)
            if num_systems < 5:
                integration_score += 15  # Well consolidated
            elif num_systems > 20:
                integration_score -= 15  # Too many systems
            
            return min(100, max(0, integration_score))
            
        except Exception as e:
            logger.error(f"Error calculating technology integration score: {str(e)}")
            return 50.0
    
    def _get_industry_benchmarks(self, industry: str) -> Dict[str, float]:
        """Get industry-specific benchmarks"""
        return self.industry_benchmarks.get(industry, self.industry_benchmarks['manufacturing'])
    
    def _perform_benchmark_analysis(self, current_metrics: Dict[str, float], 
                                  benchmarks: Dict[str, float]) -> Dict[str, Any]:
        """Perform detailed benchmarking analysis"""
        try:
            analysis = {
                'metric_comparisons': {},
                'performance_gaps': {},
                'strengths': [],
                'weaknesses': [],
                'overall_score': 0.0
            }
            
            total_weighted_score = 0.0
            total_weight = 0.0
            
            for metric, current_value in current_metrics.items():
                benchmark_value = benchmarks.get(metric, 50.0)
                
                # Calculate performance ratio
                if benchmark_value > 0:
                    performance_ratio = (current_value / benchmark_value) * 100
                else:
                    performance_ratio = 100.0
                
                gap = current_value - benchmark_value
                
                analysis['metric_comparisons'][metric] = {
                    'current': current_value,
                    'benchmark': benchmark_value,
                    'performance_ratio': performance_ratio,
                    'gap': gap,
                    'status': 'above_benchmark' if gap > 0 else 'below_benchmark'
                }
                
                analysis['performance_gaps'][metric] = gap
                
                # Identify strengths and weaknesses
                if gap > 10:
                    analysis['strengths'].append({
                        'metric': metric,
                        'advantage': gap,
                        'description': f"{metric.replace('_', ' ').title()} exceeds industry benchmark by {gap:.1f} points"
                    })
                elif gap < -10:
                    analysis['weaknesses'].append({
                        'metric': metric,
                        'deficit': abs(gap),
                        'description': f"{metric.replace('_', ' ').title()} below industry benchmark by {abs(gap):.1f} points"
                    })
                
                # Calculate weighted score
                weight = self.efficiency_weights.get(metric, 0.1)
                weighted_score = min(100, max(0, performance_ratio)) * weight
                total_weighted_score += weighted_score
                total_weight += weight
            
            # Calculate overall score
            if total_weight > 0:
                analysis['overall_score'] = total_weighted_score / total_weight
            else:
                analysis['overall_score'] = 50.0
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error performing benchmark analysis: {str(e)}")
            return {'error': str(e), 'overall_score': 50.0}
    
    def _identify_optimization_opportunities(self, current_metrics: Dict[str, float], 
                                           benchmarks: Dict[str, float], 
                                           company_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify specific optimization opportunities"""
        opportunities = []
        
        try:
            # Facility consolidation opportunities
            facilities = company_data.get('facilities', [])
            if len(facilities) > 5:
                utilization_avg = current_metrics.get('facility_utilization', 70)
                if utilization_avg < 80:
                    opportunities.append({
                        'category': 'facility_consolidation',
                        'priority': 'high',
                        'description': 'Consolidate underutilized facilities to improve efficiency',
                        'current_state': f'{len(facilities)} facilities with {utilization_avg:.1f}% average utilization',
                        'target_state': 'Reduce to optimal facility count with 85%+ utilization',
                        'estimated_savings': '15-25%',
                        'implementation_time': '6-12 months',
                        'complexity': 'medium'
                    })
            
            # Process automation opportunities
            tech_score = current_metrics.get('technology_integration', 50)
            if tech_score < 70:
                opportunities.append({
                    'category': 'process_automation',
                    'priority': 'high',
                    'description': 'Implement process automation to improve efficiency',
                    'current_state': f'Technology integration score: {tech_score:.1f}%',
                    'target_state': 'Achieve 85%+ automation in key processes',
                    'estimated_savings': '20-30%',
                    'implementation_time': '12-18 months',
                    'complexity': 'high'
                })
            
            # Supply chain optimization
            supply_chain_score = current_metrics.get('supply_chain_efficiency', 50)
            supply_chain_benchmark = benchmarks.get('supply_chain_efficiency', 70)
            if supply_chain_score < supply_chain_benchmark - 10:
                opportunities.append({
                    'category': 'supply_chain_optimization',
                    'priority': 'medium',
                    'description': 'Optimize supply chain for better efficiency and cost reduction',
                    'current_state': f'Supply chain efficiency: {supply_chain_score:.1f}%',
                    'target_state': f'Achieve industry benchmark of {supply_chain_benchmark:.1f}%',
                    'estimated_savings': '10-15%',
                    'implementation_time': '6-9 months',
                    'complexity': 'medium'
                })
            
            # Technology consolidation
            tech_data = company_data.get('technology', {})
            num_systems = tech_data.get('number_of_systems', 10)
            if num_systems > 15:
                opportunities.append({
                    'category': 'technology_consolidation',
                    'priority': 'medium',
                    'description': 'Consolidate technology systems to reduce complexity and costs',
                    'current_state': f'{num_systems} separate systems',
                    'target_state': 'Consolidate to 8-10 integrated systems',
                    'estimated_savings': '5-10%',
                    'implementation_time': '3-6 months',
                    'complexity': 'low'
                })
            
            # Geographic optimization
            geo_efficiency = current_metrics.get('geographic_efficiency', 50)
            geo_benchmark = benchmarks.get('geographic_efficiency', 65)
            if geo_efficiency < geo_benchmark - 15:
                opportunities.append({
                    'category': 'geographic_optimization',
                    'priority': 'medium',
                    'description': 'Optimize geographic footprint for better operational efficiency',
                    'current_state': f'Geographic efficiency: {geo_efficiency:.1f}%',
                    'target_state': f'Achieve {geo_benchmark:.1f}% geographic efficiency',
                    'estimated_savings': '8-12%',
                    'implementation_time': '9-15 months',
                    'complexity': 'high'
                })
            
            # Sort opportunities by priority and potential impact
            priority_order = {'high': 3, 'medium': 2, 'low': 1}
            opportunities.sort(key=lambda x: priority_order.get(x['priority'], 1), reverse=True)
            
            return opportunities
            
        except Exception as e:
            logger.error(f"Error identifying optimization opportunities: {str(e)}")
            return []
    
    def _generate_efficiency_recommendations(self, benchmark_analysis: Dict[str, Any], 
                                           optimization_opportunities: List[Dict[str, Any]]) -> List[str]:
        """Generate actionable efficiency recommendations"""
        recommendations = []
        
        try:
            overall_score = benchmark_analysis.get('overall_score', 50)
            
            # Overall performance recommendations
            if overall_score < 60:
                recommendations.append("PRIORITY: Comprehensive operational efficiency improvement program required")
                recommendations.append("Focus on top 3 optimization opportunities for maximum impact")
            elif overall_score < 80:
                recommendations.append("Implement targeted efficiency improvements in underperforming areas")
                recommendations.append("Benchmark against industry leaders for best practices")
            else:
                recommendations.append("Maintain current efficiency levels and focus on continuous improvement")
            
            # Specific opportunity recommendations
            high_priority_ops = [op for op in optimization_opportunities if op.get('priority') == 'high']
            for op in high_priority_ops[:3]:  # Top 3 high priority
                recommendations.append(f"Implement {op['category'].replace('_', ' ')}: {op['description']}")
            
            # Weakness-specific recommendations
            weaknesses = benchmark_analysis.get('weaknesses', [])
            for weakness in weaknesses[:2]:  # Top 2 weaknesses
                metric = weakness['metric']
                if metric == 'facility_utilization':
                    recommendations.append("Improve facility utilization through capacity optimization and consolidation")
                elif metric == 'supply_chain_efficiency':
                    recommendations.append("Streamline supply chain operations and reduce supplier complexity")
                elif metric == 'technology_integration':
                    recommendations.append("Invest in technology integration and automation initiatives")
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating efficiency recommendations: {str(e)}")
            return ["Conduct detailed operational efficiency analysis"]
    
    def _calculate_potential_improvements(self, optimization_opportunities: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate potential improvements from optimization opportunities"""
        try:
            total_savings_min = 0.0
            total_savings_max = 0.0
            implementation_timeline = 0
            
            for opportunity in optimization_opportunities:
                # Parse savings range
                savings_str = opportunity.get('estimated_savings', '0-0%')
                try:
                    savings_range = savings_str.replace('%', '').split('-')
                    min_savings = float(savings_range[0])
                    max_savings = float(savings_range[1]) if len(savings_range) > 1 else min_savings
                    
                    total_savings_min += min_savings
                    total_savings_max += max_savings
                except:
                    pass
                
                # Parse implementation time
                time_str = opportunity.get('implementation_time', '0 months')
                try:
                    if 'months' in time_str:
                        time_range = time_str.replace(' months', '').split('-')
                        max_time = float(time_range[-1])
                        implementation_timeline = max(implementation_timeline, max_time)
                except:
                    pass
            
            return {
                'cost_savings_range': f"{total_savings_min:.0f}-{total_savings_max:.0f}%",
                'efficiency_improvement': f"{total_savings_min * 0.8:.0f}-{total_savings_max * 1.2:.0f}%",
                'implementation_timeline_months': implementation_timeline,
                'roi_estimate': 'High' if total_savings_max > 20 else 'Medium' if total_savings_max > 10 else 'Low',
                'risk_level': 'Medium',  # Default assessment
                'confidence_level': 0.75
            }
            
        except Exception as e:
            logger.error(f"Error calculating potential improvements: {str(e)}")
            return {
                'cost_savings_range': '5-15%',
                'efficiency_improvement': '10-20%',
                'implementation_timeline_months': 12,
                'roi_estimate': 'Medium',
                'risk_level': 'Medium',
                'confidence_level': 0.5
            }
    
    def _create_implementation_roadmap(self, optimization_opportunities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Create implementation roadmap for optimization opportunities"""
        try:
            roadmap = []
            
            # Phase 1: Quick wins (0-6 months)
            phase1_ops = [op for op in optimization_opportunities 
                         if 'months' in op.get('implementation_time', '') and 
                         int(op.get('implementation_time', '12 months').split('-')[0]) <= 6]
            
            if phase1_ops:
                roadmap.append({
                    'phase': 'Phase 1: Quick Wins',
                    'timeline': '0-6 months',
                    'focus': 'Low complexity, high impact improvements',
                    'opportunities': phase1_ops[:3],
                    'expected_savings': '5-10%',
                    'key_activities': [
                        'Technology system consolidation',
                        'Process standardization',
                        'Immediate cost reduction initiatives'
                    ]
                })
            
            # Phase 2: Strategic improvements (6-12 months)
            phase2_ops = [op for op in optimization_opportunities 
                         if op not in phase1_ops and op.get('priority') == 'high']
            
            if phase2_ops:
                roadmap.append({
                    'phase': 'Phase 2: Strategic Improvements',
                    'timeline': '6-12 months',
                    'focus': 'Medium to high complexity operational improvements',
                    'opportunities': phase2_ops[:2],
                    'expected_savings': '10-20%',
                    'key_activities': [
                        'Facility consolidation planning and execution',
                        'Supply chain optimization',
                        'Process automation implementation'
                    ]
                })
            
            # Phase 3: Transformation (12+ months)
            phase3_ops = [op for op in optimization_opportunities 
                         if op not in phase1_ops and op not in phase2_ops]
            
            if phase3_ops:
                roadmap.append({
                    'phase': 'Phase 3: Transformation',
                    'timeline': '12+ months',
                    'focus': 'Complex, long-term operational transformation',
                    'opportunities': phase3_ops,
                    'expected_savings': '15-25%',
                    'key_activities': [
                        'Geographic footprint optimization',
                        'Advanced automation and AI implementation',
                        'Organizational restructuring'
                    ]
                })
            
            return roadmap
            
        except Exception as e:
            logger.error(f"Error creating implementation roadmap: {str(e)}")
            return [{
                'phase': 'Phase 1: Assessment',
                'timeline': '0-3 months',
                'focus': 'Detailed operational analysis and planning',
                'opportunities': [],
                'expected_savings': 'TBD',
                'key_activities': ['Comprehensive operational assessment']
            }]
    
    def _calculate_efficiency_grade(self, overall_score: float) -> str:
        """Calculate efficiency grade based on overall score"""
        if overall_score >= 90:
            return 'A+'
        elif overall_score >= 85:
            return 'A'
        elif overall_score >= 80:
            return 'A-'
        elif overall_score >= 75:
            return 'B+'
        elif overall_score >= 70:
            return 'B'
        elif overall_score >= 65:
            return 'B-'
        elif overall_score >= 60:
            return 'C+'
        elif overall_score >= 55:
            return 'C'
        elif overall_score >= 50:
            return 'C-'
        else:
            return 'D'