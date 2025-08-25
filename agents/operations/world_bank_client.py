"""
World Bank API Client

Provides access to World Bank indicators for geopolitical and economic risk assessment
"""

import logging
import asyncio
import aiohttp
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import pandas as pd

logger = logging.getLogger(__name__)

class WorldBankClient:
    """
    Client for accessing World Bank Open Data API
    """
    
    BASE_URL = "https://api.worldbank.org/v2"
    
    # Key indicators for geopolitical and economic risk assessment
    KEY_INDICATORS = {
        'NY.GDP.MKTP.CD': 'GDP (current US$)',
        'NY.GDP.PCAP.CD': 'GDP per capita (current US$)',
        'FP.CPI.TOTL.ZG': 'Inflation, consumer prices (annual %)',
        'SL.UEM.TOTL.ZS': 'Unemployment, total (% of total labor force)',
        'GC.DOD.TOTL.GD.ZS': 'Central government debt, total (% of GDP)',
        'BX.KLT.DINV.WD.GD.ZS': 'Foreign direct investment, net inflows (% of GDP)',
        'CC.EST': 'Control of Corruption: Estimate',
        'GE.EST': 'Government Effectiveness: Estimate',
        'PV.EST': 'Political Stability and Absence of Violence/Terrorism: Estimate',
        'RL.EST': 'Rule of Law: Estimate',
        'RQ.EST': 'Regulatory Quality: Estimate',
        'VA.EST': 'Voice and Accountability: Estimate'
    }
    
    def __init__(self):
        self.session = None
        self._country_cache = {}
        self._indicator_cache = {}
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def get_country_indicators(self, country_code: str, years: int = 3) -> Dict[str, Any]:
        """
        Get key economic and governance indicators for a country
        
        Args:
            country_code: ISO 3-letter country code or country name
            years: Number of recent years to fetch data for
            
        Returns:
            Dictionary containing country indicators and risk assessment
        """
        try:
            # Normalize country code
            country_iso = await self._get_country_iso_code(country_code)
            if not country_iso:
                logger.warning(f"Could not find ISO code for country: {country_code}")
                return self._get_default_country_data(country_code)
            
            # Check cache first
            cache_key = f"{country_iso}_{years}"
            if cache_key in self._indicator_cache:
                cache_time, data = self._indicator_cache[cache_key]
                if datetime.now() - cache_time < timedelta(hours=24):
                    return data
            
            if not self.session:
                self.session = aiohttp.ClientSession()
            
            # Fetch indicators
            indicators_data = {}
            for indicator_code, indicator_name in self.KEY_INDICATORS.items():
                try:
                    data = await self._fetch_indicator(country_iso, indicator_code, years)
                    if data:
                        indicators_data[indicator_code] = {
                            'name': indicator_name,
                            'values': data,
                            'latest_value': data[0]['value'] if data else None,
                            'trend': self._calculate_trend(data)
                        }
                except Exception as e:
                    logger.warning(f"Failed to fetch {indicator_name} for {country_iso}: {str(e)}")
                    continue
            
            # Calculate risk scores
            result = {
                'country_code': country_iso,
                'country_name': country_code,
                'indicators': indicators_data,
                'economic_risk_score': self._calculate_economic_risk(indicators_data),
                'governance_risk_score': self._calculate_governance_risk(indicators_data),
                'overall_country_risk': 0,
                'data_timestamp': datetime.now().isoformat()
            }
            
            # Calculate overall country risk
            result['overall_country_risk'] = (
                result['economic_risk_score'] * 0.6 + 
                result['governance_risk_score'] * 0.4
            )
            
            # Cache the result
            self._indicator_cache[cache_key] = (datetime.now(), result)
            
            return result
            
        except Exception as e:
            logger.error(f"Error fetching country indicators for {country_code}: {str(e)}")
            return self._get_default_country_data(country_code)
    
    async def _get_country_iso_code(self, country_input: str) -> Optional[str]:
        """Convert country name to ISO 3-letter code"""
        try:
            # Check cache first
            if country_input in self._country_cache:
                return self._country_cache[country_input]
            
            # If already looks like ISO code, validate it
            if len(country_input) == 3 and country_input.isupper():
                return country_input
            
            if not self.session:
                self.session = aiohttp.ClientSession()
            
            # Search for country
            url = f"{self.BASE_URL}/country"
            params = {
                'format': 'json',
                'per_page': 300
            }
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    if len(data) > 1:  # First element is metadata
                        countries = data[1]
                        
                        # Look for exact or partial match
                        country_input_lower = country_input.lower()
                        for country in countries:
                            country_name = country.get('name', '').lower()
                            country_id = country.get('id', '')
                            
                            if (country_input_lower == country_name or 
                                country_input_lower in country_name or
                                country_input.upper() == country_id):
                                
                                self._country_cache[country_input] = country_id
                                return country_id
            
            # Fallback: try common country mappings
            country_mappings = {
                'usa': 'USA', 'united states': 'USA', 'us': 'USA',
                'uk': 'GBR', 'united kingdom': 'GBR', 'britain': 'GBR',
                'china': 'CHN', 'prc': 'CHN',
                'russia': 'RUS', 'russian federation': 'RUS',
                'germany': 'DEU', 'deutschland': 'DEU',
                'japan': 'JPN', 'nippon': 'JPN',
                'india': 'IND', 'bharat': 'IND',
                'france': 'FRA', 'république française': 'FRA',
                'canada': 'CAN',
                'australia': 'AUS',
                'brazil': 'BRA', 'brasil': 'BRA',
                'south korea': 'KOR', 'korea': 'KOR',
                'italy': 'ITA', 'italia': 'ITA',
                'spain': 'ESP', 'españa': 'ESP',
                'netherlands': 'NLD', 'holland': 'NLD',
                'switzerland': 'CHE', 'schweiz': 'CHE',
                'sweden': 'SWE', 'sverige': 'SWE',
                'norway': 'NOR', 'norge': 'NOR',
                'denmark': 'DNK', 'danmark': 'DNK',
                'finland': 'FIN', 'suomi': 'FIN'
            }
            
            country_key = country_input.lower()
            if country_key in country_mappings:
                iso_code = country_mappings[country_key]
                self._country_cache[country_input] = iso_code
                return iso_code
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting ISO code for {country_input}: {str(e)}")
            return None
    
    async def _fetch_indicator(self, country_code: str, indicator_code: str, years: int) -> List[Dict]:
        """Fetch specific indicator data for a country"""
        try:
            url = f"{self.BASE_URL}/country/{country_code}/indicator/{indicator_code}"
            params = {
                'format': 'json',
                'per_page': years,
                'date': f"{datetime.now().year - years}:{datetime.now().year}"
            }
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    if len(data) > 1 and data[1]:  # First element is metadata
                        # Filter out null values and sort by date
                        valid_data = [
                            item for item in data[1] 
                            if item.get('value') is not None
                        ]
                        return sorted(valid_data, key=lambda x: x.get('date', ''), reverse=True)
            
            return []
            
        except Exception as e:
            logger.error(f"Error fetching indicator {indicator_code} for {country_code}: {str(e)}")
            return []
    
    def _calculate_trend(self, data: List[Dict]) -> str:
        """Calculate trend direction from time series data"""
        try:
            if len(data) < 2:
                return 'stable'
            
            values = [item['value'] for item in data if item.get('value') is not None]
            if len(values) < 2:
                return 'stable'
            
            # Simple trend calculation
            recent_avg = sum(values[:len(values)//2]) / (len(values)//2)
            older_avg = sum(values[len(values)//2:]) / (len(values) - len(values)//2)
            
            change_pct = ((recent_avg - older_avg) / older_avg) * 100 if older_avg != 0 else 0
            
            if change_pct > 5:
                return 'improving'
            elif change_pct < -5:
                return 'declining'
            else:
                return 'stable'
                
        except Exception:
            return 'stable'
    
    def _calculate_economic_risk(self, indicators: Dict[str, Any]) -> float:
        """Calculate economic risk score from indicators"""
        try:
            risk_score = 50  # Base score (moderate risk)
            
            # GDP per capita (higher = lower risk)
            gdp_per_capita = indicators.get('NY.GDP.PCAP.CD', {}).get('latest_value')
            if gdp_per_capita:
                if gdp_per_capita > 50000:
                    risk_score -= 15
                elif gdp_per_capita > 25000:
                    risk_score -= 10
                elif gdp_per_capita > 10000:
                    risk_score -= 5
                elif gdp_per_capita < 5000:
                    risk_score += 15
            
            # Inflation (higher = higher risk)
            inflation = indicators.get('FP.CPI.TOTL.ZG', {}).get('latest_value')
            if inflation:
                if inflation > 10:
                    risk_score += 20
                elif inflation > 5:
                    risk_score += 10
                elif inflation < 2:
                    risk_score -= 5
            
            # Unemployment (higher = higher risk)
            unemployment = indicators.get('SL.UEM.TOTL.ZS', {}).get('latest_value')
            if unemployment:
                if unemployment > 15:
                    risk_score += 15
                elif unemployment > 10:
                    risk_score += 10
                elif unemployment < 5:
                    risk_score -= 5
            
            # Government debt (higher = higher risk)
            debt = indicators.get('GC.DOD.TOTL.GD.ZS', {}).get('latest_value')
            if debt:
                if debt > 100:
                    risk_score += 15
                elif debt > 60:
                    risk_score += 10
                elif debt < 30:
                    risk_score -= 5
            
            # FDI inflows (higher = lower risk)
            fdi = indicators.get('BX.KLT.DINV.WD.GD.ZS', {}).get('latest_value')
            if fdi:
                if fdi > 5:
                    risk_score -= 10
                elif fdi > 2:
                    risk_score -= 5
                elif fdi < 0:
                    risk_score += 10
            
            return max(0, min(100, risk_score))
            
        except Exception as e:
            logger.error(f"Error calculating economic risk: {str(e)}")
            return 50.0
    
    def _calculate_governance_risk(self, indicators: Dict[str, Any]) -> float:
        """Calculate governance risk score from World Bank governance indicators"""
        try:
            governance_indicators = ['CC.EST', 'GE.EST', 'PV.EST', 'RL.EST', 'RQ.EST', 'VA.EST']
            scores = []
            
            for indicator in governance_indicators:
                value = indicators.get(indicator, {}).get('latest_value')
                if value is not None:
                    # World Bank governance indicators range from -2.5 to 2.5
                    # Convert to 0-100 risk scale (higher governance score = lower risk)
                    risk_score = 50 - (value * 20)  # Convert to 0-100 scale
                    scores.append(max(0, min(100, risk_score)))
            
            if scores:
                return sum(scores) / len(scores)
            else:
                return 50.0  # Default moderate risk if no governance data
                
        except Exception as e:
            logger.error(f"Error calculating governance risk: {str(e)}")
            return 50.0
    
    def _get_default_country_data(self, country_name: str) -> Dict[str, Any]:
        """Return default country data when API fails"""
        return {
            'country_code': 'UNKNOWN',
            'country_name': country_name,
            'indicators': {},
            'economic_risk_score': 50.0,
            'governance_risk_score': 50.0,
            'overall_country_risk': 50.0,
            'data_timestamp': datetime.now().isoformat(),
            'error': 'Unable to fetch World Bank data'
        }
    
    async def close(self):
        """Close the HTTP session"""
        if self.session:
            await self.session.close()
            self.session = None