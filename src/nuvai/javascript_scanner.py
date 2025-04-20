"""
File: javascript_scanner.py

Description:
This module scans JavaScript source code for common security vulnerabilities.
It is part of Nuvai's multi-language static analysis engine and focuses on
identifying patterns that lead to injection attacks, insecure DOM manipulation,
unsafe APIs, or logic flaws.

Implemented Checks:
- Use of eval, new Function, or setTimeout with string
- Direct DOM access with innerHTML or document.write
- Unsanitized user input from location, cookies, or forms
- Insecure use of XMLHttpRequest or fetch with dynamic input
- Suspicious script inclusion from untrusted domains
- Hardcoded secrets like API keys or tokens
- Overwritten or shadowed built-in objects

Note: This is a lightweight static scanner using regular expressions.
It does not parse or execute JavaScript.
"""

import re

class JavaScriptScanner:
    def __init__(self, code):
        self.code = code
        self.findings = []

    def run_all_checks(self):
        self.check_eval_usage()
        self.check_dom_injection()
        self.check_user_input_sources()
        self.check_insecure_fetch()
        self.check_external_scripts()
        self.check_hardcoded_tokens()
        self.check_shadowed_globals()
        return self.findings

    def add_finding(self, level, ftype, message, recommendation):
        self.findings.append({
            "level": level,
            "type": ftype,
            "message": message,
            "recommendation": recommendation
        })

    def check_eval_usage(self):
        if re.search(r'eval\s*\(', self.code) or re.search(r'new Function\s*\(', self.code):
            self.add_finding(
                "CRITICAL",
                "Dynamic Code Execution",
                "Use of eval() or new Function() detected.",
                "Avoid dynamic execution. Use safe logic alternatives."
            )
        if re.search(r'setTimeout\s*\(\s*"', self.code):
            self.add_finding(
                "HIGH",
                "String-based Timer Execution",
                "setTimeout uses a string, which behaves like eval().",
                "Use function references or arrow functions instead."
            )

    def check_dom_injection(self):
        if re.search(r'(innerHTML|document\.write)\s*=\s*', self.code):
            self.add_finding(
                "HIGH",
                "DOM-Based Injection",
                "Direct DOM manipulation via innerHTML or document.write.",
                "Use textContent or DOM sanitization libraries."
            )

    def check_user_input_sources(self):
        if re.search(r'(location|document\.cookie|window\.name|localStorage\.getItem)', self.code):
            self.add_finding(
                "MEDIUM",
                "Untrusted Input Source",
                "Reading from URL, cookies, or localStorage without sanitization.",
                "Validate and sanitize input before usage."
            )

    def check_insecure_fetch(self):
        if re.search(r'(fetch|XMLHttpRequest)', self.code) and re.search(r'\+\s*user', self.code):
            self.add_finding(
                "MEDIUM",
                "Insecure Request Composition",
                "Dynamic fetch or XHR URL may allow SSRF or data leaks.",
                "Build URLs safely with strict input validation."
            )

    def check_external_scripts(self):
        if re.search(r'<script\s+src=\"http://', self.code):
            self.add_finding(
                "HIGH",
                "External Script Inclusion",
                "Script loaded from an untrusted or insecure source.",
                "Only include trusted scripts over HTTPS."
            )

    def check_hardcoded_tokens(self):
        if re.search(r'(apiKey|token|secret)\s*=\s*["\']\w{20,}["\']', self.code):
            self.add_finding(
                "HIGH",
                "Hardcoded Secret",
                "Sensitive key or token hardcoded in the code.",
                "Use environment configs or secret managers."
            )

    def check_shadowed_globals(self):
        if re.search(r'(Array|Object|String|window|document)\s*=\s*', self.code):
            self.add_finding(
                "WARNING",
                "Overwriting Built-In Objects",
                "Global built-in object is being reassigned.",
                "Avoid redefining built-ins to prevent unexpected behavior."
            )
