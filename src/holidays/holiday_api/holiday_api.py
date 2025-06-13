from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.db_session.database import get_db
from src.holidays.holiday_model.holiday_model import Holidays
from src.holidays.holiday_schema.holiday_schema import CreateHoliday, UpdateHoliday, DeleteHoliday
from datetime import date

router = APIRouter()

class HolidayAPI:
    @router.post("/holiday")
    def create_holiday(data: CreateHoliday, db: Session = Depends(get_db)):
        try:
            # Directly use data.is_national (which is bool)
            existing = db.query(Holidays).filter(Holidays.date == data.date).first()
            if existing:
                raise HTTPException(status_code=400, detail="Holiday already exists for this date")

            new_holiday = Holidays(
                date=data.date,
                occasion=data.occasion,
                is_national=data.is_national  # use as is
            )
            db.add(new_holiday)
            db.commit()
            db.refresh(new_holiday)

            return {"message": "Holiday created successfully", "holiday_id": new_holiday.id}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

    @router.get("/holidays")
    def get_all_holidays(db: Session = Depends(get_db)):
        try:
            holidays = db.query(Holidays).all()
            return {"total": len(holidays), "data": holidays}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

    @router.get("/holiday/by-id/{holiday_id}")
    def get_holiday_by_id(holiday_id: int, db: Session = Depends(get_db)):
        try:
            holiday = db.query(Holidays).filter(Holidays.id == holiday_id).first()
            if not holiday:
                raise HTTPException(status_code=404, detail="Holiday not found with this ID")
            return holiday
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


    @router.get("/holiday/by-date/{holiday_date}")
    def get_holiday_by_date(holiday_date: date, db: Session = Depends(get_db)):
        try:
            holiday = db.query(Holidays).filter(Holidays.date == holiday_date).first()
            if not holiday:
                raise HTTPException(status_code=404, detail="Holiday not found with this date")
            return holiday
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
        
    
    @router.put("/holiday")
    def update_holiday(data: UpdateHoliday, db: Session = Depends(get_db)):
        try:
            holiday = db.query(Holidays).filter(Holidays.id == data.id).first()
            if not holiday:
                raise HTTPException(status_code=404, detail="Holiday not found")

            # Check if the new date already exists in another holiday
            if data.date is not None:
                existing = db.query(Holidays).filter(Holidays.date == data.date, Holidays.id != data.id).first()
                if existing:
                    raise HTTPException(status_code=400, detail="Holiday already exists with this date")
                holiday.date = data.date

            if data.occasion is not None:
                holiday.occasion = data.occasion

            if data.is_national is not None:
                holiday.is_national = data.is_national

            db.commit()
            db.refresh(holiday)

            return {"message": "Holiday updated successfully", "holiday_id": holiday.id}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


    @router.delete("/holiday")
    def delete_holiday(data: DeleteHoliday, db: Session = Depends(get_db)):
        try:
            holiday = db.query(Holidays).filter(Holidays.id == data.id).first()
            if not holiday:
                raise HTTPException(status_code=404, detail="Holiday not found")

            db.delete(holiday)
            db.commit()

            return {"message": "Holiday deleted successfully", "holiday_id": data.id}
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")