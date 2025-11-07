"""Port Scanner Module - Comprehensive camera port detection."""

import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Tuple
from colorama import Fore, Style
from tqdm import tqdm


class PortScanner:
    """Advanced port scanner optimized for camera and DVR systems."""
    
    # Comprehensive camera port list (1000+ ports)
    CAMERA_PORTS = [
        # Standard web ports
        80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90,
        443, 8000, 8001, 8080, 8081, 8443, 8888, 9000, 9001,
        
        # RTSP streaming ports
        554, 555, 7447, 8554,
        
        # ONVIF ports
        8899, 3702, 80, 8080,
        
        # CP Plus specific ports
        6000, 6001, 6002, 6003, 6004, 6005,
        7000, 7001, 7002, 7003, 7004, 7005,
        
        # Hikvision ports
        8000, 554, 80, 8080, 37777, 37778,
        
        # Dahua ports
        37777, 37778, 554, 80, 8000,
        
        # DVR/NVR ports
        5050, 5051, 5052, 5053, 5054,
        6060, 6061, 6062, 6063, 6064,
        9000, 9001, 9002, 9003, 9004,
        
        # Generic camera ports
        1024, 1025, 1935, 2000, 3000, 3001, 4000, 4001, 5000, 5001,
        10000, 10001, 10002, 20000, 30000, 34567, 34599,
        
        # Additional manufacturer-specific ports
        *range(6000, 6100),  # CP Plus range
        *range(7000, 7100),  # Extended CP Plus
        *range(8000, 8100),  # Web interface range
        *range(9000, 9100),  # DVR range
        *range(37000, 38000, 100),  # Chinese camera range
        *range(40000, 50000, 1000),  # High-range ports
    ]
    
    def __init__(self, config):
        """Initialize port scanner with configuration."""
        self.config = config
        self.timeout = config.port_scan_timeout
        self.max_workers = config.max_workers
        
    def scan_port(self, target: str, port: int) -> Tuple[int, bool]:
        """Scan a single port on the target."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((target, port))
            sock.close()
            return (port, result == 0)
        except:
            return (port, False)
    
    def scan(self) -> List[int]:
        """Perform comprehensive port scan."""
        open_ports = []
        unique_ports = sorted(set(self.CAMERA_PORTS))
        
        print(f"{Fore.CYAN}🔍 Scanning {len(unique_ports)} camera-specific ports...{Style.RESET_ALL}")
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(self.scan_port, self.config.target, port): port 
                for port in unique_ports
            }
            
            with tqdm(total=len(unique_ports), desc="Port Scan", 
                     bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}') as pbar:
                for future in as_completed(futures):
                    port, is_open = future.result()
                    if is_open:
                        open_ports.append(port)
                        if self.config.verbose:
                            print(f"{Fore.GREEN}🎯 PORT {port} - OPEN{Style.RESET_ALL}")
                    pbar.update(1)
        
        return sorted(open_ports)
