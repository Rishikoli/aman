"""
OpenCorporates API Client for corporate structure and ownership verification
Uses the free OpenCorporates API to retrieve company registration and ownership data
"""

import logging
import requests
import time
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
import os

logger = logging.getLogger(__name__)

class OpenCorporatesClient:
    """
    Client for accessing OpenCorporates API for corporate structure data
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize OpenCorporates client
        
        Args:
            api_key: Optional API key for higher rate limits
        """
        self.base_url = "https://api.opencorporates.com/v0.4"
        self.api_key = api_key or os.getenv('OPENCORPORATES_API_KEY')
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'AMAN Legal Agent 1.0',
            'Accept': 'application/json'
        })
        
        # Rate limiting: Free tier allows 500 requests per month, 5 per minute
        self.rate_limit_delay = 12  # 12 seconds between requests for free tier
        self.last_request_time = 0
        
        logger.info("OpenCorporates client initialized")
    
    def _rate_limit(self):
        """Enforce rate limiting for OpenCorporates API requests"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.rate_limit_delay:
            sleep_time = self.rate_limit_delay - time_since_last
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """
        Make a rate-limited request to OpenCorporates API
        
        Args:
            endpoint: API endpoint path
            params: Query parameters
            
        Returns:
            JSON response data or None if failed
        """
        try:
            self._rate_limit()
            
            url = f"{self.base_url}/{endpoint}"
            
            # Add API key if available
            if params is None:
                params = {}
            
            if self.api_key:
                params['api_token'] = self.api_key
            
            response = self.session.get(url, params=params, timeout=30)
            
            # Handle rate limiting
            if response.status_code == 429:
                logger.warning("Rate limit exceeded, waiting longer...")
                time.sleep(60)  # Wait 1 minute
                response = self.session.get(url, params=params, timeout=30)
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"OpenCorporates API request failed: {e}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse OpenCorporates API response: {e}")
            return None
    
    def search_companies(self, query: str, jurisdiction: Optional[str] = None, 
                        limit: int = 10) -> Optional[Dict]:
        """
        Search for companies by name
        
        Args:
            query: Company name to search for
            jurisdiction: Optional jurisdiction code (e.g., 'us_de', 'gb')
            limit: Maximum number of results
            
        Returns:
            Search results
        """
        try:
            params = {
                'q': query,
                'per_page': min(limit, 30)  # API limit
            }
            
            if jurisdiction:
                params['jurisdiction_code'] = jurisdiction
            
            data = self._make_request('companies/search', params)
            if not data:
                return None
            
            companies = []
            results = data.get('results', {}).get('companies', [])
            
            for company_data in results:
                company = company_data.get('company', {})
                companies.append({
                    'name': company.get('name', ''),
                    'company_number': company.get('company_number', ''),
                    'jurisdiction_code': company.get('jurisdiction_code', ''),
                    'company_type': company.get('company_type', ''),
                    'incorporation_date': company.get('incorporation_date', ''),
                    'dissolution_date': company.get('dissolution_date', ''),
                    'current_status': company.get('current_status', ''),
                    'registered_address': company.get('registered_address_in_full', ''),
                    'opencorporates_url': company.get('opencorporates_url', '')
                })
            
            return {
                'companies': companies,
                'total_count': data.get('results', {}).get('total_count', 0),
                'page': data.get('results', {}).get('page', 1),
                'per_page': data.get('results', {}).get('per_page', limit)
            }
            
        except Exception as e:
            logger.error(f"Error searching companies: {e}")
            return None
    
    def get_company_details(self, jurisdiction_code: str, company_number: str) -> Optional[Dict]:
        """
        Get detailed information about a specific company
        
        Args:
            jurisdiction_code: Jurisdiction code (e.g., 'us_de')
            company_number: Company registration number
            
        Returns:
            Detailed company information
        """
        try:
            endpoint = f"companies/{jurisdiction_code}/{company_number}"
            data = self._make_request(endpoint)
            
            if not data:
                return None
            
            company = data.get('results', {}).get('company', {})
            
            return {
                'basic_info': {
                    'name': company.get('name', ''),
                    'company_number': company.get('company_number', ''),
                    'jurisdiction_code': company.get('jurisdiction_code', ''),
                    'company_type': company.get('company_type', ''),
                    'incorporation_date': company.get('incorporation_date', ''),
                    'dissolution_date': company.get('dissolution_date', ''),
                    'current_status': company.get('current_status', ''),
                    'registered_address': company.get('registered_address_in_full', ''),
                    'agent_name': company.get('agent_name', ''),
                    'agent_address': company.get('agent_address', '')
                },
                'financial_info': {
                    'annual_return_last_made_up_date': company.get('annual_return_last_made_up_date', ''),
                    'accounts_next_due': company.get('accounts_next_due', ''),
                    'confirmation_statement_next_due': company.get('confirmation_statement_next_due', '')
                },
                'identifiers': company.get('identifiers', []),
                'industry_codes': company.get('industry_codes', []),
                'previous_names': company.get('previous_names', []),
                'source': company.get('source', {}),
                'opencorporates_url': company.get('opencorporates_url', ''),
                'retrieved_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting company details: {e}")
            return None
    
    def get_company_officers(self, jurisdiction_code: str, company_number: str) -> Optional[List[Dict]]:
        """
        Get officers/directors information for a company
        
        Args:
            jurisdiction_code: Jurisdiction code
            company_number: Company registration number
            
        Returns:
            List of company officers
        """
        try:
            endpoint = f"companies/{jurisdiction_code}/{company_number}/officers"
            data = self._make_request(endpoint)
            
            if not data:
                return None
            
            officers = []
            results = data.get('results', {}).get('officers', [])
            
            for officer_data in results:
                officer = officer_data.get('officer', {})
                officers.append({
                    'name': officer.get('name', ''),
                    'position': officer.get('position', ''),
                    'start_date': officer.get('start_date', ''),
                    'end_date': officer.get('end_date', ''),
                    'nationality': officer.get('nationality', ''),
                    'occupation': officer.get('occupation', ''),
                    'address': officer.get('address', ''),
                    'date_of_birth': officer.get('date_of_birth', ''),
                    'inactive': officer.get('inactive', False)
                })
            
            return officers
            
        except Exception as e:
            logger.error(f"Error getting company officers: {e}")
            return None
    
    def get_company_filings(self, jurisdiction_code: str, company_number: str) -> Optional[List[Dict]]:
        """
        Get recent filings for a company
        
        Args:
            jurisdiction_code: Jurisdiction code
            company_number: Company registration number
            
        Returns:
            List of company filings
        """
        try:
            endpoint = f"companies/{jurisdiction_code}/{company_number}/filings"
            data = self._make_request(endpoint)
            
            if not data:
                return None
            
            filings = []
            results = data.get('results', {}).get('filings', [])
            
            for filing_data in results:
                filing = filing_data.get('filing', {})
                filings.append({
                    'title': filing.get('title', ''),
                    'filing_type': filing.get('filing_type', ''),
                    'date': filing.get('date', ''),
                    'description': filing.get('description', ''),
                    'uid': filing.get('uid', ''),
                    'opencorporates_url': filing.get('opencorporates_url', '')
                })
            
            return filings
            
        except Exception as e:
            logger.error(f"Error getting company filings: {e}")
            return None
    
    def verify_company_ownership(self, company_name: str, 
                                jurisdiction: Optional[str] = None) -> Dict[str, Any]:
        """
        Verify company ownership and corporate structure
        
        Args:
            company_name: Name of company to verify
            jurisdiction: Optional jurisdiction to search in
            
        Returns:
            Ownership verification results
        """
        try:
            # Search for the company
            search_results = self.search_companies(company_name, jurisdiction, limit=5)
            
            if not search_results or not search_results.get('companies'):
                return {
                    'found': False,
                    'company_name': company_name,
                    'error': 'Company not found in OpenCorporates database'
                }
            
            # Get the most likely match (first result)
            company = search_results['companies'][0]
            jurisdiction_code = company['jurisdiction_code']
            company_number = company['company_number']
            
            # Get detailed company information
            details = self.get_company_details(jurisdiction_code, company_number)
            
            # Get officers/directors
            officers = self.get_company_officers(jurisdiction_code, company_number)
            
            # Get recent filings
            filings = self.get_company_filings(jurisdiction_code, company_number)
            
            # Analyze corporate structure
            structure_analysis = self._analyze_corporate_structure(details, officers)
            
            return {
                'found': True,
                'company_name': company_name,
                'matched_company': company,
                'company_details': details,
                'officers': officers or [],
                'recent_filings': filings or [],
                'structure_analysis': structure_analysis,
                'verification_date': datetime.now().isoformat(),
                'data_source': 'OpenCorporates'
            }
            
        except Exception as e:
            logger.error(f"Error verifying company ownership: {e}")
            return {
                'found': False,
                'company_name': company_name,
                'error': str(e)
            }
    
    def _analyze_corporate_structure(self, details: Optional[Dict], 
                                   officers: Optional[List[Dict]]) -> Dict[str, Any]:
        """
        Analyze corporate structure and identify potential risks
        
        Args:
            details: Company details
            officers: List of officers
            
        Returns:
            Structure analysis results
        """
        analysis = {
            'status': 'unknown',
            'risk_factors': [],
            'governance_score': 0,
            'officer_count': 0,
            'active_officers': 0,
            'key_positions_filled': []
        }
        
        if not details:
            analysis['risk_factors'].append('No company details available')
            return analysis
        
        basic_info = details.get('basic_info', {})
        
        # Check company status
        current_status = basic_info.get('current_status', '').lower()
        analysis['status'] = current_status
        
        if current_status in ['dissolved', 'inactive', 'struck off']:
            analysis['risk_factors'].append(f'Company status: {current_status}')
        
        # Analyze officers
        if officers:
            analysis['officer_count'] = len(officers)
            active_officers = [o for o in officers if not o.get('inactive', False)]
            analysis['active_officers'] = len(active_officers)
            
            # Check for key positions
            positions = [o.get('position', '').lower() for o in active_officers]
            key_positions = ['director', 'ceo', 'president', 'secretary', 'treasurer']
            
            for position in key_positions:
                if any(position in p for p in positions):
                    analysis['key_positions_filled'].append(position)
            
            # Calculate governance score
            governance_score = 0
            if analysis['active_officers'] > 0:
                governance_score += 20
            if len(analysis['key_positions_filled']) >= 2:
                governance_score += 30
            if analysis['active_officers'] >= 3:
                governance_score += 25
            if current_status == 'active':
                governance_score += 25
            
            analysis['governance_score'] = governance_score
            
            # Risk factors
            if analysis['active_officers'] == 0:
                analysis['risk_factors'].append('No active officers found')
            elif analysis['active_officers'] == 1:
                analysis['risk_factors'].append('Only one active officer (single point of failure)')
            
            if len(analysis['key_positions_filled']) < 2:
                analysis['risk_factors'].append('Key governance positions not filled')
        
        else:
            analysis['risk_factors'].append('No officer information available')
        
        # Check incorporation date
        incorporation_date = basic_info.get('incorporation_date')
        if incorporation_date:
            try:
                inc_date = datetime.strptime(incorporation_date, '%Y-%m-%d')
                days_since_incorporation = (datetime.now() - inc_date).days
                
                if days_since_incorporation < 365:
                    analysis['risk_factors'].append('Recently incorporated company (less than 1 year)')
                elif days_since_incorporation < 30:
                    analysis['risk_factors'].append('Very recently incorporated (less than 30 days)')
            except ValueError:
                pass
        
        return analysis
    
    def get_corporate_network(self, company_name: str, 
                            jurisdiction: Optional[str] = None) -> Dict[str, Any]:
        """
        Get corporate network information including related entities
        
        Args:
            company_name: Name of company
            jurisdiction: Optional jurisdiction
            
        Returns:
            Corporate network analysis
        """
        try:
            # Get basic company verification
            verification = self.verify_company_ownership(company_name, jurisdiction)
            
            if not verification.get('found'):
                return verification
            
            # Extract officer names for network analysis
            officers = verification.get('officers', [])
            officer_names = [o.get('name', '') for o in officers if o.get('name')]
            
            # Search for other companies with same officers (simplified network analysis)
            related_companies = []
            
            # Limit network search to avoid rate limits
            for officer_name in officer_names[:3]:  # Only check top 3 officers
                if len(officer_name) > 5:  # Skip very short names
                    try:
                        search_results = self.search_companies(officer_name, limit=3)
                        if search_results and search_results.get('companies'):
                            for company in search_results['companies']:
                                if company['name'].lower() != company_name.lower():
                                    related_companies.append({
                                        'company': company,
                                        'connection': f'Shared officer: {officer_name}'
                                    })
                    except Exception as e:
                        logger.warning(f"Error searching for related companies: {e}")
                        continue
            
            # Remove duplicates
            unique_related = []
            seen_companies = set()
            
            for item in related_companies:
                company_key = f"{item['company']['name']}_{item['company']['jurisdiction_code']}"
                if company_key not in seen_companies:
                    seen_companies.add(company_key)
                    unique_related.append(item)
            
            return {
                'primary_company': verification,
                'related_companies': unique_related[:10],  # Limit to 10
                'network_analysis': {
                    'total_related_found': len(unique_related),
                    'officer_connections': len(officer_names),
                    'network_complexity': 'high' if len(unique_related) > 5 else 'medium' if len(unique_related) > 2 else 'low'
                },
                'analysis_date': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting corporate network: {e}")
            return {
                'found': False,
                'company_name': company_name,
                'error': str(e)
            }