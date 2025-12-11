#!/bin/bash

# Parameter Bug Hunter Pro - Runner Script

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to display help
show_help() {
    echo -e "${BLUE}Parameter Bug Hunter Pro - Usage${NC}"
    echo ""
    echo "  ./run.sh [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -h, --help          Show this help message"
    echo "  -p, --project NAME  Use existing project"
    echo "  -t, --target URL    Set target URL"
    echo "  -q, --quick         Quick scan mode"
    echo "  -f, --full          Full scan mode"
    echo "  -i, --interactive   Interactive mode (default)"
    echo "  --install           Install dependencies"
    echo "  --update            Update tools and wordlists"
    echo ""
}

# Function to check Python version
check_python() {
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}Python3 is not installed${NC}"
        exit 1
    fi
    
    python_version=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
    if [[ $(echo "$python_version < 3.8" | bc) -eq 1 ]]; then
        echo -e "${RED}Python 3.8 or higher is required${NC}"
        exit 1
    fi
}

# Function to install dependencies
install_deps() {
    echo -e "${YELLOW}Installing dependencies...${NC}"
    
    # Check if pip is installed
    if ! command -v pip3 &> /dev/null; then
        echo -e "${RED}pip3 is not installed${NC}"
        exit 1
    fi
    
    # Install Python packages
    pip3 install -r requirements.txt
    
    # Create directories
    mkdir -p ~/.parameter_hunter/{projects,wordlists,templates}
    
    echo -e "${GREEN}Dependencies installed successfully!${NC}"
}

# Function to update tools
update_tools() {
    echo -e "${YELLOW}Updating tools...${NC}"
    
    # Update wordlists
    cd ~/.parameter_hunter/wordlists
    wget -q -O parameter-names.txt https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/burp-parameter-names.txt
    wget -q -O subdomains.txt https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/DNS/subdomains-top1million-110000.txt
    
    echo -e "${GREEN}Tools updated successfully!${NC}"
}

# Main execution
main() {
    # Check Python first
    check_python
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            --install)
                install_deps
                exit 0
                ;;
            --update)
                update_tools
                exit 0
                ;;
            -p|--project)
                PROJECT="$2"
                shift 2
                ;;
            -t|--target)
                TARGET="$2"
                shift 2
                ;;
            -q|--quick)
                MODE="quick"
                shift
                ;;
            -f|--full)
                MODE="full"
                shift
                ;;
            -i|--interactive)
                MODE="interactive"
                shift
                ;;
            *)
                echo -e "${RED}Unknown option: $1${NC}"
                show_help
                exit 1
                ;;
        esac
    done
    
    # Default to interactive mode
    MODE=${MODE:-interactive}
    
    # Build command
    CMD="python3 parameter_bug_hunter.py"
    
    if [[ ! -z "$PROJECT" ]]; then
        CMD="$CMD --project $PROJECT"
    fi
    
    if [[ ! -z "$TARGET" ]]; then
        CMD="$CMD --target $TARGET"
    fi
    
    if [[ "$MODE" == "quick" ]]; then
        CMD="$CMD --quick"
    fi
    
    echo -e "${GREEN}Starting Parameter Bug Hunter Pro...${NC}"
    echo -e "${BLUE}Mode: $MODE${NC}"
    
    # Execute
    eval $CMD
}

# Run main function
main "$@"
