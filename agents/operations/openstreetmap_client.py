"""
OpenStreetMap API Client

Provides geospatial analysis capabilities using OpenStreetMap Nominatim API
"""

import logging
import asyncio
import aiohttp
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta
import time

logger = logging.getLogger(__name__)

class OpenStreetMapClient:
    """
    Client for OpenStreetMap Nominatim geocoding and geospatial analysis
    """
    
    BASE_URL = "https://nominatim.openstreetmap.org"
    
    def __init__(self):
        self.session = None
        self._geocode_cache = {}
        self._rate_limit_delay = 1.0  # Nominatim requires 1 second between requests
        self._last_request_time = 0
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            headers={'User-Agent': 'AMAN-Operations-Agent/1.0'}
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def geocode(self, location: str) -> Optional[Tuple[float, float]]:
        """
        Geocode a location string to latitude/longitude coordinates
        
        Args:
            location: Location string (e.g., "New York, USA" or "Berlin, Germany")
            
        Returns:
            Tuple of (latitude, longitude) or None if not found
        """
        try:
            # Check cache first
            if location in self._geocode_cache:
                cache_time, coords = self._geocode_cache[location]
                if datetime.now() - cache_time < timedelta(days=30):
                    return coords
            
            if not self.session:
                self.session = aiohttp.ClientSession(
                    headers={'User-Agent': 'AMAN-Operations-Agent/1.0'}
                )
            
            # Rate limiting
            await self._rate_limit()
            
            url = f"{self.BASE_URL}/search"
            params = {
                'q': location,
                'format': 'json',
                'limit': 1,
                'addressdetails': 1
            }
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    if data:
                        result = data[0]
                        lat = float(result['lat'])
                        lon = float(result['lon'])
                        coords = (lat, lon)
                        
                        # Cache the result
                        self._geocode_cache[location] = (datetime.now(), coords)
                        
                        return coords
            
            return None
            
        except Exception as e:
            logger.error(f"Error geocoding location {location}: {str(e)}")
            return None
    
    async def reverse_geocode(self, lat: float, lon: float) -> Optional[Dict[str, Any]]:
        """
        Reverse geocode coordinates to location information
        
        Args:
            lat: Latitude
            lon: Longitude
            
        Returns:
            Dictionary with location details or None if not found
        """
        try:
            if not self.session:
                self.session = aiohttp.ClientSession(
                    headers={'User-Agent': 'AMAN-Operations-Agent/1.0'}
                )
            
            # Rate limiting
            await self._rate_limit()
            
            url = f"{self.BASE_URL}/reverse"
            params = {
                'lat': lat,
                'lon': lon,
                'format': 'json',
                'addressdetails': 1
            }
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    if data:
                        address = data.get('address', {})
                        return {
                            'display_name': data.get('display_name'),
                            'country': address.get('country'),
                            'country_code': address.get('country_code', '').upper(),
                            'state': address.get('state'),
                            'city': address.get('city') or address.get('town') or address.get('village'),
                            'postcode': address.get('postcode'),
                            'coordinates': (lat, lon)
                        }
            
            return None
            
        except Exception as e:
            logger.error(f"Error reverse geocoding {lat}, {lon}: {str(e)}")
            return None
    
    async def find_nearby_facilities(self, lat: float, lon: float, 
                                   facility_type: str = "industrial", 
                                   radius_km: float = 50.0) -> List[Dict[str, Any]]:
        """
        Find nearby facilities of a specific type
        
        Args:
            lat: Latitude of center point
            lon: Longitude of center point
            facility_type: Type of facility to search for
            radius_km: Search radius in kilometers
            
        Returns:
            List of nearby facilities with their details
        """
        try:
            if not self.session:
                self.session = aiohttp.ClientSession(
                    headers={'User-Agent': 'AMAN-Operations-Agent/1.0'}
                )
            
            # Rate limiting
            await self._rate_limit()
            
            # Map facility types to OSM amenity/landuse tags
            facility_mappings = {
                'industrial': 'landuse=industrial',
                'commercial': 'landuse=commercial',
                'port': 'amenity=ferry_terminal',
                'airport': 'aeroway=aerodrome',
                'warehouse': 'building=warehouse',
                'factory': 'man_made=works',
                'logistics': 'amenity=post_office'
            }
            
            query_tag = facility_mappings.get(facility_type, 'landuse=industrial')
            
            # Use Overpass API for more detailed queries
            overpass_url = "https://overpass-api.de/api/interpreter"
            
            # Calculate bounding box
            lat_offset = radius_km / 111.0  # Rough conversion
            lon_offset = radius_km / (111.0 * abs(lat))
            
            bbox = f"{lat - lat_offset},{lon - lon_offset},{lat + lat_offset},{lon + lon_offset}"
            
            overpass_query = f"""
            [out:json][timeout:25];
            (
              way[{query_tag}]({bbox});
              relation[{query_tag}]({bbox});
            );
            out center meta;
            """
            
            async with self.session.post(overpass_url, data=overpass_query) as response:
                if response.status == 200:
                    data = await response.json()
                    facilities = []
                    
                    for element in data.get('elements', []):
                        if 'center' in element or ('lat' in element and 'lon' in element):
                            center = element.get('center', {
                                'lat': element.get('lat'),
                                'lon': element.get('lon')
                            })
                            
                            if center.get('lat') and center.get('lon'):
                                facility = {
                                    'id': element.get('id'),
                                    'type': facility_type,
                                    'name': element.get('tags', {}).get('name', 'Unknown'),
                                    'latitude': center['lat'],
                                    'longitude': center['lon'],
                                    'tags': element.get('tags', {}),
                                    'distance_km': self._calculate_distance(
                                        lat, lon, center['lat'], center['lon']
                                    )
                                }
                                facilities.append(facility)
                    
                    # Sort by distance
                    facilities.sort(key=lambda x: x['distance_km'])
                    return facilities[:20]  # Limit to 20 results
            
            return []
            
        except Exception as e:
            logger.error(f"Error finding nearby facilities: {str(e)}")
            return []
    
    async def analyze_geographic_distribution(self, locations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze geographic distribution of locations
        
        Args:
            locations: List of location dictionaries with coordinates
            
        Returns:
            Analysis of geographic distribution
        """
        try:
            if not locations:
                return {'error': 'No locations provided'}
            
            # Extract coordinates
            coordinates = []
            countries = set()
            regions = set()
            
            for location in locations:
                if 'latitude' in location and 'longitude' in location:
                    lat, lon = location['latitude'], location['longitude']
                    coordinates.append((lat, lon))
                    
                    # Get country information
                    if 'country' in location:
                        countries.add(location['country'])
                    
                    # Determine region based on coordinates
                    region = self._get_region_from_coordinates(lat, lon)
                    if region:
                        regions.add(region)
            
            if not coordinates:
                return {'error': 'No valid coordinates found'}
            
            # Calculate geographic metrics
            analysis = {
                'total_locations': len(locations),
                'valid_coordinates': len(coordinates),
                'countries': list(countries),
                'regions': list(regions),
                'geographic_spread': self._calculate_geographic_spread(coordinates),
                'centroid': self._calculate_centroid(coordinates),
                'distribution_metrics': self._calculate_distribution_metrics(coordinates)
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing geographic distribution: {str(e)}")
            return {'error': str(e)}
    
    async def _rate_limit(self):
        """Implement rate limiting for Nominatim API"""
        current_time = time.time()
        time_since_last = current_time - self._last_request_time
        
        if time_since_last < self._rate_limit_delay:
            await asyncio.sleep(self._rate_limit_delay - time_since_last)
        
        self._last_request_time = time.time()
    
    def _calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance between two coordinates using Haversine formula"""
        import math
        
        # Convert to radians
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        
        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        # Earth's radius in kilometers
        r = 6371
        
        return c * r
    
    def _get_region_from_coordinates(self, lat: float, lon: float) -> str:
        """Determine geographic region from coordinates"""
        # Simple region classification based on coordinates
        if lat > 60:
            return "Arctic"
        elif lat > 35:
            if lon > -30 and lon < 60:
                return "Europe"
            elif lon >= 60 and lon < 150:
                return "Asia"
            elif lon >= -170 and lon < -30:
                return "North America"
        elif lat > -35:
            if lon > -20 and lon < 60:
                return "Africa/Middle East"
            elif lon >= 60 and lon < 150:
                return "Asia"
            elif lon >= -170 and lon < -30:
                return "Americas"
            elif lon >= 150 or lon < -170:
                return "Oceania"
        else:
            if lon > -80 and lon < -30:
                return "South America"
            elif lon >= -30 and lon < 60:
                return "Africa"
            elif lon >= 60 and lon < 180:
                return "Asia/Oceania"
            else:
                return "Antarctica"
        
        return "Unknown"
    
    def _calculate_geographic_spread(self, coordinates: List[Tuple[float, float]]) -> float:
        """Calculate the geographic spread of coordinates"""
        if len(coordinates) < 2:
            return 0.0
        
        # Calculate maximum distance between any two points
        max_distance = 0.0
        for i in range(len(coordinates)):
            for j in range(i + 1, len(coordinates)):
                distance = self._calculate_distance(
                    coordinates[i][0], coordinates[i][1],
                    coordinates[j][0], coordinates[j][1]
                )
                max_distance = max(max_distance, distance)
        
        return max_distance
    
    def _calculate_centroid(self, coordinates: List[Tuple[float, float]]) -> Tuple[float, float]:
        """Calculate the geographic centroid of coordinates"""
        if not coordinates:
            return (0.0, 0.0)
        
        lat_sum = sum(coord[0] for coord in coordinates)
        lon_sum = sum(coord[1] for coord in coordinates)
        
        return (lat_sum / len(coordinates), lon_sum / len(coordinates))
    
    def _calculate_distribution_metrics(self, coordinates: List[Tuple[float, float]]) -> Dict[str, float]:
        """Calculate distribution metrics for coordinates"""
        if not coordinates:
            return {}
        
        # Calculate standard deviations
        centroid = self._calculate_centroid(coordinates)
        
        lat_variance = sum((coord[0] - centroid[0])**2 for coord in coordinates) / len(coordinates)
        lon_variance = sum((coord[1] - centroid[1])**2 for coord in coordinates) / len(coordinates)
        
        # Calculate average distance from centroid
        avg_distance = sum(
            self._calculate_distance(centroid[0], centroid[1], coord[0], coord[1])
            for coord in coordinates
        ) / len(coordinates)
        
        return {
            'latitude_std': lat_variance ** 0.5,
            'longitude_std': lon_variance ** 0.5,
            'average_distance_from_centroid': avg_distance,
            'geographic_concentration': 1.0 / (1.0 + avg_distance / 1000)  # Normalized concentration score
        }
    
    async def close(self):
        """Close the HTTP session"""
        if self.session:
            await self.session.close()
            self.session = None