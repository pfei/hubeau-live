import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import * as Sentry from "@sentry/react";
import "./index.css";
import App from "./App";

const dsn = import.meta.env.VITE_SENTRY_DSN as string | undefined;

if (dsn) {
  Sentry.init({
    dsn,
    tunnel: "/sentry-tunnel",
    environment: import.meta.env.MODE,
    integrations: [Sentry.browserTracingIntegration()],
    tracesSampleRate: 0.2,
    sendDefaultPii: false,
  });
}

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
