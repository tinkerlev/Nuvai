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
- Returns structured JSON response
- Deletes file after scan
- Supports CORS and .env configuration
- Enforces max file size from environment

"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

from src.nuvai import get_language, scan_code

# Load environment variables
load_dotenv()

# Constants
UPLOAD_FOLDER = "temp_uploads"
API_PORT = int(os.getenv("API_PORT", 5000))
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000")
MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", 1048576))  # Default: 1MB

# Prepare environment
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# App setup
app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_FILE_SIZE
CORS(app, origins=ALLOWED_ORIGINS.split(","))

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
    app.run(debug=True, port=API_PORT)