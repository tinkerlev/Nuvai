"""
File: scanner.py

Description:
This module is part of the Nuvai suite.
It performs static code analysis to identify a wide range of common
security risks in AI-generated or No-Code applications. Checks are categorized
and use pattern matching to detect dangerous constructs. Designed to provide
clear output for both technical and non-technical users.

Categories covered:
- Code injection (eval, exec, SQLi, command injection, template injection)
- Secrets (API keys, tokens, hardcoded passwords)
- Configuration (debug mode, open CORS)
- Access control (auth bypass, IDOR)
- Transport (insecure HTTP)
"""

import re

class CodeScanner:
    def __init__(self, code):
        self.code = code
        self.findings = []

    def run_all_checks(self):
        self.check_injection()
        self.check_secrets()
        self.check_config()
        self.check_access_control()
        self.check_transport()
        return self.findings

    def add_finding(self, level, type_, message, recommendation):
        self.findings.append({
            "level": level,
            "type": type_,
            "message": message,
            "recommendation": recommendation
        })

    def check_injection(self):
        if re.search(r"\b(eval|exec)\s*\(", self.code):
            self.add_finding("CRITICAL", "Dynamic Code Execution",
                "This code uses 'eval' or 'exec', which can be very dangerous.",
                "Avoid using eval/exec. Use safer alternatives.")

        if re.search(r"SELECT .* ['\"]\s*\+", self.code, re.IGNORECASE):
            self.add_finding("CRITICAL", "SQL Injection",
                "Possible SQL injection vulnerability.",
                "Use parameterized queries.")

        if re.search(r"os\.system\(.*input\(", self.code):
            self.add_finding("CRITICAL", "Command Injection",
                "User input may be passed into a shell command.",
                "Use subprocess with array input and sanitize parameters.")

        if re.search(r"render_template\(.*\{\{.*\}\}", self.code):
            self.add_finding("WARNING", "Template Injection",
                "Possible unescaped input in template rendering.",
                "Ensure proper escaping in templates.")

        if re.search(r"request\.args\[.*\]", self.code):
            self.add_finding("WARNING", "Cross-Site Scripting (XSS)",
                "Unescaped user input may be included in output.",
                "Sanitize and encode all output displayed in HTML.")

    def check_secrets(self):
        if re.search(r"(?i)password\s*=\s*['\"].+['\"]", self.code):
            self.add_finding("WARNING", "Hardcoded Password",
                "Password is hardcoded in the code.",
                "Store secrets in environment variables or secure vaults.")

        if re.search(r"(?i)(api|token|bearer)[\s:=]+['\"][a-z0-9-_]{16,}['\"]", self.code):
            self.add_finding("WARNING", "Exposed Token",
                "This file may contain an exposed API key or token.",
                "Move sensitive tokens to environment variables.")

    def check_config(self):
        if re.search(r"DEBUG\s*=\s*True", self.code):
            self.add_finding("INFO", "Debug Mode Enabled",
                "Debug mode is enabled in the code.",
                "Disable debug mode before deploying to production.")

        if re.search(r"Access-Control-Allow-Origin\s*[:=]\s*['\"]\*['\"]", self.code):
            self.add_finding("WARNING", "Open CORS Policy",
                "CORS is open to all origins.",
                "Restrict CORS to trusted domains.")

    def check_access_control(self):
        if re.search(r"@app\.route\(.*\)\n\s*def .*\(.*\):", self.code):
            if not re.search(r"@login_required", self.code):
                self.add_finding("WARNING", "Missing Authentication",
                    "Sensitive route may be exposed without authentication.",
                    "Ensure proper authentication decorators are applied.")

        if re.search(r"/user/\d+", self.code):
            self.add_finding("WARNING", "IDOR (Insecure Direct Object Reference)",
                "Direct object reference detected.",
                "Validate object ownership before serving requests.")

    def check_transport(self):
        if re.search(r"http://", self.code) and not re.search(r"http://localhost", self.code):
            self.add_finding("INFO", "Insecure HTTP",
                "Unencrypted HTTP URL detected.",
                "Use HTTPS for all external requests.")