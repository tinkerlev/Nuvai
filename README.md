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
- ⚠️ **Detects vulnerabilities:** Code injection, XSS, SSRF, insecure deserialization, hardcoded secrets, weak crypto, etc.
- 📁 **Flexible reports:** JSON, TXT, HTML, and PDF
- 🧠 **AI-Aware:** Scans AI-generated or low-code scripts for critical flaws
- 💬 **Guided remediation tips** for every issue
- 🌐 **User-friendly Web UI** built in React
- 🖥️ **Works via CLI, GUI, or API**

---

## 🗂️ Folder Structure
```bash
Nuvai/
├── assets/                  # Logos and static visuals
├── backend/                 # Flask API for file scanning
│   └── server.py            # Handles incoming requests
├── config/                  # Default parameters & logging config
├── frontend/
│   └── src/
│       ├── api/             # Axios client & scan handler
│       ├── components/      # FileUpload, UI blocks
│       ├── pages/           # Home, ScanResult
│       └── App.jsx          # Entry point
├── examples/                # Test files with real-world vulnerabilities
├── src/nuvai/               # Core scanning logic
│   ├── scanner.py           # Detects language & routes scan
│   ├── *_scanner.py         # Language-specific scanners
│   ├── utils.py             # Regex + entropy detection
│   ├── config.py            # Global rules, thresholds
│   ├── report_saver.py      # Save results to disk
│   ├── logger.py            # Secure audit-ready logging
│   └── scanner_controller.py # Central rule executor
├── run.py                   # CLI runner
├── install.sh               # One-click installer for backend
├── LICENSE
├── README.md
├── SECURITY.md
└── CONTRIBUTING.md
```

---

## 🛠️ Getting Started
### For Linux/Kali/Ubuntu (Recommended):
```bash
chmod +x install.sh
./install.sh
```

### For Windows:
1. Enable WSL or Git Bash
2. Run `install.sh` using bash or manually:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install flask flask-cors
```

### For macOS:
```bash
brew install python3
python3 -m venv .venv
source .venv/bin/activate
pip install flask flask-cors
```

---

## 🧪 How to Scan Code
### Run via CLI:
```bash
python3 run.py examples/vulnerable_app.py
```
Or scan a full folder:
```bash
python3 run.py /path/to/my-folder
```

### Run via Web UI:
```bash
source .venv/bin/activate
cd backend && python3 server.py
```
Then open the React frontend:
```bash
cd frontend
npm install && npm run dev
```

---

## 📄 Report Outputs
- **JSON** – for developers, APIs, pipelines
- **TXT** – for terminals and logs
- **HTML** – for browsers and documentation
- **PDF** – for clients, audits, compliance teams

---

## 🔒 Security Practices (ISO 27001 Alignment)
- 🔹 Encrypted communication support (future-ready)
- 🔹 Input validation + output encoding
- 🔹 Secure file handling + cleanup
- 🔹 No raw error exposure to end-users
- 🔹 Activity logging for audit traceability

---

## 🎯 Roadmap Highlights
- [x] Multi-language support
- [x] Smart report export
- [x] Modern UI
- [ ] OAuth2 Authentication (Coming Soon)
- [ ] Docker Deployment
- [ ] CI/CD Auto Scanning Plugin
- [ ] Plugin System for Rules

---

## 🧑‍💻 Contribute
Want to help us? Fork the repo and check [`CONTRIBUTING.md`](./CONTRIBUTING.md) for how to:
- Add scanners
- Suggest new rules
- Help improve UX or onboarding

---

## 👨‍🏫 Creator
**Eliran Loai Deeb**  
LinkedIn: [linkedin.com/in/loai-deeb](https://www.linkedin.com/in/loai-deeb)  
GitHub: [@tinkerlev](https://github.com/tinkerlev)

---

> Built with ❤️ for builders, hackers, educators and code reviewers.

Stay tuned. Stay secure. 🛡️