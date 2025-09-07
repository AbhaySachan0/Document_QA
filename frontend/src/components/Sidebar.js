import React, { useState } from "react";

function Sidebar({ onUpload, onAsk, loading }) {
  const [file, setFile] = useState(null);
  const [question, setQuestion] = useState("");
  const [topK, setTopK] = useState(5);

  const handleUploadClick = () => {
    if (file) onUpload(file);
  };

  const handleAskClick = () => {
    if (question.trim()) {
      onAsk(question, topK);
      setQuestion("");
    }
  };

  return (
    <div className="sidebar">
      <h2>📂 Document Q&A</h2>
      <div className="upload-section">
        <input type="file" onChange={(e) => setFile(e.target.files[0])} />
        <button onClick={handleUploadClick}>Upload</button>
      </div>

      <div className="ask-section">
        <textarea
          placeholder="Ask a question..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
        />
        <div className="controls">
          <label>Top K:</label>
          <input
            type="number"
            min="1"
            max="10"
            value={topK}
            onChange={(e) => setTopK(e.target.value)}
          />
          <button onClick={handleAskClick} disabled={loading}>
            {loading ? "Thinking..." : "Ask"}
          </button>
        </div>
      </div>
    </div>
  );
}

export default Sidebar;
