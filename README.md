# 💀 Recon Pro (1.0.v)
### Advanced Asynchronous OSINT & Infrastructure Mapping Framework

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?style=for-the-badge&logo=python)
![AsyncIO](https://img.shields.io/badge/Core-AsyncIO-red?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-purple?style=for-the-badge)
![Category](https://img.shields.io/badge/Category-Red%20Team%20/%20Pentest-black?style=for-the-badge)

**Recon Pro** is a high-performance reconnaissance engine designed for Red Team operators and Bug Bounty hunters. Built with a focus on speed, modularity, and tactical output, it leverages a 100% asynchronous architecture to map an organization's attack surface in seconds.

---
<br>

## 🚩 Overview

Traditional reconnaissance tools often suffer from sequential bottlenecks. **Recon Pro** solves this by utilizing `asyncio` and non-blocking I/O, allowing multiple intelligence-gathering modules to run concurrently. It doesn't just collect data; it transforms raw OSINT into actionable intelligence.


## ⚡ Core Features

### 🚀 Extreme Performance
- **Fully Asynchronous Core:** Powered by `asyncio` and `aiohttp` for massive concurrency without the overhead of threads.
- **Persistent Sessions:** Optimized TCP connection pooling for ultra-fast HTTP requests.

### 🛡️ Intelligence Modules
- **Passive Subdomain Enumeration:** Scrapes Certificate Transparency (CT) logs via **CRT.sh** and queries **HackerTarget**'s global database.
- **Robust DNS Mapping:** Hybrid resolution engine using **DNSPython** with hardcoded public DNS fallbacks (Google/Cloudflare) to bypass local DNS limitations or poisoning.
- **Active TCP Port Scanning:** Fast, asynchronous TCP handshake scanner targeting top operational ports to identify live services and potential entry points.

### 📊 Tactical Reporting
- **Rich CLI Interface:** Real-time feedback with progress bars, status updates, and color-coded logging.
- **Interactive HTML Dashboard:** Generates a professional Dark-Mode report featuring:
    - **Executive Summary:** Quick-view statistics of found assets.
    - **Searchable Tables:** Powered by **DataTables.js** for instant filtering of thousands of records.
    - **Risk Highlighting:** Automatic flagging of critical services (SSH, RDP, SMB).

<br>

## 🛠️ Installation

### Prerequisites
- Python 3.11 or higher
- Internet access for API modules and DNS resolution

### Setup

```bash
# Clone the repository
git clone [https://github.com/YOUR_USERNAME/Recon1.0.v.git](https://github.com/YOUR_USERNAME/Recon1.0.v.git)
cd Recon1.0.v

# Set up a virtual environment (Recommended)
python -m venv .venv

# Activate the environment
# Windows:
.\.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

<br>

## 🚀 Usage

Execute a full scan by pointing to a target domain:

```Bash
python cli.py -t example.com
```

<br>

## Tactical Command Options

| Flag | Description |
| :--- | :--- |
| -t, --target | Required. The target domain (e.g., tesla.com).
| -h, --help | Show the help message and exit.

<br>

## 🛡️ Operational Security (OPSEC)

    Custom User-Agents: Mimics modern browsers to avoid basic header-based detection.

    Graceful Failure: Individual module crashes do not affect the overall scan integrity.

    Passive-First Logic: Prioritizes OSINT sources before performing active probing.

## ⚠️ Legal Disclaimer
Recon1.0.v is for educational purposes only and for authorized security testing (Pentesting/Red Teaming/Blue Teaming/Bug Bounty). Unauthorized scanning of targets is illegal and unethical. The developer assumes no liability for misuse or damage caused by this program. Always obtain written consent before testing any infrastructure.

<br>
<br>
<div align="center"> Made for the InfoSec community by <b> Gabriel Lira </b> 💀 </div>

