# Backend (FastAPI)

## Features

- REST endpoints for chat, messages, file upload, and RAG
- Local SQLite DB (easy swap for Postgres)
- Uses Ollama LLM for both chat and document embeddings
- Clean modular code for developers

---

## Setup

python -m venv .venv
source .venv/bin/activate # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
python init_db.py # Creates tables (run once)

## Running the Backend

uvicorn app.main:app --reload

Server listens on http://localhost:8000

**Ollama** must be running, and its embedding/chatbot models must be pulled.  
Example:
ollama run llama3:8b

- Change model as needed (see chatbot.py).

---

## Environment

- `.env` for overrides/secrets (never committed)
- All vector and uploads data is kept local for privacy

---

## API Reference

- `POST /chats/`          Create new chat
- `GET /chats/`           List all chats
- `POST /upload/`         Upload document (PDF/TXT)
- `POST /chats/{id}/message_and_response`  Send a message and receive bot's reply

See `app/main.py` for more details.

