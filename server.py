# File: server.py

"""
Description:
This is the Flask backend API for Nuvai, the AI-powered code vulnerability scanner.
It receives a code file via HTTP POST (from the React frontend), determines the programming language,
passes the code to the appropriate scanner, and returns the list of security findings as JSON.

The file upload is handled via the "/scan" route, and a temporary directory is used to store incoming files.

🚀 Features:
- Accepts secure file uploads from frontend
- Automatically detects code language
- Integrates with Nuvai static analysis
- Returns structured JSON response with severity, title, description, recommendation
- Deletes file after scan
- Supports CORS and .env configuration
- Enforces max file size from environment
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import uuid

from src.nuvai import get_language, scan_code

# Load .env config
load_dotenv()

UPLOAD_FOLDER = "temp_uploads"
API_PORT = int(os.getenv("API_PORT", 5000))
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173")
MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", 1048576))

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_FILE_SIZE
CORS(app, origins=ALLOWED_ORIGINS.split(","))

@app.route("/scan", methods=["POST"])
def scan_file_or_files():
    """
    Accepts one or multiple files via form-data.
    Responds with one result (dict) or a list of results (array of dicts).
    """
    if not request.files:
        return jsonify({"error": "No file(s) uploaded"}), 400

    file_items = list(request.files.items())

    # Case: Single file – return flat result
    if len(file_items) == 1:
        _, file = file_items[0]
        return scan_single_file(file)

    # Case: Multiple files – return list
    results = []
    for _, file in file_items:
        result = scan_and_return(file)
        results.append(result)
    return jsonify(results)

def scan_single_file(file):
    result = scan_and_return(file)
    return jsonify(result)

def scan_and_return(file):
    file_id = uuid.uuid4().hex
    filename = f"{file_id}_{file.filename}"
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    try:
        file.save(file_path)
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()

        language = get_language(file.filename, code)
        findings = scan_code(code, language)

        # Normalize structure to always return 'severity', 'title', 'description', 'recommendation'
        normalized_findings = []
        for item in findings:
            normalized_findings.append({
                "severity": item.get("severity") or item.get("level", "info").lower(),
                "title": item.get("title") or item.get("type", "Untitled Finding"),
                "description": item.get("description") or item.get("message", "No description provided."),
                "recommendation": item.get("recommendation", "No recommendation available.")
            })

        return {
            "filename": file.filename,
            "language": language,
            "vulnerabilities": normalized_findings
        }
    except Exception as e:
        return {
            "filename": file.filename,
            "error": str(e)
        }
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

if __name__ == "__main__":
    app.run(debug=True, port=API_PORT)
