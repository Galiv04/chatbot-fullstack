Start-Process powershell -ArgumentList 'ollama run llama3:8b'
Start-Process powershell -ArgumentList 'cd backend; .venv\Scripts\activate; uvicorn app.main:app --reload'
Start-Process powershell -ArgumentList 'cd frontend; npm run dev'
