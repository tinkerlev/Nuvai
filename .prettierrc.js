{
  // ───────────────────────────────────────────────────────────────
  // Prettier – Automatic Code Formatter for Consistent Styling
  //
  // 🛡️ Purpose:
  // This configuration ensures a consistent and clean code style
  // across the entire project. It's used by all developers and
  // automated CI tools to reduce bugs and misunderstandings.
  //
  // ✅ Supports ISO/IEC 27001 by:
  // - Enforcing code readability and traceability
  // - Preventing ambiguity in code collaboration
  // - Supporting auditable development practices
  //
  // 👥 For non-developers:
  // This file automatically formats the code to look professional.
  // It doesn't change logic – only how the code looks (spacing, commas, etc.).
  // ───────────────────────────────────────────────────────────────

  "printWidth": 100,            // Wrap lines longer than 100 characters for better readability
  "tabWidth": 2,                // Use 2 spaces per indentation level
  "useTabs": false,             // Use spaces, not tabs (ensures alignment in all editors)
  "semi": true,                 // Always end statements with semicolons
  "singleQuote": true,          // Use single quotes for strings (standard in many JS/React teams)
  "quoteProps": "as-needed",    // Only quote object properties when necessary
  "jsxSingleQuote": false,      // Use double quotes in JSX (for clarity in HTML-like syntax)
  "trailingComma": "es5",       // Add trailing commas in objects/arrays (improves diffs)
  "bracketSpacing": true,       // Add spaces inside object braces: { foo: bar }
  "bracketSameLine": false,     // Put the closing > of multi-line JSX elements on a new line
  "arrowParens": "always",      // Always include parentheses in arrow functions: (x) => x
  "proseWrap": "preserve",      // Don't reformat markdown/text content automatically
  "endOfLine": "lf"             // Use LF for all line endings (recommended for Linux/WSL environments)
}
