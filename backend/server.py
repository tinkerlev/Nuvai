# File: server.py

"""
Description:
This is the Flask backend API for Nuvai, the AI-powered code vulnerability scanner.
It receives a code file via HTTP POST (from the React frontend), determines the programming language,
passes the code to the appropriate scanner, and returns the list of security findings as JSON.

The file upload is handled via the "/scan" route, and a temporary directory is used to store incoming files.
This backend is designed to be cross-platform, lightweight, and easy to integrate with various frontends.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from src.nuvai import get_language, scan_code

app = Flask(__name__)
CORS(app)  # Enable cross-origin requests from React frontend

UPLOAD_FOLDER = "temp_uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure the folder exists

@app.route("/scan", methods=["POST"])
def scan_file():
    """
    Endpoint: /scan
    Method: POST
    Accepts a single code file upload via form-data.
    Determines language, scans with Nuvai, and returns JSON results.
    """
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()
        language = get_language(file.filename)
        findings = scan_code(code, language)
        return jsonify(findings)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)  # Clean up uploaded file after scanning

if __name__ == "__main__":
    app.run(debug=True, port=5000)  # Run development server on port 5000
