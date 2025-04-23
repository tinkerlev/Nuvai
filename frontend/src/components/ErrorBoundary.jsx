// File: src/components/ErrorBoundary.jsx

/**
 * Description:
 * A robust, ISO/IEC 27001-aligned global Error Boundary for the Nuvai React app.
 * It catches rendering errors, protects the UI from crashing, logs the issue,
 * and shows a clear, friendly message with recovery options.
 *
 * Security & UX Enhancements:
 * - Differentiates between dev/prod environments
 * - Logs structured diagnostics (timestamp, user agent, component stack)
 * - Assigns a unique error ID (UUID) for traceability
 * - Safe error fallback UI with ARIA accessibility and developer stack trace
 * - Local storage for post-crash diagnostics
 * - Ready for backend error logging or Sentry integration
 */

import React from "react";
import PropTypes from "prop-types";
import { v4 as uuidv4 } from "uuid";

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      hasError: false,
      errorSummary: null,
      errorInfo: null,
      errorId: uuidv4(),
    };
  }

  static getDerivedStateFromError(error) {
    return {
      hasError: true,
      errorSummary: error?.toString() || "Unknown rendering error",
    };
  }

  componentDidCatch(error, info) {
    const payload = {
      type: "frontend_render_error",
      id: this.state.errorId,
      error: error?.message || "Unknown error",
      stack: info?.componentStack || "No component stack",
      timestamp: new Date().toISOString(),
      userAgent: navigator?.userAgent,
      path: window.location.pathname,
    };

    console.error("📉 Nuvai ErrorBoundary Log:", payload);

    // Store locally for potential export/logging
    localStorage.setItem("nuvai_last_error", JSON.stringify(payload));

    // 🔒 Optional: Send to backend or bug tracking
    const isDev = import.meta.env.MODE === "development";
    const endpoint = import.meta.env.VITE_ERROR_ENDPOINT || null;

    if (!isDev && endpoint) {
      fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      }).then(() => {
        console.info("📤 Error report sent to server.");
      }).catch((err) => {
        console.warn("⚠️ Failed to send error report:", err);
      });
    }
  }

  handleRecover = () => {
    this.setState({ hasError: false, errorSummary: null, errorInfo: null });
    window.location.href = "/";
  };

  render() {
    if (this.state.hasError) {
      return (
        <div
          className="bg-red-50 text-red-800 border border-red-300 rounded-xl p-6 mt-12 max-w-xl mx-auto text-center shadow-lg"
          role="alert"
          aria-live="assertive"
        >
          <h2 className="text-xl font-bold mb-2">⚠️ Unexpected Error</h2>
          <p className="text-sm mb-2">
            Something went wrong. Our system has recorded the issue to help improve Nuvai’s stability.
          </p>
          <p className="text-xs text-slate-500">
            Error ID: <code>{this.state.errorId}</code>
          </p>
          <button
            onClick={this.handleRecover}
            className="mt-4 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 transition"
          >
            🔁 Return to Homepage
          </button>

          {import.meta.env.MODE === "development" && this.state.errorInfo && (
            <details className="mt-4 text-left text-xs text-slate-600 whitespace-pre-wrap max-h-48 overflow-y-auto">
              <summary className="cursor-pointer text-slate-500">
                Developer Stack Trace
              </summary>
              {this.state.errorInfo.componentStack}
            </details>
          )}
        </div>
      );
    }

    return this.props.children;
  }
}

ErrorBoundary.propTypes = {
  children: PropTypes.node.isRequired,
};

export default ErrorBoundary;
