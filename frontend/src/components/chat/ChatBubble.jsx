/** Chat bubble — single message bubble. Phase 7: implement. */
export default function ChatBubble({ role, content }) {
  const isUser = role === "user";
  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"} mb-2`}>
      <div className={`max-w-xs px-3 py-2 rounded-lg text-sm ${isUser ? "bg-blue-600 text-white" : "bg-gray-200 text-gray-800"}`}>
        {content}
      </div>
    </div>
  );
}
