from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import date, time

class CreateAttendance(BaseModel):
    user_id: UUID
    shift_id: int
    date: date
    clock_in: Optional[time] = None
    clock_out: Optional[time] = None
    working_hours: Optional[float] = None
    status: Optional[str] = "Present"

class UpdateAttendance(BaseModel):
    attendance_id: int
    clock_in: Optional[time] = None
    clock_out: Optional[time] = None
    working_hours: Optional[float] = None
    status: Optional[str] = None
    shift_id: Optional[int] = None

class DeleteAttendance(BaseModel):
    attendance_id : int