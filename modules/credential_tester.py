"""Credential Tester Module - Ethical credential testing with advanced engine."""

import requests
import time
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style
from tqdm import tqdm

try:
    from modules.credential_engine import MassCredentialEngine
    ADVANCED_ENGINE_AVAILABLE = True
except ImportError:
    ADVANCED_ENGINE_AVAILABLE = False


class CredentialTester:
    """Ethical credential testing with advanced credential engine."""
    
    DEFAULT_CREDENTIALS = [
        ('admin', 'admin'),
        ('admin', ''),
        ('admin', '12345'),
        ('admin', 'password'),
        ('root', 'root'),
        ('root', ''),
        ('user', 'user'),
        ('admin', '1234'),
        ('admin', '123456'),
        ('888888', '888888'),
        ('666666', '666666'),
        ('admin', 'admin123'),
        ('default', 'default'),
        ('service', 'service'),
    ]
    
    def __init__(self, config):
        """Initialize credential tester with ethical limits."""
        self.config = config
        self.attempts = 0
        self.max_attempts = min(config.max_credential_attempts, 1000)
        
        # Initialize advanced credential engine if available
        if ADVANCED_ENGINE_AVAILABLE:
            try:
                self.credential_engine = MassCredentialEngine()
                print(f"{Fore.CYAN}🔥 Advanced Credential Engine loaded!{Style.RESET_ALL}")
                stats = self.credential_engine.get_database_stats()
                print(f"{Fore.GREEN}   📊 Database: {stats['total_entries']} credentials ready{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.YELLOW}⚠️  Using default credentials (engine init failed){Style.RESET_ALL}")
                self.credential_engine = None
        else:
            self.credential_engine = None
        
    def test_http_auth(self, target: str, port: int, username: str, password: str) -> bool:
        """Test HTTP basic authentication."""
        if self.attempts >= self.max_attempts:
            return False
        
        self.attempts += 1
        
        try:
            url = f"http://{target}:{port}"
            response = requests.get(url, auth=(username, password), timeout=3, verify=False)
            
            # Rate limiting - ethical delay
            time.sleep(0.1)
            
            return response.status_code == 200
        except:
            return False
    
    def test_port(self, target: str, port: int) -> List[Dict]:
        """Test credentials on a specific port."""
        found = []
        
        for username, password in self.DEFAULT_CREDENTIALS:
            if self.attempts >= self.max_attempts:
                print(f"{Fore.YELLOW}⚠️  Reached maximum attempt limit ({self.max_attempts}){Style.RESET_ALL}")
                break
            
            if self.test_http_auth(target, port, username, password):
                cred = {
                    'port': port,
                    'username': username,
                    'password': password,
                    'protocol': 'HTTP'
                }
                found.append(cred)
                print(f"{Fore.RED}⚠️  CRITICAL: Default credentials found on port {port}: "
                      f"{username}:{password}{Style.RESET_ALL}")
        
        return found
    
    def test(self, open_ports: List[int]) -> List[Dict]:
        """Test credentials on all open ports."""
        all_credentials = []
        
        web_ports = [p for p in open_ports if p in [80, 81, 8000, 8080, 8081, 8888]]
        
        if not web_ports:
            print(f"{Fore.YELLOW}No web ports found for credential testing{Style.RESET_ALL}")
            return all_credentials
        
        # Use advanced engine if available
        if self.credential_engine:
            print(f"{Fore.CYAN}🎯 Using Advanced Credential Engine (strategy: common_only)...{Style.RESET_ALL}")
            credentials_to_test = []
            for cred in self.credential_engine.get_credentials('common_only'):
                if ':' in cred:
                    username, password = cred.split(':', 1)
                    credentials_to_test.append((username, password))
                else:
                    credentials_to_test.append(('admin', cred))
                if len(credentials_to_test) >= self.max_attempts:
                    break
        else:
            credentials_to_test = self.DEFAULT_CREDENTIALS
        
        print(f"{Fore.CYAN}Testing {len(credentials_to_test)} credentials on "
              f"{len(web_ports)} ports...{Style.RESET_ALL}")
        
        with tqdm(total=len(web_ports) * len(credentials_to_test), 
                 desc="Credential Test") as pbar:
            for port in web_ports:
                if self.attempts >= self.max_attempts:
                    break
                found = self.test_port_advanced(self.config.target, port, credentials_to_test)
                all_credentials.extend(found)
                pbar.update(len(credentials_to_test))
        
        return all_credentials
    
    def test_port_advanced(self, target: str, port: int, credentials: List[tuple]) -> List[Dict]:
        """Test credentials on a specific port using advanced list."""
        found = []
        
        for username, password in credentials:
            if self.attempts >= self.max_attempts:
                print(f"{Fore.YELLOW}⚠️  Reached maximum attempt limit ({self.max_attempts}){Style.RESET_ALL}")
                break
            
            if self.test_http_auth(target, port, username, password):
                cred = {
                    'port': port,
                    'username': username,
                    'password': password,
                    'protocol': 'HTTP'
                }
                found.append(cred)
                print(f"{Fore.RED}⚠️  CRITICAL: Default credentials found on port {port}: "
                      f"{username}:{password}{Style.RESET_ALL}")
        
        return found
