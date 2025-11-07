#!/usr/bin/env python3
"""
🔐 Advanced Credential Engine for OmniCamXploit v1.0
Author: Md. Abu Naser Khan
Massive Password Database + Smart Generation + Attack Simulation
"""

import itertools
import random
import string
import hashlib
import json
import os
import time
from typing import List, Dict, Any, Generator, Set
from dataclasses import dataclass
from colorama import Fore, Style
import logging

logger = logging.getLogger(__name__)

@dataclass
class CredentialStrategy:
    """🎯 Attack strategy configuration"""
    name: str
    priority: int
    max_attempts: int
    description: str

class MassCredentialEngine:
    """🔥 Massive Credential Database with Smart Generation"""
    
    def __init__(self, database_path: str = "credential_database"):
        self.database_path = database_path
        self.strategies = self._initialize_strategies()
        self.credential_cache: Dict[str, List[str]] = {}
        
        # Ensure database exists
        self._initialize_database()
    
    def _initialize_strategies(self) -> Dict[str, CredentialStrategy]:
        """🎯 Initialize attack strategies"""
        return {
            'ultra_fast': CredentialStrategy(
                name="Ultra Fast",
                priority=1,
                max_attempts=100,
                description="Quick common passwords only"
            ),
            'common_only': CredentialStrategy(
                name="Common Passwords", 
                priority=2,
                max_attempts=1000,
                description="Top 1K most common passwords"
            ),
            'brand_targeted': CredentialStrategy(
                name="Brand Targeted",
                priority=3, 
                max_attempts=5000,
                description="Manufacturer-specific credentials"
            ),
            'comprehensive': CredentialStrategy(
                name="Comprehensive",
                priority=4,
                max_attempts=25000,
                description="Extended password database"
            ),
            'brute_force': CredentialStrategy(
                name="Brute Force",
                priority=5,
                max_attempts=100000,
                description="Massive credential attack"
            )
        }
    
    def _initialize_database(self):
        """🗃️ Initialize credential database structure"""
        os.makedirs(self.database_path, exist_ok=True)
        
        # Create subdirectories for different credential types
        subdirs = ['common', 'brand_specific', 'patterns', 'generated', 'custom']
        for subdir in subdirs:
            os.makedirs(os.path.join(self.database_path, subdir), exist_ok=True)
        
        # Generate databases if they don't exist
        self._generate_common_passwords()
        self._generate_brand_specific()
        self._generate_pattern_passwords()
        self._generate_custom_wordlists()
    
    def _generate_common_passwords(self):
        """📊 Generate massive common password database"""
        common_file = os.path.join(self.database_path, 'common', 'top_100k.txt')
        
        if not os.path.exists(common_file):
            logger.info("🔧 Generating common passwords database...")
            
            common_passwords = set()
            
            # Top 100 most common (quick attacks)
            top_100 = [
                '123456', 'password', '12345678', 'qwerty', '123456789',
                '12345', '1234', '111111', '1234567', 'dragon',
                '123123', 'baseball', 'abc123', 'football', 'monkey',
                'letmein', '696969', 'shadow', 'master', '666666',
                'qwertyuiop', '123321', 'mustang', '1234567890', 'michael',
                '654321', 'superman', '1qaz2wsx', '7777777', '121212',
                '000000', 'qazwsx', '123qwe', 'killer', 'trustno1',
                'jordan', 'jennifer', 'zxcvbnm', 'asdfgh', 'hunter',
                'buster', 'soccer', 'harley', 'batman', 'andrew',
                'tigger', 'sunshine', 'iloveyou', '2000', 'charlie',
                'robert', 'thomas', 'hockey', 'ranger', 'daniel',
                'starwars', 'klaster', '112233', 'george', 'computer',
                'michelle', 'jessica', 'pepper', '1111', 'zxcvbn',
                '555555', '11111111', '131313', 'freedom', '777777',
                'pass', 'maggie', '159753', 'aaaaaa', 'ginger',
                'princess', 'joshua', 'cheese', 'amanda', 'summer',
                'love', 'ashley', '6969', 'nicole', 'chelsea',
                'biteme', 'matthew', 'access', 'yankees', '987654321',
                'dallas', 'austin', 'thunder', 'taylor', 'matrix'
            ]
            common_passwords.update(top_100)
            
            # Number sequences (1K variations)
            for i in range(10000):
                common_passwords.add(str(i).zfill(4))  # 0000-9999
                if i < 100000:
                    common_passwords.add(str(i).zfill(5))  # 00000-99999
                if i < 1000:
                    common_passwords.add(str(i).zfill(3))  # 000-999
            
            # Keyboard patterns (500 variations)
            keyboard_patterns = [
                'qwerty', 'asdfgh', 'zxcvbn', 'qazwsx', 'edcrfv',
                '1qaz2wsx', '1q2w3e4r', '1q2w3e4r5t', 'qwer1234',
                'abcd1234', 'qwe123', 'qweasd', 'qweasdzxc',
                'zaq12wsx', 'zaq1xsw2', '!qaz2wsx', '1qaz@wsx'
            ]
            common_passwords.update(keyboard_patterns)
            
            # Write to file
            with open(common_file, 'w') as f:
                for pwd in sorted(common_passwords):
                    f.write(pwd + '\n')
            
            logger.info(f"✅ Generated {len(common_passwords)} common passwords")
    
    def _generate_brand_specific(self):
        """🏷️ Generate manufacturer-specific credentials"""
        brand_credentials = {
            'Hikvision': {
                'usernames': ['admin', 'root', 'user', 'operator'],
                'passwords': ['12345', 'hikvision', 'admin12345', '', '1234abcd']
            },
            'Dahua': {
                'usernames': ['admin', 'root', 'default'],
                'passwords': ['admin', 'dahua', '666666', '888888', '']
            },
            'CP_Plus': {
                'usernames': ['admin', 'root', 'supervisor'],
                'passwords': ['admin', '1234', 'password', '', 'cpplus']
            },
            'Axis': {
                'usernames': ['root', 'admin', 'operator'],
                'passwords': ['pass', 'axis', 'admin', '']
            },
            'Sony': {
                'usernames': ['admin', 'root', 'viewer'],
                'passwords': ['admin', 'sony', '']
            },
            'Bosch': {
                'usernames': ['admin', 'service', 'user'],
                'passwords': ['admin', 'bosch', '1234', '']
            },
            'Generic_DVR': {
                'usernames': ['admin', 'root', 'user', 'guest', 'supervisor'],
                'passwords': ['admin', 'password', '1234', '12345', '123456', '']
            }
        }
        
        for brand, creds in brand_credentials.items():
            brand_file = os.path.join(self.database_path, 'brand_specific', f'{brand.lower()}.txt')
            
            with open(brand_file, 'w') as f:
                for username in creds['usernames']:
                    for password in creds['passwords']:
                        f.write(f"{username}:{password}\n")
        
        logger.info(f"✅ Generated credentials for {len(brand_credentials)} brands")
    
    def _generate_pattern_passwords(self):
        """🎭 Generate pattern-based passwords"""
        pattern_file = os.path.join(self.database_path, 'patterns', 'common_patterns.txt')
        
        patterns = set()
        
        # Date patterns (10K variations)
        for year in range(1990, 2030):
            patterns.add(str(year))
            for month in range(1, 13):
                patterns.add(f"{month:02d}{year}")
                patterns.add(f"{year}{month:02d}")
        
        # Company name patterns
        companies = ['cisco', 'hikvision', 'dahua', 'axis', 'sony', 'bosch', 'samsung']
        for company in companies:
            patterns.add(company)
            patterns.add(company + '123')
            patterns.add(company + '1234')
            patterns.add(company.upper())
            patterns.add(company.capitalize())
        
        # Sequential patterns
        for length in range(3, 8):
            for start in range(10 - length):
                seq = ''.join(str((start + i) % 10) for i in range(length))
                patterns.add(seq)
        
        with open(pattern_file, 'w') as f:
            for pattern in sorted(patterns):
                f.write(pattern + '\n')
        
        logger.info(f"✅ Generated {len(patterns)} pattern passwords")
    
    def _generate_custom_wordlists(self):
        """📝 Generate custom wordlists for specific attacks"""
        # Empty passwords and simple variations
        empty_file = os.path.join(self.database_path, 'custom', 'empty_simple.txt')
        with open(empty_file, 'w') as f:
            f.write("\n".join(['', ' ', '  ', '\t', '\n', 'null', 'none']))
        
        # Default camera passwords
        camera_defaults = os.path.join(self.database_path, 'custom', 'camera_defaults.txt')
        with open(camera_defaults, 'w') as f:
            defaults = [
                'admin', 'password', '1234', '12345', '123456', '0000', '1111',
                '888888', '666666', '9999', 'admin1234', 'admin12345', 'camera',
                'security', 'surveillance', 'default', 'root', 'pass', '12345678',
                '123456789', '1234567890', 'qwerty', 'abc123', 'password1'
            ]
            f.write("\n".join(defaults))
    
    def get_credentials(self, strategy: str, brand: str = None) -> Generator[str, None, None]:
        """🎯 Get credentials based on attack strategy"""
        if strategy not in self.strategies:
            raise ValueError(f"Unknown strategy: {strategy}")
        
        strategy_config = self.strategies[strategy]
        credentials = set()
        
        # Ultra Fast - Only top 100
        if strategy == 'ultra_fast':
            common_file = os.path.join(self.database_path, 'common', 'top_100k.txt')
            if os.path.exists(common_file):
                with open(common_file, 'r') as f:
                    for i, line in enumerate(f):
                        if i >= 100:
                            break
                        credentials.add(line.strip())
        
        # Common passwords
        elif strategy == 'common_only':
            common_file = os.path.join(self.database_path, 'common', 'top_100k.txt')
            if os.path.exists(common_file):
                with open(common_file, 'r') as f:
                    for i, line in enumerate(f):
                        if i >= 1000:
                            break
                        credentials.add(line.strip())
        
        # Brand targeted
        elif strategy == 'brand_targeted':
            if brand:
                brand_file = os.path.join(self.database_path, 'brand_specific', f'{brand.lower()}.txt')
                if os.path.exists(brand_file):
                    with open(brand_file, 'r') as f:
                        for line in f:
                            credentials.add(line.strip())
            
            # Fallback to common passwords
            common_file = os.path.join(self.database_path, 'common', 'top_100k.txt')
            if os.path.exists(common_file):
                with open(common_file, 'r') as f:
                    for i, line in enumerate(f):
                        if i >= 2000:
                            break
                        credentials.add(line.strip())
        
        # Comprehensive attack
        elif strategy == 'comprehensive':
            sources = [
                os.path.join(self.database_path, 'common', 'top_100k.txt'),
                os.path.join(self.database_path, 'patterns', 'common_patterns.txt'),
                os.path.join(self.database_path, 'custom', 'camera_defaults.txt')
            ]
            
            for source in sources:
                if os.path.exists(source):
                    with open(source, 'r') as f:
                        for line in f:
                            credentials.add(line.strip())
        
        # Brute force - massive attack
        elif strategy == 'brute_force':
            for root, dirs, files in os.walk(self.database_path):
                for file in files:
                    if file.endswith('.txt'):
                        file_path = os.path.join(root, file)
                        with open(file_path, 'r') as f:
                            for line in f:
                                credentials.add(line.strip())
        
        # Yield credentials with limit
        count = 0
        for cred in credentials:
            if count >= strategy_config.max_attempts:
                break
            yield cred
            count += 1
        
        logger.info(f"🎯 Strategy '{strategy}' yielded {count} credentials")
    
    def get_database_stats(self) -> Dict[str, Any]:
        """📈 Get credential database statistics"""
        stats = {
            'total_files': 0,
            'total_entries': 0,
            'categories': {}
        }
        
        for root, dirs, files in os.walk(self.database_path):
            category = os.path.basename(root)
            category_entries = 0
            
            for file in files:
                if file.endswith('.txt'):
                    file_path = os.path.join(root, file)
                    stats['total_files'] += 1
                    
                    try:
                        with open(file_path, 'r') as f:
                            entries = len(f.readlines())
                            stats['total_entries'] += entries
                            category_entries += entries
                    except:
                        pass
            
            if category_entries > 0:
                stats['categories'][category] = category_entries
        
        return stats
