/**
 * Axios instance — pre-configured with the backend base URL.
 *
 * VITE_API_BASE_URL is read from the environment:
 *   Local dev:   set in frontend/.env
 *   Production:  set in Vercel dashboard → Environment Variables
 *
 * IBM credentials are NEVER stored here. The frontend only calls
 * your own backend (Render). The backend calls IBM services.
 */
import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1",
  timeout: 60000,       // 60 s — AI endpoints can take time
  headers: {
    "Content-Type": "application/json",
  },
});

export default api;
