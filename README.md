# Chatbot Fullstack

A full-stack RAG chatbot that lets you upload PDFs/text files and chat with a local LLM (Ollama).  
Built with **FastAPI** (backend), **React + Vite** (frontend), and Ollama for private, local inference.

---

## Features

- Upload PDFs/text files for custom knowledge base Q&A
- FastAPI backend with clean REST API, SQLite (swappable to Postgres)
- React SPA frontend (modern, modular UI)
- Ollama LLM for chat and document embeddings (runs locally)
- Easy local development & onboarding

---

## Quick Start (After Cloning)

### 1. Clone the repo

    
    git clone https://github.com/Galiv04/chatbot-fullstack.git
    cd chatbot-fullstack
    

### 2. Project Setup Scripts

**You can use one of these scripts for one-shot setup:**

#### On Unix/macOS/Git Bash/WSL

- First, make setup scripts executable (run this once per script):

    ```
    chmod +x dev_setup.sh
    chmod +x dev_tmux.sh   # If you want to use the tmux terminal launcher
    ```

- Then run the quick setup:

    ```
    ./dev_setup.sh
    ```

#### On Windows PowerShell

- Run the PowerShell setup script:

    ```
    .\dev_setup.ps1
    ```

---

### 3. Running the Development Servers

After setup, you need **three terminals** (or use the launcher scripts—see below):

#### (A) Start Ollama LLM model

    ollama run llama3.1:8b

*(Alternatively, use another supported model as configured in your backend)*

#### (B) Start the backend (FastAPI)
    cd backend
    source .venv/bin/activate # (On Windows: .venv\Scripts\activate)
    uvicorn app.main:app --reload

#### (C) Start the frontend (React)

    cd frontend
    npm run dev

Then access http://localhost:5173 in your browser.

---

## Terminal Launch Scripts (Optional for Convenience)

You may use these provided scripts to open all required terminals automatically:

### On Unix/macOS/Linux (with **tmux** installed)

- **First, make the script executable:**

    ```
    chmod +x dev_tmux.sh
    ```

- **Then run:**

    ```
    ./dev_tmux.sh
    ```

This will open three panes/tabs in tmux for Ollama, backend, and frontend servers.

---

### On Windows

- Use the provided PowerShell script to open all servers in new windows:

    ```
    .\dev_launcher.ps1
    ```

This will open three new terminal windows: one for Ollama LLM, one for the backend server, and one for the frontend UI.

---

## Scripts Summary Table

| Script             | Platform         | Purpose                                | How to Use                                          |
|--------------------|------------------|----------------------------------------|-----------------------------------------------------|
| dev_setup.sh       | Unix/macOS/WSL   | One-time setup of backend/frontend     | `chmod +x dev_setup.sh` then `./dev_setup.sh`       |
| dev_tmux.sh        | Unix/macOS/WSL   | Launch all servers in tmux panes       | `chmod +x dev_tmux.sh` then `./dev_tmux.sh`         |
| dev_setup.ps1      | Windows PowerShell| One-time setup of backend/frontend     | `.\dev_setup.ps1`                                   |
| dev_launcher.ps1   | Windows PowerShell| Launch all servers in separate consoles| `.\dev_launcher.ps1`                                |

---

## Directory Structure

    chatbot-fullstack/
    ├── backend/
    │ ├── app/
    │ │ ├── main.py
    │ │ ├── chatbot.py
    │ │ ├── document_loader.py
    │ │ └── ... # (Other backend code files)
    │ ├── requirements.txt
    │ ├── .venv/ # (Python virtual environment)
    │ ├── vector_db/ # (ChromaDB / vector database)
    │ └── uploads/ # (Uploaded PDFs/texts)
    ├── frontend/
    │ ├── src/
    │ │ ├── components/
    │ │ │ ├── Chat.jsx
    │ │ │ ├── MessageBubble.jsx
    │ │ │ └── ... # (Other React component files)
    │ │ ├── api.js
    │ │ ├── App.jsx
    │ │ └── ...
    │ ├── package.json
    │ ├── node_modules/
    │ └── dist/ # (Frontend build output)
    ├── .gitignore
    ├── README.md # (Project documentation)
    ├── dev_setup.sh # (Unix/macOS quick setup script)
    ├── dev_setup.ps1 # (Windows PowerShell setup script)
    ├── dev_tmux.sh # (tmux multi-terminal starter, Unix)
    └── dev_launcher.ps1 # (Windows PowerShell multi-terminal starter)


---

## More Information

- [backend/README.md](backend/README.md) for API/dev setup
- [frontend/README.md](frontend/README.md) for UI/dev setup

---

> **Tip:**  
> For any shell script (.sh) on Unix/macOS, make it executable with `chmod +x scriptname.sh` before running `./scriptname.sh`.

If you have questions or hit snags during setup, check the scripts or reach out!
