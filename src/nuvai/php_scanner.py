"""
File: php_scanner.py

Description:
This module scans PHP source code for common and critical security vulnerabilities.
It is part of Nuvai's multi-language static analysis engine, focusing on insecure
coding practices such as unsanitized input, insecure functions, weak configurations,
and authentication/session management issues.

Implemented Checks:
- Use of dangerous functions: eval, system, exec, passthru, shell_exec, popen
- SQL injection via unsanitized $_GET/$_POST/$_REQUEST
- Reflected XSS using echo/print on raw input
- File inclusion attacks (LFI/RFI)
- Hardcoded credentials (DB user/pass)
- Enabled error_reporting in production
- Missing session_regenerate_id after login
- Unvalidated file uploads ($_FILES)
- Use of insecure hashing (md5, sha1)
- Lack of CSRF protection in forms
- Use of insecure random functions (rand, mt_rand)
- Exposure of PHP version via headers

Note: This module uses regex-based scanning and is not a full PHP parser.
It aims to detect risky patterns in AI-generated, legacy, or hand-written code.
"""

import re

class PHPScanner:
    def __init__(self, code):
        self.code = code
        self.findings = []

    def run_all_checks(self):
        self.check_eval_system()
        self.check_sql_injection()
        self.check_xss_echo()
        self.check_file_inclusion()
        self.check_hardcoded_credentials()
        self.check_error_reporting()
        self.check_session_security()
        self.check_file_uploads()
        self.check_insecure_hashing()
        self.check_csrf_tokens()
        self.check_insecure_random()
        self.check_php_version_exposure()
        return self.findings

    def add_finding(self, level, ftype, message, recommendation):
        self.findings.append({
            "level": level,
            "type": ftype,
            "message": message,
            "recommendation": recommendation
        })

    def check_eval_system(self):
        if re.search(r'\b(eval|system|exec|passthru|shell_exec|popen)\s*\(', self.code):
            self.add_finding(
                "CRITICAL",
                "Dangerous Function Execution",
                "Use of functions like eval, system, exec, shell_exec, or popen detected.",
                "Avoid dangerous execution functions. Use built-in PHP logic or sandboxed subprocesses."
            )

    def check_sql_injection(self):
        if re.search(r'\$_(GET|POST|REQUEST).*\.("|\')?\s*(SELECT|INSERT|UPDATE|DELETE)', self.code, re.IGNORECASE):
            self.add_finding(
                "HIGH",
                "Possible SQL Injection",
                "SQL query appears to use unsanitized user input.",
                "Use PDO or MySQLi prepared statements with bound parameters."
            )

    def check_xss_echo(self):
        if re.search(r'(echo|print)\s*\$_(GET|POST|REQUEST|COOKIE)', self.code):
            self.add_finding(
                "HIGH",
                "Reflected XSS",
                "User input is printed without encoding or sanitization.",
                "Escape output with htmlspecialchars or use a templating engine."
            )

    def check_file_inclusion(self):
        if re.search(r'(include|require|include_once|require_once)\s*\(\s*\$_(GET|POST|REQUEST)', self.code):
            self.add_finding(
                "HIGH",
                "Dynamic File Inclusion",
                "Includes file path directly from user input.",
                "Use strict whitelisting or routing mechanisms."
            )

    def check_hardcoded_credentials(self):
        if re.search(r'(host|user|pass|dbname)\s*=\s*[\'\"]\w{4,}[\'\"]', self.code, re.IGNORECASE):
            self.add_finding(
                "HIGH",
                "Hardcoded Credentials",
                "Sensitive database credentials found in source code.",
                "Store them in environment variables or secure config outside webroot."
            )

    def check_error_reporting(self):
        if re.search(r'error_reporting\s*\(', self.code):
            self.add_finding(
                "INFO",
                "Error Reporting Enabled",
                "Production code should not reveal detailed errors.",
                "Turn off error reporting or log to secure location in production."
            )

    def check_session_security(self):
        if 'session_start()' in self.code and 'session_regenerate_id' not in self.code:
            self.add_finding(
                "WARNING",
                "Session Fixation Risk",
                "Session started without regenerating session ID after authentication.",
                "Call session_regenerate_id(true) immediately after login."
            )

    def check_file_uploads(self):
        if re.search(r'\$_FILES\[.+\]', self.code):
            if not re.search(r'(mime_content_type|finfo_open|pathinfo)', self.code):
                self.add_finding(
                    "HIGH",
                    "Unvalidated File Upload",
                    "Detected file upload without proper validation.",
                    "Use finfo/mime type checks, whitelist extensions, and store outside webroot."
                )

    def check_insecure_hashing(self):
        if re.search(r'(md5|sha1)\s*\(', self.code):
            self.add_finding(
                "MEDIUM",
                "Weak Hashing Algorithm",
                "Use of MD5 or SHA1 is insecure for password storage or signatures.",
                "Use password_hash() or SHA-256/SHA-512."
            )

    def check_csrf_tokens(self):
        if re.search(r'<form', self.code) and not re.search(r'csrf_token', self.code, re.IGNORECASE):
            self.add_finding(
                "WARNING",
                "CSRF Protection Missing",
                "Form does not appear to implement CSRF tokens.",
                "Add hidden CSRF tokens and validate them server-side."
            )

    def check_insecure_random(self):
        if re.search(r'\b(rand|mt_rand)\s*\(', self.code):
            self.add_finding(
                "WARNING",
                "Insecure Random Generator",
                "Use of rand() or mt_rand() is not cryptographically secure.",
                "Use random_bytes() or random_int() instead."
            )

    def check_php_version_exposure(self):
        if re.search(r'header\s*\(\s*\"X-Powered-By:\s*PHP', self.code, re.IGNORECASE):
            self.add_finding(
                "INFO",
                "PHP Version Disclosure",
                "Response header reveals PHP version.",
                "Disable 'expose_php' in php.ini to hide version info."
            )
