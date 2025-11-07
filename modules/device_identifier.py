"""Device Identifier Module - Advanced camera fingerprinting."""

import requests
from typing import List, Dict
from colorama import Fore, Style
from urllib3.exceptions import InsecureRequestWarning

# Suppress SSL warnings for security testing
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class DeviceIdentifier:
    """Advanced device fingerprinting for cameras and DVR systems."""
    
    DEVICE_SIGNATURES = {
        'CP Plus': [
            b'CP-UVR',
            b'CP Plus',
            b'CPPLUS',
            b'CP-Plus',
            b'/cp_',
        ],
        'Hikvision': [
            b'Hikvision',
            b'HIKVISION',
            b'/doc/page/login.asp',
            b'DVR Login',
        ],
        'Dahua': [
            b'Dahua',
            b'DAHUA',
            b'/RPC2_Login',
        ],
        'Axis': [
            b'AXIS',
            b'axis-cgi',
        ],
        'Foscam': [
            b'Foscam',
            b'FOSCAM',
        ],
        'TP-Link': [
            b'TP-LINK',
            b'tplink',
        ],
        'D-Link': [
            b'D-Link',
            b'DLINK',
        ],
        'Generic DVR': [
            b'DVR',
            b'NVR',
            b'Digital Video Recorder',
        ],
    }
    
    def __init__(self, config):
        """Initialize device identifier."""
        self.config = config
        
    def identify_device(self, target: str, port: int) -> Dict:
        """Identify device type from HTTP response."""
        device_info = {
            'port': port,
            'brand': 'Unknown',
            'confidence': 'Low',
            'details': []
        }
        
        protocols = ['http', 'https'] if port in [443, 8443] else ['http']
        
        for protocol in protocols:
            try:
                url = f"{protocol}://{target}:{port}"
                response = requests.get(url, timeout=3, verify=False, allow_redirects=True)
                
                content = response.content
                headers = str(response.headers).encode()
                
                # Check signatures
                for brand, signatures in self.DEVICE_SIGNATURES.items():
                    matches = sum(1 for sig in signatures if sig in content or sig in headers)
                    if matches > 0:
                        device_info['brand'] = brand
                        device_info['confidence'] = 'High' if matches > 1 else 'Medium'
                        device_info['details'].append(f"Matched {matches} signature(s)")
                        break
                
                # Check for CP Plus specific model
                if b'CP-UVR-0401E1-IC2' in content:
                    device_info['brand'] = 'CP Plus CP-UVR-0401E1-IC2'
                    device_info['confidence'] = 'Very High'
                    device_info['details'].append('Exact model detected')
                
                if device_info['brand'] != 'Unknown':
                    break
                    
            except:
                continue
        
        return device_info
    
    def identify(self, open_ports: List[int]) -> List[Dict]:
        """Identify all devices on open ports."""
        identified = []
        
        for port in open_ports:
            device = self.identify_device(self.config.target, port)
            if device['brand'] != 'Unknown' or self.config.verbose:
                identified.append(device)
                print(f"{Fore.YELLOW}📱 Port {port}: {device['brand']} "
                      f"({device['confidence']} Confidence){Style.RESET_ALL}")
        
        return identified
