"""
File: typescript_scanner.py

Description:
This module scans TypeScript source code for security vulnerabilities.
It is part of Nuvai's multi-language static analysis engine and is designed to catch
patterns that could lead to injection, insecure data handling, or logic flaws in
modern frontend/backend TypeScript apps (including Node.js and Angular/React codebases).

Implemented Checks:
- Use of eval, new Function, setTimeout/setInterval with string
- Unsanitized user input from URL, cookies, headers
- Access to window/document with direct DOM manipulation
- Exposure of tokens/API keys in code
- Missing input validation on parameters
- Insecure deserialization via JSON.parse
- Usage of innerHTML or dangerouslySetInnerHTML
- Overuse of any type
- Insecure random generation (Math.random)
- Console logging of sensitive data
- Bypassing TypeScript type system with type assertions (as unknown as ...)
- Using allowJs or skipLibCheck in tsconfig
- Inclusion of secrets in source maps (.map files)
- Missing helmet/cors middleware in Express apps

Note: Uses regex-based scanning for simplicity and speed. Not a full AST parser.
"""

import re

class TypeScriptScanner:
    def __init__(self, code):
        self.code = code
        self.findings = []

    def run_all_checks(self):
        self.check_eval_usage()
        self.check_user_input_sources()
        self.check_dom_access()
        self.check_secrets_exposure()
        self.check_missing_validation()
        self.check_json_parse()
        self.check_innerhtml()
        self.check_any_type()
        self.check_insecure_random()
        self.check_sensitive_logging()
        self.check_type_assertions()
        self.check_tsconfig_flags()
        self.check_express_middleware()
        self.check_source_map_leak()
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
            self.add_finding("CRITICAL", "Dynamic Code Execution", "Use of eval() or new Function() detected.", "Avoid dynamic execution. Use safe logic alternatives.")
        if re.search(r'setTimeout\s*\(\s*"', self.code) or re.search(r'setInterval\s*\(\s*"', self.code):
            self.add_finding("HIGH", "String-based Timer Execution", "Timer function receives a string, which behaves like eval().", "Pass functions instead of strings.")

    def check_user_input_sources(self):
        if re.search(r'(location|document\.cookie|headers|params|req\.query|req\.body)', self.code):
            self.add_finding("MEDIUM", "Untrusted Input Source", "Reading from URL, cookies, or request objects.", "Always sanitize and validate user input.")

    def check_dom_access(self):
        if re.search(r'document\.(getElementById|getElementsByClassName|querySelector)', self.code):
            self.add_finding("WARNING", "Direct DOM Access", "Accessing DOM directly can lead to XSS or logic flaws.", "Use frameworks' safe methods or sanitize input.")

    def check_secrets_exposure(self):
        if re.search(r'(apiKey|token|secret)\s*=\s*["\']\w{20,}["\']', self.code):
            self.add_finding("HIGH", "Hardcoded Secret", "Found what appears to be a hardcoded secret.", "Move secrets to env vars or secure configs.")

    def check_missing_validation(self):
        if re.search(r'(req|input)\.(query|body|params)', self.code) and not re.search(r'(validate|zod|joi|class-validator)', self.code):
            self.add_finding("MEDIUM", "Missing Input Validation", "No validation logic found on user-supplied parameters.", "Use input validation libraries such as Joi or Zod.")

    def check_json_parse(self):
        if re.search(r'JSON\.parse\s*\(', self.code):
            self.add_finding("MEDIUM", "Insecure Deserialization", "Use of JSON.parse may deserialize unsafe data.", "Wrap in try/catch and validate structure after parsing.")

    def check_innerhtml(self):
        if re.search(r'(innerHTML|dangerouslySetInnerHTML)\s*=', self.code):
            self.add_finding("HIGH", "Unsafe HTML Injection", "Direct assignment to innerHTML or dangerouslySetInnerHTML.", "Use safe rendering practices and sanitize HTML.")

    def check_any_type(self):
        if re.search(r'\:\s*any', self.code):
            self.add_finding("WARNING", "Overuse of any Type", "Use of 'any' defeats type safety.", "Use explicit interfaces or stricter types instead.")

    def check_insecure_random(self):
        if re.search(r'Math\.random\s*\(', self.code):
            self.add_finding("WARNING", "Insecure Random Generator", "Math.random is not cryptographically secure.", "Use crypto.getRandomValues or external lib.")

    def check_sensitive_logging(self):
        if re.search(r'console\.(log|debug)\([^)]*(password|token|secret)', self.code, re.IGNORECASE):
            self.add_finding("INFO", "Sensitive Data in Logs", "Sensitive keyword logged to console.", "Avoid logging sensitive values in production.")

    def check_type_assertions(self):
        if re.search(r'as\s+unknown\s+as\s+', self.code):
            self.add_finding("WARNING", "Unsafe Type Assertion", "Bypassing type system using 'as unknown as'.", "Use safe type guards or validators instead.")

    def check_tsconfig_flags(self):
        if re.search(r'("skipLibCheck"\s*:\s*true|"allowJs"\s*:\s*true)', self.code):
            self.add_finding("INFO", "Weak TypeScript Configuration", "TypeScript config may be suppressing important checks.", "Avoid skipLibCheck and allowJs for strict type safety.")

    def check_express_middleware(self):
        if 'express()' in self.code and not re.search(r'(helmet|cors)', self.code):
            self.add_finding("WARNING", "Missing Security Middleware", "Express app missing Helmet or CORS setup.", "Use helmet() and cors() for basic security headers and protections.")

    def check_source_map_leak(self):
        if re.search(r'\.map\s*$', self.code):
            self.add_finding("WARNING", "Source Map Exposure", "Possible inclusion of source maps in production.", "Ensure .map files are not deployed in production environments.")
