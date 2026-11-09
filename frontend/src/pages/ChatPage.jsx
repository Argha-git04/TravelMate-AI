import { useState, useRef, useEffect } from "react";
import Card from "../components/common/Card";
import Badge from "../components/common/Badge";
import Button from "../components/common/Button";

const SUGGESTIONS = [
  "What are the best places to visit in Japan in spring?",
  "Create a 3-day budget itinerary for Barcelona",
  "What vaccinations do I need for Thailand?",
  "Best time to visit Bali for surfing?",
];

export default function ChatPage() {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content:
        "Hi! I'm TravelMate AI, your personal travel assistant powered by IBM Granite. Ask me anything about destinations, itineraries, visa requirements, packing tips, or travel budgets. How can I help you today? ✈️",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async (text) => {
    const userMessage = text || input.trim();
    if (!userMessage) return;

    setInput("");
    setMessages((prev) => [...prev, { role: "user", content: userMessage }]);
    setLoading(true);

    // Phase 7: call POST /api/v1/chat/message with real Granite backend
    setTimeout(() => {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "Great question! IBM Granite chat integration will be available in Phase 7 of TravelMate-AI. This UI is fully ready to connect to the backend. 🚀",
        },
      ]);
      setLoading(false);
    }, 1000);
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      {/* Header */}
      <div className="mb-6">
        <div className="flex items-center gap-2 mb-2">
          <Badge variant="ai">🤖 IBM Granite</Badge>
          <Badge variant="live">Ready</Badge>
        </div>
        <h1 className="text-3xl font-bold text-slate-900">Travel Assistant</h1>
        <p className="text-slate-500 mt-1">
          Ask me anything about travel — destinations, budgets, tips, and more.
        </p>
      </div>

      {/* Chat window */}
      <Card padding="none" className="flex flex-col overflow-hidden" style={{ height: "500px" }}>
        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((msg, i) => (
            <div
              key={i}
              className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
            >
              {msg.role === "assistant" && (
                <div className="w-7 h-7 rounded-full bg-blue-600 flex items-center justify-center text-white text-sm mr-2 flex-shrink-0 mt-0.5">
                  ✈
                </div>
              )}
              <div
                className={`max-w-[80%] px-4 py-3 rounded-2xl text-sm leading-relaxed ${
                  msg.role === "user"
                    ? "bg-blue-600 text-white rounded-br-sm"
                    : "bg-slate-100 text-slate-800 rounded-bl-sm"
                }`}
              >
                {msg.content}
              </div>
            </div>
          ))}

          {loading && (
            <div className="flex justify-start">
              <div className="w-7 h-7 rounded-full bg-blue-600 flex items-center justify-center text-white text-sm mr-2 flex-shrink-0">
                ✈
              </div>
              <div className="bg-slate-100 px-4 py-3 rounded-2xl rounded-bl-sm">
                <div className="flex gap-1 items-center h-4">
                  <span className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
                  <span className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
                  <span className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
                </div>
              </div>
            </div>
          )}
          <div ref={bottomRef} />
        </div>

        {/* Input */}
        <div className="border-t border-slate-200 p-3">
          <div className="flex gap-2">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask about destinations, budgets, tips..."
              rows={1}
              className="flex-1 resize-none px-4 py-2.5 rounded-xl border border-slate-300 text-sm text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            <Button
              onClick={() => handleSend()}
              disabled={!input.trim() || loading}
              className="flex-shrink-0 rounded-xl"
            >
              Send
            </Button>
          </div>
        </div>
      </Card>

      {/* Suggestion chips */}
      <div className="mt-4">
        <p className="text-xs text-slate-400 mb-2">Try asking:</p>
        <div className="flex flex-wrap gap-2">
          {SUGGESTIONS.map((s) => (
            <button
              key={s}
              onClick={() => handleSend(s)}
              className="text-xs px-3 py-1.5 rounded-full bg-white border border-slate-200 text-slate-600 hover:border-blue-400 hover:text-blue-600 transition-colors"
            >
              {s}
            </button>
          ))}
        </div>
      </div>

      {/* Disclaimer */}
      <p className="mt-4 text-xs text-slate-400 text-center">
        AI responses are for planning purposes only. Prices mentioned are estimates.
      </p>
    </div>
  );
}
