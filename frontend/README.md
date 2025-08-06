# Frontend (React + Vite)

## Features

- Clean, responsive chat UI
- Upload files, view chat history, see bot reasoning live
- Modular components (Chat, MessageBubble, FileUpload, etc.)

---

## Setup

npm install


## Run

npm run dev

Opens http://localhost:5173


`src/api.js` configures API endpoints.  
Ensure the backend (FastAPI) is running on port 8000.

---

## Environment

- No special `.env` needed for local dev
- `node_modules/` and `dist/` are ignored from git

---

## Editing

All source lives in `src/` (see `components/` for modular UI parts).
