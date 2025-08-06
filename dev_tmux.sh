#!/bin/bash
tmux new-session -d -s chatbotfs 'ollama run llama3:8b'
sleep 2
tmux split-window -h 'cd backend && source .venv/bin/activate && uvicorn app.main:app --reload'
tmux split-window -v 'cd frontend && npm run dev'
tmux select-layout even-horizontal
tmux attach -t chatbotfs
