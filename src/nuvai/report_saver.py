"""
File: report_saver.py

Description:
This module is part of the Nuvai suite.
It provides a function to save security scan results in various formats:
JSON, TXT, HTML, or PDF. It creates a directory named "security_reports" in the
user's home folder (if it doesn't already exist), and saves the report file there
with a timestamp in the filename (e.g., scanner_2025-04-19_17-30-00.pdf).

Supported formats:
- json  → structured machine-readable format
- txt   → plain text for easy reading
- html  → styled document viewable in browsers
- pdf   → printable or shareable format (only if FPDF is available)

The goal is to provide users with clear, professional reporting options
and ensure seamless integration with the Nuvai code auditing workflow.
"""

import os
from datetime import datetime

# Try to import FPDF
PDF_AVAILABLE = True
try:
    from fpdf import FPDF
except ImportError:
    PDF_AVAILABLE = False

def ensure_report_directory():
    home = os.path.expanduser("~")
    report_dir = os.path.join(home, "security_reports")
    os.makedirs(report_dir, exist_ok=True)
    return report_dir

def generate_filename(extension: str):
    date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return f"scanner_{date_str}.{extension}"

def save_report(findings, extension):
    report_dir = ensure_report_directory()
    filename = generate_filename(extension)
    full_path = os.path.join(report_dir, filename)

    if extension == "json":
        import json
        with open(full_path, "w", encoding="utf-8") as f:
            json.dump(findings, f, indent=4, ensure_ascii=False)

    elif extension == "txt":
        with open(full_path, "w", encoding="utf-8") as f:
            for fnd in findings:
                f.write(f"[{fnd['level']}] {fnd['type']}\n")
                f.write(f"- Description: {fnd['message']}\n")
                f.write(f"- Recommendation: {fnd['recommendation']}\n\n")

    elif extension == "html":
        with open(full_path, "w", encoding="utf-8") as f:
            f.write("<html><head><meta charset='UTF-8'><title>Nuvai Scan Report</title></head><body>")
            f.write("<h1>Security Scan Report - Nuvai</h1>")
            for fnd in findings:
                f.write(f"<h2>[{fnd['level']}] {fnd['type']}</h2>")
                f.write(f"<p><strong>Description:</strong> {fnd['message']}</p>")
                f.write(f"<p><strong>Recommendation:</strong> {fnd['recommendation']}</p><hr>")
            f.write("</body></html>")

    elif extension == "pdf":
        if not PDF_AVAILABLE:
            print("⚠️ PDF export not available. Please install 'fpdf' to enable PDF reports.")
            return None

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Nuvai Security Scan Report", ln=True, align="C")
        for fnd in findings:
            pdf.set_font("Arial", "B", 12)
            pdf.cell(200, 10, txt=f"[{fnd['level']}] {fnd['type']}", ln=True)
            pdf.set_font("Arial", size=11)
            pdf.multi_cell(0, 10, txt=f"Description: {fnd['message']}")
            pdf.multi_cell(0, 10, txt=f"Recommendation: {fnd['recommendation']}")
            pdf.ln()
        pdf.output(full_path)

    else:
        print(f"❌ Unsupported format: {extension}")
        return None

    return full_path