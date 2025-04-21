// File: api/scan.js

/**
 * Description:
 * This module provides a clean abstraction over the scan API.
 * It uses the centralized client (with logging, error handling, and future auth) to send code files
 * to the backend and receive structured vulnerability findings.

 * Highlights:
 * - Handles file upload using FormData
 * - Returns raw findings or throws detailed error
 * - Easily extendable for scan options, user metadata, or future authentication
 * - Logs success/failure via `client` hooks (auditable)

 * Safe to use in frontend apps or admin dashboards.
 */

import client from "./client";

export const submitFileForScan = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await client.post("/scan", formData);
    return response.data;
  } catch (error) {
    console.error("❌ Scan API failed:", error.message || error);
    throw new Error(error.message || "Unknown scan error");
  }
};
