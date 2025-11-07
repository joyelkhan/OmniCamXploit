"""Stream Validator Module - Validates live camera streams."""

import socket
from typing import List, Dict
from colorama import Fore, Style


class StreamValidator:
    """Validates actual camera streams (RTSP, HTTP, etc.)."""
    
    RTSP_PATHS = [
        '/live',
        '/stream',
        '/cam/realmonitor',
        '/h264',
        '/video',
        '/ch01/0',
        '/Streaming/Channels/1',
        '/Streaming/Channels/101',
        '/onvif1',
        '/onvif2',
    ]
    
    def __init__(self, config):
        """Initialize stream validator."""
        self.config = config
        
    def validate_rtsp(self, target: str, port: int) -> List[str]:
        """Validate RTSP streams on a port."""
        valid_streams = []
        
        if port not in [554, 555, 7447, 8554]:
            return valid_streams
        
        for path in self.RTSP_PATHS:
            try:
                # Simple RTSP DESCRIBE request
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(self.config.stream_validation_timeout)
                sock.connect((target, port))
                
                request = f"DESCRIBE rtsp://{target}:{port}{path} RTSP/1.0\r\nCSeq: 1\r\n\r\n"
                sock.send(request.encode())
                
                response = sock.recv(1024).decode('utf-8', errors='ignore')
                sock.close()
                
                if 'RTSP/1.0 200 OK' in response or 'RTSP/1.0 401' in response:
                    stream_url = f"rtsp://{target}:{port}{path}"
                    valid_streams.append(stream_url)
                    if self.config.verbose:
                        print(f"{Fore.GREEN}📹 Valid stream: {stream_url}{Style.RESET_ALL}")
            except:
                continue
        
        return valid_streams
    
    def validate_http_stream(self, target: str, port: int) -> List[str]:
        """Validate HTTP/MJPEG streams."""
        valid_streams = []
        
        http_paths = ['/video', '/mjpeg', '/stream', '/cam.mjpg']
        
        for path in http_paths:
            try:
                import requests
                url = f"http://{target}:{port}{path}"
                response = requests.get(url, timeout=2, stream=True)
                
                if response.status_code == 200 or response.status_code == 401:
                    valid_streams.append(url)
                    if self.config.verbose:
                        print(f"{Fore.GREEN}📹 Valid HTTP stream: {url}{Style.RESET_ALL}")
            except:
                continue
        
        return valid_streams
    
    def validate(self, open_ports: List[int]) -> List[Dict]:
        """Validate all streams on open ports."""
        all_streams = []
        
        for port in open_ports:
            streams = {
                'port': port,
                'rtsp_streams': self.validate_rtsp(self.config.target, port),
                'http_streams': self.validate_http_stream(self.config.target, port)
            }
            
            total = len(streams['rtsp_streams']) + len(streams['http_streams'])
            if total > 0:
                all_streams.append(streams)
                print(f"{Fore.GREEN}📹 Port {port}: Found {total} valid stream(s){Style.RESET_ALL}")
        
        return all_streams
