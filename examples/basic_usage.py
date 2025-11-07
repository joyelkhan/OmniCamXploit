#!/usr/bin/env python3
"""
Example: Basic usage of OmniCamXploit as a Python module
"""

import sys
sys.path.insert(0, '..')

from omnicamxploit import OmniCamXploitEngine, ScanConfig


def main():
    """Run a basic security assessment."""
    
    # Create configuration
    config = ScanConfig(
        target="192.168.1.100",
        enable_credential_testing=False,  # Set to True for credential testing
        verbose=True
    )
    
    # Initialize engine
    engine = OmniCamXploitEngine(config)
    
    # Run scan
    results = engine.run_scan()
    
    # Access results
    print(f"\n📊 Scan Results:")
    print(f"  Open Ports: {len(results['open_ports'])}")
    print(f"  Identified Devices: {len(results['identified_devices'])}")
    print(f"  Validated Streams: {len(results['validated_streams'])}")
    print(f"  Risk Score: {results['risk_score']}/100")
    
    # Process results
    if results['credentials_found']:
        print(f"\n⚠️  WARNING: Found {len(results['credentials_found'])} default credentials!")
        for cred in results['credentials_found']:
            print(f"    Port {cred['port']}: {cred['username']}:{cred['password']}")


if __name__ == '__main__':
    main()
