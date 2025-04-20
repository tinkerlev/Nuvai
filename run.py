'''
File: run.py

Description:
Main CLI entry point for Nuvai.
This script allows scanning a single code file (e.g., vulnerable_app.py),
or, if no file is provided, scans all supported example files in the /examples directory.
It supports export in multiple formats and automatically saves the report.
'''

import os
import argparse
from src.nuvai import get_language, scan_code
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

def scan_and_save(file):
    print(f"\n🧪 Scanning: {file}")
    code = load_code(file)
    lang = get_language(file)
    findings = scan_code(code, lang)
    print_results(findings)

    format_choice = input("\nSelect export format (json / txt / html / pdf): ").strip().lower()
    path = save_report(findings, format_choice)
    if path:
        print(f"\n✅ Report saved to: {path}")

def main():
    parser = argparse.ArgumentParser(description="Nuvai - AI Security Code Scanner")
    parser.add_argument("file", nargs='?', help="Path to the code file to scan (e.g. app.py)")
    args = parser.parse_args()

    if args.file:
        scan_and_save(args.file)
    else:
        example_dir = os.path.join(os.path.dirname(__file__), "examples")
        files = [f for f in os.listdir(example_dir) if f.startswith("vulnerable_app.")]
        for file in files:
            file_path = os.path.join(example_dir, file)
            scan_and_save(file_path)

if __name__ == "__main__":
    main()
