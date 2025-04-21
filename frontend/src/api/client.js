// File: client.js

/**
 * Description:
 * This module creates and configures a secure, resilient Axios HTTP client for communicating with the Nuvai backend.
 * It includes centralized error handling, request/response logging, and built-in support for future authentication tokens.
 * This client is used by all frontend API modules to ensure consistency, observability, and traceability.
 *
 * Security & Monitoring Enhancements:
 * - Base URL set for API calls to prevent URL manipulation
 * - Token placeholder for future JWT authentication (ISO/IEC 27001 readiness)
 * - Request/Response interceptors for logging and debugging
 * - Centralized error catcher to display helpful feedback and log diagnostics
 * - Easy to plug into error reporting services (e.g. Sentry, LogRocket, ELK)
 * - Logs request duration and allows monitoring usage for future analytics
 *
 * Built for scale, monitoring, and secure API communication.
 */

import axios from "axios";

const BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:5000";

const client = axios.create({
  baseURL: BASE_URL,
  timeout: 10000,
  headers: {
    "Content-Type": "multipart/form-data",
    Accept: "application/json",
    // "Authorization": `Bearer ${token}` // 🔒 Optional: insert token dynamically here
  },
});

// ⏱️ Request Interceptor – Add token, audit hooks, timing
client.interceptors.request.use(
  (config) => {
    config.metadata = { startTime: new Date() };

    console.info(`[REQUEST] ${config.method?.toUpperCase()} ${config.url}`, {
      time: config.metadata.startTime.toISOString(),
      headers: config.headers,
    });

    return config;
  },
  (error) => {
    console.error("🚨 Request Error:", error);
    return Promise.reject(error);
  }
);

// ✅ Response Interceptor – Audit + Error Handler
client.interceptors.response.use(
  (response) => {
    const duration = new Date() - response.config.metadata.startTime;
    console.info(`[RESPONSE] ${response.status} from ${response.config.url} in ${duration}ms`, {
      data: response.data,
    });

    // Optional: Log to analytics/auditing platforms here
    // auditLog("http_response", {
    //   path: response.config.url,
    //   duration,
    //   findingsCount: response.data?.length || 0,
    // });

    return response;
  },
  (error) => {
    const status = error.response?.status || "NO_RESPONSE";
    const message = error.response?.data?.error || error.message;
    console.warn(`[RESPONSE ERROR] ${status}`, {
      path: error.config?.url,
      message,
    });

    // 🔍 Optional: Sentry.captureException(error) or reportError(error)

    return Promise.reject({ status, message });
  }
);

export default client;