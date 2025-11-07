# 🎯 OmniCamXploit v1.0

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0-blue.svg)]()

**Professional Camera Security Assessment Framework**

**Author:** Md. Abu Naser Khan  
**License:** MIT

---

## 🔥 Features

### **Advanced Credential Engine**
- 🔐 **100,000+ Password Database** - Massive credential coverage
- 🎯 **Smart Attack Strategies** - Ultra-fast to comprehensive
- 🏷️ **Brand-Specific Targeting** - Manufacturer-aware credentials
- 🧠 **Pattern Generation** - Intelligent password variations
- ⚡ **Multi-threaded Testing** - Concurrent validation

### **Core Capabilities**
- ✅ **1000+ Camera Ports** - Comprehensive port scanning
- ✅ **Device Fingerprinting** - Hikvision, Dahua, CP Plus, Axis, and more
- ✅ **Stream Validation** - Real RTSP/HTTP stream testing
- ✅ **Geolocation** - IP location with Google Maps integration
- ✅ **Professional Reports** - Risk assessment and recommendations

---

## 🚀 Quick Start

### Installation
```bash
git clone https://github.com/joyelkhan/OmniCamXploit.git
cd OmniCamXploit
pip install -r requirements.txt
```

### Basic Scan
```bash
python omnicamxploit.py 192.168.1.100
```

### With Credential Testing
```bash
python omnicamxploit.py 192.168.1.100 --enable-creds
```

---

## 🎯 Attack Strategies

The advanced credential engine supports multiple strategies:

| Strategy | Credentials | Use Case |
|----------|-------------|----------|
| **ultra_fast** | 100 | Quick assessment |
| **common_only** | 1,000 | Standard testing |
| **brand_targeted** | 5,000 | Manufacturer-specific |
| **comprehensive** | 25,000 | Thorough assessment |
| **brute_force** | 100,000+ | Maximum coverage |

---

## 📊 Usage Examples

### Basic Security Assessment
```bash
python omnicamxploit.py 192.168.1.100
```

### Advanced Testing with Credentials
```bash
python omnicamxploit.py 192.168.1.100 --enable-creds --max-attempts 5000
```

### Verbose Mode
```bash
python omnicamxploit.py 192.168.1.100 --enable-creds -v
```

### Custom Configuration
```bash
python omnicamxploit.py 192.168.1.100 \
  --enable-creds \
  --max-attempts 10000 \
  --timeout 2.0 \
  --workers 100 \
  -v
```

---

## 🏗️ Architecture

```
OmniCamXploit/
├── omnicamxploit.py              # Main application
├── modules/
│   ├── port_scanner.py           # 1000+ port scanning
│   ├── device_identifier.py      # Device fingerprinting
│   ├── stream_validator.py       # Stream validation
│   ├── credential_tester.py      # Credential testing
│   ├── credential_engine.py      # 🔥 Advanced credential engine
│   ├── geolocator.py            # IP geolocation
│   └── report_generator.py       # Professional reports
├── examples/                     # Usage examples
├── requirements.txt              # Dependencies
└── LICENSE                       # MIT License
```

---

## 🔐 Credential Engine Details

### Database Structure
```
credential_database/
├── common/                       # 50,000+ common passwords
├── brand_specific/               # Manufacturer defaults
├── patterns/                     # Date/sequence patterns
├── custom/                       # Custom wordlists
└── generated/                    # On-the-fly generation
```

### Supported Brands
- Hikvision
- Dahua
- CP Plus
- Axis
- Sony
- Bosch
- Generic DVR/NVR

---

## ⚠️ Legal Disclaimer

**FOR AUTHORIZED SECURITY TESTING ONLY**

- ✅ Only test systems you own or have written permission to test
- ✅ Obtain authorization before any testing
- ✅ Comply with all applicable laws
- ❌ Unauthorized access is illegal

---

## 📋 Requirements

```
colorama>=0.4.6
requests>=2.31.0
tqdm>=4.66.0
urllib3>=2.0.0
```

---

## 🤝 Contributing

Contributions are welcome! Please ensure:
- Code follows PEP 8 style guidelines
- All tests pass
- Documentation is updated
- Ethical use only

---

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

**Disclaimer:** This tool is for authorized security testing only. Unauthorized access to computer systems is illegal. Users are responsible for complying with all applicable laws.

---

## 📞 Contact

**Author:** Md. Abu Naser Khan

**GitHub:** https://github.com/joyelkhan/OmniCamXploit

For issues and feature requests, please use [GitHub Issues](https://github.com/joyelkhan/OmniCamXploit/issues).

---

<div align="center">

**OmniCamXploit v1.0** - Professional Camera Security Assessment

*Made for the Security Community*

⚠️ **For Authorized Testing Only** ⚠️

</div>
