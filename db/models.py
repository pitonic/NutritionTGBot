from sqlalchemy import Column, Integer, BigInteger, String, DateTime, ForeignKey, Enum, Float, Identity
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, Identity(), nullable=False)
    telegram_id = Column(BigInteger, primary_key=True, unique=True, nullable=False)
    username = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User(id={self.id}, telegram_id={self.telegram_id}, username={self.username})>"

