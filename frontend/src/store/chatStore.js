/** Zustand store for chat state. Phase 7: expand with full session state. */
import { create } from "zustand";

const useChatStore = create((set) => ({
  sessionId: null,
  messages: [],
  isLoading: false,
  error: null,

  setSessionId: (id) => set({ sessionId: id }),
  addMessage: (message) => set((state) => ({ messages: [...state.messages, message] })),
  setMessages: (messages) => set({ messages }),
  setLoading: (loading) => set({ isLoading: loading }),
  setError: (error) => set({ error }),
  clearChat: () => set({ sessionId: null, messages: [], error: null }),
}));

export default useChatStore;
