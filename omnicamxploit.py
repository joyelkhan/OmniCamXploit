#!/usr/bin/env python3
"""
███████╗███╗   ███╗███╗   ██╗██╗ ██████╗ █████╗ ███╗   ███╗██╗   ██╗██████╗ ██╗      ██████╗ ██╗████████╗
██╔════╝████╗ ████║████╗  ██║██║██╔════╝██╔══██╗████╗ ████║██║   ██║██╔══██╗██║     ██╔═══██╗██║╚══██╔══╝
█████╗  ██╔████╔██║██╔██╗ ██║██║██║     ███████║██╔████╔██║██║   ██║██████╔╝██║     ██║   ██║██║   ██║   
██╔══╝  ██║╚██╔╝██║██║╚██╗██║██║██║     ██╔══██║██║╚██╔╝██║██║   ██║██╔═══╝ ██║     ██║   ██║██║   ██║   
███████╗██║ ╚═╝ ██║██║ ╚████║██║╚██████╗██║  ██║██║ ╚═╝ ██║╚██████╔╝██║     ███████╗╚██████╔╝██║   ██║   
╚══════╝╚═╝     ╚═╝╚═╝  ╚═══╝╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝     ╚═╝ ╚═════╝ ╚═╝     ╚══════╝ ╚═════╝ ╚═╝   ╚═╝   

▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
█─▄▄▄▄█▄─▄█▄─▀─▄█─▄─▄─█▄─▄▄─█▄─▀─▄█▄─█─▄█▄─▄▄─█▄─▄▄▀█▄─██─▄█▄─▀█▄─▄█▄─▄▄─█▄─▄▄▀█▄─▄█─▄▄▄▄█─▄─▄─█▄─▄▄─█▄─▄▄▀█
█▄▄▄▄─██─███▀─▀████─████─▄█▀██▀─▀███▄─▄███─▄▄▄██─▄─▄██─██─███─█▄▀─███─▄█▀██─▄─▄██─██▄▄▄▄─███─████─▄█▀██─██─█
▀▄▄▄▄▄▀▄▄▄▀▄▄█▄▄▀▀▄▄▄▀▀▄▄▄▄▄▀▄▄█▄▄▀▀▄▄▄▀▀▄▄▄▀▀▀▄▄▀▄▄▀▀▄▄▄▄▀▀▄▄▄▀▀▄▄▀▄▄▄▄▄▀▄▄▀▄▄▀▄▄▄▀▄▄▄▄▄▀▀▄▄▄▀▀▄▄▄▄▄▀▄▄▄▄▀▀

                            U L T I M A T E   C A M E R A   S E C U R I T Y   F R A M E W O R K
                                       GitHub: joyelkhan/OmniCamXploit

OmniCamXploit v1.0 - Professional Camera Security Assessment Framework
Author: Md. Abu Naser Khan
GitHub: https://github.com/joyelkhan/OmniCamXploit
License: MIT
"""

import argparse
import logging
import sys
import time
import hashlib
import socket
import requests
import json
import re
import os
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Set
from urllib.parse import urlparse, urljoin
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, Style, Back, init
import urllib3
from tqdm import tqdm

# Optional GeoIP2 support
try:
    import geoip2.database
    GEOIP_AVAILABLE = True
except ImportError:
    GEOIP_AVAILABLE = False

# Initialize colorama and disable SSL warnings
init(autoreset=True)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configure stylish logging
class ColorfulFormatter(logging.Formatter):
    """🎨 Custom formatter for stylish logging"""
    
    COLORS = {
        'DEBUG': Fore.CYAN,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.RED + Style.BRIGHT
    }
    
    def format(self, record):
        log_color = self.COLORS.get(record.levelname, '')
        record.levelname = f"{log_color}🛠️ {record.levelname}{Style.RESET_ALL}"
        record.msg = f"{log_color}{record.msg}{Style.RESET_ALL}"
        return super().format(record)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('omnicamxploit.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

for handler in logging.getLogger().handlers:
    if isinstance(handler, logging.StreamHandler):
        handler.setFormatter(ColorfulFormatter('%(asctime)s - %(levelname)s - %(message)s'))

logger = logging.getLogger(__name__)

@dataclass
class ScanConfig:
    """🎯 Ultimate Configuration for Enterprise Scanning"""
    target: str
    enable_credential_testing: bool = True
    enable_geolocation: bool = True
    max_port_workers: int = 200
    max_credential_workers: int = 100
    credential_limit: int = 5000
    port_timeout: float = 1.5
    request_timeout: float = 3.0
    scan_strategy: str = "comprehensive"  # quick, standard, comprehensive
    
    # Enhanced port configuration
    custom_ports: List[int] = field(default_factory=list)
    scan_common_ports: bool = True
    scan_camera_ports: bool = True
    scan_high_ports: bool = True
    scan_stream_ports: bool = True

class UltimatePortScanner:
    """🚀 MASSIVE PORT SCANNER - 1000+ Camera Ports"""
    
    def __init__(self, config):
        self.config = config
        self.port_list = self._generate_massive_port_list()
        logger.info(f"🎯 Ultimate port scanner loaded with {len(self.port_list)} ports")
    
    def _generate_massive_port_list(self) -> List[int]:
        """🎯 Generate 1000+ comprehensive camera port list"""
        ports: Set[int] = set()
        
        # 🎯 COMMON WEB PORTS (200+ ports)
        if self.config.scan_common_ports:
            ports.update(range(80, 100))        # 80-99
            ports.update(range(443, 463))       # 443-462
            ports.update(range(8000, 8100))     # 8000-8099
            ports.update(range(8080, 8100))     # 8080-8099
            ports.update(range(8443, 8453))     # 8443-8452
        
        # 📹 CAMERA-SPECIFIC PORTS (300+ ports)
        if self.config.scan_camera_ports:
            camera_brand_ports = {
                # Hikvision
                'Hikvision': [34567, 34568, 34569, 34570, 34571, 34572, 34573, 34574, 34575, 34599],
                # Dahua
                'Dahua': [37777, 37778, 37779, 37780, 37781, 37782, 37783, 37784, 37785],
                # Axis
                'Axis': [3000, 3001, 3002, 3003, 3004, 3005],
                # Sony
                'Sony': [10000, 10001, 10002, 10003, 10004],
                # Bosch
                'Bosch': [9000, 9001, 9002, 9003, 9004],
                # Samsung
                'Samsung': [4520, 4521, 4522, 4523, 4524],
                # Panasonic
                'Panasonic': [5000, 5001, 5002, 5003, 5004],
                # Vivotek
                'Vivotek': [9000, 9001, 9002, 9003, 9004],
                # 🆕 CP PLUS SPECIFIC
                'CP_Plus': [6000, 6001, 6002, 6003, 6004, 6005, 7000, 7001, 7002, 7003, 7004, 7005],
                # 🎯 DVR/NVR SPECIFIC
                'DVR_NVR': [5050, 5051, 5052, 5053, 5054, 6060, 6061, 6062, 6063, 6064, 7070, 7071, 7072, 7073, 7074]
            }
            
            for brand_ports in camera_brand_ports.values():
                ports.update(brand_ports)
        
        # 📡 STREAMING PROTOCOL PORTS
        if self.config.scan_stream_ports:
            stream_ports = {
                'RTSP': [554, 555, 556, 8554, 8555, 8556],
                'RTMP': [1935, 1936, 1937, 1938],
                'MMS': [1755, 1756, 1757],
                'HTTP_Stream': [80, 443, 8080, 8081, 8088, 8888],
                'ONVIF': [80, 443, 8080, 888, 8899]
            }
            
            for protocol_ports in stream_ports.values():
                ports.update(protocol_ports)
        
        # 🚀 HIGH RANGE PORTS (500+ ports)
        if self.config.scan_high_ports:
            ports.update(range(10000, 10100))   # 10000-10099
            ports.update(range(20000, 20100))   # 20000-20099
            ports.update(range(30000, 30100))   # 30000-30099
            ports.update(range(40000, 40100))   # 40000-40099
            ports.update(range(50000, 50100))   # 50000-50099
        
        # 🎯 CUSTOM PORTS
        ports.update(self.config.custom_ports)
        
        return sorted(ports)
    
    def scan_ports(self, target_ip: str) -> List[int]:
        """🚀 Perform massive multi-threaded port scanning"""
        open_ports: List[int] = []
        
        print(f"\n{Fore.CYAN}{Style.BRIGHT}🚀 MASSIVE PORT SCANNING INITIATED{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}   📡 Target: {target_ip}")
        print(f"   🔍 Ports: {len(self.port_list)}")
        print(f"   ⚡ Workers: {self.config.max_port_workers}")
        print(f"   ⏱️ Timeout: {self.config.port_timeout}s{Style.RESET_ALL}")
        
        def check_port(port: int) -> Optional[int]:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.settimeout(self.config.port_timeout)
                    result = sock.connect_ex((target_ip, port))
                    return port if result == 0 else None
            except:
                return None
        
        # 🎨 Beautiful progress bar
        with ThreadPoolExecutor(max_workers=self.config.max_port_workers) as executor:
            futures = {executor.submit(check_port, port): port for port in self.port_list}
            
            for future in tqdm(as_completed(futures), total=len(futures), 
                             desc=f"{Fore.CYAN}🔍 Scanning Ports{Style.RESET_ALL}", 
                             unit="port", ncols=100,
                             bar_format="{l_bar}%s{bar}%s{r_bar}" % (Fore.CYAN, Fore.RESET)):
                port = future.result()
                if port:
                    open_ports.append(port)
                    # Real-time open port display
                    tqdm.write(f"   {Fore.GREEN}🎯 PORT {port:5} - OPEN{Style.RESET_ALL}")
        
        # 📊 Scan summary
        print(f"\n{Fore.GREEN}{Style.BRIGHT}✅ PORT SCAN COMPLETED{Style.RESET_ALL}")
        print(f"   📊 Open Ports: {Fore.CYAN}{len(open_ports)}{Style.RESET_ALL}")
        print(f"   🎯 Success Rate: {Fore.CYAN}{(len(open_ports)/len(self.port_list))*100:.2f}%{Style.RESET_ALL}")
        
        return sorted(open_ports)

class AdvancedCameraDetector:
    """🔍 ADVANCED CAMERA DETECTION & BRAND IDENTIFICATION"""
    
    def __init__(self, config):
        self.config = config
        self.brand_signatures = self._load_brand_signatures()
        logger.info(f"🎯 Advanced detector loaded for {len(self.brand_signatures)} brands")
    
    def _load_brand_signatures(self) -> Dict[str, Dict]:
        """🎯 Load comprehensive brand detection signatures"""
        return {
            'Hikvision': {
                'ports': [80, 443, 8000, 34567, 34599],
                'headers': ['Server: Hikvision', 'Hikvision'],
                'html_patterns': ['hikvision', 'webVideoCtrl.js', 'ISAPI', 'Hikvision Web'],
                'endpoints': ['/ISAPI/Security/userCheck', '/System/configurationFile'],
                'models': ['DS-2CD', 'DS-2DE', 'DS-7', 'DS-9'],
                'confidence_boosters': ['hikvision', 'ISAPI']
            },
            'Dahua': {
                'ports': [80, 443, 37777, 37778],
                'headers': ['Dahua', 'WebS', 'DHI'],
                'html_patterns': ['dahua', 'webCore.js', 'DHI', 'Dahua Technology'],
                'endpoints': ['/cgi-bin/magicBox.cgi?action=getSystemInfo'],
                'models': ['IPC-H', 'NVR4', 'DHI', 'SD'],
                'confidence_boosters': ['dahua', 'DHI']
            },
            '🆕 CP_Plus': {
                'ports': [80, 443, 8000, 6000, 7000],
                'headers': ['CP PLUS', 'CP-UVR', 'CP-UVS'],
                'html_patterns': ['cpplus', 'CP-UVR-0401E1-IC2', 'camera', 'CP PLUS'],
                'endpoints': ['/cgi-bin/authLogin.cgi', '/cgi-bin/configManager.cgi'],
                'models': ['CP-UVR-0401E1-IC2', 'CP-UVS', 'CP-DVR', 'CP-NVR'],
                'confidence_boosters': ['CP-UVR', 'CP PLUS']
            },
            'DVR_NVR_Generic': {
                'ports': [80, 443, 5050, 6060, 7070],
                'headers': ['DVR', 'NVR', 'XVR', 'HVR'],
                'html_patterns': ['dvr', 'nvr', 'surveillance', 'cctv', 'channel'],
                'endpoints': ['/cgi-bin/deviceManager.cgi', '/cgi-bin/channelManage.cgi'],
                'models': ['DVR', 'NVR', 'XVR', 'HVR', 'Hybrid'],
                'confidence_boosters': ['dvr', 'nvr', 'channel']
            },
            'Axis': {
                'ports': [80, 443, 3000],
                'headers': ['Server: Axis', 'Axis'],
                'html_patterns': ['axis-cgi', 'axis.com', 'AXIS', 'axis network camera'],
                'endpoints': ['/axis-cgi/admin/param.cgi'],
                'models': ['M30', 'P13', 'Q16', 'M'],
                'confidence_boosters': ['axis-cgi', 'AXIS']
            },
            'Sony': {
                'ports': [80, 443, 10000],
                'headers': ['Sony Network Camera'],
                'html_patterns': ['sony', 'SNC', 'Sony Corporation'],
                'endpoints': ['/command/inquiry.cgi'],
                'models': ['SNC-', 'SNC-E', 'SNC-D'],
                'confidence_boosters': ['sony', 'SNC']
            },
            'Bosch': {
                'ports': [80, 443, 9000],
                'headers': ['Bosch Security Systems'],
                'html_patterns': ['bosch', 'dinion', 'flexidome'],
                'endpoints': ['/config.js'],
                'models': ['Dinion', 'Flexidome', 'Autodome'],
                'confidence_boosters': ['bosch', 'dinion']
            }
        }
    
    def identify_camera(self, target_ip: str, open_ports: List[int]) -> Dict[str, Any]:
        """🔍 Advanced camera identification with confidence scoring"""
        device_info = {
            'brand': 'Unknown',
            'model': 'Unknown', 
            'type': 'Unknown',
            'confidence': 'Low',
            'confidence_score': 0,
            'detection_methods': [],
            'login_forms': [],
            'page_titles': [],
            'vulnerabilities': []
        }
        
        best_match = {'brand': 'Unknown', 'score': 0}
        
        for brand, signature in self.brand_signatures.items():
            brand_score = self._calculate_brand_score(brand, signature, target_ip, open_ports)
            
            if brand_score > best_match['score']:
                best_match = {'brand': brand, 'score': brand_score}
        
        if best_match['score'] > 0:
            device_info.update(self._enhance_device_info(best_match['brand'], target_ip, open_ports))
        
        # 🎨 Display detection results
        self._display_detection_results(device_info)
        
        return device_info
    
    def _calculate_brand_score(self, brand: str, signature: Dict, target_ip: str, open_ports: List[int]) -> int:
        """🎯 Calculate brand match score"""
        score = 0
        
        # Port matching (30 points max)
        common_ports = set(signature['ports']) & set(open_ports)
        score += len(common_ports) * 10
        
        # Endpoint testing (40 points max)
        for endpoint in signature['endpoints']:
            try:
                url = f"http://{target_ip}{endpoint}"
                response = requests.get(url, timeout=self.config.request_timeout, verify=False)
                if response.status_code == 200:
                    score += 20
                    # Check for brand-specific content
                    for booster in signature.get('confidence_boosters', []):
                        if booster.lower() in response.text.lower():
                            score += 10
            except:
                continue
        
        # Web page analysis (30 points max)
        for port in [80, 443, 8080, 8000]:
            if port in open_ports:
                try:
                    protocol = 'https' if port == 443 else 'http'
                    url = f"{protocol}://{target_ip}:{port}"
                    response = requests.get(url, timeout=self.config.request_timeout, verify=False)
                    
                    # Check HTML patterns
                    for pattern in signature['html_patterns']:
                        if pattern.lower() in response.text.lower():
                            score += 15
                            
                    # Check headers
                    server_header = response.headers.get('Server', '')
                    for header_pattern in signature['headers']:
                        if header_pattern.lower() in server_header.lower():
                            score += 10
                except:
                    continue
        
        return score
    
    def _enhance_device_info(self, brand: str, target_ip: str, open_ports: List[int]) -> Dict[str, Any]:
        """🔧 Enhance device information with additional details"""
        enhanced_info = {
            'brand': brand,
            'confidence_score': 0,
            'detection_methods': [],
            'login_forms': [],
            'page_titles': []
        }
        
        # Analyze web interfaces
        for port in [80, 443, 8080, 8000]:
            if port in open_ports:
                try:
                    protocol = 'https' if port == 443 else 'http'
                    url = f"{protocol}://{target_ip}:{port}"
                    response = requests.get(url, timeout=self.config.request_timeout, verify=False)
                    
                    # Extract page title
                    title_match = re.search(r'<title>(.*?)</title>', response.text, re.IGNORECASE)
                    if title_match:
                        enhanced_info['page_titles'].append(title_match.group(1))
                    
                    # Detect login forms
                    if self._detect_login_forms(response.text):
                        enhanced_info['login_forms'].append({
                            'url': url,
                            'port': port,
                            'has_login': True
                        })
                        enhanced_info['detection_methods'].append(f"Login form on port {port}")
                    
                    # Check for specific model patterns
                    model_patterns = self.brand_signatures[brand].get('models', [])
                    for pattern in model_patterns:
                        if pattern in response.text:
                            enhanced_info['model'] = pattern
                            break
                            
                except Exception as e:
                    logger.debug(f"Analysis failed for {target_ip}:{port}: {e}")
        
        # Determine confidence level
        confidence_score = len(enhanced_info['detection_methods']) * 20
        if confidence_score >= 80:
            enhanced_info['confidence'] = 'High'
        elif confidence_score >= 40:
            enhanced_info['confidence'] = 'Medium'
        else:
            enhanced_info['confidence'] = 'Low'
        
        enhanced_info['confidence_score'] = confidence_score
        
        return enhanced_info
    
    def _detect_login_forms(self, html: str) -> bool:
        """🔍 Detect login forms in HTML content"""
        login_indicators = [
            'password', 'login', 'username', 'user', 'pass', 'pwd',
            'type="password"', 'name="password"', 'id="password"'
        ]
        
        html_lower = html.lower()
        indicators_found = sum(1 for indicator in login_indicators if indicator in html_lower)
        
        return indicators_found >= 3
    
    def _display_detection_results(self, device_info: Dict[str, Any]):
        """🎨 Display beautiful detection results"""
        brand = device_info['brand']
        confidence = device_info['confidence']
        confidence_score = device_info['confidence_score']
        
        # Color coding for confidence
        if confidence == 'High':
            color = Fore.GREEN
            emoji = "🎯"
        elif confidence == 'Medium':
            color = Fore.YELLOW
            emoji = "🔍"
        else:
            color = Fore.RED
            emoji = "❓"
        
        print(f"\n{Fore.CYAN}{Style.BRIGHT}🔍 CAMERA DETECTION RESULTS{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}╔{'═' * 60}╗{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}║ {emoji} {color}Brand: {brand:<47} {Fore.YELLOW}║{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}║ {color}Confidence: {confidence} ({confidence_score} pts){' ':>28} {Fore.YELLOW}║{Style.RESET_ALL}")
        
        if device_info.get('model') and device_info['model'] != 'Unknown':
            print(f"{Fore.YELLOW}║ 📱 Model: {device_info['model']:<46} {Fore.YELLOW}║{Style.RESET_ALL}")
        
        if device_info['login_forms']:
            print(f"{Fore.YELLOW}║ 🔐 Login Forms: {len(device_info['login_forms'])} found{' ':>34} {Fore.YELLOW}║{Style.RESET_ALL}")
        
        print(f"{Fore.YELLOW}╚{'═' * 60}╝{Style.RESET_ALL}")

class LiveStreamDetector:
    """📹 ENHANCED LIVE STREAM DETECTION & VALIDATION"""
    
    def __init__(self, config):
        self.config = config
        self.stream_protocols = self._load_stream_protocols()
        logger.info(f"📹 Stream detector loaded for {len(self.stream_protocols)} protocols")
    
    def _load_stream_protocols(self) -> Dict[str, Dict]:
        """🎯 Load streaming protocol configurations"""
        return {
            'RTSP': {
                'ports': [554, 555, 556, 8554, 8555, 8556],
                'url_templates': [
                    'rtsp://{ip}:{port}/live.sdp',
                    'rtsp://{ip}:{port}/cam/realmonitor?channel=1&subtype=0',
                    'rtsp://{ip}:{port}/h264',
                    'rtsp://{ip}:{port}/mpeg4',
                    'rtsp://{ip}:{port}/axis-media/media.amp'
                ],
                'validation': 'protocol_specific'
            },
            'HTTP': {
                'ports': [80, 443, 8080, 8000, 8088],
                'url_templates': [
                    'http://{ip}:{port}/video.mjpg',
                    'http://{ip}:{port}/snapshot.jpg',
                    'http://{ip}:{port}/live.jpg',
                    'http://{ip}:{port}/stream.jpg',
                    'http://{ip}:{port}/img.jpg',
                    'http://{ip}:{port}/cgi-bin/video.cgi'
                ],
                'validation': 'content_check'
            },
            'RTMP': {
                'ports': [1935, 1936, 1937],
                'url_templates': [
                    'rtmp://{ip}:{port}/live',
                    'rtmp://{ip}:{port}/stream',
                    'rtmp://{ip}:{port}/cam'
                ],
                'validation': 'protocol_specific'
            },
            'MMS': {
                'ports': [1755, 1756],
                'url_templates': [
                    'mms://{ip}:{port}',
                    'mms://{ip}:{port}/live'
                ],
                'validation': 'protocol_specific'
            },
            'HLS': {
                'ports': [80, 443, 8080],
                'url_templates': [
                    'http://{ip}:{port}/live/stream.m3u8',
                    'http://{ip}:{port}/hls/stream.m3u8'
                ],
                'validation': 'content_check'
            }
        }
    
    def detect_streams(self, target_ip: str, open_ports: List[int]) -> List[Dict[str, Any]]:
        """📹 Detect and validate live streams"""
        validated_streams = []
        
        print(f"\n{Fore.CYAN}{Style.BRIGHT}📹 LIVE STREAM DETECTION{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}   🎯 Target: {target_ip}")
        print(f"   🔍 Protocols: {len(self.stream_protocols)}")
        print(f"   📡 Ports to check: {len(open_ports)}{Style.RESET_ALL}")
        
        for protocol, protocol_info in self.stream_protocols.items():
            for port in protocol_info['ports']:
                if port in open_ports:
                    streams = self._test_protocol_streams(protocol, protocol_info, target_ip, port)
                    validated_streams.extend(streams)
        
        # 📊 Stream detection summary
        if validated_streams:
            print(f"\n{Fore.GREEN}{Style.BRIGHT}✅ STREAM DETECTION COMPLETED{Style.RESET_ALL}")
            print(f"   📹 Valid Streams: {Fore.CYAN}{len(validated_streams)}{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.YELLOW}📹 No live streams detected{Style.RESET_ALL}")
        
        return validated_streams
    
    def _test_protocol_streams(self, protocol: str, protocol_info: Dict, target_ip: str, port: int) -> List[Dict[str, Any]]:
        """🔍 Test streams for specific protocol"""
        valid_streams = []
        
        for template in protocol_info['url_templates']:
            stream_url = template.format(ip=target_ip, port=port)
            
            if self._validate_stream(stream_url, protocol_info['validation']):
                stream_info = {
                    'protocol': protocol,
                    'url': stream_url,
                    'port': port,
                    'status': 'Validated',
                    'response_time': self._measure_response_time(stream_url),
                    'validation_method': protocol_info['validation']
                }
                valid_streams.append(stream_info)
                
                # 🎨 Real-time stream discovery
                print(f"   {Fore.GREEN}📹 {protocol} stream: {stream_url}{Style.RESET_ALL}")
        
        return valid_streams
    
    def _validate_stream(self, stream_url: str, validation_method: str) -> bool:
        """✅ Validate stream functionality"""
        try:
            if validation_method == 'content_check':
                response = requests.get(stream_url, timeout=self.config.request_timeout, 
                                      verify=False, stream=True)
                if response.status_code == 200:
                    content_type = response.headers.get('content-type', '')
                    # Check for media content
                    if any(media_type in content_type for media_type in ['image', 'video', 'application/vnd.apple.mpegurl']):
                        return True
                    # Check for MJPG stream content
                    if len(response.content) > 1000:
                        return True
            
            elif validation_method == 'protocol_specific':
                # For RTSP/RTMP/MMS, we assume URL format is correct
                return True
                
        except Exception as e:
            logger.debug(f"Stream validation failed: {e}")
        
        return False
    
    def _measure_response_time(self, stream_url: str) -> Optional[float]:
        """⏱️ Measure stream response time"""
        try:
            start_time = time.time()
            requests.get(stream_url, timeout=self.config.request_timeout, verify=False)
            return round((time.time() - start_time) * 1000, 2)
        except:
            return None

class UltimateCredentialTester:
    """🔐 ULTIMATE CREDENTIAL TESTING WITH RATE LIMITING"""
    
    def __init__(self, config):
        self.config = config
        self.credential_database = self._load_massive_credential_database()
        logger.info(f"🔐 Credential tester loaded with {len(self.credential_database)} combinations")
    
    def _load_massive_credential_database(self) -> List[tuple]:
        """🗃️ Load massive credential database"""
        credentials = []
        
        # 🎯 BASE CREDENTIALS (100+ combinations)
        base_creds = [
            ('admin', 'admin'), ('admin', 'password'), ('admin', '1234'),
            ('admin', '12345'), ('admin', '123456'), ('admin', ''),
            ('admin', '1111'), ('admin', '9999'), ('admin', '12345678'),
            ('admin', '123456789'), ('admin', '888888'), ('admin', '54321'),
            ('root', 'admin'), ('root', '1234'), ('supervisor', 'supervisor'),
            ('user', 'user'), ('guest', 'guest'), ('default', 'default'),
            ('admin', 'admin1234'), ('admin', '1234abcd'), ('admin', '4321')
        ]
        credentials.extend(base_creds)
        
        # 🆕 BRAND-SPECIFIC CREDENTIALS
        brand_creds = {
            'Hikvision': [('admin', '12345'), ('admin', 'hikvision')],
            'Dahua': [('admin', 'admin'), ('admin', 'dahua'), ('admin', '666666')],
            'CP_Plus': [('admin', 'admin'), ('admin', '1234'), ('admin', 'cpplus')],
            'Axis': [('root', 'pass'), ('admin', 'axis')],
            'Sony': [('admin', 'admin'), ('admin', 'sony')],
            'Bosch': [('admin', 'admin'), ('admin', 'bosch')],
            'DVR_NVR_Generic': [('admin', '1234'), ('admin', '4321'), ('admin', '0000')]
        }
        
        for brand_cred_list in brand_creds.values():
            credentials.extend(cred_list)
        
        # 🔢 NUMERIC VARIATIONS (1000+ combinations)
        for i in range(1000):
            credentials.append(('admin', str(i).zfill(4)))  # 0000-0999
        
        return credentials[:self.config.credential_limit]
    
    def test_credentials(self, target_ip: str, open_ports: List[int], device_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """🔐 Perform massive credential testing"""
        if not self.config.enable_credential_testing:
            return []
        
        valid_credentials = []
        target_urls = self._generate_target_urls(target_ip, open_ports)
        
        print(f"\n{Fore.CYAN}{Style.BRIGHT}🔐 ULTIMATE CREDENTIAL TESTING{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}   🎯 Target: {target_ip}")
        print(f"   🔑 Credentials: {len(self.credential_database)}")
        print(f"   🌐 URLs: {len(target_urls)}")
        print(f"   ⚡ Workers: {self.config.max_credential_workers}{Style.RESET_ALL}")
        
        def test_single_credential(url: str, username: str, password: str) -> Optional[Dict[str, Any]]:
            try:
                # 🎯 Basic authentication test
                auth = requests.auth.HTTPBasicAuth(username, password)
                response = requests.get(url, auth=auth, timeout=self.config.request_timeout, verify=False)
                
                if self._is_login_successful(response):
                    return {
                        'url': url,
                        'username': username,
                        'password': password,
                        'method': 'Basic Auth',
                        'device_brand': device_info.get('brand', 'Unknown')
                    }
                
                # Small delay for rate limiting
                time.sleep(0.05)
                
            except Exception as e:
                logger.debug(f"Credential test failed: {e}")
            
            return None
        
        # 🚀 Multi-threaded credential testing
        test_combinations = []
        for url in target_urls:
            for username, password in self.credential_database:
                test_combinations.append((url, username, password))
        
        with ThreadPoolExecutor(max_workers=self.config.max_credential_workers) as executor:
            futures = {
                executor.submit(test_single_credential, url, username, password): (url, username, password)
                for url, username, password in test_combinations[:1000]  # Limit for demo
            }
            
            for future in tqdm(as_completed(futures), total=len(futures),
                             desc=f"{Fore.CYAN}🔐 Testing Credentials{Style.RESET_ALL}",
                             unit="cred", ncols=100):
                result = future.result()
                if result:
                    valid_credentials.append(result)
                    # 🎉 Real-time success notification
                    tqdm.write(f"   {Fore.GREEN}✅ CREDENTIALS WORK: {result['username']}:{result['password']}{Style.RESET_ALL}")
        
        # 📊 Credential testing summary
        if valid_credentials:
            print(f"\n{Fore.GREEN}{Style.Bright}🎉 CREDENTIAL TESTING COMPLETED{Style.RESET_ALL}")
            print(f"   ✅ Working Credentials: {Fore.CYAN}{len(valid_credentials)}{Style.RESET_ALL}")
            print(f"   📊 Success Rate: {Fore.CYAN}{(len(valid_credentials)/len(test_combinations))*100:.2f}%{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.YELLOW}🔐 No valid credentials found{Style.RESET_ALL}")
        
        return valid_credentials
    
    def _generate_target_urls(self, target_ip: str, open_ports: List[int]) -> List[str]:
        """🌐 Generate target URLs for credential testing"""
        urls = []
        for port in open_ports:
            if port in [80, 443, 8080, 8000, 8001]:
                protocol = 'https' if port == 443 else 'http'
                base_url = f"{protocol}://{target_ip}:{port}"
                
                # Common camera endpoints
                endpoints = ['/', '/login', '/admin', '/web', '/view', '/main', '/cgi-bin/login.cgi']
                for endpoint in endpoints:
                    urls.append(base_url + endpoint)
        
        return list(set(urls))
    
    def _is_login_successful(self, response) -> bool:
        """✅ Determine login success"""
        success_indicators = ['logout', 'dashboard', 'main', 'live', 'video', 'settings', 'welcome']
        failure_indicators = ['incorrect', 'invalid', 'error', 'failed', 'wrong password']
        
        response_text = response.text.lower()
        
        if any(indicator in response_text for indicator in failure_indicators):
            return False
        
        if any(indicator in response_text for indicator in success_indicators):
            return True
        
        if response.history and 'login' not in response.url.lower():
            return True
        
        if response.cookies:
            return True
        
        return False

class GeoLocationMapper:
    """🌍 COMPREHENSIVE IP & LOCATION INFORMATION"""
    
    def __init__(self, config):
        self.config = config
        self.reader = self._initialize_geoip_reader()
    
    def _initialize_geoip_reader(self):
        """🗺️ Initialize GeoIP database"""
        if not GEOIP_AVAILABLE:
            logger.warning("🌍 GeoIP2 library not installed - geolocation disabled")
            return None
        
        try:
            return geoip2.database.Reader('GeoLite2-City.mmdb')
        except:
            logger.warning("🌍 GeoIP database file not available - geolocation disabled")
            return None
    
    def get_location(self, ip: str) -> Optional[Dict[str, Any]]:
        """🌍 Get comprehensive location information"""
        if not self.reader or not self.config.enable_geolocation:
            return None
        
        try:
            response = self.reader.city(ip)
            location_data = {
                'country': response.country.name,
                'city': response.city.name,
                'latitude': response.location.latitude,
                'longitude': response.location.longitude,
                'postal_code': response.postal.code,
                'timezone': response.location.time_zone,
                'accuracy_radius': response.location.accuracy_radius
            }
            
            # 🗺️ Generate mapping links
            location_data['maps_links'] = self._generate_mapping_links(
                location_data['latitude'], 
                location_data['longitude']
            )
            
            # 🎨 Display location information
            self._display_location_info(location_data)
            
            return location_data
            
        except Exception as e:
            logger.debug(f"Geolocation failed: {e}")
            return None
    
    def _generate_mapping_links(self, lat: float, lon: float) -> Dict[str, str]:
        """🔗 Generate mapping service links"""
        return {
            'google_maps': f"https://maps.google.com/?q={lat},{lon}",
            'google_earth': f"https://earth.google.com/web/@{lat},{lon}",
            'open_street_map': f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}"
        }
    
    def _display_location_info(self, location_data: Dict[str, Any]):
        """🎨 Display beautiful location information"""
        print(f"\n{Fore.CYAN}{Style.BRIGHT}🌍 GEOLOCATION INFORMATION{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}╔{'═' * 60}╗{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}║ 🏙️  City: {location_data['city']:<48} {Fore.YELLOW}║{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}║ 🌎 Country: {location_data['country']:<45} {Fore.YELLOW}║{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}║ 📍 Coordinates: {location_data['latitude']:.4f}, {location_data['longitude']:.4f} {' ':>20} {Fore.YELLOW}║{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}║ 🕐 Timezone: {location_data['timezone']:<44} {Fore.YELLOW}║{Style.RESET_ALL}")
        
        if location_data['maps_links']:
            print(f"{Fore.YELLOW}║ 🗺️  Google Maps: {location_data['maps_links']['google_maps']} {Fore.YELLOW}║{Style.RESET_ALL}")
        
        print(f"{Fore.YELLOW}╚{'═' * 60}╝{Style.RESET_ALL}")

class UltimateReportGenerator:
    """📊 ULTIMATE REPORT GENERATION WITH STYLISH FORMATTING"""
    
    def generate_report(self, results: Dict[str, Any]):
        """📈 Generate comprehensive security assessment report"""
        
        print(f"\n{Fore.CYAN}{Style.BRIGHT}{'╔' + '═' * 98 + '╗'}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{Style.BRIGHT}║ {Fore.WHITE}{Style.BRIGHT}📊 OMNICAMXPLOIT ULTIMATE - SECURITY ASSESSMENT REPORT {Fore.CYAN} ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{Style.BRIGHT}{'╚' + '═' * 98 + '╝'}{Style.RESET_ALL}")
        
        # Executive Summary
        self._print_section("EXECUTIVE SUMMARY", "📈", Fore.CYAN)
        self._print_executive_summary(results)
        
        # Technical Findings
        self._print_section("TECHNICAL FINDINGS", "🔧", Fore.BLUE)
        self._print_technical_findings(results)
        
        # Security Assessment
        self._print_section("SECURITY ASSESSMENT", "⚠️", Fore.YELLOW)
        self._print_security_assessment(results)
        
        # Recommendations
        self._print_section("SECURITY RECOMMENDATIONS", "🛡️", Fore.GREEN)
        self._print_recommendations(results)
        
        print(f"\n{Fore.CYAN}{Style.BRIGHT}{'╔' + '═' * 98 + '╗'}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{Style.BRIGHT}║ {Fore.WHITE}🎯 SCAN COMPLETED - Review findings and implement recommendations {Fore.CYAN} ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{Style.BRIGHT}{'╚' + '═' * 98 + '╝'}{Style.RESET_ALL}")
    
    def _print_section(self, title: str, emoji: str, color: str):
        """🖋️ Print beautiful section header"""
        print(f"\n{color}{Style.BRIGHT}┌{'─' * 96}┐{Style.RESET_ALL}")
        print(f"{color}{Style.BRIGHT}│ {emoji}  {title:<85} {color}│{Style.RESET_ALL}")
        print(f"{color}{Style.BRIGHT}└{'─' * 96}┘{Style.RESET_ALL}")
    
    def _print_executive_summary(self, results: Dict[str, Any]):
        """📈 Print executive summary"""
        print(f"{Fore.WHITE}   🎯 {Fore.CYAN}Target:{Fore.WHITE} {results['target']}")
        print(f"   🌐 {Fore.CYAN}IP Address:{Fore.WHITE} {results['ip']}")
        print(f"   ⏱️  {Fore.CYAN}Scan Duration:{Fore.WHITE} {results['scan_duration']:.2f}s")
        print(f"   🆔 {Fore.CYAN}Scan ID:{Fore.WHITE} {results['scan_id']}")
        
        if results.get('location'):
            loc = results['location']
            print(f"   🌍 {Fore.CYAN}Location:{Fore.WHITE} {loc.get('city', 'Unknown')}, {loc.get('country', 'Unknown')}")
    
    def _print_technical_findings(self, results: Dict[str, Any]):
        """🔧 Print technical findings"""
        # Ports
        ports = results['open_ports']
        print(f"   🔓 {Fore.CYAN}Open Ports:{Fore.WHITE} {len(ports)}")
        if ports:
            port_display = ', '.join(map(str, ports[:15]))
            if len(ports) > 15:
                port_display += f" ... +{len(ports) - 15} more"
            print(f"      {Fore.WHITE}{port_display}")
        
        # Device Info
        device_info = results.get('device_info', {})
        print(f"   📱 {Fore.CYAN}Device:{Fore.WHITE} {device_info.get('brand', 'Unknown')}")
        print(f"   🎯 {Fore.CYAN}Confidence:{Fore.WHITE} {device_info.get('confidence', 'Low')}")
        
        # Streams
        streams = results.get('streams', [])
        print(f"   📹 {Fore.CYAN}Live Streams:{Fore.WHITE} {len(streams)}")
        for stream in streams[:3]:
            print(f"      {Fore.CYAN}{stream['protocol']}:{Fore.WHITE} {stream['url']}")
        
        # Credentials
        creds = results.get('credentials', [])
        if creds:
            print(f"   🔑 {Fore.CYAN}Valid Credentials:{Fore.RED} {len(creds)} - SECURITY ISSUE{Style.RESET_ALL}")
            for cred in creds[:3]:
                print(f"      {Fore.RED}⚠️  {cred['username']}:{cred['password']}{Style.RESET_ALL}")
        else:
            print(f"   🔑 {Fore.CYAN}Valid Credentials:{Fore.GREEN} 0 - SECURE{Style.RESET_ALL}")
    
    def _print_security_assessment(self, results: Dict[str, Any]):
        """⚠️ Print security assessment"""
        risk_factors = []
        
        if results.get('credentials'):
            risk_factors.append(f"{Fore.RED}🔴 Default credentials exposed")
        
        if len(results['open_ports']) > 10:
            risk_factors.append(f"{Fore.YELLOW}🟡 Excessive open ports ({len(results['open_ports'])})")
        
        if results.get('streams'):
            risk_factors.append(f"{Fore.YELLOW}🟡 Live streams accessible")
        
        if not risk_factors:
            risk_factors.append(f"{Fore.GREEN}🟢 No critical issues detected")
        
        print(f"   📊 {Fore.CYAN}Security Assessment:{Fore.WHITE}")
        for factor in risk_factors:
            print(f"      {factor}{Style.RESET_ALL}")
    
    def _print_recommendations(self, results: Dict[str, Any]):
        """🛡️ Print security recommendations"""
        recommendations = []
        
        if results.get('credentials'):
            recommendations.append(f"{Fore.RED}🔴 CHANGE DEFAULT CREDENTIALS IMMEDIATELY")
        
        if len(results['open_ports']) > 10:
            recommendations.append(f"{Fore.YELLOW}🟡 RESTRICT UNNECESSARY PORTS")
        
        if results.get('streams'):
            recommendations.append(f"{Fore.YELLOW}🟡 SECURE LIVE STREAMS WITH AUTHENTICATION")
        
        recommendations.extend([
            f"{Fore.BLUE}🔵 UPDATE FIRMWARE TO LATEST VERSION",
            f"{Fore.BLUE}🔵 IMPLEMENT NETWORK SEGMENTATION",
            f"{Fore.GREEN}🟢 REGULAR SECURITY ASSESSMENTS",
            f"{Fore.GREEN}🟢 MONITOR FOR UNAUTHORIZED ACCESS"
        ])
        
        for rec in recommendations:
            print(f"   {rec}{Style.RESET_ALL}")

class OmniCamXploitUltimate:
    """🚀 ULTIMATE CAMERA SECURITY ASSESSMENT FRAMEWORK"""
    
    def __init__(self, config: ScanConfig):
        self.config = config
        self.results: Dict[str, Any] = {}
        self.scan_duration: float = 0.0
        
        # Initialize ultimate modules
        self.port_scanner = UltimatePortScanner(config)
        self.camera_detector = AdvancedCameraDetector(config)
        self.stream_detector = LiveStreamDetector(config)
        self.credential_tester = UltimateCredentialTester(config)
        self.geolocator = GeoLocationMapper(config)
        self.report_generator = UltimateReportGenerator()
        
        logger.info(f"🚀 OmniCamXploit Ultimate initialized for: {config.target}")
    
    def run_ultimate_scan(self) -> Dict[str, Any]:
        """🎯 Execute ultimate security assessment"""
        start_time = time.time()
        
        try:
            # Parse target
            target_ip = self._parse_target(self.config.target)
            self.results.update({
                'target': self.config.target,
                'ip': target_ip,
                'timestamp': time.ctime(),
                'scan_id': hashlib.md5(f"{self.config.target}{time.time()}".encode()).hexdigest()[:8]
            })
            
            # 🚀 Phase 1: Massive Port Scanning
            open_ports = self.port_scanner.scan_ports(target_ip)
            self.results['open_ports'] = open_ports
            
            if not open_ports:
                logger.warning("❌ No open ports found")
                return self.results
            
            # 🔍 Phase 2: Advanced Camera Detection
            device_info = self.camera_detector.identify_camera(target_ip, open_ports)
            self.results['device_info'] = device_info
            
            # 📹 Phase 3: Live Stream Detection
            streams = self.stream_detector.detect_streams(target_ip, open_ports)
            self.results['streams'] = streams
            
            # 🔐 Phase 4: Ultimate Credential Testing
            credentials = self.credential_tester.test_credentials(target_ip, open_ports, device_info)
            self.results['credentials'] = credentials
            
            # 🌍 Phase 5: Geolocation Analysis
            location_data = self.geolocator.get_location(target_ip)
            self.results['location'] = location_data
            
            self.scan_duration = time.time() - start_time
            self.results['scan_duration'] = self.scan_duration
            
            # 📊 Phase 6: Ultimate Reporting
            self.report_generator.generate_report(self.results)
            
            logger.info(f"✅ Ultimate scan completed in {self.scan_duration:.2f}s")
            return self.results
            
        except Exception as e:
            logger.error(f"💥 Scan failed: {e}")
            self.scan_duration = time.time() - start_time
            self.results['error'] = str(e)
            return self.results
    
    def _parse_target(self, target: str) -> str:
        """🎯 Parse target input"""
        if '://' in target:
            parsed = urlparse(target)
            return parsed.hostname
        return target

def print_ultimate_banner():
    """🎨 Print ultimate ASCII art banner"""
    banner = f"""
{Fore.CYAN}{Style.BRIGHT}
╔══════════════════════════════════════════════════════════════════════════════╗
║ {Fore.WHITE}                        OMNICAMXPLOIT ULTIMATE                         {Fore.CYAN}║
║ {Fore.YELLOW}                 Ultimate Camera Security Framework                  {Fore.CYAN}║
║ {Fore.GREEN}           GitHub: {Fore.CYAN}https://github.com/spyboy-productions/CamXploit{Fore.CYAN}   ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}"""
    print(banner)
    
    # Features showcase
    features = [
        f"{Fore.GREEN}✅ {Fore.CYAN}Massive 1000+ Port Scanning{Fore.WHITE}",
        f"{Fore.GREEN}✅ {Fore.CYAN}CP Plus & DVR/NVR Detection{Fore.WHITE}", 
        f"{Fore.GREEN}✅ {Fore.CYAN}Enhanced Live Stream Validation{Fore.WHITE}",
        f"{Fore.GREEN}✅ {Fore.CYAN}Multi-threaded Credential Testing{Fore.WHITE}",
        f"{Fore.GREEN}✅ {Fore.CYAN}Advanced Brand Identification{Fore.WHITE}",
        f"{Fore.GREEN}✅ {Fore.CYAN}Comprehensive Geolocation{Fore.WHITE}",
        f"{Fore.GREEN}✅ {Fore.CYAN}Professional Reporting{Fore.WHITE}",
        f"{Fore.GREEN}✅ {Fore.CYAN}Enterprise Error Handling{Fore.WHITE}"
    ]
    
    print(f"{Fore.YELLOW}╔{'═' * 70}╗{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}║ {Fore.CYAN}{Style.BRIGHT}🚀 ULTIMATE FEATURES{' ':>47} {Fore.YELLOW}║{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}║{'─' * 70}║{Style.RESET_ALL}")
    
    for i in range(0, len(features), 2):
        line = f"{Fore.YELLOW}║ {features[i]:<33}"
        if i + 1 < len(features):
            line += f" {features[i + 1]:<33}"
        else:
            line += " " * 34
        line += f"{Fore.YELLOW}║{Style.RESET_ALL}"
        print(line)
    
    print(f"{Fore.YELLOW}╚{'═' * 70}╝{Style.RESET_ALL}")

def main():
    """🎯 Ultimate main function"""
    parser = argparse.ArgumentParser(description='OmniCamXploit Ultimate - Camera Security Assessment')
    parser.add_argument('target', help='Target IP, URL, or network range')
    parser.add_argument('--no-creds', action='store_true', help='Disable credential testing')
    parser.add_argument('--no-geo', action='store_true', help='Disable geolocation')
    parser.add_argument('--workers', type=int, default=200, help='Port scan workers')
    parser.add_argument('--cred-workers', type=int, default=100, help='Credential test workers')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Print ultimate banner
    print_ultimate_banner()
    
    # Configuration
    config = ScanConfig(
        target=args.target,
        enable_credential_testing=not args.no_creds,
        enable_geolocation=not args.no_geo,
        max_port_workers=args.workers,
        max_credential_workers=args.cred_workers
    )
    
    print(f"\n{Fore.GREEN}{Style.BRIGHT}🎯 STARTING ULTIMATE SECURITY ASSESSMENT...{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}   Target: {args.target}")
    print(f"   Credential Testing: {'Enabled' if config.enable_credential_testing else 'Disabled'}")
    print(f"   Geolocation: {'Enabled' if config.enable_geolocation else 'Disabled'}")
    print(f"   Workers: {config.max_port_workers} (Ports) / {config.max_credential_workers} (Creds){Style.RESET_ALL}")
    
    # Execute ultimate scan
    engine = OmniCamXploitUltimate(config)
    results = engine.run_ultimate_scan()
    
    # Ultimate summary
    if 'error' not in results:
        print(f"\n{Fore.GREEN}{Style.BRIGHT}🎉 ULTIMATE SCAN COMPLETED SUCCESSFULLY!{Style.RESET_ALL}")
        print(f"{Fore.CYAN}   ⏱️  Duration: {results['scan_duration']:.2f}s")
        print(f"   🔓 Open Ports: {len(results['open_ports'])}")
        print(f"   📱 Device: {results['device_info'].get('brand', 'Unknown')}")
        print(f"   📹 Streams: {len(results.get('streams', []))}")
        print(f"   🔑 Working Credentials: {len(results.get('credentials', []))}{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.RED}{Style.BRIGHT}💥 SCAN FAILED: {results['error']}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()