#!/usr/bin/env python3
"""
OmniCamXploit v1.0 - Professional Camera Security Assessment Framework
Author: Md. Abu Naser Khan
License: MIT

Enterprise-grade security assessment tool for IP cameras and surveillance systems.
"""

import argparse
import sys
from dataclasses import dataclass
from typing import Optional
from colorama import init, Fore, Style

from modules.port_scanner import PortScanner
from modules.device_identifier import DeviceIdentifier
from modules.stream_validator import StreamValidator
from modules.credential_tester import CredentialTester
from modules.geolocator import GeoLocator
from modules.report_generator import ReportGenerator

# Initialize colorama for cross-platform color support
init(autoreset=True)


@dataclass
class ScanConfig:
    """Configuration for security assessment scan."""
    target: str
    enable_credential_testing: bool = False
    max_credential_attempts: int = 1000
    port_scan_timeout: float = 1.0
    stream_validation_timeout: float = 5.0
    max_workers: int = 200
    verbose: bool = False


class OmniCamXploitEngine:
    """Main engine for camera security assessment."""
    
    VERSION = "1.0"
    BANNER = f"""
╔═══════════════════════════════════════════════════════════════╗
║                    OMNICAMXPLOIT v{VERSION}                       ║
║          Professional Camera Security Assessment              ║
║                                                               ║
║  {Fore.YELLOW}⚠️  FOR AUTHORIZED SECURITY TESTING ONLY ⚠️{Style.RESET_ALL}              ║
╚═══════════════════════════════════════════════════════════════╝
"""
    
    def __init__(self, config: ScanConfig):
        """Initialize the assessment engine."""
        self.config = config
        self.results = {
            'target': config.target,
            'open_ports': [],
            'identified_devices': [],
            'validated_streams': [],
            'credentials_found': [],
            'geolocation': None,
            'risk_score': 0
        }
        
    def print_banner(self):
        """Display the application banner."""
        print(self.BANNER)
        
    def run_scan(self) -> dict:
        """Execute the complete security assessment."""
        self.print_banner()
        
        print(f"{Fore.CYAN}🎯 Target: {Fore.WHITE}{self.config.target}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
        
        # Phase 1: Port Scanning
        print(f"{Fore.GREEN}[Phase 1/5]{Style.RESET_ALL} Port Scanning...")
        scanner = PortScanner(self.config)
        self.results['open_ports'] = scanner.scan()
        print(f"{Fore.GREEN}✓{Style.RESET_ALL} Found {len(self.results['open_ports'])} open ports\n")
        
        if not self.results['open_ports']:
            print(f"{Fore.YELLOW}⚠️  No open camera ports detected{Style.RESET_ALL}")
            return self.results
        
        # Phase 2: Device Identification
        print(f"{Fore.GREEN}[Phase 2/5]{Style.RESET_ALL} Device Identification...")
        identifier = DeviceIdentifier(self.config)
        self.results['identified_devices'] = identifier.identify(self.results['open_ports'])
        print(f"{Fore.GREEN}✓{Style.RESET_ALL} Identified {len(self.results['identified_devices'])} devices\n")
        
        # Phase 3: Stream Validation
        print(f"{Fore.GREEN}[Phase 3/5]{Style.RESET_ALL} Stream Validation...")
        validator = StreamValidator(self.config)
        self.results['validated_streams'] = validator.validate(self.results['open_ports'])
        print(f"{Fore.GREEN}✓{Style.RESET_ALL} Validated {len(self.results['validated_streams'])} live streams\n")
        
        # Phase 4: Credential Testing (Optional)
        if self.config.enable_credential_testing:
            print(f"{Fore.RED}[Phase 4/5]{Style.RESET_ALL} Credential Testing (Ethical Mode)...")
            print(f"{Fore.YELLOW}⚠️  Limited to {self.config.max_credential_attempts} attempts{Style.RESET_ALL}")
            tester = CredentialTester(self.config)
            self.results['credentials_found'] = tester.test(self.results['open_ports'])
            print(f"{Fore.GREEN}✓{Style.RESET_ALL} Testing complete\n")
        else:
            print(f"{Fore.YELLOW}[Phase 4/5]{Style.RESET_ALL} Credential Testing: SKIPPED (use --enable-creds)\n")
        
        # Phase 5: Geolocation
        print(f"{Fore.GREEN}[Phase 5/5]{Style.RESET_ALL} Geolocation Analysis...")
        geolocator = GeoLocator(self.config)
        self.results['geolocation'] = geolocator.locate(self.config.target)
        print(f"{Fore.GREEN}✓{Style.RESET_ALL} Location data retrieved\n")
        
        # Generate Report
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}📊 Generating Security Assessment Report...{Style.RESET_ALL}\n")
        
        report_gen = ReportGenerator(self.config)
        report_gen.generate(self.results)
        
        return self.results


def main():
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(
        description='OmniCamXploit v4.0 - Professional Camera Security Assessment',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python omnicamxploit.py 192.168.1.100
  python omnicamxploit.py 192.168.1.100 --enable-creds
  python omnicamxploit.py 192.168.1.100 --enable-creds --max-attempts 500 -v

For authorized security testing only. Unauthorized access is illegal.
        """
    )
    
    parser.add_argument('target', help='Target IP address or hostname')
    parser.add_argument('--enable-creds', action='store_true',
                       help='Enable credential testing (requires authorization)')
    parser.add_argument('--max-attempts', type=int, default=1000,
                       help='Maximum credential attempts (default: 1000)')
    parser.add_argument('--timeout', type=float, default=1.0,
                       help='Port scan timeout in seconds (default: 1.0)')
    parser.add_argument('--workers', type=int, default=200,
                       help='Number of worker threads (default: 200)')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Enable verbose output')
    parser.add_argument('--version', action='version',
                       version=f'OmniCamXploit v{OmniCamXploitEngine.VERSION}')
    
    args = parser.parse_args()
    
    # Display ethical warning for credential testing
    if args.enable_creds:
        print(f"\n{Fore.RED}{'='*60}")
        print(f"{Fore.RED}⚠️  CREDENTIAL TESTING ENABLED ⚠️")
        print(f"{Fore.RED}{'='*60}")
        print(f"{Fore.YELLOW}This feature should only be used on systems you own or")
        print(f"have explicit written authorization to test.")
        print(f"Unauthorized access is illegal and punishable by law.{Style.RESET_ALL}")
        print(f"{Fore.RED}{'='*60}\n{Style.RESET_ALL}")
        
        response = input(f"{Fore.CYAN}Do you have authorization to test this target? (yes/no): {Style.RESET_ALL}")
        if response.lower() not in ['yes', 'y']:
            print(f"{Fore.RED}❌ Authorization not confirmed. Exiting.{Style.RESET_ALL}")
            sys.exit(1)
    
    # Create configuration
    config = ScanConfig(
        target=args.target,
        enable_credential_testing=args.enable_creds,
        max_credential_attempts=args.max_attempts,
        port_scan_timeout=args.timeout,
        max_workers=args.workers,
        verbose=args.verbose
    )
    
    # Run the assessment
    try:
        engine = OmniCamXploitEngine(config)
        results = engine.run_scan()
        
        print(f"\n{Fore.GREEN}✅ Assessment Complete!{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Results saved to: omnicamxploit_report_{config.target.replace('.', '_')}.txt{Style.RESET_ALL}\n")
        
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}⚠️  Scan interrupted by user{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}❌ Error: {str(e)}{Style.RESET_ALL}")
        if config.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
