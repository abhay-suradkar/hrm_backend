from sqlalchemy import Column, Integer, String, Time, Numeric
from src.db_session.database import Base

class Shifts(Base):
    __tablename__ = "shifts"
    __table_args__ = {'schema': 'dev'}

    shift_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    shift_name = Column(String(100), nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    working_hours = Column(Numeric(4, 2), nullable=True)
