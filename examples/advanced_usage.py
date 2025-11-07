#!/usr/bin/env python3
"""
Example: Advanced usage with custom configuration
"""

import sys
sys.path.insert(0, '..')

from omnicamxploit import OmniCamXploitEngine, ScanConfig
import json


def main():
    """Run advanced security assessment with custom settings."""
    
    # Advanced configuration
    config = ScanConfig(
        target="192.168.1.100",
        enable_credential_testing=True,
        max_credential_attempts=500,  # Limit attempts
        port_scan_timeout=2.0,  # Longer timeout for slow networks
        stream_validation_timeout=10.0,
        max_workers=100,  # Reduce workers for resource-constrained systems
        verbose=True
    )
    
    # Initialize engine
    engine = OmniCamXploitEngine(config)
    
    # Run scan
    print("🚀 Starting advanced security assessment...")
    results = engine.run_scan()
    
    # Export results to JSON
    output_file = f"scan_results_{config.target.replace('.', '_')}.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n✅ Results exported to: {output_file}")
    
    # Custom analysis
    print("\n🔍 Custom Analysis:")
    
    # Check for high-risk ports
    high_risk_ports = [p for p in results['open_ports'] if p in [23, 21, 3389]]
    if high_risk_ports:
        print(f"  ⚠️  High-risk ports detected: {high_risk_ports}")
    
    # Check for specific brands
    cp_plus_devices = [d for d in results['identified_devices'] if 'CP Plus' in d['brand']]
    if cp_plus_devices:
        print(f"  📱 CP Plus devices found: {len(cp_plus_devices)}")
    
    # Stream analysis
    total_streams = sum(
        len(s['rtsp_streams']) + len(s['http_streams']) 
        for s in results['validated_streams']
    )
    print(f"  📹 Total validated streams: {total_streams}")
    
    # Geolocation
    if results['geolocation']:
        geo = results['geolocation']
        print(f"  🌍 Location: {geo['city']}, {geo['country']}")
        print(f"  📍 View on map: {geo['google_maps']}")


if __name__ == '__main__':
    main()
