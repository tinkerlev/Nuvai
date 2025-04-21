# File: run.py

"""
Description:
This is the main CLI entry point for the Nuvai static code analysis engine.
It allows users to scan a code file for vulnerabilities and export results in multiple formats.

Features:
- Accepts file path input via command line
- Auto-detects code language by file extension or content
- Runs static analysis using language-specific modules
- Outputs clear terminal results and saves report to file
- Supports export formats: json, txt, html, pdf (auto fallback if PDF not available)
- Prompts user for export format and filename
- Provides contextual security improvement suggestions based on findings
- Handles unexpected input or format errors gracefully

Suitable for technical and non-technical users.
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
        print(f"❌ Failed to load file: {e}")
        exit(1)


def print_results(findings):
    print("\n🔍 Security Findings:")
    for f in findings:
        print(f"\n[{f['level']}] {f['type']}")
        print(f"- Description: {f['message']}")
        print(f"- Recommendation: {f['recommendation']}")

    # Derive dynamic improvement tips based on findings
    unique_tips = set()
    for f in findings:
        if "input" in f['message'].lower():
            unique_tips.add("Use input validation and sanitization wherever user input is accepted.")
        if "hardcoded" in f['message'].lower():
            unique_tips.add("Move hardcoded secrets to environment variables or secret managers.")
        if "debug" in f['message'].lower():
            unique_tips.add("Disable debug mode in production environments.")
        if "logging" in f['message'].lower():
            unique_tips.add("Avoid logging sensitive information like passwords or tokens.")

    if unique_tips:
        print("\n💡 Security Improvement Tips:")
        for tip in sorted(unique_tips):
            print(f"- {tip}")


def prompt_export_settings():
    print("\n💾 Export Report")
    format_choice = input("Select export format (json / txt / html / pdf): ").strip().lower()
    while format_choice not in ["json", "txt", "html", "pdf"]:
        format_choice = input("❗ Invalid format. Please choose from (json / txt / html / pdf): ").strip().lower()
    return format_choice


def main():
    parser = argparse.ArgumentParser(description="Nuvai AI Code Security Scanner")
    parser.add_argument("file", help="Path to the code file to scan (e.g. app.py)")
    args = parser.parse_args()

    file_path = args.file
    code = load_code(file_path)

    language = get_language(file_path, code)
    if not language:
        print("❌ Unable to detect the programming language of this file.")
        exit(1)

    findings = scan_code(code, language)
    print_results(findings)

    format_choice = prompt_export_settings()
    saved = save_report(findings, format_choice)
    if saved:
        print(f"\n📁 Report saved to: {saved}")


if __name__ == "__main__":
    main()
