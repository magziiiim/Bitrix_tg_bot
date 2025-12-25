import datetime
from sqlalchemy import create_engine, Column, Integer, BigInteger, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME

DATABASE_URL = "postgresql://octagon:12345@127.0.0.1:5432/bitrix_bot_db"
Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger)
    question = Column(Text)
    answer = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)

def save_message(user_id, question, answer):
    db = SessionLocal()
    try:
        new_msg = Message(user_id=user_id, question=question, answer=answer)
        db.add(new_msg)
        db.commit()
    finally:
        db.close()
