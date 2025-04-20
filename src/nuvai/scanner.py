"""
File: scanner.py

Description:
This is the central scanner dispatcher in the Nuvai system. It determines the language of the source file,
selects the appropriate scanner module, and runs security checks accordingly.

Supported Languages:
- Python (.py)
- JavaScript (.js)
- JSX (.jsx)
- HTML (.html)
- PHP (.php)
- TypeScript (.ts)
- C++ (.cpp)

This dispatcher simplifies multi-language support for both CLI tools and future GUI integrations.
"""

import os

from .python_scanner import PythonScanner
from .javascript_scanner import JavaScriptScanner
from .jsx_scanner import JSXScanner
from .html_scanner import HTMLScanner
from .php_scanner import PHPScanner
from .typescript_scanner import TypeScriptScanner
from .cpp_scanner import CppScanner


def get_language(file_path):
    ext = os.path.splitext(file_path)[-1].lower()
    return {
        ".py": "python",
        ".js": "javascript",
        ".jsx": "jsx",
        ".html": "html",
        ".php": "php",
        ".ts": "typescript",
        ".cpp": "cpp",
    }.get(ext, "unknown")


def scan_code(code, language):
    if language == "python":
        scanner = PythonScanner(code)
    elif language == "javascript":
        scanner = JavaScriptScanner(code)
    elif language == "jsx":
        scanner = JSXScanner(code)
    elif language == "html":
        scanner = HTMLScanner(code)
    elif language == "php":
        scanner = PHPScanner(code)
    elif language == "typescript":
        scanner = TypeScriptScanner(code)
    elif language == "cpp":
        scanner = CppScanner(code)
    else:
        print("❌ Unsupported file type.")
        return []

    return scanner.run_all_checks()