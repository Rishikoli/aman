"""
SEC EDGAR API Client for fetching legal filings and regulatory documents
Uses the SEC EDGAR API to retrieve 10-K, 8-K, and other regulatory filings
"""

import logging
import requests
import time
import json
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import os
from pathlib import Path
import re

logger = logging.getLogger(__name__)

class SECEdgarClient:
    """
    Client for accessing SEC EDGAR database for legal filings
    """
    
    def __init__(self, user_agent: str = "AMAN Legal Agent 1.0"):
        """
        Initialize SEC EDGAR client
        
        Args:
            user_agent: User agent string for SEC API requests (required by SEC)
        """
        self.base_url = "https://data.sec.gov"
        self.user_agent = user_agent
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': self.user_agent,
            'Accept-Encoding': 'gzip, deflate',
            'Host': 'data.sec.gov'
        })
        
        # Rate limiting: SEC allows 10 requests per second
        self.rate_limit_delay = 0.1  # 100ms between requests
        self.last_request_time = 0
        
        # Cache directory for downloaded filings
        self.cache_dir = Path("temp/sec_filings")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info("SEC EDGAR client initialized")
    
    def _rate_limit(self):
        """Enforce rate limiting for SEC API requests"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.rate_limit_delay:
            sleep_time = self.rate_limit_delay - time_since_last
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def _make_request(self, url: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """
        Make a rate-limited request to SEC API
        
        Args:
            url: API endpoint URL
            params: Query parameters
            
        Returns:
            JSON response data or None if failed
        """
        try:
            self._rate_limit()
            
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            if response.headers.get('content-type', '').startswith('application/json'):
                return response.json()
            else:
                return {'content': response.text}
                
        except requests.exceptions.RequestException as e:
            logger.error(f"SEC API request failed: {e}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse SEC API response: {e}")
            return None
    
    def search_company_filings(self, cik: str, form_types: List[str] = None, 
                             limit: int = 10) -> Optional[Dict]:
        """
        Search for company filings by CIK
        
        Args:
            cik: Central Index Key (company identifier)
            form_types: List of form types to search for (e.g., ['10-K', '8-K'])
            limit: Maximum number of filings to return
            
        Returns:
            Filing search results
        """
        if form_types is None:
            form_types = ['10-K', '10-Q', '8-K', 'DEF 14A']
        
        # Normalize CIK (pad with zeros to 10 digits)
        cik_padded = str(cik).zfill(10)
        
        url = f"{self.base_url}/submissions/CIK{cik_padded}.json"
        
        try:
            data = self._make_request(url)
            if not data:
                return None
            
            # Filter filings by form type
            filings = data.get('filings', {}).get('recent', {})
            if not filings:
                return None
            
            filtered_filings = []
            forms = filings.get('form', [])
            filing_dates = filings.get('filingDate', [])
            accession_numbers = filings.get('accessionNumber', [])
            primary_documents = filings.get('primaryDocument', [])
            
            for i, form in enumerate(forms[:limit * 2]):  # Get more to filter
                if form in form_types and len(filtered_filings) < limit:
                    filtered_filings.append({
                        'form_type': form,
                        'filing_date': filing_dates[i] if i < len(filing_dates) else None,
                        'accession_number': accession_numbers[i] if i < len(accession_numbers) else None,
                        'primary_document': primary_documents[i] if i < len(primary_documents) else None,
                        'cik': cik_padded
                    })
            
            return {
                'company_info': {
                    'cik': cik_padded,
                    'name': data.get('name', 'Unknown'),
                    'sic': data.get('sic', ''),
                    'sicDescription': data.get('sicDescription', ''),
                    'tickers': data.get('tickers', []),
                    'exchanges': data.get('exchanges', [])
                },
                'filings': filtered_filings,
                'total_found': len(filtered_filings)
            }
            
        except Exception as e:
            logger.error(f"Error searching company filings: {e}")
            return None
    
    def get_filing_content(self, cik: str, accession_number: str, 
                          primary_document: str) -> Optional[str]:
        """
        Retrieve the full text content of a specific filing
        
        Args:
            cik: Central Index Key
            accession_number: Filing accession number
            primary_document: Primary document filename
            
        Returns:
            Filing content as text
        """
        try:
            # Normalize CIK and accession number
            cik_padded = str(cik).zfill(10)
            accession_clean = accession_number.replace('-', '')
            
            # Construct filing URL
            url = f"{self.base_url}/Archives/edgar/data/{int(cik)}/{accession_clean}/{primary_document}"
            
            # Check cache first
            cache_file = self.cache_dir / f"{cik_padded}_{accession_number}_{primary_document}.txt"
            if cache_file.exists():
                logger.info(f"Loading filing from cache: {cache_file}")
                return cache_file.read_text(encoding='utf-8', errors='ignore')
            
            # Fetch from SEC
            response = self._make_request(url)
            if not response:
                return None
            
            content = response.get('content', '')
            
            # Cache the content
            try:
                cache_file.write_text(content, encoding='utf-8')
                logger.info(f"Cached filing content: {cache_file}")
            except Exception as e:
                logger.warning(f"Failed to cache filing: {e}")
            
            return content
            
        except Exception as e:
            logger.error(f"Error retrieving filing content: {e}")
            return None
    
    def search_company_by_ticker(self, ticker: str) -> Optional[Dict]:
        """
        Search for company information by ticker symbol
        
        Args:
            ticker: Stock ticker symbol
            
        Returns:
            Company information including CIK
        """
        try:
            # Use company tickers JSON endpoint
            url = f"{self.base_url}/files/company_tickers.json"
            
            data = self._make_request(url)
            if not data:
                return None
            
            # Search for ticker in the data
            ticker_upper = ticker.upper()
            
            for key, company_info in data.items():
                if company_info.get('ticker', '').upper() == ticker_upper:
                    return {
                        'cik': str(company_info.get('cik_str', '')).zfill(10),
                        'name': company_info.get('title', ''),
                        'ticker': company_info.get('ticker', ''),
                        'found': True
                    }
            
            return {'found': False, 'ticker': ticker}
            
        except Exception as e:
            logger.error(f"Error searching company by ticker: {e}")
            return None
    
    def get_recent_8k_filings(self, cik: str, days_back: int = 30) -> List[Dict]:
        """
        Get recent 8-K filings for a company (material events)
        
        Args:
            cik: Central Index Key
            days_back: Number of days to look back
            
        Returns:
            List of recent 8-K filings
        """
        try:
            filings_data = self.search_company_filings(cik, ['8-K'], limit=50)
            if not filings_data:
                return []
            
            cutoff_date = datetime.now() - timedelta(days=days_back)
            recent_filings = []
            
            for filing in filings_data.get('filings', []):
                filing_date_str = filing.get('filing_date', '')
                if filing_date_str:
                    try:
                        filing_date = datetime.strptime(filing_date_str, '%Y-%m-%d')
                        if filing_date >= cutoff_date:
                            recent_filings.append(filing)
                    except ValueError:
                        continue
            
            return recent_filings
            
        except Exception as e:
            logger.error(f"Error getting recent 8-K filings: {e}")
            return []
    
    def extract_legal_risks_from_10k(self, cik: str) -> Dict[str, Any]:
        """
        Extract legal risks and litigation information from most recent 10-K filing
        
        Args:
            cik: Central Index Key
            
        Returns:
            Extracted legal risk information
        """
        try:
            # Get most recent 10-K filing
            filings_data = self.search_company_filings(cik, ['10-K'], limit=1)
            if not filings_data or not filings_data.get('filings'):
                return {'error': 'No 10-K filings found'}
            
            filing = filings_data['filings'][0]
            content = self.get_filing_content(
                cik, 
                filing['accession_number'], 
                filing['primary_document']
            )
            
            if not content:
                return {'error': 'Could not retrieve filing content'}
            
            # Extract legal proceedings section (Item 3)
            legal_risks = self._extract_legal_proceedings(content)
            
            # Extract risk factors (Item 1A)
            risk_factors = self._extract_risk_factors(content)
            
            return {
                'company_info': filings_data.get('company_info', {}),
                'filing_info': filing,
                'legal_proceedings': legal_risks,
                'risk_factors': risk_factors,
                'analysis_date': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error extracting legal risks from 10-K: {e}")
            return {'error': str(e)}
    
    def _extract_legal_proceedings(self, content: str) -> Dict[str, Any]:
        """Extract legal proceedings section from 10-K filing"""
        try:
            # Look for Item 3 - Legal Proceedings
            patterns = [
                r'item\s*3\s*[.\-–—]*\s*legal\s*proceedings(.*?)(?=item\s*[4-9]|$)',
                r'legal\s*proceedings(.*?)(?=item\s*[4-9]|risk\s*factors|$)'
            ]
            
            content_lower = content.lower()
            legal_section = ""
            
            for pattern in patterns:
                match = re.search(pattern, content_lower, re.DOTALL | re.IGNORECASE)
                if match:
                    legal_section = match.group(1).strip()
                    break
            
            if not legal_section:
                return {'found': False, 'content': ''}
            
            # Extract key information
            litigation_indicators = [
                'lawsuit', 'litigation', 'legal proceeding', 'court',
                'plaintiff', 'defendant', 'settlement', 'damages',
                'injunction', 'regulatory action', 'investigation'
            ]
            
            found_indicators = []
            for indicator in litigation_indicators:
                if indicator in legal_section:
                    found_indicators.append(indicator)
            
            return {
                'found': True,
                'content': legal_section[:2000],  # Limit content length
                'indicators': found_indicators,
                'risk_level': 'high' if len(found_indicators) > 3 else 'medium' if found_indicators else 'low'
            }
            
        except Exception as e:
            logger.error(f"Error extracting legal proceedings: {e}")
            return {'found': False, 'error': str(e)}
    
    def _extract_risk_factors(self, content: str) -> Dict[str, Any]:
        """Extract risk factors section from 10-K filing"""
        try:
            # Look for Item 1A - Risk Factors
            patterns = [
                r'item\s*1a\s*[.\-–—]*\s*risk\s*factors(.*?)(?=item\s*[2-9]|$)',
                r'risk\s*factors(.*?)(?=item\s*[2-9]|unresolved|$)'
            ]
            
            content_lower = content.lower()
            risk_section = ""
            
            for pattern in patterns:
                match = re.search(pattern, content_lower, re.DOTALL | re.IGNORECASE)
                if match:
                    risk_section = match.group(1).strip()
                    break
            
            if not risk_section:
                return {'found': False, 'content': ''}
            
            # Extract legal-related risks
            legal_risk_keywords = [
                'legal', 'litigation', 'regulatory', 'compliance',
                'lawsuit', 'investigation', 'enforcement', 'penalty',
                'violation', 'sanctions', 'intellectual property'
            ]
            
            legal_risks = []
            sentences = re.split(r'[.!?]+', risk_section)
            
            for sentence in sentences[:50]:  # Limit to first 50 sentences
                sentence_lower = sentence.lower().strip()
                if len(sentence_lower) > 50:  # Skip very short sentences
                    for keyword in legal_risk_keywords:
                        if keyword in sentence_lower:
                            legal_risks.append({
                                'sentence': sentence.strip(),
                                'keyword': keyword,
                                'risk_type': 'legal'
                            })
                            break
            
            return {
                'found': True,
                'content': risk_section[:3000],  # Limit content length
                'legal_risks': legal_risks[:10],  # Top 10 legal risks
                'total_risks_found': len(legal_risks)
            }
            
        except Exception as e:
            logger.error(f"Error extracting risk factors: {e}")
            return {'found': False, 'error': str(e)}
    
    def get_company_legal_intelligence(self, ticker_or_cik: str) -> Dict[str, Any]:
        """
        Get comprehensive legal intelligence for a company
        
        Args:
            ticker_or_cik: Stock ticker or CIK
            
        Returns:
            Comprehensive legal intelligence report
        """
        try:
            # Determine if input is ticker or CIK
            if ticker_or_cik.isdigit() and len(ticker_or_cik) >= 6:
                cik = ticker_or_cik
                company_info = {'cik': cik}
            else:
                # Search by ticker
                company_info = self.search_company_by_ticker(ticker_or_cik)
                if not company_info or not company_info.get('found'):
                    return {'error': f'Company not found: {ticker_or_cik}'}
                cik = company_info['cik']
            
            # Get legal risks from 10-K
            legal_analysis = self.extract_legal_risks_from_10k(cik)
            
            # Get recent 8-K filings (material events)
            recent_8k = self.get_recent_8k_filings(cik, days_back=90)
            
            # Get all recent filings for context
            all_filings = self.search_company_filings(cik, limit=20)
            
            return {
                'company_info': company_info,
                'legal_analysis': legal_analysis,
                'recent_material_events': recent_8k,
                'recent_filings': all_filings.get('filings', []) if all_filings else [],
                'analysis_timestamp': datetime.now().isoformat(),
                'data_source': 'SEC EDGAR'
            }
            
        except Exception as e:
            logger.error(f"Error getting company legal intelligence: {e}")
            return {'error': str(e)}