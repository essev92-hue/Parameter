# Troubleshooting Guide

## Common Issues and Solutions

### 1. "Tool not found" errors
```bash
# Install missing tools
sudo apt-get install sqlmap ffuf

# For Go tools
go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
