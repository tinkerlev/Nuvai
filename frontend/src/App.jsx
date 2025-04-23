// File: App.jsx

/**
 * 📂 Description:
 * This is the central shell of the Nuvai frontend React application.
 * It handles global layout, page routing, and error isolation.
 *
 * ✅ Key Features:
 * - Uses React Router for navigation between pages like Home and Results
 * - Contains a Header and Footer that appear on all pages
 * - Loads the correct screen based on the URL path ("/", "/result", etc.)
 * - Wraps the entire app with an <ErrorBoundary> to prevent app crashes
 * - Logs when the app is loaded (useful for developers & analytics)
 *
 * 🛡️ Security & Compliance:
 * - Built according to ISO/IEC 27001: secure layout, isolated error handling
 * - Accessible HTML structure: uses roles and ARIA for screen readers
 * - Designed for future secure session handling (e.g. AuthProvider)
 *
 * 🧠 Non-Technical Explanation:
 * This file connects the UI parts of Nuvai. When you visit a page,
 * it shows the correct content. If something breaks, the error is caught,
 * and the app doesn’t crash. It also prints useful logs for debugging.
 */

import { useEffect } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

// Pages
import Home from "./pages/Home";
import ScanResult from "./pages/ScanResult";
import NotFound from "./pages/NotFound";
import Forbidden from "./pages/Forbidden"; 


// Layout
import Header from "./components/Header";
import Footer from "./components/Footer";

// Error handling
import ErrorBoundary from "./components/ErrorBoundary";
// import { AuthProvider } from "./auth/AuthContext"; // For future secure sessions

function App() {
  // Log once when app loads
  useEffect(() => {
    console.info("✅ Nuvai React App successfully loaded at", new Date().toISOString());
  }, []);

  return (
    // Optional Auth wrapper for future user sessions
    // <AuthProvider>
    <ErrorBoundary>
      <Router>
        <div className="min-h-screen flex flex-col bg-gray-50 text-gray-800">
          <Header />
          <main
            className="flex-grow px-4 py-6 max-w-4xl mx-auto w-full"
            role="main"
            aria-label="Main content area"
          >
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/result" element={<ScanResult />} />
              <Route path="*" element={<NotFound />} />
              <Route path="/403" element={<Forbidden />} />
              {/* 🔐 Future routes (403/401) can be added here if Flask returns errors */}
            </Routes>
          </main>
          <Footer />
        </div>
      </Router>
    </ErrorBoundary>
    // </AuthProvider>
  );
}

export default App;
