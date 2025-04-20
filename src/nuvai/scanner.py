"""
File: scanner.py

Description:
This file serves as the central dispatcher for the Nuvai scanner.
Its job is to detect what programming language the input code file is written in,
and then delegate the scanning task to the appropriate scanner module (one per language).

This makes the system flexible and easy to extend — for example, today we support Python,
but tomorrow we can add scanners for JavaScript, HTML, C++, TypeScript, JSX, PHP and more.

Currently supported:
- Python (.py)

Planned:
- JavaScript (.js)
- TypeScript (.ts, .tsx)
- React JSX (.jsx)
- HTML (.html)
- C++ (.cpp, .cc)
- PHP (.php)
"""

import os
from .python_scanner import PythonScanner
# from .javascript_scanner import JavaScriptScanner
# from .html_scanner import HTMLScanner
# from .cpp_scanner import CppScanner
# from .typescript_scanner import TypeScriptScanner
# from .php_scanner import PhpScanner


def get_language(file_path):
    """
    Identify the programming language based on file extension.
    """
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".py":
        return "python"
    elif ext == ".js":
        return "javascript"
    elif ext in [".ts", ".tsx"]:
        return "typescript"
    elif ext == ".jsx":
        return "jsx"
    elif ext == ".html":
        return "html"
    elif ext in [".cpp", ".cc"]:
        return "cpp"
    elif ext == ".php":
        return "php"
    return "unknown"


def scan_code(code: str, language: str):
    """
    Run the appropriate scanner based on the detected language.
    Returns a list of security findings.
    """
    if language == "python":
        scanner = PythonScanner(code)
        return scanner.run_all_checks()

    elif language == "javascript":
        print("[INFO] JavaScript scanning not yet implemented.")
        return []

    elif language == "typescript":
        print("[INFO] TypeScript scanning not yet implemented.")
        return []

    elif language == "jsx":
        print("[INFO] JSX scanning not yet implemented.")
        return []

    elif language == "html":
        print("[INFO] HTML scanning not yet implemented.")
        return []

    elif language == "cpp":
        print("[INFO] C++ scanning not yet implemented.")
        return []

    elif language == "php":
        print("[INFO] PHP scanning not yet implemented.")
        return []

    else:
        print("[ERROR] Unsupported or unknown file type.")
        return []
