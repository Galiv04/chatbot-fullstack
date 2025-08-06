#!/bin/bash
set -e
echo "=== Chatbot Fullstack Quick Setup ==="

# Create backend venv and install deps
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python init_db.py
cd ..

# Install frontend deps
cd frontend
npm install
cd ..

echo
echo "Setup done!"
echo
echo "To start everything, you need three terminals:"
echo "1. ollama run llama3.1:8b"
echo "2. cd backend && source .venv/bin/activate && uvicorn app.main:app --reload"
echo "3. cd frontend && npm run dev"
