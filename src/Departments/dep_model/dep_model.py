from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid4

from src.db_session.database import Base

class Departments(Base):
    __tablename__ = 'departments'
    __table_args__ = {"schema": "dev"}

    dep_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    dep_name = Column(String(), nullable=False)

    dep_head_id = Column(UUID(as_uuid=True), ForeignKey("dev.users.id", ondelete="CASCADE"), nullable=True)

    dep_head = relationship("Users", foreign_keys=[dep_head_id], back_populates="managed_department")