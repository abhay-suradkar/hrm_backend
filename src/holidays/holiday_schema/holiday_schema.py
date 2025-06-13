from pydantic import BaseModel, validator
from datetime import date, datetime
from typing import Optional
from fastapi import HTTPException


class CreateHoliday(BaseModel):
    date: date
    occasion: str
    is_national: bool = False 


class UpdateHoliday(BaseModel):
    id: int
    date: date
    occasion: Optional[str] = None
    is_national: Optional[bool] = None

    
# DELETE (just id)
class DeleteHoliday(BaseModel):
    id: int