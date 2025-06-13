from sqlalchemy import Column, Integer, Time, Date, Numeric, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from src.db_session.database import Base

class Attendance(Base):
    __tablename__ = "attendance"
    __table_args__ = {'schema': 'dev'}

    attendance_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("dev.users.id"))
    shift_id = Column(Integer, ForeignKey("dev.shifts.shift_id"))
    date = Column(Date, nullable=False)
    clock_in = Column(Time)
    clock_out = Column(Time)
    working_hours = Column(Numeric(4, 2))
    status = Column(String)
