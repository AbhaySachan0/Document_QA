import React from "react";
import MessageCard from "./MessageCard";

function ChatWindow({ messages }) {
  return (
    <div className="chat-window">
      <h2>💬 Conversation</h2>
      {messages.map((msg, i) => (
        <MessageCard key={i} role={msg.role} text={msg.text} contexts={msg.contexts} />
      ))}
    </div>
  );
}

export default ChatWindow;
