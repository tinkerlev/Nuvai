# README.md

## 🔐 Welcome to Nuvai – AI-Powered Secure Code Scanner

**Where AI meets precision, with the rigor of real-world penetration testing.**

Nuvai is an advanced static code analysis engine designed for both technical and non-technical users. It scans source code in multiple programming languages to detect vulnerabilities — especially in AI-generated, No-Code, and Low-Code environments.

---

## 🧠 What is Nuvai?
Nuvai automatically detects security flaws in your code using intelligent pattern recognition, code heuristics, and content-based detection.

It’s built with:
- 🔍 Deep code inspection logic
- 🔒 ISO/IEC 27001-aligned architecture
- 🧠 AI awareness and resilience against generated code patterns
- 📄 Professional-grade reporting

---

## 🚀 Features
- ✅ **Multi-language scanning:** Python, JavaScript, HTML, JSX, TypeScript, PHP, C++
- ⚠️ **Detects vulnerabilities:** Code injection, XSS, SSRF, insecure deserialization, hardcoded secrets, weak crypto, and more
- 📁 **Flexible reports:** JSON, TXT, HTML, and PDF
- 🧠 **AI-Aware:** Scans AI-generated or low-code scripts for critical flaws
- 💬 **Guided remediation tips** for every issue
- 🌐 **User-friendly Web UI** built in React
- 🖥️ **Works via CLI, GUI, or API**

---

## 🗂️ Folder Structure
```bash
Nuvai/
├── assets/                  # Static images and branding assets (e.g., logos)
├── backend/                 # Backend logic (Flask API and support scripts)
│   ├── server.py            # API entry point for code scanning
│   ├── utils.py             # Low-level helpers (e.g. pattern extractors)
│   └── update_init.py       # Dynamically creates missing __init__.py files
├── config/                  # Central configuration for rules and thresholds
├── examples/                # Example vulnerable code samples for testing
├── frontend/
│   └── src/
│       ├── api/             # API clients for backend communication
│       │   ├── client.js    # Axios instance with interceptors and error handling
│       │   └── scan.js      # Specific scan API call function
│       ├── components/      # Reusable UI components (e.g., file upload, buttons)
│       │   └── FileUpload.jsx
│       ├── pages/           # Page-level React components
│       │   ├── Home.jsx     # Main interface with file upload and scan results
│       │   └── ScanResult.jsx # Results rendering and formatting
│       └── App.jsx          # Root component with routing
├── src/
│   └── nuvai/
│       ├── scanner.py           # Main dispatcher for language detection and routing
│       ├── scanner_controller.py # Central orchestrator for initiating scans
│       ├── cpp_scanner.py       # C++ vulnerability scanner
│       ├── html_scanner.py      # HTML vulnerability scanner
│       ├── javascript_scanner.py # JavaScript scanner
│       ├── jsx_scanner.py       # JSX-specific rules
│       ├── php_scanner.py       # PHP scanner
│       ├── python_scanner.py    # Python vulnerability checks
│       ├── typescript_scanner.py # TypeScript scanner
│       ├── utils.py             # Security helpers (regex, entropy detection, etc.)
│       ├── report_saver.py      # Exports results to different file types
│       ├── config.py            # Default scanning options, thresholds, severity levels
│       └── logger.py            # Secure logger, audit trail support
├── run.py                   # CLI entry point for scanning a file or directory
├── install.sh               # Shell script to install dependencies (cross-platform aware)
├── .gitignore               # Files and folders to exclude from Git
├── LICENSE
├── README.md
├── SECURITY.md              # Description of implemented security practices
└── CONTRIBUTING.md          # Guidelines for contributors
```

---

## 🛠️ Getting Started
### Linux / WSL / Kali (recommended):
```bash
chmod +x install.sh
./install.sh
```

### Windows:
1. Install WSL or use Git Bash
2. Run:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install flask flask-cors
```

### macOS:
```bash
brew install python3
python3 -m venv .venv
source .venv/bin/activate
pip install flask flask-cors
```

### Web UI Setup
```bash
cd frontend
npm install && npm run dev
```

---

## 🧪 How to Run a Scan
### CLI Mode:
```bash
python3 run.py examples/vulnerable_app.py
```
Scan a full folder:
```bash
python3 run.py /path/to/codebase
```

### Web Mode:
```bash
source .venv/bin/activate
cd backend && python3 server.py
```
Then visit: [http://localhost:5173](http://localhost:5173)

---

## 📄 Report Formats
- `.json` — for APIs and automation
- `.html` — for browsers and documentation
- `.pdf` — for audits and clients
- `.txt` — for logs and fast review

Reports saved to: `~/security_reports/`

---

## 🔒 Built with Security in Mind (ISO/IEC 27001)
- ✔ Input validation + output encoding
- ✔ Temporary files are deleted after scan
- ✔ No user secrets or logs exposed
- ✔ Modular logging for audit readiness
- ✔ Supports offline and privacy-respecting usage
- ✔ Read `SECURITY.md` for our complete security model

---

## 📍 Roadmap
- [x] Static engine with 7+ language scanners
- [x] Advanced PDF/HTML/JSON export
- [x] React frontend
- [ ] OAuth2 Login support (frontend/backend)
- [ ] Docker build + CI pipeline
- [ ] Plugin SDK for adding new rules
- [ ] Support SARIF/OWASP ZAP exports

---

## 🤝 Contribute
See [`CONTRIBUTING.md`](./CONTRIBUTING.md) for full instructions.
You can:
- Write rules and scanners
- Improve documentation or UI
- Report bugs and ideas

> 🧠 Want to learn how to contribute? Just run:
```bash
open CONTRIBUTING.md
```

---

## 👨‍💻 Created by
**Eliran Loai Deeb**  
GitHub: [@tinkerlev](https://github.com/tinkerlev)  
LinkedIn: [linkedin.com/in/loai-deeb](https://www.linkedin.com/in/loai-deeb)

---

> Built with ❤️ for builders, red teamers, and ethical coders.

Stay secure. Stay smart. 🛡️