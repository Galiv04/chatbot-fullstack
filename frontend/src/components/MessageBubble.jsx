import React from "react";
import "./Chat.css";

function MessageBubble({ sender, content, loading }) {
  const isUser = sender === "user";
  return (
    <div className={`message-bubble ${isUser ? "user" : "bot"}`}>
      <span className="message-label">{isUser ? "You" : "Bot"}:</span>{" "}
      {content === "..." && loading && !isUser ? (
        <em className="message-loading">Bot is thinking...</em>
      ) : (
        content
      )}
    </div>
  );
}

export default MessageBubble;
