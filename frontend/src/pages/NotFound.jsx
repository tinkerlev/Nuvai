// File: NotFound.jsx

/**
 * Description:
 * This component displays a graceful and branded 404 error page when a user navigates to an unknown route.
 * It preserves the application’s professionalism, helps with user orientation, and encourages secure interaction.

 * UX & Security Highlights:
 * - Minimal data exposure (no internal routing hints)
 * - Clear feedback with a way back to safety
 * - ISO/IEC 27001 aligned: controlled failure handling
 * - Built with TailwindCSS for responsive and accessible UI
 * - Includes ARIA and semantic tags for screen readers
 */

import React from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";

const NotFound = () => {
  return (
    <div className="flex flex-col items-center justify-center h-full text-center p-8">
      <motion.h1
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.4 }}
        className="text-5xl font-extrabold text-slate-800 mb-4"
        aria-label="Page not found"
      >
        404 – Not Found
      </motion.h1>

      <p className="text-gray-600 text-lg mb-6 max-w-xl">
        Oops! The page you're looking for doesn't exist, was moved, or never existed.
      </p>

      <Link
        to="/"
        className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg shadow transition"
      >
        🔙 Back to Home
      </Link>
    </div>
  );
};

export default NotFound;
