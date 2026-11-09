/**
 * Chat service — travel assistant messages via Granite backend.
 * Separate from aiService to allow independent scaling and caching.
 */
import api from "./api";

// TODO Phase 7: implement
export const sendChatMessage = (sessionId, message, history) =>
  api.post("/chat/message", { session_id: sessionId, message, history });

export const getChatSession = (sessionId) => api.get(`/chat/${sessionId}`);
