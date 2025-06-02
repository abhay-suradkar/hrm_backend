from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, text, Boolean, UUID
from sqlalchemy.ext.declarative import declarative_base
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID 

Base = declarative_base()
class Users(Base):
    __tablename__ = "users"
    __table_args__ = {'schema': 'dev'}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique= True, nullable=False)

    name = Column(String(), nullable=True)
    phone = Column(String(225), nullable=True)
    email = Column(String(), nullable=True)
    status = Column(Boolean, nullable=False, default=True)
    role = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)