from sqlalchemy.orm import Session
from . import models

def create_chat(db: Session, title="New Chat"):
    chat = models.Chat(title=title)
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat

def get_chats(db: Session):
    return db.query(models.Chat).all()

def get_chat(db: Session, chat_id: int):
    return db.query(models.Chat).filter(models.Chat.id == chat_id).first()

def add_message(db: Session, chat_id: int, sender: str, content: str):
    msg = models.Message(chat_id=chat_id, sender=sender, content=content)
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg

def get_messages(db: Session, chat_id: int):
    return db.query(models.Message).filter(models.Message.chat_id == chat_id).order_by(models.Message.timestamp).all()
