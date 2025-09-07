import React from "react";

function MessageCard({ role, text, contexts }) {
  return (
    <div className={`message-card ${role}`}>
      <p>{text}</p>
      {contexts && (
        <div className="contexts">
          <h5>Sources:</h5>
          <ul>
            {contexts.map((c, idx) => (
              <li key={idx}>
                {c.source} (chunk {c.chunk_id}, score {c.score.toFixed(2)})
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default MessageCard;
