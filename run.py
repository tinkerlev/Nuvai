"""
File: run.py

Description:
This script is the main entry point of the Nuvai scanner tool.
It loads a source code file, detects its language, routes the content to the correct scanner,
and then prints a clear summary of the security findings.

It also allows the user to export the report in multiple formats.
"""

import argparse
from src.nuvai import get_language, scan_code
from src.nuvai import report_saver
import os


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


def prompt_export(findings):
    format_choice = input("\nSelect export format (json / txt / html / pdf): ").strip().lower()
    path = report_saver.save_report(findings, format_choice)
    if path:
        print(f"\n📁 Report saved to: {path}")


def main():
    parser = argparse.ArgumentParser(description="Nuvai - Multi-language Code Security Scanner")
    parser.add_argument("file", help="Path to the code file to scan (e.g. app.py, index.js, main.cpp, page.tsx, view.php)")
    args = parser.parse_args()

    file_path = args.file
    code = load_code(file_path)
    language = get_language(file_path)

    print(f"\n🔎 Detected language: {language.capitalize()}")
    findings = scan_code(code, language)

    print_results(findings)
    if findings:
        prompt_export(findings)


if __name__ == "__main__":
    main()