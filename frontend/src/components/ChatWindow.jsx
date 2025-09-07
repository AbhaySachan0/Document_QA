import React, { useState } from "react";
import MessageCard from "./MessageCard";

function ChatWindow({ messages, setMessages }) {
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    // Add user message to chat
    const newMessage = { role: "user", text: input, contexts: [] };
    setMessages((prev) => [...prev, newMessage]);

    setLoading(true);
    try {
      // Send to backend
      const res = await fetch("http://127.0.0.1:8000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: input }),
      });

      const data = await res.json();

      // Add assistant's response to chat
      const botMessage = {
        role: "assistant",
        text: data.answer || "No answer received",
        contexts: [],
      };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error(error);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", text: "⚠️ Backend request failed", contexts: [] },
      ]);
    } finally {
      setLoading(false);
      setInput("");
    }
  };

  return (
    <div className="chat-window">
      <h2>💬 Conversation</h2>

      {messages.map((msg, i) => (
        <MessageCard
          key={i}
          role={msg.role}
          text={msg.text}
          contexts={msg.contexts}
        />
      ))}

      {/* Input box */}
      <div style={{ marginTop: "1rem" }}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
          style={{ padding: "8px", width: "70%", marginRight: "8px" }}
        />
        <button onClick={sendMessage} disabled={loading}>
          {loading ? "Sending..." : "Send"}
        </button>
      </div>
    </div>
  );
}

export default ChatWindow;
