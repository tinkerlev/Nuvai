"""
File: run.py

Description:
Nuvai is the main entry point to the CLI-based code vulnerability scanner.
It loads a source code file, runs comprehensive static security checks,
and prints out a summary of the findings. It also offers report export
in multiple formats such as JSON, TXT, HTML, or PDF.

This tool is part of the Nuvai suite for AI-generated and No-Code application auditing.
"""

import argparse
from src.nuvai.scanner import CodeScanner
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
    parser.add_argument("file", help="Path to the code file to scan (e.g. app.py)")
    args = parser.parse_args()

    code = load_code(args.file)
    scanner = CodeScanner(code)
    findings = scanner.run_all_checks()
    print_results(findings)

    if findings:
        format_choice = input("\nSelect export format (json / txt / html / pdf): ").strip().lower()
        if format_choice in ["json", "txt", "html", "pdf"]:
            saved_path = save_report(findings, format_choice)
            if saved_path:
                print(f"\n✅ Report saved to: {saved_path}")
            else:
                print("⚠️ Report could not be saved in the selected format.")
        else:
            print("❌ Invalid format. Report was not saved.")

if __name__ == "__main__":
    main()