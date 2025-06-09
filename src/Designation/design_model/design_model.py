from src.db_session.database import Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from src.Departments.dep_model.dep_model import Departments

class Designation(Base):
    __tablename__ = 'designation'
    __table_args__ = {"schema": "dev"}

    design_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    design_title = Column(String(100), nullable=False)
    description = Column(String(100), nullable=True)
    dep_id = Column(UUID(as_uuid=True), ForeignKey("dev.departments.dep_id"))

    department = relationship("Departments", back_populates="designations")