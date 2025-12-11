"""
Error Handler untuk Parameter Bug Hunter Pro
"""

import sys
import traceback
from datetime import datetime
from colorama import Fore, Style

class ErrorHandler:
    @staticmethod
    def handle_error(error, context=""):
        """Handle and log errors gracefully"""
        error_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        error_msg = f"""
{Fore.RED}╔═══════════════════════════════════════════════════════════╗
║                     ERROR DETECTED                          ║
╚═══════════════════════════════════════════════════════════╝{Style.RESET_ALL}

{Fore.YELLOW}Timestamp: {error_time}{Style.RESET_ALL}
{Fore.YELLOW}Context: {context}{Style.RESET_ALL}
{Fore.RED}Error Type: {type(error).__name__}{Style.RESET_ALL}
{Fore.RED}Error Message: {str(error)}{Style.RESET_ALL}

{Fore.CYAN}Traceback:{Style.RESET_ALL}
{traceback.format_exc()}

{Fore.GREEN}Suggested Actions:{Style.RESET_ALL}
1. Check if all required tools are installed
2. Verify internet connection
3. Check API keys configuration
4. Ensure sufficient permissions
"""
        print(error_msg)
        
        # Log to file
        with open("error_log.txt", "a") as f:
            f.write(f"\n{'='*60}\n")
            f.write(f"Time: {error_time}\n")
            f.write(f"Context: {context}\n")
            f.write(f"Error: {type(error).__name__} - {str(error)}\n")
            f.write(f"Traceback:\n{traceback.format_exc()}\n")
        
        return False
    
    @staticmethod
    def check_tools(tools_required):
        """Check if required tools are installed"""
        import shutil
        
        missing_tools = []
        for tool in tools_required:
            if not shutil.which(tool):
                missing_tools.append(tool)
        
        if missing_tools:
            print(f"{Fore.RED}Missing tools: {', '.join(missing_tools)}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Please install them using: ./install.sh{Style.RESET_ALL}")
            return False
        return True
    
    @staticmethod
    def validate_url(url):
        """Validate URL format"""
        from urllib.parse import urlparse
        
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False
