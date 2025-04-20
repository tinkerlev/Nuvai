"""
File: jsx_scanner.py

Description:
This module scans JSX (React) source code for common security vulnerabilities.
It is part of Nuvai's multi-language static analysis engine and focuses on
identifying issues in React components such as unsafe rendering, improper use
of dangerouslySetInnerHTML, weak prop validation, and other anti-patterns.

Implemented Checks:
- Use of dangerouslySetInnerHTML
- Inline JavaScript in JSX attributes
- Usage of eval, new Function, or setTimeout with strings
- Hardcoded tokens or API keys
- Components without PropTypes or validation
- Usage of innerHTML assignments via refs
- Exposure of internal state in console logs

Note: This scanner uses pattern-based matching, not full AST parsing.
"""

import re

class JSXScanner:
    def __init__(self, code):
        self.code = code
        self.findings = []

    def run_all_checks(self):
        self.check_dangerous_innerhtml()
        self.check_inline_js_handlers()
        self.check_eval_or_function()
        self.check_hardcoded_tokens()
        self.check_missing_proptypes()
        self.check_innerhtml_via_refs()
        self.check_console_exposure()
        return self.findings

    def add_finding(self, level, ftype, message, recommendation):
        self.findings.append({
            "level": level,
            "type": ftype,
            "message": message,
            "recommendation": recommendation
        })

    def check_dangerous_innerhtml(self):
        if re.search(r'dangerouslySetInnerHTML\s*=\s*\{', self.code):
            self.add_finding(
                "CRITICAL",
                "dangerouslySetInnerHTML Used",
                "React component uses dangerouslySetInnerHTML, which may expose to XSS.",
                "Avoid it or sanitize input with a trusted library like DOMPurify."
            )

    def check_inline_js_handlers(self):
        if re.search(r'on\w+\s*=\s*\{\(.*\)=>', self.code):
            self.add_finding(
                "WARNING",
                "Inline JS in JSX",
                "Inline functions used in JSX can affect performance and reusability.",
                "Move logic to a separate method or memoized callback."
            )

    def check_eval_or_function(self):
        if re.search(r'eval\s*\(', self.code) or re.search(r'new Function\s*\(', self.code):
            self.add_finding(
                "HIGH",
                "Dynamic Code Execution",
                "Detected eval() or new Function() inside a JSX file.",
                "Avoid dynamic code execution in React apps."
            )
        if re.search(r'setTimeout\s*\(\s*"', self.code):
            self.add_finding(
                "MEDIUM",
                "String-based Timer Execution",
                "setTimeout uses a string, which acts like eval().",
                "Pass a function instead of a string."
            )

    def check_hardcoded_tokens(self):
        if re.search(r'(apiKey|token|secret)\s*=\s*["\']\w{20,}["\']', self.code):
            self.add_finding(
                "HIGH",
                "Hardcoded Secret",
                "Sensitive API key or token found hardcoded.",
                "Store secrets securely using environment variables."
            )

    def check_missing_proptypes(self):
        if re.search(r'class\s+\w+\s+extends\s+React\.Component', self.code):
            if not re.search(r'\w+\.propTypes\s*=\s*{', self.code):
                self.add_finding(
                    "WARNING",
                    "Missing PropTypes",
                    "React class component has no defined propTypes.",
                    "Use prop-types to validate component props."
                )

    def check_innerhtml_via_refs(self):
        if re.search(r'ref\.[^;]*\.innerHTML\s*=\s*', self.code):
            self.add_finding(
                "HIGH",
                "Direct innerHTML via ref",
                "Detected assignment to innerHTML using a React ref.",
                "Avoid this pattern unless strictly necessary and sanitized."
            )

    def check_console_exposure(self):
        if re.search(r'console\.(log|debug|info)\(', self.code):
            self.add_finding(
                "INFO",
                "Console Logging Found",
                "Found use of console.log or similar in JSX file.",
                "Remove or wrap logging for production environments."
            )
