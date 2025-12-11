#!/usr/bin/env python3
"""
PARAMETER BUG HUNTER PRO - Version 2.0
A Comprehensive Parameter Analysis Framework for Bug Bounty Hunters
Author: Security Researcher
GitHub: @parameterhunter
"""

import os
import sys
import json
import yaml
import subprocess
import argparse
from datetime import datetime
from pathlib import Path
from colorama import init, Fore, Style
import threading
import queue
import requests
from urllib.parse import urlparse
import sqlite3
import hashlib
import shutil
from pathlib import Path
import sys

# Add this function to check dependencies
def check_dependencies():
    """Check if all dependencies are met"""
    required_packages = ['colorama', 'requests', 'yaml']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"{Fore.RED}Missing packages: {', '.join(missing_packages)}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Install with: pip install {' '.join(missing_packages)}{Style.RESET_ALL}")
        return False
    
    # Check for tools
    required_tools = ['sqlmap', 'ffuf']
    missing_tools = []
    
    for tool in required_tools:
        if not shutil.which(tool):
            missing_tools.append(tool)
    
    if missing_tools:
        print(f"{Fore.YELLOW}Some tools are missing. Some features may be limited.{Style.RESET_ALL}")
        print(f"Missing: {', '.join(missing_tools)}")
    
    return True

# Modify main function to check dependencies
def main():
    """Main function"""
    if not check_dependencies():
        print(f"{Fore.RED}Please install missing dependencies first.{Style.RESET_ALL}")
        sys.exit(1)

# Initialize colorama
init(autoreset=True)

class ParameterBugHunter:
    def __init__(self):
        self.config = self.load_config()
        self.project_path = ""
        self.results_db = None
        self.current_workflow = {}
        
    def load_config(self):
        """Load configuration from YAML file"""
        config_path = Path.home() / ".parameter_hunter" / "config.yaml"
        if config_path.exists():
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        return {
            'tools': {
                'arjun': '/usr/bin/arjun',
                'sqlmap': '/usr/bin/sqlmap',
                'ffuf': '/usr/bin/ffuf',
                'gau': '/usr/bin/gau',
                'waybackurls': '/usr/bin/waybackurls',
                'nuclei': '/usr/bin/nuclei',
                'subfinder': '/usr/bin/subfinder'
            },
            'wordlists': {
                'parameters': '/usr/share/wordlists/parameter-names.txt',
                'subdomains': '/usr/share/wordlists/subdomains-top1million.txt'
            },
            'api_keys': {},
            'proxy': None
        }
    
    def save_config(self):
        """Save configuration to YAML file"""
        config_dir = Path.home() / ".parameter_hunter"
        config_dir.mkdir(exist_ok=True)
        config_path = config_dir / "config.yaml"
        with open(config_path, 'w') as f:
            yaml.dump(self.config, f)
    
    def display_banner(self):
        """Display the main banner"""
        banner = f"""{Fore.CYAN}
╔═══════════════════════════════════════════════════════════╗
║                PARAMETER BUG HUNTER PRO                   ║
║                  Version 2.0 - Systematic                 ║
╚═══════════════════════════════════════════════════════════╝
{Style.RESET_ALL}"""
        print(banner)
    
    def display_menu(self):
        """Display the main menu"""
        menus = {
            "1": "🎯 RECONNAISSANCE & DISCOVERY",
            "2": "🔍 PARAMETER EXTRACTION PHASE",
            "3": "📊 PARAMETER CLASSIFICATION",
            "4": "⚔️ AUTOMATED TESTING SUITE",
            "5": "🧠 BUSINESS LOGIC TESTING",
            "6": "🔬 ADVANCED TECHNIQUES",
            "7": "📈 VALIDATION & VERIFICATION",
            "8": "📋 REPORTING & DOCUMENTATION",
            "9": "⚙️ TOOL MANAGEMENT",
            "10": "📚 LEARNING & IMPROVEMENT"
        }
        
        while True:
            self.display_banner()
            print(f"{Fore.YELLOW}MAIN MENU - PARAMETER ANALYSIS FRAMEWORK{Style.RESET_ALL}\n")
            
            for key, value in menus.items():
                print(f"{Fore.GREEN}[{key}] {value}{Style.RESET_ALL}")
            
            print(f"\n{Fore.CYAN}[99] Exit")
            print(f"[00] Create New Project{Style.RESET_ALL}")
            
            choice = input(f"\n{Fore.YELLOW}Select option: {Style.RESET_ALL}").strip()
            
            if choice == "99":
                print(f"{Fore.RED}Exiting...{Style.RESET_ALL}")
                sys.exit(0)
            elif choice == "00":
                self.create_project()
            elif choice in menus:
                self.handle_menu_choice(choice)
            else:
                print(f"{Fore.RED}Invalid choice!{Style.RESET_ALL}")
    
    def create_project(self):
        """Create a new project directory"""
        project_name = input(f"{Fore.YELLOW}Enter project name: {Style.RESET_ALL}").strip()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.project_path = Path(f"projects/{project_name}_{timestamp}")
        
        # Create directory structure
        dirs = [
            "reconnaissance",
            "parameters",
            "testing",
            "business_logic",
            "advanced",
            "validation",
            "reports",
            "evidence",
            "tools"
        ]
        
        for dir_name in dirs:
            (self.project_path / dir_name).mkdir(parents=True, exist_ok=True)
        
        # Create project config
        project_config = {
            "name": project_name,
            "created": timestamp,
            "target": "",
            "scope": "",
            "status": "active"
        }
        
        with open(self.project_path / "project.json", 'w') as f:
            json.dump(project_config, f, indent=2)
        
        print(f"{Fore.GREEN}Project created at: {self.project_path}{Style.RESET_ALL}")
        self.initialize_database()
    
    def initialize_database(self):
        """Initialize SQLite database for results"""
        db_path = self.project_path / "results.db"
        self.results_db = sqlite3.connect(db_path)
        cursor = self.results_db.cursor()
        
        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS targets (
                id INTEGER PRIMARY KEY,
                url TEXT UNIQUE,
                domain TEXT,
                discovered_at TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS parameters (
                id INTEGER PRIMARY KEY,
                url TEXT,
                parameter TEXT,
                parameter_type TEXT,
                risk_level TEXT,
                discovered_at TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vulnerabilities (
                id INTEGER PRIMARY KEY,
                parameter_id INTEGER,
                vulnerability_type TEXT,
                severity TEXT,
                poc TEXT,
                verified BOOLEAN,
                discovered_at TIMESTAMP,
                FOREIGN KEY (parameter_id) REFERENCES parameters (id)
            )
        ''')
        
        self.results_db.commit()
    
    def handle_menu_choice(self, choice):
        """Handle main menu choices"""
        menu_handlers = {
            "1": self.reconnaissance_menu,
            "2": self.extraction_menu,
            "3": self.classification_menu,
            "4": self.testing_menu,
            "5": self.business_logic_menu,
            "6": self.advanced_menu,
            "7": self.validation_menu,
            "8": self.reporting_menu,
            "9": self.tools_menu,
            "10": self.learning_menu
        }
        
        handler = menu_handlers.get(choice)
        if handler:
            handler()
    
    def reconnaissance_menu(self):
        """Reconnaissance & Discovery menu"""
        menu_items = [
            "[1] Target Setup & Scope Definition",
            "[2] Subdomain Enumeration",
            "[3] URL Collection (All Sources)",
            "[4] JavaScript Analysis for Parameters",
            "[5] Wayback Machine & Archive Analysis",
            "[6] GitHub/GitLab Recon (API Keys, Endpoints)",
            "[7] Back to Main Menu"
        ]
        
        while True:
            print(f"\n{Fore.CYAN}🎯 RECONNAISSANCE & DISCOVERY{Style.RESET_ALL}")
            for item in menu_items:
                print(item)
            
            choice = input(f"\n{Fore.YELLOW}Select option: {Style.RESET_ALL}").strip()
            
            if choice == "1":
                self.target_setup()
            elif choice == "2":
                self.subdomain_enumeration()
            elif choice == "3":
                self.url_collection()
            elif choice == "4":
                self.javascript_analysis()
            elif choice == "5":
                self.wayback_analysis()
            elif choice == "6":
                self.github_recon()
            elif choice == "7":
                break
    
    def target_setup(self):
        """Target Setup & Scope Definition"""
        print(f"\n{Fore.GREEN}Target Setup & Scope Definition{Style.RESET_ALL}")
        
        target = input("Enter target domain: ").strip()
        scope = input("Enter scope (e.g., *.example.com): ").strip()
        
        # Save to project config
        config_path = self.project_path / "project.json"
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        config['target'] = target
        config['scope'] = scope
        
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"{Fore.GREEN}Target saved: {target}{Style.RESET_ALL}")
    
    def subdomain_enumeration(self):
        """Perform subdomain enumeration"""
        if not self.project_path:
            print(f"{Fore.RED}No project created!{Style.RESET_ALL}")
            return
        
        target = input("Enter target domain: ").strip()
        
        tools = {
            "subfinder": f"subfinder -d {target} -silent",
            "assetfinder": f"assetfinder --subs-only {target}",
            "amass": f"amass enum -passive -d {target}"
        }
        
        print(f"\n{Fore.GREEN}Starting subdomain enumeration...{Style.RESET_ALL}")
        
        subdomains = set()
        for tool, command in tools.items():
            try:
                print(f"Running {tool}...")
                result = subprocess.run(command.split(), capture_output=True, text=True)
                if result.stdout:
                    new_subs = set(result.stdout.strip().split('\n'))
                    subdomains.update(new_subs)
                    print(f"Found {len(new_subs)} subdomains with {tool}")
            except FileNotFoundError:
                print(f"{Fore.RED}{tool} not found!{Style.RESET_ALL}")
        
        # Save results
        output_file = self.project_path / "reconnaissance" / "subdomains.txt"
        with open(output_file, 'w') as f:
            for subdomain in sorted(subdomains):
                f.write(f"{subdomain}\n")
        
        print(f"{Fore.GREEN}Total subdomains found: {len(subdomains)}")
        print(f"Saved to: {output_file}{Style.RESET_ALL}")
    
    def url_collection(self):
        """Collect URLs from various sources"""
        print(f"\n{Fore.GREEN}URL Collection from All Sources{Style.RESET_ALL}")
        
        target = input("Enter target domain: ").strip()
        
        # Use various tools for URL collection
        urls = set()
        
        # GAU (GitHub All URLs)
        try:
            print("Running gau...")
            result = subprocess.run(["gau", target], capture_output=True, text=True)
            if result.stdout:
                urls.update(result.stdout.strip().split('\n'))
        except FileNotFoundError:
            print(f"{Fore.RED}gau not found!{Style.RESET_ALL}")
        
        # Wayback Machine
        try:
            print("Running waybackurls...")
            result = subprocess.run(["waybackurls", target], capture_output=True, text=True)
            if result.stdout:
                urls.update(result.stdout.strip().split('\n'))
        except FileNotFoundError:
            print(f"{Fore.RED}waybackurls not found!{Style.RESET_ALL}")
        
        # Save results
        output_file = self.project_path / "reconnaissance" / "urls.txt"
        with open(output_file, 'w') as f:
            for url in sorted(urls):
                f.write(f"{url}\n")
        
        print(f"{Fore.GREEN}Total URLs collected: {len(urls)}")
        print(f"Saved to: {output_file}{Style.RESET_ALL}")
    
    def extraction_menu(self):
        """Parameter Extraction Phase menu"""
        menu_items = [
            "[1] Basic Parameter Extraction (from URLs)",
            "[2] Hidden Parameter Discovery (Arjun/x8)",
            "[3] API Endpoint Discovery",
            "[4] GraphQL Endpoint & Schema Analysis",
            "[5] WebSocket Endpoint Discovery",
            "[6] Custom Parameter Wordlist Generation",
            "[7] Back to Main Menu"
        ]
        
        while True:
            print(f"\n{Fore.CYAN}🔍 PARAMETER EXTRACTION PHASE{Style.RESET_ALL}")
            for item in menu_items:
                print(item)
            
            choice = input(f"\n{Fore.YELLOW}Select option: {Style.RESET_ALL}").strip()
            
            if choice == "1":
                self.basic_parameter_extraction()
            elif choice == "2":
                self.hidden_parameter_discovery()
            elif choice == "3":
                self.api_endpoint_discovery()
            elif choice == "4":
                self.graphql_analysis()
            elif choice == "5":
                self.websocket_discovery()
            elif choice == "6":
                self.custom_wordlist_generation()
            elif choice == "7":
                break
    
    def basic_parameter_extraction(self):
        """Extract parameters from collected URLs"""
        print(f"\n{Fore.GREEN}Basic Parameter Extraction{Style.RESET_ALL}")
        
        urls_file = self.project_path / "reconnaissance" / "urls.txt"
        if not urls_file.exists():
            print(f"{Fore.RED}No URLs file found! Run URL collection first.{Style.RESET_ALL}")
            return
        
        with open(urls_file, 'r') as f:
            urls = f.read().splitlines()
        
        parameters = set()
        for url in urls:
            parsed = urlparse(url)
            if parsed.query:
                query_params = parsed.query.split('&')
                for param in query_params:
                    if '=' in param:
                        param_name = param.split('=')[0]
                        parameters.add(param_name)
        
        # Save parameters
        output_file = self.project_path / "parameters" / "extracted_params.txt"
        with open(output_file, 'w') as f:
            for param in sorted(parameters):
                f.write(f"{param}\n")
        
        # Store in database
        cursor = self.results_db.cursor()
        for param in parameters:
            cursor.execute(
                "INSERT OR IGNORE INTO parameters (url, parameter, discovered_at) VALUES (?, ?, ?)",
                ("multiple", param, datetime.now().isoformat())
            )
        self.results_db.commit()
        
        print(f"{Fore.GREEN}Extracted {len(parameters)} unique parameters")
        print(f"Saved to: {output_file}{Style.RESET_ALL}")
    
    def hidden_parameter_discovery(self):
        """Discover hidden parameters using Arjun"""
        print(f"\n{Fore.GREEN}Hidden Parameter Discovery{Style.RESET_ALL}")
        
        target = input("Enter target URL: ").strip()
        
        # Check if Arjun is available
        arjun_path = self.config['tools'].get('arjun')
        if not arjun_path or not os.path.exists(arjun_path):
            print(f"{Fore.RED}Arjun not found! Install it first.{Style.RESET_ALL}")
            return
        
        # Run Arjun
        output_file = self.project_path / "parameters" / "hidden_params.json"
        command = f"{arjun_path} -u {target} -oT {output_file} --disable-redirects"
        
        try:
            print(f"Running Arjun on {target}...")
            subprocess.run(command.split(), check=True)
            
            # Parse results
            if output_file.exists():
                with open(output_file, 'r') as f:
                    results = json.load(f)
                
                print(f"\n{Fore.GREEN}Hidden parameters found:{Style.RESET_ALL}")
                for param in results.get('params', []):
                    print(f"  - {param}")
        except subprocess.CalledProcessError as e:
            print(f"{Fore.RED}Error running Arjun: {e}{Style.RESET_ALL}")
    
    def classification_menu(self):
        """Parameter Classification menu"""
        menu_items = [
            "[1] Classify by Type",
            "[2] Risk Assessment (Critical/High/Medium/Low)",
            "[3] Parameter Dependency Mapping",
            "[4] Back to Main Menu"
        ]
        
        while True:
            print(f"\n{Fore.CYAN}📊 PARAMETER CLASSIFICATION{Style.RESET_ALL}")
            for item in menu_items:
                print(item)
            
            choice = input(f"\n{Fore.YELLOW}Select option: {Style.RESET_ALL}").strip()
            
            if choice == "1":
                self.classify_by_type()
            elif choice == "2":
                self.risk_assessment()
            elif choice == "3":
                self.parameter_dependency_mapping()
            elif choice == "4":
                break
    
    def classify_by_type(self):
        """Classify parameters by type"""
        print(f"\n{Fore.GREEN}Parameter Classification by Type{Style.RESET_ALL}")
        
        # Classification patterns
        classifications = {
            "Authentication": ["token", "session", "api_key", "auth", "password", "key"],
            "Business Logic": ["price", "quantity", "user_id", "order", "amount"],
            "File Operations": ["file", "path", "upload", "download", "dir"],
            "Debug/Admin": ["debug", "test", "admin", "console", "backup"],
            "Search/Filter": ["q", "search", "filter", "sort", "page"],
            "Miscellaneous": ["callback", "redirect", "lang", "version", "mode"]
        }
        
        params_file = self.project_path / "parameters" / "extracted_params.txt"
        if not params_file.exists():
            print(f"{Fore.RED}No parameters file found!{Style.RESET_ALL}")
            return
        
        with open(params_file, 'r') as f:
            parameters = f.read().splitlines()
        
        classified = {category: [] for category in classifications.keys()}
        classified["Unknown"] = []
        
        for param in parameters:
            param_lower = param.lower()
            categorized = False
            
            for category, patterns in classifications.items():
                for pattern in patterns:
                    if pattern in param_lower:
                        classified[category].append(param)
                        categorized = True
                        break
                if categorized:
                    break
            
            if not categorized:
                classified["Unknown"].append(param)
        
        # Display results
        for category, params in classified.items():
            if params:
                print(f"\n{Fore.YELLOW}{category} ({len(params)}):{Style.RESET_ALL}")
                for param in params[:10]:  # Show first 10
                    print(f"  - {param}")
                if len(params) > 10:
                    print(f"  ... and {len(params) - 10} more")
        
        # Save classification
        output_file = self.project_path / "parameters" / "classification.json"
        with open(output_file, 'w') as f:
            json.dump(classified, f, indent=2)
        
        print(f"\n{Fore.GREEN}Classification saved to: {output_file}{Style.RESET_ALL}")
    
    def testing_menu(self):
        """Automated Testing Suite menu"""
        menu_items = [
            "[1] SQL Injection Testing Suite",
            "[2] XSS & Client-Side Testing",
            "[3] Server-Side Attacks",
            "[4] API-Specific Testing",
            "[5] Back to Main Menu"
        ]
        
        while True:
            print(f"\n{Fore.CYAN}⚔️ AUTOMATED TESTING SUITE{Style.RESET_ALL}")
            for item in menu_items:
                print(item)
            
            choice = input(f"\n{Fore.YELLOW}Select option: {Style.RESET_ALL}").strip()
            
            if choice == "1":
                self.sql_injection_testing()
            elif choice == "2":
                self.xss_testing()
            elif choice == "3":
                self.server_side_testing()
            elif choice == "4":
                self.api_testing()
            elif choice == "5":
                break
    
    def sql_injection_testing(self):
        """Perform SQL injection testing"""
        print(f"\n{Fore.GREEN}SQL Injection Testing Suite{Style.RESET_ALL}")
        
        target_url = input("Enter target URL with parameter: ").strip()
        
        # Check for sqlmap
        sqlmap_path = self.config['tools'].get('sqlmap')
        if not sqlmap_path or not os.path.exists(sqlmap_path):
            print(f"{Fore.RED}sqlmap not found! Install it first.{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.YELLOW}Available SQL injection tests:{Style.RESET_ALL}")
        print("1. Standard SQLmap scan")
        print("2. Time-based blind SQLi")
        print("3. Error-based SQLi")
        print("4. Boolean-based SQLi")
        print("5. Union-based SQLi")
        
        test_choice = input("Select test type (1-5): ").strip()
        
        test_options = {
            "1": "",
            "2": "--technique=T",
            "3": "--technique=E",
            "4": "--technique=B",
            "5": "--technique=U"
        }
        
        if test_choice in test_options:
            output_dir = self.project_path / "testing" / "sql_injection"
            output_dir.mkdir(exist_ok=True)
            
            output_file = output_dir / f"sqlmap_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            command = [
                sqlmap_path,
                "-u", target_url,
                "--batch",
                "--level=3",
                "--risk=3",
                test_options[test_choice],
                f"--output-dir={output_dir}"
            ]
            
            if self.config.get('proxy'):
                command.extend(["--proxy", self.config['proxy']])
            
            print(f"\n{Fore.YELLOW}Running command:{Style.RESET_ALL}")
            print(" ".join(command))
            
            try:
                subprocess.run(command, check=True)
                print(f"\n{Fore.GREEN}SQLmap scan completed!")
                print(f"Check results in: {output_dir}{Style.RESET_ALL}")
            except subprocess.CalledProcessError as e:
                print(f"{Fore.RED}Error running sqlmap: {e}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Invalid choice!{Style.RESET_ALL}")
    
    def business_logic_menu(self):
        """Business Logic Testing menu"""
        menu_items = [
            "[1] IDOR Testing",
            "[2] Authentication & Authorization",
            "[3] Payment & Transaction Logic",
            "[4] File Upload & Processing",
            "[5] Back to Main Menu"
        ]
        
        while True:
            print(f"\n{Fore.CYAN}🧠 BUSINESS LOGIC TESTING{Style.RESET_ALL}")
            for item in menu_items:
                print(item)
            
            choice = input(f"\n{Fore.YELLOW}Select option: {Style.RESET_ALL}").strip()
            
            if choice == "1":
                self.idor_testing()
            elif choice == "2":
                self.auth_testing()
            elif choice == "3":
                self.payment_testing()
            elif choice == "4":
                self.file_upload_testing()
            elif choice == "5":
                break
    
    def idor_testing(self):
        """IDOR (Insecure Direct Object Reference) testing"""
        print(f"\n{Fore.GREEN}IDOR Testing Suite{Style.RESET_ALL}")
        
        base_url = input("Enter base URL (e.g., https://api.example.com/users/): ").strip()
        param_name = input("Enter parameter name (e.g., id, user_id): ").strip()
        
        print(f"\n{Fore.YELLOW}IDOR Test Types:{Style.RESET_ALL}")
        print("1. Sequential ID testing")
        print("2. UUID predictability")
        print("3. Horizontal privilege escalation")
        print("4. Vertical privilege escalation")
        
        test_type = input("Select test type (1-4): ").strip()
        
        if test_type == "1":
            start_id = int(input("Start ID: ").strip())
            end_id = int(input("End ID: ").strip())
            
            print(f"\n{Fore.YELLOW}Testing sequential IDs from {start_id} to {end_id}{Style.RESET_ALL}")
            
            results = []
            for i in range(start_id, end_id + 1):
                test_url = f"{base_url}?{param_name}={i}"
                response = self.make_request(test_url)
                
                if response:
                    status = response.status_code
                    if status == 200:
                        results.append((test_url, "SUCCESS - Access granted"))
                    elif status == 403:
                        results.append((test_url, "FORBIDDEN"))
                    elif status == 404:
                        results.append((test_url, "NOT FOUND"))
                    else:
                        results.append((test_url, f"Status: {status}"))
            
            # Display results
            print(f"\n{Fore.GREEN}IDOR Test Results:{Style.RESET_ALL}")
            for url, result in results:
                if "SUCCESS" in result:
                    print(f"{Fore.RED}{url}: {result}{Style.RESET_ALL}")
                else:
                    print(f"{url}: {result}")
    
    def make_request(self, url, method="GET", headers=None):
        """Make HTTP request with error handling"""
        try:
            if headers is None:
                headers = {
                    'User-Agent': 'ParameterBugHunter/2.0'
                }
            
            if method.upper() == "GET":
                response = requests.get(url, headers=headers, timeout=10)
            elif method.upper() == "POST":
                response = requests.post(url, headers=headers, timeout=10)
            else:
                response = requests.request(method, url, headers=headers, timeout=10)
            
            return response
        except requests.RequestException as e:
            print(f"{Fore.RED}Request failed: {e}{Style.RESET_ALL}")
            return None
    
    def reporting_menu(self):
        """Reporting & Documentation menu"""
        menu_items = [
            "[1] Vulnerability Template Filling",
            "[2] Evidence Collection",
            "[3] Report Generation",
            "[4] Back to Main Menu"
        ]
        
        while True:
            print(f"\n{Fore.CYAN}📋 REPORTING & DOCUMENTATION{Style.RESET_ALL}")
            for item in menu_items:
                print(item)
            
            choice = input(f"\n{Fore.YELLOW}Select option: {Style.RESET_ALL}").strip()
            
            if choice == "1":
                self.vulnerability_template()
            elif choice == "2":
                self.evidence_collection()
            elif choice == "3":
                self.report_generation()
            elif choice == "4":
                break
    
    def vulnerability_template(self):
        """Fill vulnerability template"""
        print(f"\n{Fore.GREEN}Vulnerability Report Template{Style.RESET_ALL}")
        
        template = {
            "title": input("Vulnerability Title: ").strip(),
            "description": input("Description: ").strip(),
            "steps_to_reproduce": [],
            "impact": input("Impact: ").strip(),
            "risk_rating": "",
            "remediation": input("Remediation Suggestions: ").strip(),
            "cvss_score": input("CVSS Score (e.g., 7.5): ").strip(),
            "references": []
        }
        
        # Steps to reproduce
        print("\nEnter steps to reproduce (enter 'done' when finished):")
        step_num = 1
        while True:
            step = input(f"Step {step_num}: ").strip()
            if step.lower() == 'done':
                break
            template["steps_to_reproduce"].append(step)
            step_num += 1
        
        # Risk rating
        print("\nRisk Rating Options:")
        print("1. Critical")
        print("2. High")
        print("3. Medium")
        print("4. Low")
        print("5. Informational")
        
        risk_choice = input("Select risk rating (1-5): ").strip()
        risk_map = {
            "1": "Critical",
            "2": "High",
            "3": "Medium",
            "4": "Low",
            "5": "Informational"
        }
        template["risk_rating"] = risk_map.get(risk_choice, "Medium")
        
        # References
        print("\nEnter references (enter 'done' when finished):")
        ref_num = 1
        while True:
            ref = input(f"Reference {ref_num}: ").strip()
            if ref.lower() == 'done':
                break
            template["references"].append(ref)
            ref_num += 1
        
        # Save template
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = self.project_path / "reports" / f"vuln_{timestamp}.json"
        
        with open(output_file, 'w') as f:
            json.dump(template, f, indent=2)
        
        print(f"\n{Fore.GREEN}Vulnerability template saved to: {output_file}{Style.RESET_ALL}")
    
    def report_generation(self):
        """Generate comprehensive report"""
        print(f"\n{Fore.GREEN}Report Generation{Style.RESET_ALL}")
        
        print("Report Formats:")
        print("1. HackerOne Template")
        print("2. Markdown Format")
        print("3. PDF Export")
        print("4. Executive Summary")
        
        format_choice = input("Select format (1-4): ").strip()
        
        if format_choice == "1":
            self.generate_hackerone_report()
        elif format_choice == "2":
            self.generate_markdown_report()
        elif format_choice == "3":
            self.generate_pdf_report()
        elif format_choice == "4":
            self.generate_executive_summary()
        else:
            print(f"{Fore.RED}Invalid choice!{Style.RESET_ALL}")
    
    def generate_markdown_report(self):
        """Generate markdown report"""
        report_content = f"""# Security Assessment Report

## Project Information
- **Target**: {self.project_path.name}
- **Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Scope**: {self.get_project_scope()}

## Executive Summary
Brief summary of findings...

## Methodology
1. Reconnaissance & Discovery
2. Parameter Extraction
3. Automated Testing
4. Business Logic Testing
5. Validation & Verification

## Findings

### Critical Findings
- No critical findings identified

### High Risk Findings
- No high risk findings identified

### Medium Risk Findings
- No medium risk findings identified

### Low Risk Findings
- No low risk findings identified

## Recommendations
1. Implement proper input validation
2. Use parameterized queries
3. Implement rate limiting
4. Regular security assessments

## Appendix
- Tools used: {', '.join(self.config['tools'].keys())}
- Wordlists: {', '.join(self.config['wordlists'].keys())}
"""
        
        output_file = self.project_path / "reports" / "full_report.md"
        with open(output_file, 'w') as f:
            f.write(report_content)
        
        print(f"{Fore.GREEN}Markdown report generated: {output_file}{Style.RESET_ALL}")
    
    def get_project_scope(self):
        """Get project scope from config"""
        config_path = self.project_path / "project.json"
        if config_path.exists():
            with open(config_path, 'r') as f:
                config = json.load(f)
            return config.get('scope', 'Not defined')
        return 'Not defined'
    
    def tools_menu(self):
        """Tool Management menu"""
        menu_items = [
            "[1] API Keys Setup",
            "[2] Proxy Configuration",
            "[3] Wordlist Management",
            "[4] Custom Template Creation",
            "[5] Save Current Workflow",
            "[6] Load Previous Workflow",
            "[7] Back to Main Menu"
        ]
        
        while True:
            print(f"\n{Fore.CYAN}⚙️ TOOL MANAGEMENT{Style.RESET_ALL}")
            for item in menu_items:
                print(item)
            
            choice = input(f"\n{Fore.YELLOW}Select option: {Style.RESET_ALL}").strip()
            
            if choice == "1":
                self.api_keys_setup()
            elif choice == "2":
                self.proxy_configuration()
            elif choice == "3":
                self.wordlist_management()
            elif choice == "4":
                self.custom_template_creation()
            elif choice == "5":
                self.save_workflow()
            elif choice == "6":
                self.load_workflow()
            elif choice == "7":
                break
    
    def api_keys_setup(self):
        """Setup API keys for various services"""
        print(f"\n{Fore.GREEN}API Keys Setup{Style.RESET_ALL}")
        
        services = [
            "GitHub",
            "GitLab",
            "Shodan",
            "Censys",
            "VirusTotal",
            "BinaryEdge",
            "Hunter.io",
            "SecurityTrails"
        ]
        
        for service in services:
            key = input(f"{service} API Key (press Enter to skip): ").strip()
            if key:
                self.config['api_keys'][service.lower()] = key
        
        self.save_config()
        print(f"{Fore.GREEN}API keys saved!{Style.RESET_ALL}")
    
    def wordlist_management(self):
        """Manage wordlists"""
        print(f"\n{Fore.GREEN}Wordlist Management{Style.RESET_ALL}")
        
        print("Current wordlists:")
        for name, path in self.config['wordlists'].items():
            print(f"  {name}: {path}")
        
        print("\nOptions:")
        print("1. Add new wordlist")
        print("2. Update existing wordlist")
        print("3. Remove wordlist")
        
        choice = input("Select option: ").strip()
        
        if choice == "1":
            name = input("Wordlist name: ").strip()
            path = input("Full path to wordlist: ").strip()
            if os.path.exists(path):
                self.config['wordlists'][name] = path
                self.save_config()
                print(f"{Fore.GREEN}Wordlist added!{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}File not found!{Style.RESET_ALL}")
    
    # Other methods would be implemented similarly...
    
    def learning_menu(self):
        """Learning & Improvement menu"""
        menu_items = [
            "[1] Case Studies Analysis",
            "[2] Update Attack Patterns",
            "[3] Custom Payload Development",
            "[4] Tool Integration Scripting",
            "[5] Performance Optimization",
            "[6] Back to Main Menu"
        ]
        
        while True:
            print(f"\n{Fore.CYAN}📚 LEARNING & IMPROVEMENT{Style.RESET_ALL}")
            for item in menu_items:
                print(item)
            
            choice = input(f"\n{Fore.YELLOW}Select option: {Style.RESET_ALL}").strip()
            
            if choice == "1":
                self.case_studies()
            elif choice == "2":
                self.update_attack_patterns()
            elif choice == "3":
                self.custom_payloads()
            elif choice == "4":
                self.tool_integration()
            elif choice == "5":
                self.performance_optimization()
            elif choice == "6":
                break
    
    def case_studies(self):
        """Analyze security case studies"""
        print(f"\n{Fore.GREEN}Security Case Studies{Style.RESET_ALL}")
        
        case_studies = [
            "GitLab SQL Injection - CVE-2023-XXXX",
            "Shopify IDOR - $XX,000 bounty",
            "Uber Subdomain Takeover",
            "Facebook OAuth Misconfiguration",
            "Twitter API Key Leak"
        ]
        
        print("Available case studies:")
        for i, case in enumerate(case_studies, 1):
            print(f"{i}. {case}")
        
        choice = input("Select case study (1-5): ").strip()
        
        if choice in ["1", "2", "3", "4", "5"]:
            case_index = int(choice) - 1
            print(f"\n{Fore.YELLOW}Analyzing: {case_studies[case_index]}{Style.RESET_ALL}")
            
            # This would typically load from a database or file
            analysis = {
                "vulnerability": "SQL Injection",
                "impact": "Data leakage, privilege escalation",
                "root_cause": "Improper input validation",
                "remediation": "Parameterized queries, input validation",
                "tools_used": ["sqlmap", "Burp Suite"],
                "methodology": "Recon -> Parameter discovery -> Testing -> Validation"
            }
            
            print("\nAnalysis:")
            for key, value in analysis.items():
                print(f"{key.title()}: {value}")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Parameter Bug Hunter Pro')
    parser.add_argument('--project', '-p', help='Project directory')
    parser.add_argument('--target', '-t', help='Target domain')
    parser.add_argument('--quick', '-q', action='store_true', help='Quick scan')
    
    args = parser.parse_args()
    
    hunter = ParameterBugHunter()
    
    if args.project:
        hunter.project_path = Path(args.project)
        if hunter.project_path.exists():
            hunter.initialize_database()
        else:
            print(f"{Fore.RED}Project not found!{Style.RESET_ALL}")
            sys.exit(1)
    
    if args.target and args.quick:
        # Quick scan mode
        print(f"{Fore.GREEN}Starting quick scan on {args.target}{Style.RESET_ALL}")
        # Implement quick scan logic
    else:
        # Interactive mode
        hunter.display_menu()

if __name__ == "__main__":
    main()
