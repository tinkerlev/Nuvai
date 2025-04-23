// File: src/pages/Forbidden.jsx

/**
 * Description:
 * This component renders a secure and accessible 403 Forbidden error page.
 * It informs the user that access to the requested resource is restricted,
 * in compliance with ISO/IEC 27001 principles of least privilege and clarity.
 *
 * UX & Security Enhancements:
 * - ARIA-friendly markup
 * - Minimal exposure of internal logic
 * - Visual clarity for non-technical users
 * - Styled with TailwindCSS
 */

import React from "react";
import { Link } from "react-router-dom";

const Forbidden = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-red-50 p-8">
      <div className="max-w-md text-center">
        <h1 className="text-6xl font-extrabold text-red-600 mb-4">403</h1>
        <h2 className="text-2xl font-semibold text-gray-800 mb-2">Access Forbidden</h2>
        <p className="text-gray-600 mb-6">
          Sorry, you don’t have permission to access this page.
          Please contact your administrator or return to a safe area.
        </p>
        <Link
          to="/"
          className="inline-block bg-red-600 hover:bg-red-700 text-white px-6 py-2 rounded-md transition"
        >
          Go Back Home
        </Link>
      </div>
    </div>
  );
};

export default Forbidden;
