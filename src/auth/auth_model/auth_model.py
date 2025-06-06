from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid4

from src.db_session.database import Base

class Users(Base):
    __tablename__ = "users"
    __table_args__ = {'schema': 'dev'}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    name = Column(String(), nullable=False)
    phone = Column(String(225), nullable=False)
    email = Column(String(), nullable=False)
    status = Column(Boolean, nullable=False, default=False)
    role = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)

    managed_department = relationship(
        "Departments",
        back_populates="dep_head",
        primaryjoin="Users.id == Departments.dep_head_id"
    )