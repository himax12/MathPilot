import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App.tsx";
import { ThemeProvider } from "./components/ThemeProvider";
import { GoogleOAuthProvider } from "@react-oauth/google";
import { AuthProvider } from "./context/AuthContext";

const GOOGLE_CLIENT_ID =
  (import.meta.env.VITE_GOOGLE_CLIENT_ID as string) || "";

console.log("MathPilot starting...", {
  GOOGLE_CLIENT_ID: GOOGLE_CLIENT_ID ? "SET" : "MISSING",
});

const rootElement = document.getElementById("root");
if (!rootElement) {
  console.error("Root element not found!");
  throw new Error("Root element not found");
}

console.log("Mounting React app...");

try {
  createRoot(rootElement).render(
    <StrictMode>
      <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
        <GoogleOAuthProvider clientId={GOOGLE_CLIENT_ID}>
          <AuthProvider>
            <App />
          </AuthProvider>
        </GoogleOAuthProvider>
      </ThemeProvider>
    </StrictMode>,
  );
  console.log("React app mounted successfully!");
} catch (error) {
  console.error("Failed to mount React app:", error);
  document.body.innerHTML = `
    <div style="padding: 20px; color: red; font-family: monospace;">
      <h1>MathPilot Failed to Load</h1>
      <pre>${error}</pre>
      <p>Check browser console for details.</p>
    </div>
  `;
}
