from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from config import DATABASE_URL

Base = declarative_base()

# Модель таблицы (заменяет database.models)
class MessageHistory(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    question = Column(Text)
    answer = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

class Database:
    def __init__(self):
        self.engine = create_engine(DATABASE_URL)
        Base.metadata.create_all(self.engine) # Создает таблицы, если их нет
        self.SessionLocal = sessionmaker(bind=self.engine)

    def save_message(self, user_id, question, answer):
        session = self.SessionLocal()
        try:
            new_msg = MessageHistory(user_id=user_id, question=question, answer=answer)
            session.add(new_msg)
            session.commit()
        except Exception as e:
            print(f"Database Error: {e}")
            session.rollback()
        finally:
            session.close()