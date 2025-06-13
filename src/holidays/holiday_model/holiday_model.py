from src.db_session.database import Base
from sqlalchemy import Column, String, Integer, Date, Boolean, DateTime
from datetime import datetime

class Holidays(Base):
    __tablename__ = "holidays"
    __table_args__ = {"schema": "dev"}

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date = Column(Date, nullable=False)
    occasion = Column(String(100), nullable=False)
    is_national = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
