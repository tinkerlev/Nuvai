// File: ResultCard.jsx

/**
 * Description:
 * A reusable, secure, and accessible React component that displays one finding (vulnerability) 
 * from the Nuvai scanner. Designed to be clear to both technical and non-technical users.
 *
 * ✨ Features:
 * - Color-coded card based on severity (CRITICAL to TIP)
 * - Safe rendering without any injected or dynamic HTML
 * - Graceful error handling with fallback UI
 * - ISO/IEC 27001-aligned: privacy-safe, minimal exposure, ARIA-compliant
 * - Used in: ScanResult.jsx and Home.jsx (UI for scan results)
 *
 * 📦 Input:
 * `finding` = {
 *    level: "CRITICAL" | "HIGH" | "MEDIUM" | "TIP" | ...,
 *    type: "XSS" | "Insecure Deserialization" | ...,
 *    message: "What the issue is",
 *    recommendation: "What to do about it"
 * }
 */

import React from "react";
import PropTypes from "prop-types";

const SEVERITY_CLASSES = {
  CRITICAL: "border-red-600 bg-red-50",
  HIGH: "border-orange-500 bg-orange-50",
  MEDIUM: "border-yellow-400 bg-yellow-50",
  WARNING: "border-blue-400 bg-blue-50",
  INFO: "border-gray-300 bg-gray-50",
  TIP: "border-emerald-400 bg-emerald-50",
  ERROR: "border-gray-500 bg-gray-100",
};

const ResultCard = ({ finding }) => {
  try {
    if (!finding || typeof finding !== "object") {
      throw new Error("Invalid finding data.");
    }

    const {
      level = "INFO",
      type = "Unknown",
      message = "No description provided.",
      recommendation = "No recommendation available.",
    } = finding;

    const severityClass = SEVERITY_CLASSES[level] || "border-slate-300 bg-white";

    return (
      <div
        className={`rounded-lg shadow-sm border-l-4 p-4 mb-4 text-slate-800 ${severityClass}`}
        role="region"
        aria-label={`${level} vulnerability: ${type}`}
      >
        <h3 className="font-semibold text-sm mb-1">
          [{level}] {type}
        </h3>
        <p className="text-sm mb-1">
          <strong>Description:</strong> {message}
        </p>
        <p className="text-sm italic text-slate-600">
          💡 <strong>Recommendation:</strong> {recommendation}
        </p>
      </div>
    );
  } catch (error) {
    console.error("⚠️ ResultCard rendering error:", error);
    return (
      <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4">
        ❌ Unable to display this result. Please check your scan output format.
      </div>
    );
  }
};

ResultCard.propTypes = {
  finding: PropTypes.shape({
    level: PropTypes.string.isRequired,
    type: PropTypes.string.isRequired,
    message: PropTypes.string.isRequired,
    recommendation: PropTypes.string.isRequired,
  }).isRequired,
};

export default ResultCard;