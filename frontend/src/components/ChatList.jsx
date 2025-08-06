import React from "react";
function ChatList({ chats, onSelect, onCreate, activeId }) {
  return (
    <div style={{ marginBottom: 20 }}>
      <div>
        <button onClick={onCreate}>+ New Chat</button>
      </div>
      <ul>
        {chats.map(chat => (
          <li
            style={{ cursor: "pointer", fontWeight: chat.id === activeId ? "bold" : "normal" }}
            key={chat.id}
            onClick={() => onSelect(chat.id)}
          >
            {chat.title || `Chat #${chat.id}`}
          </li>
        ))}
      </ul>
    </div>
  );
}
export default ChatList;
