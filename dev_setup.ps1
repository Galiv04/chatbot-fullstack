Write-Host "=== Chatbot Fullstack Quick Setup ==="

# Backend
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python init_db.py
deactivate
cd ..

# Frontend
cd frontend
npm install
cd ..

Write-Host "`nSetup done!"
Write-Host "To start everything, use three terminals:"
Write-Host "1. ollama run llama3.1:8b"
Write-Host "2. cd backend; .venv\Scripts\activate; uvicorn app.main:app --reload"
Write-Host "3. cd frontend; npm run dev"
