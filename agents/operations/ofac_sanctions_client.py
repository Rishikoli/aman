"""
OFAC Sanctions List Client

Provides sanctions compliance checking against OFAC Specially Designated Nationals (SDN) list
"""

import logging
import asyncio
import aiohttp
import csv
import io
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import difflib
import re

logger = logging.getLogger(__name__)

class OFACSanctionsClient:
    """
    Client for checking entities against OFAC Sanctions lists
    """
    
    # OFAC SDN List URL (CSV format)
    SDN_LIST_URL = "https://www.treasury.gov/ofac/downloads/sdn.csv"
    CONSOLIDATED_LIST_URL = "https://www.treasury.gov/ofac/downloads/consolidated/consolidated.csv"
    
    def __init__(self):
        self.session = None
        self._sdn_list = []
        self._last_update = None
        self._update_interval = timedelta(hours=24)  # Update daily
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def check_entities(self, entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Check a list of entities against OFAC sanctions lists
        
        Args:
            entities: List of entity dictionaries containing name and other details
            
        Returns:
            List of check results with match information
        """
        try:
            # Ensure we have the latest sanctions data
            await self._update_sanctions_data()
            
            results = []
            for entity in entities:
                entity_name = entity.get('name', '').strip()
                if not entity_name:
                    continue
                
                # Check against SDN list
                match_result = await self._check_entity_against_sdn(entity_name, entity)
                
                results.append({
                    'entity': entity,
                    'entity_name': entity_name,
                    'match_found': match_result['match_found'],
                    'match_confidence': match_result['match_confidence'],
                    'matched_entries': match_result['matched_entries'],
                    'risk_level': self._calculate_risk_level(match_result),
                    'check_timestamp': datetime.now().isoformat()
                })
            
            return results
            
        except Exception as e:
            logger.error(f"Error checking entities against sanctions: {str(e)}")
            return [{'error': str(e), 'entities_checked': len(entities)}]
    
    async def _update_sanctions_data(self):
        """Update sanctions data if needed"""
        try:
            # Check if update is needed
            if (self._last_update and 
                datetime.now() - self._last_update < self._update_interval and
                self._sdn_list):
                return
            
            logger.info("Updating OFAC sanctions data...")
            
            if not self.session:
                self.session = aiohttp.ClientSession()
            
            # Download SDN list
            async with self.session.get(self.SDN_LIST_URL) as response:
                if response.status == 200:
                    content = await response.text()
                    self._sdn_list = self._parse_sdn_csv(content)
                    self._last_update = datetime.now()
                    logger.info(f"Updated SDN list with {len(self._sdn_list)} entries")
                else:
                    logger.warning(f"Failed to download SDN list: HTTP {response.status}")
                    if not self._sdn_list:
                        # Use fallback data if no existing data
                        self._sdn_list = self._get_fallback_sdn_data()
            
        except Exception as e:
            logger.error(f"Error updating sanctions data: {str(e)}")
            if not self._sdn_list:
                self._sdn_list = self._get_fallback_sdn_data()
    
    def _parse_sdn_csv(self, csv_content: str) -> List[Dict[str, Any]]:
        """Parse SDN CSV content into structured data"""
        try:
            sdn_entries = []
            csv_reader = csv.reader(io.StringIO(csv_content))
            
            # Skip header if present
            first_row = next(csv_reader, None)
            if first_row and not first_row[0].isdigit():
                # This is likely a header row, skip it
                pass
            else:
                # Process first row as data
                if first_row:
                    entry = self._parse_sdn_row(first_row)
                    if entry:
                        sdn_entries.append(entry)
            
            # Process remaining rows
            for row in csv_reader:
                entry = self._parse_sdn_row(row)
                if entry:
                    sdn_entries.append(entry)
            
            return sdn_entries
            
        except Exception as e:
            logger.error(f"Error parsing SDN CSV: {str(e)}")
            return []
    
    def _parse_sdn_row(self, row: List[str]) -> Optional[Dict[str, Any]]:
        """Parse a single SDN CSV row"""
        try:
            if len(row) < 2:
                return None
            
            # SDN CSV format: ent_num, sdn_name, sdn_type, program, title, call_sign, vess_type, tonnage, grt, vess_flag, vess_owner, remarks
            entry = {
                'ent_num': row[0].strip() if len(row) > 0 else '',
                'name': row[1].strip() if len(row) > 1 else '',
                'sdn_type': row[2].strip() if len(row) > 2 else '',
                'program': row[3].strip() if len(row) > 3 else '',
                'title': row[4].strip() if len(row) > 4 else '',
                'remarks': row[11].strip() if len(row) > 11 else '',
                'search_terms': []
            }
            
            # Generate search terms for matching
            if entry['name']:
                entry['search_terms'] = self._generate_search_terms(entry['name'])
            
            return entry if entry['name'] else None
            
        except Exception as e:
            logger.error(f"Error parsing SDN row: {str(e)}")
            return None
    
    def _generate_search_terms(self, name: str) -> List[str]:
        """Generate search terms for entity matching"""
        terms = [name.lower()]
        
        # Remove common business suffixes
        business_suffixes = [
            'inc', 'inc.', 'corp', 'corp.', 'ltd', 'ltd.', 'llc', 'llp',
            'company', 'co', 'co.', 'corporation', 'limited', 'enterprises',
            'group', 'holdings', 'international', 'intl', 'global'
        ]
        
        clean_name = name.lower()
        for suffix in business_suffixes:
            clean_name = re.sub(rf'\b{re.escape(suffix)}\b', '', clean_name)
        
        clean_name = re.sub(r'\s+', ' ', clean_name).strip()
        if clean_name and clean_name != name.lower():
            terms.append(clean_name)
        
        # Add individual words for partial matching
        words = re.findall(r'\b\w{3,}\b', clean_name)  # Words with 3+ characters
        terms.extend(words)
        
        return list(set(terms))  # Remove duplicates
    
    async def _check_entity_against_sdn(self, entity_name: str, entity_data: Dict[str, Any]) -> Dict[str, Any]:
        """Check a single entity against the SDN list"""
        try:
            if not self._sdn_list:
                return {
                    'match_found': False,
                    'match_confidence': 0.0,
                    'matched_entries': [],
                    'error': 'SDN list not available'
                }
            
            entity_search_terms = self._generate_search_terms(entity_name)
            matches = []
            
            for sdn_entry in self._sdn_list:
                confidence = self._calculate_match_confidence(
                    entity_search_terms, 
                    sdn_entry['search_terms'],
                    entity_name,
                    sdn_entry['name']
                )
                
                if confidence > 0.6:  # Threshold for potential match
                    matches.append({
                        'sdn_entry': sdn_entry,
                        'confidence': confidence,
                        'match_type': self._determine_match_type(confidence)
                    })
            
            # Sort by confidence
            matches.sort(key=lambda x: x['confidence'], reverse=True)
            
            # Determine if there's a significant match
            match_found = len(matches) > 0 and matches[0]['confidence'] > 0.8
            
            return {
                'match_found': match_found,
                'match_confidence': matches[0]['confidence'] if matches else 0.0,
                'matched_entries': matches[:5],  # Top 5 matches
                'total_potential_matches': len(matches)
            }
            
        except Exception as e:
            logger.error(f"Error checking entity {entity_name}: {str(e)}")
            return {
                'match_found': False,
                'match_confidence': 0.0,
                'matched_entries': [],
                'error': str(e)
            }
    
    def _calculate_match_confidence(self, entity_terms: List[str], sdn_terms: List[str], 
                                  entity_name: str, sdn_name: str) -> float:
        """Calculate confidence score for entity match"""
        try:
            # Exact name match
            if entity_name.lower() == sdn_name.lower():
                return 1.0
            
            # High similarity using difflib
            similarity = difflib.SequenceMatcher(None, entity_name.lower(), sdn_name.lower()).ratio()
            if similarity > 0.9:
                return similarity
            
            # Term-based matching
            entity_terms_set = set(entity_terms)
            sdn_terms_set = set(sdn_terms)
            
            if not entity_terms_set or not sdn_terms_set:
                return 0.0
            
            # Calculate Jaccard similarity
            intersection = len(entity_terms_set.intersection(sdn_terms_set))
            union = len(entity_terms_set.union(sdn_terms_set))
            
            jaccard_similarity = intersection / union if union > 0 else 0.0
            
            # Boost score if significant terms match
            significant_match_bonus = 0.0
            for term in entity_terms:
                if len(term) > 5 and term in sdn_terms:  # Longer terms are more significant
                    significant_match_bonus += 0.2
            
            final_score = min(1.0, max(similarity, jaccard_similarity) + significant_match_bonus)
            return final_score
            
        except Exception as e:
            logger.error(f"Error calculating match confidence: {str(e)}")
            return 0.0
    
    def _determine_match_type(self, confidence: float) -> str:
        """Determine the type of match based on confidence"""
        if confidence >= 0.95:
            return 'exact'
        elif confidence >= 0.85:
            return 'high'
        elif confidence >= 0.7:
            return 'medium'
        else:
            return 'low'
    
    def _calculate_risk_level(self, match_result: Dict[str, Any]) -> str:
        """Calculate risk level based on match results"""
        if match_result.get('match_found', False):
            confidence = match_result.get('match_confidence', 0.0)
            if confidence >= 0.95:
                return 'critical'
            elif confidence >= 0.85:
                return 'high'
            elif confidence >= 0.7:
                return 'medium'
            else:
                return 'low'
        else:
            return 'none'
    
    def _get_fallback_sdn_data(self) -> List[Dict[str, Any]]:
        """Provide fallback SDN data for testing/demo purposes"""
        return [
            {
                'ent_num': '00001',
                'name': 'DEMO SANCTIONED ENTITY',
                'sdn_type': 'Individual',
                'program': 'DEMO',
                'title': '',
                'remarks': 'Demo entry for testing purposes',
                'search_terms': ['demo', 'sanctioned', 'entity']
            },
            {
                'ent_num': '00002',
                'name': 'TEST BLOCKED COMPANY',
                'sdn_type': 'Entity',
                'program': 'TEST',
                'title': '',
                'remarks': 'Test entry for sanctions checking',
                'search_terms': ['test', 'blocked', 'company']
            }
        ]
    
    async def get_sanctions_statistics(self) -> Dict[str, Any]:
        """Get statistics about the current sanctions data"""
        try:
            await self._update_sanctions_data()
            
            if not self._sdn_list:
                return {'error': 'No sanctions data available'}
            
            # Analyze SDN list
            programs = {}
            entity_types = {}
            
            for entry in self._sdn_list:
                program = entry.get('program', 'Unknown')
                entity_type = entry.get('sdn_type', 'Unknown')
                
                programs[program] = programs.get(program, 0) + 1
                entity_types[entity_type] = entity_types.get(entity_type, 0) + 1
            
            return {
                'total_entries': len(self._sdn_list),
                'last_updated': self._last_update.isoformat() if self._last_update else None,
                'programs': programs,
                'entity_types': entity_types,
                'update_interval_hours': self._update_interval.total_seconds() / 3600
            }
            
        except Exception as e:
            logger.error(f"Error getting sanctions statistics: {str(e)}")
            return {'error': str(e)}
    
    async def close(self):
        """Close the HTTP session"""
        if self.session:
            await self.session.close()
            self.session = None