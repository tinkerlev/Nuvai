"""
File: run.py

Description:
This is the main entry point for running Nuvai from the command line.
It loads a source code file, detects its programming language,
uses the appropriate scanner engine, and prints out a security report.

Supports output formats: json, txt, html, pdf.
Automatically stores results in ~/security_reports.

Note: This CLI interface is designed for both technical and non-technical users.
"""

import argparse
import os

from src.nuvai.scanner import get_language, scan_code
from src.nuvai.report_saver import save_report

def load_code(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"[ERROR] Failed to load file: {e}")
        exit(1)

def print_results(findings):
    if not findings:
        print("✅ No critical issues found in the code.")
        return

    print("\n🔍 Security Findings:")
    for f in findings:
        print(f"\n[{f['level']}] {f['type']}")
        print(f"- Description: {f['message']}")
        print(f"- Recommendation: {f['recommendation']}")

def main():
    parser = argparse.ArgumentParser(description="Nuvai - AI Code Vulnerability Scanner")
    parser.add_argument("file", help="Path to the code file to scan (e.g. app.py, index.js)")
    parser.add_argument("--format", choices=["json", "txt", "html", "pdf"], default="txt",
                        help="Output format for report (default: txt)")
    args = parser.parse_args()

    code = load_code(args.file)
    lang = get_language(args.file)
    print(f"🔎 Detected language: {lang}")
    findings = scan_code(code, lang)
    print_results(findings)

    path = save_report(findings, args.format)
    if path:
        print(f"\n📄 Report saved to: {path}")

if __name__ == "__main__":
    main()
