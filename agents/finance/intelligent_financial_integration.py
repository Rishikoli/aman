"""
Intelligent Financial Integration
Connects the Python Finance Agent with the Node.js Intelligent Financial Intelligence System
"""

import sys
import os
import json
import logging
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime

# Add the agents directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IntelligentFinancialIntegration:
    """
    Integration layer between Python Finance Agent and Node.js Intelligent Financial Service
    """
    
    def __init__(self, backend_url: str = "http://localhost:3001"):
        """Initialize the integration"""
        self.backend_url = backend_url.rstrip('/')
        self.api_base = f"{self.backend_url}/api/v1/intelligent-financial"
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'AMAN-Finance-Agent-Integration/1.0'
        })
        
        logger.info(f"Intelligent Financial Integration initialized with backend: {backend_url}")
    
    def smart_company_lookup(self, identifier: str, options: Dict = None) -> Dict[str, Any]:
        """
        Perform smart company lookup with multiple data source fallbacks
        
        Args:
            identifier: Company name, ticker, or partial identifier
            options: Lookup options
            
        Returns:
            Dictionary containing lookup results
        """
        try:
            if not options:
                options = {}
            
            logger.info(f"Performing smart company lookup for: {identifier}")
            
            payload = {
                'identifier': identifier,
                'options': options
            }
            
            response = self.session.post(f"{self.api_base}/lookup", json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            if result.get('success'):
                logger.info(f"Smart lookup successful: {result['data']['totalResults']} results found")
                return result['data']
            else:
                raise Exception(f"API returned error: {result.get('message', 'Unknown error')}")
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Smart company lookup failed: {str(e)}")
            raise Exception(f"Smart company lookup failed: {str(e)}")
        except Exception as e:
            logger.error(f"Smart company lookup error: {str(e)}")
            raise
    
    def identify_peer_companies(self, symbol: str, options: Dict = None) -> Dict[str, Any]:
        """
        Identify peer companies using financial similarity algorithms
        
        Args:
            symbol: Target company ticker symbol
            options: Peer identification options
            
        Returns:
            Dictionary containing peer analysis results
        """
        try:
            if not options:
                options = {}
            
            logger.info(f"Identifying peer companies for: {symbol}")
            
            payload = {
                'symbol': symbol,
                'options': options
            }
            
            response = self.session.post(f"{self.api_base}/peers", json=payload, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            if result.get('success'):
                logger.info(f"Peer identification successful: {result['data']['peersFound']} peers found")
                return result['data']
            else:
                raise Exception(f"API returned error: {result.get('message', 'Unknown error')}")
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Peer identification failed: {str(e)}")
            raise Exception(f"Peer identification failed: {str(e)}")
        except Exception as e:
            logger.error(f"Peer identification error: {str(e)}")
            raise
    
    def build_comprehensive_risk_score(self, symbol: str, options: Dict = None) -> Dict[str, Any]:
        """
        Build comprehensive financial risk scoring with ML-based insights
        
        Args:
            symbol: Company ticker symbol
            options: Risk scoring options
            
        Returns:
            Dictionary containing comprehensive risk assessment
        """
        try:
            if not options:
                options = {}
            
            logger.info(f"Building comprehensive risk score for: {symbol}")
            
            payload = {
                'symbol': symbol,
                'options': options
            }
            
            response = self.session.post(f"{self.api_base}/risk-score", json=payload, timeout=90)
            response.raise_for_status()
            
            result = response.json()
            if result.get('success'):
                risk_data = result['data']
                logger.info(f"Risk scoring successful: {risk_data['riskLevel']} ({risk_data['overallRiskScore']}/100)")
                return risk_data
            else:
                raise Exception(f"API returned error: {result.get('message', 'Unknown error')}")
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Risk scoring failed: {str(e)}")
            raise Exception(f"Risk scoring failed: {str(e)}")
        except Exception as e:
            logger.error(f"Risk scoring error: {str(e)}")
            raise
    
    def combined_intelligence_analysis(self, identifier: str, options: Dict = None) -> Dict[str, Any]:
        """
        Perform combined intelligence analysis (lookup + peers + risk scoring)
        
        Args:
            identifier: Company name, ticker, or partial identifier
            options: Analysis options
            
        Returns:
            Dictionary containing complete intelligence analysis
        """
        try:
            if not options:
                options = {}
            
            logger.info(f"Performing combined intelligence analysis for: {identifier}")
            
            payload = {
                'identifier': identifier,
                'options': options
            }
            
            response = self.session.post(f"{self.api_base}/analyze", json=payload, timeout=120)
            response.raise_for_status()
            
            result = response.json()
            if result.get('success'):
                logger.info(f"Combined analysis successful for: {identifier}")
                return result['data']
            else:
                raise Exception(f"API returned error: {result.get('message', 'Unknown error')}")
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Combined intelligence analysis failed: {str(e)}")
            raise Exception(f"Combined intelligence analysis failed: {str(e)}")
        except Exception as e:
            logger.error(f"Combined intelligence analysis error: {str(e)}")
            raise
    
    def test_service_connection(self) -> Dict[str, Any]:
        """
        Test connection to the intelligent financial service
        
        Returns:
            Dictionary containing test results
        """
        try:
            logger.info("Testing intelligent financial service connection...")
            
            response = self.session.get(f"{self.api_base}/test", timeout=30)
            response.raise_for_status()
            
            result = response.json()
            if result.get('success'):
                test_data = result['data']
                logger.info(f"Service test successful: {test_data['workingCapabilities']} capabilities operational")
                return test_data
            else:
                raise Exception(f"Service test failed: {result.get('message', 'Unknown error')}")
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Service connection test failed: {str(e)}")
            return {
                'overallStatus': 'failed',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Service connection test error: {str(e)}")
            return {
                'overallStatus': 'failed',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def get_service_status(self) -> Dict[str, Any]:
        """
        Get intelligent financial service status and capabilities
        
        Returns:
            Dictionary containing service status
        """
        try:
            logger.info("Getting intelligent financial service status...")
            
            response = self.session.get(f"{self.api_base}/status", timeout=15)
            response.raise_for_status()
            
            result = response.json()
            if result.get('success'):
                logger.info("Service status retrieved successfully")
                return result['data']
            else:
                raise Exception(f"Status check failed: {result.get('message', 'Unknown error')}")
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Service status check failed: {str(e)}")
            return {
                'service': 'Intelligent Financial Intelligence System',
                'status': 'unavailable',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Service status check error: {str(e)}")
            return {
                'service': 'Intelligent Financial Intelligence System',
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def enhance_financial_analysis(self, financial_data: Dict, company_identifier: str) -> Dict[str, Any]:
        """
        Enhance existing financial analysis with intelligent insights
        
        Args:
            financial_data: Existing financial analysis data
            company_identifier: Company identifier for intelligent analysis
            
        Returns:
            Enhanced financial analysis with intelligent insights
        """
        try:
            logger.info(f"Enhancing financial analysis with intelligent insights for: {company_identifier}")
            
            enhanced_analysis = {
                'original_analysis': financial_data,
                'intelligent_insights': {},
                'enhancement_timestamp': datetime.now().isoformat()
            }
            
            # Get intelligent analysis
            try:
                intelligent_analysis = self.combined_intelligence_analysis(company_identifier, {
                    'includePeers': True,
                    'includeRiskScore': True,
                    'includeFinancials': False,
                    'maxPeers': 5
                })
                
                enhanced_analysis['intelligent_insights'] = intelligent_analysis
                
                # Extract key insights for integration
                if 'analysis' in intelligent_analysis:
                    analysis = intelligent_analysis['analysis']
                    
                    # Add peer comparison insights
                    if 'peerAnalysis' in analysis and not analysis['peerAnalysis'].get('error'):
                        peer_data = analysis['peerAnalysis']
                        enhanced_analysis['peer_insights'] = {
                            'peers_found': peer_data.get('peersFound', 0),
                            'top_peers': [
                                {
                                    'name': peer.get('name'),
                                    'symbol': peer.get('symbol'),
                                    'similarity': peer.get('similarityScore', 0)
                                }
                                for peer in peer_data.get('peers', [])[:3]
                            ],
                            'insights': peer_data.get('insights', [])
                        }
                    
                    # Add risk assessment insights
                    if 'riskAssessment' in analysis and not analysis['riskAssessment'].get('error'):
                        risk_data = analysis['riskAssessment']
                        enhanced_analysis['risk_insights'] = {
                            'overall_risk_level': risk_data.get('riskLevel'),
                            'risk_score': risk_data.get('overallRiskScore'),
                            'risk_components': risk_data.get('riskComponents', {}),
                            'recommendations': risk_data.get('recommendations', []),
                            'peer_comparison': risk_data.get('peerComparison')
                        }
                
                # Add executive summary
                if 'executiveSummary' in intelligent_analysis:
                    enhanced_analysis['executive_summary'] = intelligent_analysis['executiveSummary']
                
                logger.info("Financial analysis enhanced successfully with intelligent insights")
                
            except Exception as e:
                logger.warning(f"Failed to get intelligent insights: {str(e)}")
                enhanced_analysis['intelligent_insights'] = {
                    'error': str(e),
                    'available': False
                }
            
            return enhanced_analysis
            
        except Exception as e:
            logger.error(f"Financial analysis enhancement failed: {str(e)}")
            return {
                'original_analysis': financial_data,
                'intelligent_insights': {
                    'error': str(e),
                    'available': False
                },
                'enhancement_timestamp': datetime.now().isoformat()
            }


def test_intelligent_financial_integration():
    """
    Test the intelligent financial integration
    """
    print("=" * 80)
    print("TESTING INTELLIGENT FINANCIAL INTEGRATION")
    print("=" * 80)
    
    integration = IntelligentFinancialIntegration()
    
    # Test 1: Service Connection
    print("\n1. Testing service connection...")
    try:
        status = integration.get_service_status()
        print(f"   ✅ Service: {status.get('service', 'Unknown')}")
        print(f"   📊 Status: {status.get('status', 'Unknown')}")
        
        if 'capabilities' in status:
            print("   🔧 Capabilities:")
            for capability in status['capabilities'][:3]:  # Show first 3
                print(f"      • {capability}")
    except Exception as e:
        print(f"   ❌ Service connection failed: {str(e)}")
    
    # Test 2: Smart Company Lookup
    print("\n2. Testing smart company lookup...")
    try:
        lookup_result = integration.smart_company_lookup('AAPL', {
            'includeFinancials': False,
            'includeRiskScore': False,
            'maxResults': 1
        })
        
        print(f"   ✅ Results found: {lookup_result.get('totalResults', 0)}")
        print(f"   📈 Confidence: {(lookup_result.get('confidence', 0) * 100):.1f}%")
        
        if lookup_result.get('results'):
            company = lookup_result['results'][0]
            print(f"   🏢 Company: {company.get('name')} ({company.get('symbol')})")
            
    except Exception as e:
        print(f"   ❌ Smart lookup failed: {str(e)}")
    
    # Test 3: Peer Identification
    print("\n3. Testing peer identification...")
    try:
        peer_result = integration.identify_peer_companies('AAPL', {
            'maxPeers': 3,
            'includeFinancials': False
        })
        
        print(f"   ✅ Peers found: {peer_result.get('peersFound', 0)}")
        
        if peer_result.get('peers'):
            print("   👥 Top peers:")
            for i, peer in enumerate(peer_result['peers'][:2]):
                similarity = peer.get('similarityScore', 0) * 100
                print(f"      {i+1}. {peer.get('name')} ({peer.get('symbol')}) - {similarity:.1f}% similar")
                
    except Exception as e:
        print(f"   ❌ Peer identification failed: {str(e)}")
    
    # Test 4: Risk Scoring
    print("\n4. Testing risk scoring...")
    try:
        risk_result = integration.build_comprehensive_risk_score('AAPL', {
            'includePeerComparison': False
        })
        
        print(f"   ✅ Risk Level: {risk_result.get('riskLevel', 'Unknown')}")
        print(f"   📊 Risk Score: {risk_result.get('overallRiskScore', 0)}/100")
        
        if risk_result.get('riskComponents'):
            print("   📈 Risk Components:")
            for component, data in list(risk_result['riskComponents'].items())[:3]:
                print(f"      • {component}: {data.get('level', 'Unknown')}")
                
    except Exception as e:
        print(f"   ❌ Risk scoring failed: {str(e)}")
    
    # Test 5: Combined Analysis
    print("\n5. Testing combined intelligence analysis...")
    try:
        combined_result = integration.combined_intelligence_analysis('AAPL', {
            'includePeers': True,
            'includeRiskScore': True,
            'maxPeers': 2
        })
        
        print(f"   ✅ Analysis completed for: {combined_result.get('identifier', 'Unknown')}")
        
        if 'executiveSummary' in combined_result:
            summary = combined_result['executiveSummary']
            print("   💡 Key Findings:")
            for finding in summary.get('keyFindings', [])[:2]:
                print(f"      • {finding}")
                
    except Exception as e:
        print(f"   ❌ Combined analysis failed: {str(e)}")
    
    print("\n" + "=" * 80)
    print("INTELLIGENT FINANCIAL INTEGRATION TEST COMPLETED")
    print("=" * 80)


if __name__ == "__main__":
    test_intelligent_financial_integration()