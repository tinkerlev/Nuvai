// File: ScanResult.jsx

/**
 * Description:
 * This component displays the results of the Nuvai security scan in a clear, professional, and accessible layout.
 * It supports sorting, color-coded severity levels, actionable tips, filtering by severity, and download functionality.
 * Designed for both technical and non-technical users.
 *
 * Security UX Highlights:
 * - Protects against rendering unsafe HTML/code
 * - Prevents leaking technical exceptions
 * - Provides security tips in plain language
 * - Built to comply with ISO/IEC 27001 UX requirements
 */

import React, { useState, useEffect } from "react";
import { motion } from "framer-motion";

const SEVERITY_COLORS = {
  CRITICAL: "bg-red-600",
  HIGH: "bg-orange-500",
  MEDIUM: "bg-yellow-400",
  WARNING: "bg-blue-400",
  INFO: "bg-gray-300",
  TIP: "bg-emerald-400",
  ERROR: "bg-gray-500",
};

const severityOrder = ["CRITICAL", "HIGH", "MEDIUM", "WARNING", "INFO", "TIP", "ERROR"];

const ScanResult = ({ findings }) => {
  const [filter, setFilter] = useState("ALL");
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!findings) {
      setError("Failed to load scan results. Please try again or contact support.");
    }
  }, [findings]);

  if (error) {
    return (
      <div className="p-4 text-center text-red-600 bg-red-100 border border-red-300 rounded-md">
        ❗ {error}
      </div>
    );
  }

  if (!findings || findings.length === 0) {
    return (
      <div className="p-4 text-center text-gray-600 italic">
        No results to display. Please upload and scan a file to see findings.
      </div>
    );
  }

  const filtered =
    filter === "ALL" ? findings : findings.filter((f) => f.level === filter);

  const sorted = [...filtered].sort(
    (a, b) => severityOrder.indexOf(a.level) - severityOrder.indexOf(b.level)
  );

  const handleDownload = () => {
    try {
      const blob = new Blob([JSON.stringify(findings, null, 2)], {
        type: "application/json",
      });
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = "nuvai_scan_results.json";
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } catch (err) {
      setError("Unable to generate download file. Please try again.");
    }
  };

  const handleCopy = (text) => {
    navigator.clipboard.writeText(text).then(() => {
      alert("✅ Recommendation copied to clipboard!");
    }).catch(() => {
      alert("❌ Failed to copy recommendation.");
    });
  };

  return (
    <div className="w-full max-w-4xl mx-auto mt-4">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-bold">🔍 Scan Results</h2>
        <button
          onClick={handleDownload}
          className="bg-slate-800 text-white text-sm px-4 py-1 rounded hover:bg-slate-700"
        >
          ⬇️ Download JSON
        </button>
      </div>

      <div className="flex flex-wrap gap-2 mb-4">
        {["ALL", ...severityOrder].map((level) => (
          <button
            key={level}
            onClick={() => setFilter(level)}
            className={`px-3 py-1 rounded text-sm font-medium transition ${
              filter === level ? "bg-black text-white" : "bg-gray-200 text-black hover:bg-gray-300"
            }`}
          >
            {level}
          </button>
        ))}
      </div>

      {sorted.map((item, index) => (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: index * 0.05 }}
          key={index}
          className={`mb-4 p-4 border rounded-xl shadow-sm ${
            SEVERITY_COLORS[item.level] || "bg-white"
          } text-black`}
        >
          <h3 className="text-lg font-semibold">
            [{item.level}] {item.type}
          </h3>
          <p className="mt-1 text-sm">
            <strong>Description:</strong> {item.message}
          </p>
          <p className="mt-1 text-sm">
            <strong>Recommendation:</strong> {item.recommendation}
          </p>
          <button
            onClick={() => handleCopy(item.recommendation)}
            className="mt-2 text-xs underline text-blue-900 hover:text-blue-700"
          >
            📋 Copy recommendation
          </button>
        </motion.div>
      ))}
    </div>
  );
};

export default ScanResult;
