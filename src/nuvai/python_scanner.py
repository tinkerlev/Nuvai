"""
File: python_scanner.py

Description:
This module scans Python source code for common and critical security vulnerabilities.
It is part of Nuvai's static analysis engine and focuses on detecting insecure coding
patterns such as code injection, deserialization, SSRF, weak cryptography, path traversal,
and more.

The scanner performs lightweight pattern-based analysis to surface security concerns
in AI-generated, no-code, or traditional hand-written Python code.

It is triggered by the main dispatcher (scanner.py) and outputs a structured list of findings.
"""

import re

class PythonScanner:
    def __init__(self, code):
        self.code = code
        self.findings = []

    def run_all_checks(self):
        self.check_eval_exec()
        self.check_command_injection()
        self.check_template_injection()
        self.check_xss()
        self.check_hardcoded_secrets()
        self.check_debug_mode()
        self.check_pickle_usage()
        self.check_ssrf_patterns()
        self.check_path_traversal()
        self.check_weak_hashes()
        self.check_raw_input()
        self.check_insecure_jwt()
        self.check_sensitive_logging()
        return self.findings

    def add_finding(self, level, ftype, message, recommendation):
        self.findings.append({
            "level": level,
            "type": ftype,
            "message": message,
            "recommendation": recommendation
        })

    def check_eval_exec(self):
        if "eval(" in self.code or "exec(" in self.code:
            self.add_finding(
                "CRITICAL",
                "Dynamic Code Execution",
                "This code uses 'eval' or 'exec', which can be very dangerous.",
                "Avoid using eval/exec. Use safer alternatives."
            )

    def check_command_injection(self):
        if re.search(r'os\.system\(.+\)', self.code):
            self.add_finding(
                "CRITICAL",
                "Command Injection",
                "User input may be passed into a shell command.",
                "Use subprocess with array input and sanitize parameters."
            )

    def check_template_injection(self):
        if re.search(r'render_template\(.+\)', self.code) and "request" in self.code:
            self.add_finding(
                "WARNING",
                "Template Injection",
                "Possible unescaped input in template rendering.",
                "Ensure proper escaping in templates."
            )

    def check_xss(self):
        if "<script>" in self.code or "document.write(" in self.code:
            self.add_finding(
                "WARNING",
                "Cross-Site Scripting (XSS)",
                "Unescaped user input may be included in output.",
                "Sanitize and encode all output displayed in HTML."
            )

    def check_hardcoded_secrets(self):
        if re.search(r'(api|token|secret|key|password)\s*[_=]\s*[\'\"].+?[\'\"]', self.code, re.IGNORECASE):
            self.add_finding(
                "HIGH",
                "Hardcoded Secret",
                "A secret or token appears to be hardcoded in the code.",
                "Store sensitive values in environment variables or a secure vault."
            )

    def check_debug_mode(self):
        if "DEBUG = True" in self.code or "app.config[\"DEBUG\"] = True" in self.code:
            self.add_finding(
                "INFO",
                "Debug Mode Enabled",
                "Debug mode is enabled in the code.",
                "Disable debug mode before deploying to production."
            )

    def check_pickle_usage(self):
        if "pickle.loads(" in self.code or "pickle.load(" in self.code:
            self.add_finding(
                "CRITICAL",
                "Insecure Deserialization",
                "Use of 'pickle' can allow arbitrary code execution.",
                "Use safer alternatives like 'json' for deserializing untrusted input."
            )

    def check_ssrf_patterns(self):
        if re.search(r'requests\.get\([^\)]+\)', self.code) and "http" in self.code:
            self.add_finding(
                "HIGH",
                "Server-Side Request Forgery (SSRF)",
                "HTTP requests using user input can be abused to target internal systems.",
                "Sanitize and validate all URLs. Limit allowed destinations."
            )

    def check_path_traversal(self):
        if re.search(r'open\(.*\.{2}/', self.code):
            self.add_finding(
                "CRITICAL",
                "Path Traversal",
                "Code may allow file path traversal (e.g. '../../etc/passwd').",
                "Sanitize file paths and use safe libraries like 'pathlib'."
            )

    def check_weak_hashes(self):
        if "md5(" in self.code or "sha1(" in self.code:
            self.add_finding(
                "MEDIUM",
                "Weak Hash Function",
                "Use of MD5 or SHA1 is insecure and can lead to collisions.",
                "Use SHA-256 or stronger hash functions."
            )

    def check_raw_input(self):
        if "input(" in self.code:
            self.add_finding(
                "MEDIUM",
                "Raw Input Usage",
                "Use of 'input()' can expose the application to unexpected user behavior.",
                "Validate and sanitize all user inputs properly."
            )

    def check_insecure_jwt(self):
        if "jwt.decode(" in self.code and "verify=False" in self.code:
            self.add_finding(
                "HIGH",
                "Insecure JWT Validation",
                "JWT tokens should always be verified.",
                "Avoid disabling verification when decoding JWT tokens."
            )

    def check_sensitive_logging(self):
        if re.search(r'logging\..*\((.*password|token|secret)', self.code, re.IGNORECASE):
            self.add_finding(
                "MEDIUM",
                "Sensitive Data in Logs",
                "Sensitive values should never be logged.",
                "Mask or remove sensitive data before logging."
            )