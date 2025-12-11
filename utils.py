"""
Utility functions for Parameter Bug Hunter Pro
"""

import os
import json
import hashlib
import random
import string
from datetime import datetime
from pathlib import Path
import requests
from colorama import Fore, Style

class Utils:
    @staticmethod
    def generate_session_id(length=16):
        """Generate unique session ID"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    @staticmethod
    def calculate_hash(data):
        """Calculate hash of data"""
        if isinstance(data, str):
            data = data.encode()
        return hashlib.md5(data).hexdigest()
    
    @staticmethod
    def save_evidence(data, filename, directory="evidence"):
        """Save evidence to file"""
        Path(directory).mkdir(exist_ok=True)
        
        filepath = Path(directory) / filename
        
        if isinstance(data, dict) or isinstance(data, list):
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
        else:
            with open(filepath, 'w') as f:
                f.write(str(data))
        
        return filepath
    
    @staticmethod
    def load_json_file(filepath):
        """Load JSON file safely"""
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
    
    @staticmethod
    def print_table(data, headers):
        """Print data in table format"""
        from tabulate import tabulate
        print(tabulate(data, headers=headers, tablefmt="grid"))
    
    @staticmethod
    def progress_bar(iterable, desc="Processing", length=50):
        """Display progress bar"""
        from tqdm import tqdm
        return tqdm(iterable, desc=desc, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}")
    
    @staticmethod
    def check_internet():
        """Check internet connection"""
        try:
            requests.get("https://www.google.com", timeout=5)
            return True
        except:
            return False
    
    @staticmethod
    def get_timestamp():
        """Get current timestamp"""
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    
    @staticmethod
    def sanitize_filename(filename):
        """Sanitize filename to remove invalid characters"""
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        return filename[:255]
