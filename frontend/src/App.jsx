import React, { useState } from "react";
import axios from "axios";
import Sidebar from "./components/Sidebar.jsx";
import ChatWindow from "./components/ChatWindow.jsx";
import "./App.css";

// Use .env value, fallback to localhost:8000
const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

function App() {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  // -----------------------------
  // Upload a file
  // -----------------------------
  const handleUpload = async (file) => {
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post(`${API_BASE}/upload`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      alert(res.data.message);
    } catch (err) {
      console.error(err);
      alert("⚠️ Upload failed – is the backend running?");
    }
  };

  // -----------------------------
  // Ask a question
  // -----------------------------
  const handleAsk = async (question, topK) => {
    if (!question.trim()) return;

    // Add user message
    setMessages((prev) => [...prev, { role: "user", text: question }]);
    setLoading(true);

    try {
      const formData = new FormData();
      formData.append("question", question);
      formData.append("top_k", topK);

      const res = await axios.post(`${API_BASE}/ask`, formData);

      const answer = res.data.answer || "No answer returned";
      const contexts = res.data.contexts || [];

      // Add assistant message
      setMessages((prev) => [
        ...prev,
        { role: "assistant", text: answer, contexts },
      ]);
    } catch (err) {
      console.error(err);
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text: "⚠️ Error contacting backend. Please try again.",
          contexts: [],
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <Sidebar onUpload={handleUpload} onAsk={handleAsk} loading={loading} />
      <ChatWindow messages={messages} />
    </div>
  );
}

export default App;
