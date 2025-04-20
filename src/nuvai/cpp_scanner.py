"""
File: cpp_scanner.py

Description:
This module scans C++ source code for common and critical security vulnerabilities.
It is part of Nuvai's multi-language static analysis engine, designed to help identify
unsafe coding practices and prevent potential exploitation of legacy or unmanaged C++ code.

Implemented Checks:
- Use of dangerous functions (gets, strcpy, sprintf, system, popen)
- Potential buffer overflows in fixed-size arrays
- Null pointer initialization without safety checks
- Unchecked return values from memory allocation (e.g., malloc)
- Uninitialized variable usage
- Infinite loops (while(1)) without exit conditions
- Use of strcpy without bounds checking
- Dangerous type casting using reinterpret_cast
- Use of goto statement (bad practice)
- Use of hardcoded credentials or keys
- Use of insecure functions like scanf without size specifier
- Usage of raw pointers instead of smart pointers
- Functions without return type specified
- Use of unsafe macros or inline assembly

Note: This is a lightweight static scanner using regular expressions.
It does not perform full parsing or semantic analysis.
"""

import re

class CppScanner:
    def __init__(self, code):
        self.code = code
        self.findings = []

    def run_all_checks(self):
        self.check_dangerous_functions()
        self.check_buffer_overflows()
        self.check_insecure_pointer_usage()
        self.check_malloc_return_check()
        self.check_uninitialized_vars()
        self.check_infinite_loops()
        self.check_strcpy_no_bounds()
        self.check_reinterpret_cast()
        self.check_goto_usage()
        self.check_hardcoded_secrets()
        self.check_scanf_no_size()
        self.check_raw_pointers()
        self.check_missing_return_type()
        self.check_inline_asm()
        return self.findings

    def add_finding(self, level, ftype, message, recommendation):
        self.findings.append({
            "level": level,
            "type": ftype,
            "message": message,
            "recommendation": recommendation
        })

    def check_dangerous_functions(self):
        patterns = [r'\bgets\s*\(', r'\bstrcpy\s*\(', r'\bsprintf\s*\(', r'\bsystem\s*\(', r'\bpopen\s*\(']
        for pattern in patterns:
            if re.search(pattern, self.code):
                self.add_finding(
                    "CRITICAL",
                    "Dangerous Function Usage",
                    f"Usage of insecure function matching pattern: {pattern}",
                    "Avoid using functions like gets, strcpy, system. Use safer and modern alternatives."
                )

    def check_buffer_overflows(self):
        if re.search(r'char\s+\w+\s*\[\s*\d+\s*\]\s*=\s*\".+\";', self.code):
            self.add_finding(
                "HIGH",
                "Possible Buffer Overflow",
                "Fixed-size character array may overflow if not validated.",
                "Ensure buffer sizes are properly checked before writing data."
            )

    def check_insecure_pointer_usage(self):
        if re.search(r'\*\s*\w+\s*=\s*NULL', self.code):
            self.add_finding(
                "WARNING",
                "Null Pointer Initialization",
                "Pointer is being initialized to NULL without safety handling.",
                "Use smart pointers or ensure proper null-checks are in place."
            )

    def check_malloc_return_check(self):
        if re.search(r'(malloc|calloc|realloc)\s*\(.*\)\s*;', self.code) and not re.search(r'if\s*\(.*!=\s*NULL\)', self.code):
            self.add_finding(
                "HIGH",
                "Unchecked Memory Allocation",
                "Memory allocation result is not checked for NULL.",
                "Always validate memory allocation success before using the pointer."
            )

    def check_uninitialized_vars(self):
        if re.search(r'(int|char|float|double)\s+\w+\s*;', self.code):
            self.add_finding(
                "WARNING",
                "Uninitialized Variable",
                "A declared variable may be used without being initialized.",
                "Always initialize variables or enforce safe usage via compiler warnings."
            )

    def check_infinite_loops(self):
        if re.search(r'while\s*\(\s*1\s*\)', self.code):
            self.add_finding(
                "MEDIUM",
                "Potential Infinite Loop",
                "Detected loop condition 'while(1)' which may run indefinitely.",
                "Ensure proper exit conditions or timeouts are in place."
            )

    def check_strcpy_no_bounds(self):
        if re.search(r'strcpy\s*\(\s*\w+\s*,\s*\w+\s*\)', self.code):
            self.add_finding(
                "HIGH",
                "Unsafe strcpy",
                "strcpy used without checking destination buffer size.",
                "Use strncpy or safer string handling mechanisms."
            )

    def check_reinterpret_cast(self):
        if re.search(r'reinterpret_cast<', self.code):
            self.add_finding(
                "WARNING",
                "Use of reinterpret_cast",
                "Dangerous type casting can lead to undefined behavior.",
                "Avoid reinterpret_cast when possible; prefer static_cast or safe conversions."
            )

    def check_goto_usage(self):
        if re.search(r'\bgoto\b', self.code):
            self.add_finding(
                "INFO",
                "Use of goto Statement",
                "goto makes code harder to maintain and debug.",
                "Avoid goto; use structured control flow (e.g., loops, functions)."
            )

    def check_hardcoded_secrets(self):
        if re.search(r'(password|secret|api_key|token)\s*=\s*\".*\"', self.code, re.IGNORECASE):
            self.add_finding(
                "HIGH",
                "Hardcoded Credential",
                "Detected hardcoded sensitive string in the code.",
                "Never store secrets in code. Use environment variables or secure config files."
            )

    def check_scanf_no_size(self):
        if re.search(r'scanf\s*\(\s*\"[^%]*%s[^\"]*\"', self.code):
            self.add_finding(
                "HIGH",
                "Unsafe scanf",
                "scanf used with %s without length limit.",
                "Use width specifiers to prevent buffer overflows (e.g., %99s)."
            )

    def check_raw_pointers(self):
        if re.search(r'(int|char|float|double)\s*\*\s*\w+', self.code):
            self.add_finding(
                "INFO",
                "Use of Raw Pointer",
                "Raw pointers used instead of safer alternatives.",
                "Consider using smart pointers or containers to manage memory."
            )

    def check_missing_return_type(self):
        if re.search(r'^\s*\w+\s+\w+\s*\([^)]*\)\s*\{', self.code, re.MULTILINE):
            if not re.search(r'(void|int|char|float|double|bool)\s+\w+\s*\(', self.code):
                self.add_finding(
                    "WARNING",
                    "Missing Function Return Type",
                    "Function declared without an explicit return type.",
                    "Always define function return types explicitly."
                )

    def check_inline_asm(self):
        if re.search(r'__asm__|asm\s*\(', self.code):
            self.add_finding(
                "HIGH",
                "Inline Assembly Usage",
                "Inline assembly may reduce code portability and introduce low-level vulnerabilities.",
                "Avoid inline assembly unless absolutely necessary and document its usage clearly."
            )
