"""
File: run.py

Description:
This is the main CLI entry point for Nuvai – the AI-aware, multi-language code vulnerability scanner.
It handles user input (file path and output format), invokes the language-specific scanner,
and provides a detailed vulnerability report either on screen or as an exportable file.

Key Features:
- Auto-detection of programming language via file extension
- Secure file loading with UTF-8 validation
- Clear CLI output and export options: json, txt, html, pdf
- Automatic creation of `~/security_reports` directory for saved results
- Designed for professional red team / audit / educational use
"""

import argparse
from src.nuvai import get_language, scan_code
from src.nuvai.report_saver import save_report
import os

def load_code(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"\n❌ Failed to load file: {e}\n")
        exit(1)

def print_results(findings):
    if not findings:
        print("\n✅ No critical issues found in the code.\n")
        return

    print("\n🔍 Security Findings:")
    for f in findings:
        print(f"\n[{f['level']}] {f['type']}")
        print(f"- Description: {f['message']}")
        print(f"- Recommendation: {f['recommendation']}")

def main():
    parser = argparse.ArgumentParser(description="Nuvai - AI-Aware Code Vulnerability Scanner")
    parser.add_argument("file", help="Path to source code file (e.g. app.py, main.ts)")
    parser.add_argument("--export", choices=["json", "txt", "html", "pdf"], help="Optional export format")
    args = parser.parse_args()

    file_path = args.file
    export_format = args.export

    code = load_code(file_path)
    language = get_language(file_path)

    if not language:
        print("\n❌ Unsupported file extension. Supported: .py, .js, .html, .php, .jsx, .ts, .cpp\n")
        exit(1)

    print(f"\n🔎 Scanning ({language.upper()}) file: {file_path}\n")
    findings = scan_code(code, language)
    print_results(findings)

    if export_format:
        path = save_report(findings, export_format)
        if path:
            print(f"\n📁 Report saved to: {path}\n")

if __name__ == "__main__":
    main()
