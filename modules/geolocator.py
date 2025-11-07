"""GeoLocator Module - IP geolocation services."""

import requests
from typing import Dict, Optional
from colorama import Fore, Style


class GeoLocator:
    """IP geolocation and mapping services."""
    
    def __init__(self, config):
        """Initialize geolocator."""
        self.config = config
        
    def locate(self, target: str) -> Optional[Dict]:
        """Get geolocation data for target IP."""
        try:
            # Using free ip-api.com service
            response = requests.get(f"http://ip-api.com/json/{target}", timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('status') == 'success':
                    geo_info = {
                        'ip': target,
                        'country': data.get('country', 'Unknown'),
                        'region': data.get('regionName', 'Unknown'),
                        'city': data.get('city', 'Unknown'),
                        'lat': data.get('lat', 0),
                        'lon': data.get('lon', 0),
                        'isp': data.get('isp', 'Unknown'),
                        'org': data.get('org', 'Unknown'),
                        'timezone': data.get('timezone', 'Unknown'),
                    }
                    
                    # Generate map links
                    lat, lon = geo_info['lat'], geo_info['lon']
                    geo_info['google_maps'] = f"https://www.google.com/maps?q={lat},{lon}"
                    geo_info['google_earth'] = f"https://earth.google.com/web/@{lat},{lon},0a,1000d,1y,0h,0t,0r"
                    
                    if self.config.verbose:
                        print(f"{Fore.CYAN}🌍 Location: {geo_info['city']}, {geo_info['country']}{Style.RESET_ALL}")
                        print(f"{Fore.CYAN}📍 Coordinates: {lat}, {lon}{Style.RESET_ALL}")
                    
                    return geo_info
        except Exception as e:
            if self.config.verbose:
                print(f"{Fore.YELLOW}⚠️  Geolocation failed: {str(e)}{Style.RESET_ALL}")
        
        return None
