// File: src/components/Footer.jsx

/**
 * Description:
 * This component renders the footer of the Nuvai web application.
 * It provides credits, legal links, and maintains visual consistency across the app.
 *
 * Security & UX Enhancements:
 * - ISO/IEC 27001 aligned: no user tracking, no external scripts
 * - Semantic HTML for accessibility
 * - ARIA attributes for assistive technology support
 * - Responsive layout with TailwindCSS
 */

import React from "react";

const Footer = () => {
  const year = new Date().getFullYear();

  return (
    <footer className="bg-white border-t border-gray-200 text-sm text-slate-600">
      <div className="max-w-6xl mx-auto px-4 py-6 flex flex-col md:flex-row justify-between items-center gap-2 md:gap-0">
        <p className="text-center md:text-left">
          © {year} Nuvai · Built with 🛡️ by Eliran Loai Deeb
        </p>
        <nav className="flex space-x-4" aria-label="Footer navigation">
          <a
            href="https://github.com/tinkerlev/Nuvai"
            className="hover:text-blue-600 transition"
            target="_blank"
            rel="noopener noreferrer"
          >
            GitHub
          </a>
          <a
            href="mailto:elirandeeb@gmail.com"
            className="hover:text-blue-600 transition"
          >
            Contact
          </a>
          <a
            href="/privacy"
            className="hover:text-blue-600 transition"
          >
            Privacy
          </a>
        </nav>
      </div>
    </footer>
  );
};

export default Footer;
