# Parameter Bug Hunter Pro 🕵️‍♂️

![Version](https://img.shields.io/badge/Version-2.0-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-green)
![License](https://img.shields.io/badge/License-MIT-orange)

**Parameter Bug Hunter Pro** adalah framework komprehensif untuk analisis parameter dan bug bounty yang sistematis. Tool ini dirancang untuk membantu penetration tester dan bug bounty hunter menemukan parameter tersembunyi, melakukan automated testing, dan mendokumentasikan hasil dengan rapi.

## ✨ Fitur Utama

### 🎯 **Reconnaissance & Discovery**
- Target Setup & Scope Definition
- Subdomain Enumeration
- URL Collection dari berbagai sumber
- JavaScript Analysis untuk parameter
- Wayback Machine & Archive Analysis
- GitHub/GitLab Recon

### 🔍 **Parameter Extraction**
- Basic Parameter Extraction
- Hidden Parameter Discovery (Arjun/x8)
- API Endpoint Discovery
- GraphQL Endpoint & Schema Analysis
- WebSocket Endpoint Discovery
- Custom Parameter Wordlist Generation

### 📊 **Parameter Classification**
- Classify by Type (Auth, Business Logic, dll)
- Risk Assessment (Critical/High/Medium/Low)
- Parameter Dependency Mapping

### ⚔️ **Automated Testing Suite**
- SQL Injection Testing Suite
- XSS & Client-Side Testing
- Server-Side Attacks
- API-Specific Testing

### 🧠 **Business Logic Testing**
- IDOR Testing
- Authentication & Authorization Testing
- Payment & Transaction Logic
- File Upload & Processing

### 🔬 **Advanced Techniques**
- SSRF Testing
- File Inclusion Testing
- Template Injection
- Deserialization Attacks
- Race Condition Testing

## 📦 Instalasi Lengkap

### **Metode 1: Instalasi Otomatis (Recommended)**

```bash
# Clone repository
git clone https://github.com/yourusername/parameter-bug-hunter-pro.git
cd parameter-bug-hunter-pro

# Berikan permission eksekusi
chmod +x install.sh run.sh

# Jalankan installer
./install.sh
```

### **Metode 2: Instalasi Manual**

#### **Langkah 1: Install Dependencies Sistem**
```bash
# Update sistem
sudo apt update && sudo apt upgrade -y

# Install Python
sudo apt install python3 python3-pip python3-venv -y

# Install tools yang diperlukan
sudo apt install -y \
    sqlmap \
    ffuf \
    golang \
    git \
    wget \
    curl \
    nmap \
    default-jre
```

#### **Langkah 2: Setup Python Environment**
```bash
# Buat virtual environment
python3 -m venv venv

# Aktifkan virtual environment
source venv/bin/activate  # Linux/Mac
# atau
venv\Scripts\activate     # Windows

# Install Python packages
pip install -r requirements.txt
```

#### **Langkah 3: Install Go Tools**
```bash
# Set Go PATH jika belum
export PATH=$PATH:$(go env GOPATH)/bin
echo 'export PATH=$PATH:$(go env GOPATH)/bin' >> ~/.bashrc
source ~/.bashrc

# Install tools Go
go install github.com/tomnomnom/assetfinder@latest
go install github.com/tomnomnom/waybackurls@latest
go install github.com/lc/gau/v2/cmd/gau@latest
go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest
go install github.com/s0md3v/Arjun@latest
```

#### **Langkah 4: Setup Wordlists**
```bash
# Buat direktori wordlists
mkdir -p ~/.parameter_hunter/wordlists
cd ~/.parameter_hunter/wordlists

# Download wordlists
wget https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/burp-parameter-names.txt
wget https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/DNS/subdomains-top1million-110000.txt
wget https://raw.githubusercontent.com/danielmiessler/SecLists/master/Fuzzing/GraphQL.txt
wget https://raw.githubusercontent.com/danielmiessler/SecLists/master/Fuzzing/API/Common-API-parameters.txt
```

#### **Langkah 5: Konfigurasi Awal**
```bash
# Buat konfigurasi default
mkdir -p ~/.parameter_hunter
cat > ~/.parameter_hunter/config.yaml << EOF
tools:
  arjun: $(which arjun || echo "/usr/bin/arjun")
  sqlmap: $(which sqlmap)
  ffuf: $(which ffuf)
  gau: $(which gau)
  waybackurls: $(which waybackurls)
  nuclei: $(which nuclei)
  subfinder: $(which subfinder)
  assetfinder: $(which assetfinder)

wordlists:
  parameters: ~/.parameter_hunter/wordlists/burp-parameter-names.txt
  subdomains: ~/.parameter_hunter/wordlists/subdomains-top1million-110000.txt

api_keys:
  github: ""
  shodan: ""
  virustotal: ""

proxy: null
EOF
```

### **Metode 3: Docker (Paling Mudah)**

```bash
# Build Docker image
docker build -t parameter-bug-hunter .

# Jalankan dengan Docker
docker run -it --rm \
  -v $(pwd)/projects:/app/projects \
  -v $(pwd)/reports:/app/reports \
  parameter-bug-hunter

# Atau dengan docker-compose
docker-compose up -d
```

### **Metode 4: Docker Compose (Full Stack)**

```bash
# Copy environment file
cp .env.example .env

# Edit .env file dengan API keys Anda
nano .env

# Jalankan semua services
docker-compose up -d

# Akses application
docker-compose exec parameter-hunter python parameter_bug_hunter.py
```

## 🚀 Cara Penggunaan

### **Mode Interaktif (Recommended)**
```bash
./run.sh --interactive
# atau
python3 parameter_bug_hunter.py
```

### **Quick Scan Mode**
```bash
./run.sh --target example.com --quick
# atau
python3 parameter_bug_hunter.py --target example.com --quick
```

### **Project-based Mode**
```bash
# Buat project baru
python3 parameter_bug_hunter.py

# Gunakan project yang ada
./run.sh --project my_project --target example.com
```

### **Full Scan Mode**
```bash
./run.sh --target example.com --full
```

## 📁 Struktur Proyek

```
parameter-bug-hunter-pro/
├── parameter_bug_hunter.py      # Main script
├── requirements.txt             # Python dependencies
├── config.yaml                  # Default configuration
├── install.sh                   # Installation script
├── run.sh                       # Runner script
├── docker-compose.yml           # Docker Compose config
├── Dockerfile                   # Docker configuration
├── error_handler.py             # Error handling module
├── utils.py                     # Utility functions
├── projects/                    # Project directory
│   ├── {project_name}_timestamp/
│   │   ├── reconnaissance/
│   │   ├── parameters/
│   │   ├── testing/
│   │   ├── business_logic/
│   │   ├── reports/
│   │   └── evidence/
├── ~/.parameter_hunter/         # User config directory
│   ├── config.yaml
│   ├── wordlists/
│   └── database.db
```

## ⚙️ Konfigurasi API Keys

### **Dapatkan API Keys Gratis:**

1. **GitHub Token:**
   - Go to https://github.com/settings/tokens
   - Generate new token with "repo" scope

2. **Shodan API:**
   - Register at https://account.shodan.io
   - Free tier: 100 queries/month

3. **VirusTotal:**
   - Register at https://www.virustotal.com/gui/join-us
   - Free: 500 requests/day

4. **Censys:**
   - Register at https://censys.io/register
   - Free tier available

### **Tambahkan ke Config:**
```bash
nano ~/.parameter_hunter/config.yaml
```

```yaml
api_keys:
  github: "ghp_your_token_here"
  shodan: "your_shodan_api_key"
  virustotal: "your_vt_api_key"
  censys_id: "your_censys_id"
  censys_secret: "your_censys_secret"
```

## 🔧 Troubleshooting

### **Issue 1: "Tool not found"**
```bash
# Perbaiki PATH untuk Go tools
export PATH=$PATH:~/go/bin

# Install ulang tools yang missing
go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
```

### **Issue 2: Python Import Error**
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Atau install manual
pip install colorama requests pyyaml
```

### **Issue 3: Permission Denied**
```bash
# Berikan permission eksekusi
chmod +x *.sh

# Jalankan sebagai user biasa (bukan root)
python3 parameter_bug_hunter.py
```

### **Issue 4: Database Error**
```bash
# Delete dan recreate database
rm ~/.parameter_hunter/database.db
python3 parameter_bug_hunter.py
```

## 📝 Contoh Penggunaan

### **Contoh 1: Full Reconnaissance**
```bash
# 1. Buat project
python3 parameter_bug_hunter.py

# 2. Pilih menu 1 (Reconnaissance)
# 3. Pilih 1 (Target Setup)
# 4. Masukkan target domain
# 5. Pilih 2 (Subdomain Enumeration)
# 6. Pilih 3 (URL Collection)
```

### **Contoh 2: Parameter Discovery**
```bash
# 1. Dari main menu, pilih 2 (Parameter Extraction)
# 2. Pilih 1 (Basic Parameter Extraction)
# 3. Pilih 2 (Hidden Parameter Discovery)
# 4. Masukkan target URL
```

### **Contoh 3: Automated Testing**
```bash
# 1. Dari main menu, pilih 4 (Automated Testing)
# 2. Pilih 1 (SQL Injection Testing)
# 3. Masukkan vulnerable URL
# 4. Pilih tipe test
```

## 🎯 Workflow Rekomendasi

1. **Phase 1: Reconnaissance**
   - Target setup
   - Subdomain enumeration
   - URL collection

2. **Phase 2: Parameter Discovery**
   - Extract parameters from URLs
   - Hidden parameter discovery
   - API endpoint discovery

3. **Phase 3: Classification**
   - Classify parameters by type
   - Risk assessment
   - Prioritize testing

4. **Phase 4: Testing**
   - Automated vulnerability scanning
   - Business logic testing
   - Manual verification

5. **Phase 5: Reporting**
   - Vulnerability template filling
   - Evidence collection
   - Report generation

## 📊 Output & Reports

Tool ini menghasilkan output dalam berbagai format:

1. **Text Files:** subdomains.txt, urls.txt, parameters.txt
2. **JSON Files:** classification.json, vulnerability_reports.json
3. **Database:** SQLite database dengan semua findings
4. **Markdown Reports:** Laporan lengkap dalam format markdown
5. **Evidence Files:** Screenshots, response dumps, PoC

## 🐳 Docker Commands

```bash
# Build image
docker build -t param-hunter .

# Run single container
docker run -it --rm param-hunter

# Run with volume mounts
docker run -it --rm \
  -v $(pwd)/data:/data \
  -v $(pwd)/reports:/reports \
  param-hunter

# Use docker-compose
docker-compose up -d
docker-compose logs -f
docker-compose down
```

## 🔄 Update Tool

```bash
# Update menggunakan script
./run.sh --update

# Update manual
git pull origin main
pip install --upgrade -r requirements.txt
go install github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest
```

## 🤝 Kontribusi

Kontribusi sangat diterima! Silakan:

1. Fork repository
2. Buat branch feature (`git checkout -b feature/AmazingFeature`)
3. Commit perubahan (`git commit -m 'Add AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

## 📄 Lisensi

Distributed under MIT License. See `LICENSE` for more information.

## ⚠️ Disclaimer

Tool ini hanya untuk tujuan testing keamanan yang sah. Penulis tidak bertanggung jawab atas penggunaan yang tidak sah atau ilegal. Selalu dapatkan izin sebelum melakukan testing terhadap sistem yang bukan milik Anda.

## 🆘 Dukungan

Jika menemukan masalah:

1. Cek [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Cek error_log.txt
3. Buat issue di GitHub
4. Atau kontak: security@example.com

---

**Happy Hunting!** 🚀

Jika tool ini membantu Anda, jangan lupa untuk memberikan ⭐ di GitHub!
