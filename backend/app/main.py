from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import logging
import os
from datetime import datetime

from .db import SessionLocal
from . import crud, models, chatbot
from .document_loader import add_documents_to_vectorstore, create_or_load_vectorstore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Or your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/chats/", response_model=dict)
def create_new_chat(db: Session = Depends(get_db)):
    chat = crud.create_chat(db)
    return {"id": chat.id, "title": chat.title, "created_at": str(chat.created_at)}

@app.get("/chats/", response_model=List[dict])
def get_all_chats(db: Session = Depends(get_db)):
    chats = crud.get_chats(db)
    return [{"id": chat.id, "title": chat.title, "created_at": str(chat.created_at)} for chat in chats]

@app.get("/chats/{chat_id}", response_model=dict)
def get_chat(chat_id: int, db: Session = Depends(get_db)):
    chat = crud.get_chat(db, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return {"id": chat.id, "title": chat.title, "created_at": str(chat.created_at)}

@app.delete("/chats/{chat_id}")
def delete_chat(chat_id: int, db: Session = Depends(get_db)):
    chat = crud.get_chat(db, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    db.delete(chat)
    db.commit()
    return {"detail": "Chat deleted"}

@app.get("/chats/{chat_id}/messages", response_model=List[dict])
def get_chat_messages(chat_id: int, db: Session = Depends(get_db)):
    msgs = crud.get_messages(db, chat_id)
    return [
        {
            "id": m.id,
            "sender": m.sender,
            "content": m.content,
            "timestamp": str(m.timestamp)
        } for m in msgs
    ]

@app.post("/chats/{chat_id}/messages", response_model=dict)
async def post_message(
    chat_id: int,
    sender: str = Form(...),
    content: str = Form(...),
    db: Session = Depends(get_db)
):
    msg = crud.add_message(db, chat_id, sender, content)
    return {
        "id": msg.id,
        "sender": msg.sender,
        "content": msg.content,
        "timestamp": str(msg.timestamp)
    }

@app.post("/chats/{chat_id}/message_and_response", response_model=dict)
async def message_and_response(
    chat_id: int,
    user_message: str = Form(...),
    db: Session = Depends(get_db)
):
    msgs = crud.get_messages(db, chat_id)
    chat_history = [m for m in msgs if m.sender in ("user", "bot")]
    logger.info(f"User message received: {user_message}")
    assistant_reply = chatbot.get_chatbot_answer(
        user_message,
        chat_history=chat_history,
        use_kb=True
    )
    logger.info(f"Bot reply: {assistant_reply}")
    crud.add_message(db, chat_id, sender="user", content=user_message)
    crud.add_message(db, chat_id, sender="bot", content=assistant_reply)
    return {"response": assistant_reply}

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "../uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post("/upload/", response_model=dict)
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Save file to disk
    filename = f"{datetime.utcnow().timestamp()}_{file.filename}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    with open(filepath, "wb") as f:
        content = await file.read()
        f.write(content)
    # Add file entry to DB
    db_file = models.KnowledgeFile(filename=file.filename, filepath=filepath)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    # -- After saving file: Index to vectorstore (so we can use content for answers!)
    logger.info(f"Indexing file into vectorstore: {filepath}")
    add_documents_to_vectorstore([filepath])
    # -- Optionally: reload the vectorstore in chatbot.py, if needed
    # chatbot.vectorstore = create_or_load_vectorstore()  # Uncomment if you use a global vectorstore in chatbot.py

    return {"filename": file.filename, "filepath": filepath}

@app.get("/")
def health():
    return {"status": "ok"}
