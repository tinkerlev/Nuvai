// File: src/main.jsx

/**
 * Description:
 * This is the root file that mounts the React application.
 * It wraps the App component inside React.StrictMode for highlighting potential issues,
 * and mounts it to the HTML DOM using ReactDOM.createRoot.
 *
 * Security & Reliability:
 * - Uses strict mode for highlighting legacy problems
 * - Logs critical failures gracefully
 * - ISO/IEC 27001 aligned (no unsafe side effects)
 */

import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";

try {
  const root = ReactDOM.createRoot(document.getElementById("root"));
  root.render(
    <React.StrictMode>
      <App />
    </React.StrictMode>
  );
} catch (err) {
  console.error("🚨 Failed to mount Nuvai App:", err);
  const fallback = document.createElement("div");
  fallback.innerText = "Critical failure loading app. Please refresh or contact support.";
  fallback.style.color = "red";
  fallback.style.textAlign = "center";
  fallback.style.padding = "2rem";
  document.body.appendChild(fallback);
}
