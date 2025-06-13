from pydantic import BaseModel
from typing import Optional
from datetime import time

class CreateShift(BaseModel):
    shift_name: str
    start_time: time
    end_time: time
    working_hours: float

class UpdateShift(BaseModel):
    shift_id: int
    shift_name: Optional[str] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    working_hours: Optional[float] = None

class DeleteShift(BaseModel):
    shift_id: int
