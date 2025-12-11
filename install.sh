#!/bin/bash

# Parameter Bug Hunter Pro - Installer
echo "[+] Installing Parameter Bug Hunter Pro..."

# Update system
sudo apt-get update

# Install Python dependencies
pip3 install -r requirements.txt

# Install system tools
sudo apt-get install -y \
    python3-pip \
    sqlmap \
    ffuf \
    golang \
    npm \
    default-jre \
    wget \
    git \
    curl

# Create project directory
mkdir -p ~/.parameter_hunter/projects
mkdir -p ~/.parameter_hunter/wordlists
mkdir -p ~/.parameter_hunter/templates

# Install Go tools
echo "[+] Installing Go tools..."
go_tools=(
    "github.com/tomnomnom/assetfinder"
    "github.com/tomnomnom/waybackurls"
    "github.com/lc/gau/v2/cmd/gau"
    "github.com/projectdiscovery/subfinder/v2/cmd/subfinder"
    "github.com/projectdiscovery/nuclei/v2/cmd/nuclei"
    "github.com/s0md3v/Arjun"
)

for tool in "${go_tools[@]}"; do
    echo "Installing: $tool"
    go install $tool@latest
done

# Add Go binaries to PATH
export PATH=$PATH:$(go env GOPATH)/bin
echo 'export PATH=$PATH:$(go env GOPATH)/bin' >> ~/.bashrc

# Download wordlists
echo "[+] Downloading wordlists..."
cd ~/.parameter_hunter/wordlists

# Common wordlists
wget -q https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/burp-parameter-names.txt -O parameter-names.txt
wget -q https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/DNS/subdomains-top1million-110000.txt -O subdomains.txt
wget -q https://raw.githubusercontent.com/danielmiessler/SecLists/master/Fuzzing/GraphQL.txt -O graphql.txt
wget -q https://raw.githubusercontent.com/danielmiessler/SecLists/master/Fuzzing/API/Common-API-parameters.txt -O api-params.txt

# Create config file
cat > ~/.parameter_hunter/config.yaml << EOF
tools:
  arjun: $(which arjun)
  sqlmap: $(which sqlmap)
  ffuf: $(which ffuf)
  gau: $(which gau)
  waybackurls: $(which waybackurls)
  nuclei: $(which nuclei)
  subfinder: $(which subfinder)
  assetfinder: $(which assetfinder)
  amass: $(which amass)

wordlists:
  parameters: ~/.parameter_hunter/wordlists/parameter-names.txt
  subdomains: ~/.parameter_hunter/wordlists/subdomains.txt
  graphql: ~/.parameter_hunter/wordlists/graphql.txt
  api: ~/.parameter_hunter/wordlists/api-params.txt

api_keys:
  github: ""
  shodan: ""
  virustotal: ""
  censys_id: ""
  censys_secret: ""

proxy: null

database:
  path: ~/.parameter_hunter/database.db
EOF

echo "[+] Creating database..."
python3 -c "
import sqlite3
conn = sqlite3.connect(os.path.expanduser('~/.parameter_hunter/database.db'))
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS global_findings (
    id INTEGER PRIMARY KEY,
    project_name TEXT,
    target TEXT,
    vulnerability TEXT,
    severity TEXT,
    discovered_at TIMESTAMP,
    status TEXT DEFAULT 'new'
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS attack_patterns (
    id INTEGER PRIMARY KEY,
    pattern_name TEXT,
    pattern_type TEXT,
    payload TEXT,
    description TEXT
)
''')

conn.commit()
conn.close()
"

# Set executable permissions
chmod +x parameter_bug_hunter.py

echo "[+] Installation complete!"
echo "[+] To start: python3 parameter_bug_hunter.py"
