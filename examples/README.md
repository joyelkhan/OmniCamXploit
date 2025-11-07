# OmniCamXploit Examples

This directory contains example scripts demonstrating various usage patterns.

## Examples

### 1. Basic Usage (`basic_usage.py`)
Simple example showing how to use OmniCamXploit as a Python module.

```bash
cd examples
python basic_usage.py
```

### 2. Advanced Usage (`advanced_usage.py`)
Advanced example with custom configuration and JSON export.

```bash
cd examples
python advanced_usage.py
```

## Command-Line Examples

### Basic Scan
```bash
python ../omnicamxploit.py 192.168.1.100
```

### With Credential Testing
```bash
python ../omnicamxploit.py 192.168.1.100 --enable-creds
```

### Custom Settings
```bash
python ../omnicamxploit.py 192.168.1.100 \
  --enable-creds \
  --max-attempts 500 \
  --timeout 2.0 \
  --workers 100 \
  -v
```

### Docker Usage
```bash
# Build image
docker build -t omnicamxploit ..

# Run scan
docker run omnicamxploit 192.168.1.100

# With credential testing
docker run -it omnicamxploit 192.168.1.100 --enable-creds
```

## Integration Examples

### Use in Your Python Project
```python
from omnicamxploit import OmniCamXploitEngine, ScanConfig

config = ScanConfig(target="192.168.1.100")
engine = OmniCamXploitEngine(config)
results = engine.run_scan()

# Process results
for port in results['open_ports']:
    print(f"Open port: {port}")
```

### Batch Scanning
```python
targets = ["192.168.1.100", "192.168.1.101", "192.168.1.102"]

for target in targets:
    config = ScanConfig(target=target)
    engine = OmniCamXploitEngine(config)
    results = engine.run_scan()
    print(f"Completed scan of {target}")
```

## Notes

- Always ensure you have **authorization** before scanning
- Use `--enable-creds` only when **legally permitted**
- Respect **rate limits** and **network policies**
- Review results carefully before taking action
