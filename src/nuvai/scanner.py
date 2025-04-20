"""
File: scanner.py

Description:
This is the central dispatcher module for the Nuvai scanning engine.
It is responsible for identifying the programming language of the target file
(based on file extension), importing the appropriate scanning module,
and running a complete analysis using that module.

It supports multiple languages:
- Python (.py)
- JavaScript (.js)
- HTML (.html)
- JSX (.jsx)
- TypeScript (.ts)
- PHP (.php)
- C++ (.cpp)

The scanner returns structured findings which can then be saved or printed.
"""

import os

from .python_scanner import PythonScanner
from .javascript_scanner import JavaScriptScanner
from .html_scanner import HTMLScanner
from .jsx_scanner import JSXScanner
from .php_scanner import PHPScanner
from .cpp_scanner import CppScanner
from .typescript_scanner import TypeScriptScanner

def get_language(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    return {
        ".py": "python",
        ".js": "javascript",
        ".html": "html",
        ".jsx": "jsx",
        ".php": "php",
        ".cpp": "cpp",
        ".ts": "typescript",
    }.get(ext, None)

def scan_code(code, language):
    scanner = None

    if language == "python":
        scanner = PythonScanner(code)
    elif language == "javascript":
        scanner = JavaScriptScanner(code)
    elif language == "html":
        scanner = HTMLScanner(code)
    elif language == "jsx":
        scanner = JSXScanner(code)
    elif language == "php":
        scanner = PHPScanner(code)
    elif language == "cpp":
        scanner = CppScanner(code)
    elif language == "typescript":
        scanner = TypeScriptScanner(code)
    else:
        raise ValueError("Unsupported language or file extension.")

    return scanner.run_all_checks()
