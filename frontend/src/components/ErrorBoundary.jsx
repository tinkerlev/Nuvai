// File: src/components/ErrorBoundary.jsx

/**
 * Description:
 * A secure, ISO/IEC 27001-aligned global Error Boundary for the Nuvai React app.
 * Prevents app crashes, protects internal state, and presents clear fallback UI for non-technical users.
 *
 * Security & UX Enhancements:
 * - Catches React rendering errors across app components
 * - Logs structured metadata (timestamp, user agent, error stack)
 * - Future support for external logging (e.g. Sentry, custom API)
 * - Offers accessible, user-friendly fallback with ARIA roles
 * - Contains a collapsible technical error trace for developers
 */

import React from "react";
import PropTypes from "prop-types";

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      hasError: false,
      errorSummary: null,
      errorInfo: null,
    };
  }

  static getDerivedStateFromError(error) {
    return {
      hasError: true,
      errorSummary: error?.toString() || "Unknown rendering error",
    };
  }

  componentDidCatch(error, info) {
    this.setState({ errorInfo: info });

    const logPayload = {
      type: "frontend_error",
      error: error?.message || "Unknown",
      stack: info?.componentStack || "Unavailable",
      time: new Date().toISOString(),
      userAgent: navigator?.userAgent,
    };

    console.error("📉 ErrorBoundary Log:", logPayload);

    // Optional: Send to external logger
    // fetch("/api/log-error", {
    //   method: "POST",
    //   headers: { "Content-Type": "application/json" },
    //   body: JSON.stringify(logPayload),
    // });
  }

  handleRecover = () => {
    this.setState({ hasError: false, errorSummary: null, errorInfo: null });
    window.location.href = "/";
  };

  render() {
    if (this.state.hasError) {
      return (
        <div
          className="bg-red-50 text-red-700 border border-red-300 rounded-lg p-6 mt-12 max-w-xl mx-auto text-center shadow"
          role="alert"
          aria-live="assertive"
        >
          <h2 className="text-xl font-bold mb-2">⚠️ Something went wrong</h2>
          <p className="text-sm mb-2">
            An unexpected error occurred. Please refresh the page or return to the homepage.
          </p>
          <button
            onClick={this.handleRecover}
            className="mt-3 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 transition"
          >
            🔁 Go to Homepage
          </button>

          {this.state.errorInfo && (
            <details className="mt-4 text-left text-xs text-slate-600 whitespace-pre-wrap max-h-48 overflow-y-auto">
              <summary className="cursor-pointer text-slate-500">
                Technical Details
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
