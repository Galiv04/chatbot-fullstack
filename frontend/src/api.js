import axios from "axios";
const API_URL = "http://localhost:8000";

export function createChat() {
  return axios.post(`${API_URL}/chats/`).then(res => res.data);
}

export function getChats() {
  return axios.get(`${API_URL}/chats/`).then(res => res.data);
}

export function getMessages(chatId) {
  return axios.get(`${API_URL}/chats/${chatId}/messages`).then(res => res.data);
}

// -- New: Send user message and get bot reply --
export function sendMessageAndGetResponse(chatId, user_message) {
  const formData = new FormData();
  formData.append("user_message", user_message);
  return axios.post(`${API_URL}/chats/${chatId}/message_and_response`, formData)
    .then(res => res.data);
}

export function uploadFile(file) {
  const formData = new FormData();
  formData.append("file", file);
  return axios.post(`${API_URL}/upload/`, formData)
    .then(res => res.data);
}
