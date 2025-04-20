"""
File: html_scanner.py

Description:
This module scans HTML content for common web-related security vulnerabilities.
It is part of Nuvai's multi-language static analysis engine and focuses on detecting
potential issues in HTML templates and static content.

Implemented Checks:
- Embedded <script> tags (inline JavaScript)
- Inline event handlers (e.g., onclick, onerror)
- Unescaped user content markers (e.g., {{ user_input }})
- Suspicious iframe embeds or remote scripts
- Comments exposing sensitive data or development notes
- Dangerous input fields (no type=password or autocomplete off)
- XSS via javascript: URIs or image error handlers
- InnerHTML assignments in script blocks
- Missing Content Security Policy meta tag
- Missing autocomplete attributes on sensitive input fields
- Forms using GET method to submit sensitive data
- Suspicious base64-encoded payloads in script tags or attributes
- Embedded <style> tags with suspicious expressions

Note: This is a lightweight static scanner using regular expressions.
It does not parse the DOM or run a browser engine.
"""

import re

class HTMLScanner:
    def __init__(self, code):
        self.code = code
        self.findings = []

    def run_all_checks(self):
        self.check_script_tags()
        self.check_inline_event_handlers()
        self.check_unescaped_template_output()
        self.check_suspicious_iframes()
        self.check_sensitive_comments()
        self.check_insecure_inputs()
        self.check_javascript_uri_links()
        self.check_innerhtml_usage()
        self.check_missing_csp()
        self.check_missing_autocomplete()
        self.check_insecure_get_forms()
        self.check_base64_payloads()
        self.check_dangerous_style_blocks()
        return self.findings

    def add_finding(self, level, ftype, message, recommendation):
        self.findings.append({
            "level": level,
            "type": ftype,
            "message": message,
            "recommendation": recommendation
        })

    def check_script_tags(self):
        if re.search(r'<script.*?>.*?</script>', self.code, re.DOTALL | re.IGNORECASE):
            self.add_finding(
                "WARNING",
                "Inline JavaScript Detected",
                "Inline <script> tags found in HTML.",
                "Consider moving JavaScript to external files and sanitizing user input."
            )

    def check_inline_event_handlers(self):
        if re.search(r'on\w+\s*=\s*"', self.code, re.IGNORECASE):
            self.add_finding(
                "WARNING",
                "Inline Event Handler",
                "HTML includes inline event handlers like onclick, onerror, etc.",
                "Avoid using inline events. Use addEventListener() from JavaScript files."
            )

    def check_unescaped_template_output(self):
        if re.search(r'\{\{\s*.*\s*\}\}', self.code):
            self.add_finding(
                "MEDIUM",
                "Unescaped Template Output",
                "HTML contains template markers that may include user content.",
                "Ensure all dynamic content is properly escaped to avoid XSS."
            )

    def check_suspicious_iframes(self):
        if re.search(r'<iframe.*?src\s*=\s*\"http', self.code, re.IGNORECASE):
            self.add_finding(
                "HIGH",
                "External iframe Embed",
                "HTML includes an iframe pointing to an external URL.",
                "Avoid embedding unknown external sources. Validate URLs and use sandboxing."
            )

    def check_sensitive_comments(self):
        if re.search(r'<!--.*(TODO|FIXME|DEBUG|api_key|secret|token).*-->', self.code, re.IGNORECASE):
            self.add_finding(
                "INFO",
                "Exposed Developer Comment",
                "Found HTML comment that may expose internal or sensitive information.",
                "Avoid shipping code with comments containing sensitive data or dev notes."
            )

    def check_insecure_inputs(self):
        if re.search(r'<input[^>]*name\s*=\s*\".*password.*\"[^>]*>', self.code, re.IGNORECASE) and not re.search(r'<input[^>]*type\s*=\s*\"password\"', self.code, re.IGNORECASE):
            self.add_finding(
                "HIGH",
                "Insecure Input Field",
                "Input field for password is missing type='password'.",
                "Always use appropriate input types and disable autocomplete for sensitive fields."
            )

    def check_javascript_uri_links(self):
        if re.search(r'href\s*=\s*\"javascript:', self.code, re.IGNORECASE):
            self.add_finding(
                "CRITICAL",
                "JavaScript URI Detected",
                "Anchor tag uses javascript: URI which may enable XSS.",
                "Avoid javascript: URIs and sanitize any dynamic href values."
            )
        if re.search(r'<img[^>]+onerror\s*=\s*"', self.code, re.IGNORECASE):
            self.add_finding(
                "HIGH",
                "Image onerror Event",
                "Image tag uses onerror event which can be abused for XSS.",
                "Avoid onerror or sanitize content passed to image tags."
            )

    def check_innerhtml_usage(self):
        if re.search(r'innerHTML\s*=\s*[^;]+;', self.code):
            self.add_finding(
                "HIGH",
                "Unsafe DOM Manipulation",
                "Detected assignment to innerHTML which can lead to XSS.",
                "Use textContent or safe DOM APIs to manipulate page content."
            )

    def check_missing_csp(self):
        if not re.search(r'http-equiv\s*=\s*\"Content-Security-Policy\"', self.code, re.IGNORECASE):
            self.add_finding(
                "INFO",
                "Missing CSP Header",
                "No Content Security Policy defined in HTML.",
                "Define CSP using meta tag or HTTP headers to restrict inline scripts and reduce attack surface."
            )

    def check_missing_autocomplete(self):
        if re.search(r'<input[^>]*(name|id)\s*=\s*\".*(password|credit|card).*\"[^>]*>', self.code, re.IGNORECASE) and not re.search(r'autocomplete\s*=\s*\"off\"', self.code):
            self.add_finding(
                "MEDIUM",
                "Autocomplete Enabled on Sensitive Field",
                "Input field for sensitive data may allow browser autofill.",
                "Disable autocomplete for inputs collecting passwords or credit card info."
            )

    def check_insecure_get_forms(self):
        if re.search(r'<form[^>]*method\s*=\s*\"get\"', self.code, re.IGNORECASE):
            self.add_finding(
                "WARNING",
                "Sensitive Form Using GET Method",
                "Forms using GET expose data in URLs and logs.",
                "Use POST for forms that process login credentials or sensitive data."
            )

    def check_base64_payloads(self):
        if re.search(r'[A-Za-z0-9+/]{40,}={0,2}', self.code):
            self.add_finding(
                "INFO",
                "Suspicious Base64 Detected",
                "Long base64-like string found in HTML, may indicate obfuscated payload.",
                "Inspect and decode content to ensure it does not contain hidden threats."
            )

    def check_dangerous_style_blocks(self):
        if re.search(r'<style.*?>.*expression\s*\(.*?\)', self.code, re.DOTALL | re.IGNORECASE):
            self.add_finding(
                "HIGH",
                "Suspicious CSS Expression",
                "CSS expression() used inside <style> block, may enable script execution in older browsers.",
                "Avoid using CSS expressions. Stick to static CSS values."
            )
