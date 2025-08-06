import React, { useEffect, useState } from "react";
import { createChat, getChats } from "./api";
import Chat from "./components/Chat";
import ChatList from "./components/ChatList";
import FileUpload from "./components/FileUpload";

function App() {
  const [chats, setChats] = useState([]);
  const [active, setActive] = useState(null);

  useEffect(() => { getChats().then(setChats); }, []);
  useEffect(() => {
    if (chats.length && !active) setActive(chats[chats.length - 1].id);
  }, [chats, active]);

  const handleCreate = async () => {
    const newChat = await createChat();
    setChats([...chats, newChat]);
    setActive(newChat.id);
  };

  return (
    <div style={{ margin: 20, maxWidth: 800 }}>
      <h1>AI Chatbot</h1>
      <FileUpload />
      <ChatList
        chats={chats}
        onSelect={setActive}
        onCreate={handleCreate}
        activeId={active}
      />
      {active && <Chat chatId={active} />}
    </div>
  );
}
export default App;
