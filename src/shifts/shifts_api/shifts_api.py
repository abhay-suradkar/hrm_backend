from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.db_session.database import get_db
from datetime import time

# Import your model and schema
from src.shifts.shift_model.shift_model import Shifts
from src.shifts.shift_schema.shift_schema import CreateShift, UpdateShift, DeleteShift

router = APIRouter()

class ShiftAPI:

    @router.post("/CreateShift")
    def create_shift(shift: CreateShift, db: Session = Depends(get_db)):
        try:
            existing_shift = db.query(Shifts).filter(Shifts.shift_name == shift.shift_name).first()
            if existing_shift:
                raise HTTPException(status_code=400, detail="Shift name already exists.")
            
            new_shift = Shifts(
                shift_name=shift.shift_name,
                start_time=shift.start_time,
                end_time=shift.end_time,
                working_hours=shift.working_hours
            )
            
            db.add(new_shift)
            db.commit()
            db.refresh(new_shift)
            
            return {"Message" : "Shift is created"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error {str(e)}")
        
    @router.get("/Shifts")
    def get_all_Shifts(db: Session = Depends(get_db)):
        try:
            shifts = db.query(Shifts).all()
            return {"total": len(shifts), "data": shifts}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
        
    @router.put("/UpdateShift")
    def update_shift(data: UpdateShift, db: Session = Depends(get_db)):
        try:
            shift = db.query(Shifts).filter(Shifts.shift_id == data.shift_id).first()
        
            if not shift:
                raise HTTPException(status_code=404, detail="Shift ID not found.")

            if data.shift_name is not None:
                shift.shift_name = data.shift_name
            if data.start_time is not None:
                shift.start_time = data.start_time
            if data.end_time is not None:
                shift.end_time = data.end_time
            if data.working_hours is not None:
                shift.working_hours = data.working_hours

            db.commit()
            db.refresh(shift)

            return {
                "message": "Shift updated successfully",
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error {str(e)}")
        
    @router.delete("/", status_code=200)
    def delete_shift(data: DeleteShift, db: Session = Depends(get_db)):
        try:
            shift = db.query(Shifts).filter(Shifts.shift_id == data.shift_id).first()
            
            if not shift:
                raise HTTPException(status_code=404, detail="Shift ID not found.")
            
            db.delete(shift)
            db.commit()

            return {"message": f"Shift with ID {data.shift_id} deleted successfully."}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error {str(e)}")