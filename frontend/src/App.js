import React, { useState } from "react";
import axios from "axios";
import Sidebar from "./components/Sidebar";
import ChatWindow from "./components/ChatWindow";
import "./App.css";

function App() {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleUpload = async (file) => {
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post("http://localhost:8000/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      alert(res.data.message);
    } catch (err) {
      console.error(err);
      alert("Upload failed");
    }
  };

  const handleAsk = async (question, topK) => {
    setMessages((prev) => [...prev, { role: "user", text: question }]);
    setLoading(true);

    try {
      const formData = new FormData();
      formData.append("question", question);
      formData.append("top_k", topK);

      const res = await axios.post("http://localhost:8000/ask", formData);
      const answer = res.data.answer;
      const contexts = res.data.contexts;

      setMessages((prev) => [
        ...prev,
        { role: "assistant", text: answer, contexts },
      ]);
    } catch (err) {
      console.error(err);
      alert("Error getting answer");
    }
    setLoading(false);
  };

  return (
    <div className="app-container">
      <Sidebar onUpload={handleUpload} onAsk={handleAsk} loading={loading} />
      <ChatWindow messages={messages} />
    </div>
  );
}

export default App;
