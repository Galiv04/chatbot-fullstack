import React, { useState, useEffect, useRef } from "react";
import { getMessages, sendMessageAndGetResponse } from "../api";
import MessageBubble from "./MessageBubble";
import "./Chat.css";

function Chat({ chatId }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const chatRef = useRef();

  useEffect(() => {
    if (chatId) {
      getMessages(chatId).then(setMessages);
    }
  }, [chatId]);

  useEffect(() => {
    chatRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  async function handleSend(e) {
    e.preventDefault();
    const userText = input.trim();
    if (!userText) return;
    setInput("");
    setMessages(msgs => [...msgs, { sender: "user", content: userText }]);
    setLoading(true);
    setMessages(msgs => [...msgs, { sender: "bot", content: "..." }]);
    try {
      const resp = await sendMessageAndGetResponse(chatId, userText);
      setMessages(msgs =>
        msgs.slice(0, -1).concat({ sender: "bot", content: resp.response })
      );
    } catch {
      setMessages(msgs =>
        msgs.slice(0, -1).concat({ sender: "bot", content: "Sorry, error!" })
      );
    }
    setLoading(false);
  }

  return (
    <div className="chat-container">
      <div className="messages-box">
        {messages.map((m, i) => (
          <MessageBubble
            key={i}
            sender={m.sender}
            content={m.content}
            loading={loading}
          />
        ))}
        <div ref={chatRef}></div>
      </div>
      <form className="chat-form" onSubmit={handleSend}>
        <input
          className="chat-input"
          value={input}
          onChange={e => setInput(e.target.value)}
          disabled={loading}
          placeholder="Type your message..."
        />
        <button type="submit" disabled={loading || !input.trim()}>Send</button>
      </form>
    </div>
  );
}

export default Chat;
