"""Report Generator Module - Professional security assessment reports."""

from typing import Dict
from datetime import datetime
from colorama import Fore, Style


class ReportGenerator:
    """Generates professional security assessment reports."""
    
    def __init__(self, config):
        """Initialize report generator."""
        self.config = config
        
    def calculate_risk_score(self, results: Dict) -> int:
        """Calculate overall risk score (0-100)."""
        score = 0
        
        # Open ports contribute to risk
        score += min(len(results['open_ports']) * 2, 30)
        
        # Identified devices
        score += min(len(results['identified_devices']) * 5, 20)
        
        # Validated streams
        score += min(len(results['validated_streams']) * 10, 30)
        
        # Default credentials are critical
        if results['credentials_found']:
            score += 20
        
        return min(score, 100)
    
    def get_risk_level(self, score: int) -> tuple:
        """Get risk level and color based on score."""
        if score >= 80:
            return ('CRITICAL', Fore.RED)
        elif score >= 60:
            return ('HIGH', Fore.LIGHTRED_EX)
        elif score >= 40:
            return ('MEDIUM', Fore.YELLOW)
        elif score >= 20:
            return ('LOW', Fore.LIGHTYELLOW_EX)
        else:
            return ('MINIMAL', Fore.GREEN)
    
    def generate_console_report(self, results: Dict, risk_score: int):
        """Generate colorful console report."""
        risk_level, risk_color = self.get_risk_level(risk_score)
        
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}📊 SECURITY ASSESSMENT REPORT{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
        
        # Target info
        print(f"{Fore.WHITE}🎯 Target: {Fore.CYAN}{results['target']}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}📅 Scan Date: {Fore.CYAN}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}")
        
        # Risk score
        print(f"\n{Fore.WHITE}🛡️  Overall Risk Score: {risk_color}{risk_score}/100 ({risk_level}){Style.RESET_ALL}")
        print(f"{risk_color}{'█' * (risk_score // 2)}{Style.RESET_ALL}{'░' * (50 - risk_score // 2)}")
        
        # Findings
        print(f"\n{Fore.CYAN}📋 FINDINGS:{Style.RESET_ALL}")
        print(f"{Fore.WHITE}  • Open Ports: {Fore.YELLOW}{len(results['open_ports'])}{Style.RESET_ALL}")
        if results['open_ports'][:10]:
            print(f"    {', '.join(map(str, results['open_ports'][:10]))}" + 
                  (f"... (+{len(results['open_ports'])-10} more)" if len(results['open_ports']) > 10 else ""))
        
        print(f"{Fore.WHITE}  • Identified Devices: {Fore.YELLOW}{len(results['identified_devices'])}{Style.RESET_ALL}")
        for device in results['identified_devices'][:5]:
            print(f"    Port {device['port']}: {device['brand']} ({device['confidence']} confidence)")
        
        print(f"{Fore.WHITE}  • Validated Streams: {Fore.YELLOW}{len(results['validated_streams'])}{Style.RESET_ALL}")
        
        if results['credentials_found']:
            print(f"{Fore.RED}  • Default Credentials: {len(results['credentials_found'])} FOUND ⚠️{Style.RESET_ALL}")
            for cred in results['credentials_found']:
                print(f"{Fore.RED}    Port {cred['port']}: {cred['username']}:{cred['password']}{Style.RESET_ALL}")
        
        # Geolocation
        if results['geolocation']:
            geo = results['geolocation']
            print(f"\n{Fore.CYAN}🌍 GEOLOCATION:{Style.RESET_ALL}")
            print(f"{Fore.WHITE}  • Location: {Fore.YELLOW}{geo['city']}, {geo['region']}, {geo['country']}{Style.RESET_ALL}")
            print(f"{Fore.WHITE}  • ISP: {Fore.YELLOW}{geo['isp']}{Style.RESET_ALL}")
            print(f"{Fore.WHITE}  • Coordinates: {Fore.YELLOW}{geo['lat']}, {geo['lon']}{Style.RESET_ALL}")
            print(f"{Fore.WHITE}  • Google Maps: {Fore.CYAN}{geo['google_maps']}{Style.RESET_ALL}")
        
        # Recommendations
        print(f"\n{Fore.CYAN}💡 RECOMMENDATIONS:{Style.RESET_ALL}")
        
        if results['credentials_found']:
            print(f"{Fore.RED}  🔴 CRITICAL: Change default credentials immediately{Style.RESET_ALL}")
        
        if len(results['open_ports']) > 10:
            print(f"{Fore.YELLOW}  🟡 HIGH: Reduce exposed ports - close unnecessary services{Style.RESET_ALL}")
        
        if results['validated_streams']:
            print(f"{Fore.YELLOW}  🟡 MEDIUM: Implement stream authentication{Style.RESET_ALL}")
        
        print(f"{Fore.CYAN}  🔵 INFO: Enable firewall rules to restrict access{Style.RESET_ALL}")
        print(f"{Fore.CYAN}  🔵 INFO: Keep firmware updated{Style.RESET_ALL}")
        print(f"{Fore.CYAN}  🔵 INFO: Use VPN for remote access{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
    
    def generate_file_report(self, results: Dict, risk_score: int) -> str:
        """Generate text file report."""
        risk_level, _ = self.get_risk_level(risk_score)
        
        report = []
        report.append("="*60)
        report.append("OMNICAMXPLOIT v4.0 - SECURITY ASSESSMENT REPORT")
        report.append("="*60)
        report.append("")
        report.append(f"Target: {results['target']}")
        report.append(f"Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Risk Score: {risk_score}/100 ({risk_level})")
        report.append("")
        report.append("FINDINGS:")
        report.append(f"  Open Ports: {len(results['open_ports'])}")
        report.append(f"    {', '.join(map(str, results['open_ports']))}")
        report.append("")
        report.append(f"  Identified Devices: {len(results['identified_devices'])}")
        for device in results['identified_devices']:
            report.append(f"    Port {device['port']}: {device['brand']} ({device['confidence']} confidence)")
        report.append("")
        report.append(f"  Validated Streams: {len(results['validated_streams'])}")
        report.append("")
        
        if results['credentials_found']:
            report.append(f"  Default Credentials Found: {len(results['credentials_found'])}")
            for cred in results['credentials_found']:
                report.append(f"    Port {cred['port']}: {cred['username']}:{cred['password']}")
            report.append("")
        
        if results['geolocation']:
            geo = results['geolocation']
            report.append("GEOLOCATION:")
            report.append(f"  Location: {geo['city']}, {geo['region']}, {geo['country']}")
            report.append(f"  ISP: {geo['isp']}")
            report.append(f"  Coordinates: {geo['lat']}, {geo['lon']}")
            report.append(f"  Google Maps: {geo['google_maps']}")
            report.append("")
        
        report.append("RECOMMENDATIONS:")
        if results['credentials_found']:
            report.append("  [CRITICAL] Change default credentials immediately")
        if len(results['open_ports']) > 10:
            report.append("  [HIGH] Reduce exposed ports")
        if results['validated_streams']:
            report.append("  [MEDIUM] Implement stream authentication")
        report.append("  [INFO] Enable firewall rules")
        report.append("  [INFO] Keep firmware updated")
        report.append("  [INFO] Use VPN for remote access")
        report.append("")
        report.append("="*60)
        
        return "\n".join(report)
    
    def generate(self, results: Dict):
        """Generate both console and file reports."""
        risk_score = self.calculate_risk_score(results)
        results['risk_score'] = risk_score
        
        # Console report
        self.generate_console_report(results, risk_score)
        
        # File report
        filename = f"omnicamxploit_report_{results['target'].replace('.', '_')}.txt"
        file_content = self.generate_file_report(results, risk_score)
        
        with open(filename, 'w') as f:
            f.write(file_content)
