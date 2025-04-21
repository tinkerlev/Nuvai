// File: Home.jsx

/**
 * Description:
 * This is the main landing page for the Nuvai frontend interface.
 * It allows users to upload a code file, trigger a scan using the Flask API backend,
 * and receive structured, real-time vulnerability results.
 *
 * Security & UX Enhancements:
 * - TailwindCSS for modern, accessible design
 * - Framer Motion for smooth visual transitions
 * - ISO/IEC 27001 aligned UX: input validation, user feedback, minimal exposure
 * - Advanced client-side validation: file type, size, and format
 * - Delegates rendering to ScanResult component for consistent, secure display
 */

import { useState } from "react";
import axios from "axios";
import ScanResult from "./ScanResult";
import { motion } from "framer-motion";

export default function Home() {
  const [file, setFile] = useState(null);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const allowedExtensions = [".py", ".js", ".jsx", ".html", ".php", ".ts", ".cpp"];

  const handleFileChange = (e) => {
    const selected = e.target.files[0];
    const ext = selected?.name.substring(selected.name.lastIndexOf("."));
    const isAllowed = allowedExtensions.includes(ext);

    if (!selected) {
      setError("Please select a file.");
    } else if (selected.size > 1024 * 1000) {
      setError("❌ File too large. Max size is 1MB.");
    } else if (!isAllowed) {
      setError("❌ Unsupported file format.");
    } else {
      setFile(selected);
      setError(null);
    }
  };

  const handleSubmit = async () => {
    if (!file) {
      setError("❌ Please select a file first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);
      setError(null);
      const res = await axios.post("http://localhost:5000/scan", formData);
      setResults(res.data);
    } catch (err) {
      if (err.response) {
        setError(`Server error (${err.response.status}): ${err.response.data.error || "Unknown error."}`);
      } else {
        setError("Network error. Please check your connection.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-100 to-slate-300 p-8">
      <div className="max-w-3xl mx-auto bg-white rounded-2xl shadow-xl p-8 border border-gray-200">
        <motion.h1 initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} className="text-3xl font-bold text-gray-800 mb-4">
          🔎 Scan Your Code with Nuvai
        </motion.h1>

        <p className="text-gray-600 mb-6">
          Upload your code file. Nuvai will analyze it using AI-enhanced static analysis to detect vulnerabilities.
        </p>

        <input
          type="file"
          onChange={handleFileChange}
          accept={allowedExtensions.join(",")}
          className="block w-full text-sm text-slate-500 file:mr-4 file:py-2 file:px-4
            file:rounded-full file:border-0
            file:text-sm file:font-semibold
            file:bg-blue-50 file:text-blue-700
            hover:file:bg-blue-100 mb-4"
        />

        {error && <p className="text-red-500 mb-3 font-medium">{error}</p>}

        <button
          onClick={handleSubmit}
          disabled={loading}
          className="bg-blue-600 text-white px-6 py-2 rounded-lg shadow hover:bg-blue-700 transition"
        >
          {loading ? "Scanning..." : "Start Scan"}
        </button>

        {results.length > 0 && (
          <div className="mt-8">
            <ScanResult findings={results} />
          </div>
        )}
      </div>
    </div>
  );
}
