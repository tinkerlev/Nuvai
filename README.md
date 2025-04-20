# Nuvai

![Nuvai Banner](./assets/nuvai_banner.png)

A professional-grade CLI tool for analyzing and reporting security vulnerabilities across multiple programming languages — including Python, JavaScript, TypeScript, HTML, C++, PHP, and more.

Developed and maintained by [Loai Deeb](https://www.linkedin.com/in/loai-deeb/)

> **Nuvai is where AI meets precision.**  
> A refined, extensible scanner built to secure the future of modern code.

---

## ✨ Overview
AI-generated and no-code tools are accelerating development — but traditional hand-written code still powers the majority of production systems. **Nuvai** bridges both worlds by providing a modern, multi-language vulnerability scanner that works on *any source file*, regardless of how it was written.

Supported languages:
- ✅ Python (`.py`)
- ⏳ JavaScript (`.js`)
- ⏳ TypeScript (`.ts`, `.tsx`)
- ⏳ React JSX (`.jsx`)
- ⏳ HTML (`.html`)
- ⏳ C++ (`.cpp`, `.cc`)
- ⏳ PHP (`.php`)

> ⏳ = Placeholder scanner exists, core engine not yet implemented

## 🔧 Project Maintenance Tools
To automatically update the `__init__.py` file inside `src/nuvai/` whenever you add or remove modules, run:
```bash
python3 update_init.py
```
This script regenerates imports and `__all__` exports.

---

## 🔒 What It Detects (Python only for now)

| Category                     | Vulnerability                       | Description                                                             | OWASP Reference |
|-----------------------------|-------------------------------------|-------------------------------------------------------------------------|------------------|
| Code Injection              | Dynamic Code Execution              | Use of `eval`, `exec` for runtime code execution                        | A03:2021 - Injection |
| Code Injection              | SQL Injection                       | Unsafe string concatenation in SQL queries                              | A03:2021 - Injection |
| Code Injection              | Command Injection                   | Use of `os.system()` or similar with user input                         | A03:2021 - Injection |
| Code Injection              | Template Injection                  | Unescaped usage of `{{ user_input }}` in templates                      | A03:2021 - Injection |
| Client-Side                 | Cross-Site Scripting (XSS)          | Unfiltered user input rendered in output                                | A03:2021 - Injection |
| Sensitive Data Exposure     | Hardcoded Secrets                   | API keys, passwords, and tokens inside the code                         | A02:2021 - Cryptographic Failures |
| Configuration               | Debug Mode Enabled                  | Use of `DEBUG = True` in production                                     | A05:2021 - Security Misconfiguration |
| Configuration               | Open CORS Policy                    | Using `Access-Control-Allow-Origin: *`                                  | A05:2021 - Security Misconfiguration |
| Access Control              | Missing Authentication              | Public routes with no auth protection                                   | A01:2021 - Broken Access Control |
| Access Control              | IDOR (Insecure Direct Object Ref.)  | Direct access to resource IDs without permission checks                 | A01:2021 - Broken Access Control |
| Transport Layer             | Insecure HTTP                       | Use of `http://` instead of secure `https://`                           | A06:2021 - Vulnerable and Outdated Components |

---

## 🛠 Installation
### 1. Clone the repository:
```bash
git clone https://github.com/tinkerlev/Nuvai.git
cd Nuvai
```

### 2. Create a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies:
```bash
pip install -r requirements.txt
```

> **Note:** PDF export requires `fpdf`. If it's not installed, the tool will skip PDF output without crashing.

---

## 🚀 Usage
### Scan any source code file:
```bash
python3 run.py path/to/your_script.py
```

Supported extensions:
- `.py`, `.js`, `.ts`, `.tsx`, `.jsx`, `.html`, `.cpp`, `.cc`, `.php`

After scanning:
- A summary of findings will be shown in the terminal
- You'll be prompted to export the report: `json`, `txt`, `html`, or `pdf`
- Reports are saved under `~/security_reports/`

---

## 📁 Project Structure
```
.
├── run.py                  # Main CLI entrypoint
├── update_init.py          # Script to auto-update __init__.py exports
├── report_saver.py         # Handles export in multiple formats
├── src/
│   └── nuvai/
│       ├── __init__.py
│       ├── scanner.py         # Language dispatcher
│       ├── python_scanner.py
│       ├── javascript_scanner.py
│       ├── html_scanner.py
│       ├── cpp_scanner.py
│       ├── typescript_scanner.py
│       ├── jsx_scanner.py
│       └── php_scanner.py
├── examples/
│   └── vulnerable_app.py   # Sample vulnerable Python code
├── security_reports/       # Output folder (auto-created)
└── requirements.txt        # Dependencies
```

---

## 📦 Requirements
- Python 3.7+
- `fpdf` (for PDF report export)

---

## ✅ Features
- CLI-based, zero GUI overhead
- Multi-language detection and routing
- Friendly fallback: handles unsupported files gracefully
- Modular scanner engine per language
- Developer- and team-friendly reports

---

## 📢 Author
Developed with care by [Loai Deeb](https://www.linkedin.com/in/loai-deeb/) — for ethical hackers and modern builders.

If you like this project, give it a ⭐ on [GitHub](https://github.com/tinkerlev/Nuvai) and follow on [LinkedIn](https://www.linkedin.com/in/loai-deeb/)!

---

## 📄 License
This project is licensed under the MIT License. See the [LICENSE](https://github.com/tinkerlev/Nuvai/blob/main/LICENSE) file for details.

> Security is not optional — this tool makes it accessible.