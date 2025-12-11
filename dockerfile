FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    wget \
    curl \
    golang \
    sqlmap \
    ffuf \
    nmap \
    default-jre \
    && rm -rf /var/lib/apt/lists/*

# Install Go tools
RUN go install github.com/tomnomnom/assetfinder@latest \
    && go install github.com/tomnomnom/waybackurls@latest \
    && go install github.com/lc/gau/v2/cmd/gau@latest \
    && go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest \
    && go install github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest

# Copy Python requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY parameter_bug_hunter.py .
COPY config.yaml /root/.parameter_hunter/config.yaml

# Create directories
RUN mkdir -p /root/.parameter_hunter/wordlists \
    && mkdir -p /root/.parameter_hunter/projects

# Download wordlists
RUN wget -q https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/burp-parameter-names.txt \
    -O /root/.parameter_hunter/wordlists/parameter-names.txt

# Set environment variables
ENV PATH="/root/go/bin:${PATH}"

# Run the application
ENTRYPOINT ["python", "parameter_bug_hunter.py"]
