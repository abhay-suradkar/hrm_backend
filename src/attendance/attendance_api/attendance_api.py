from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.db_session.database import get_db
from src.attendance.attendance_model.attendance_model import Attendance
from src.auth.auth_model.auth_model import Users        # Assuming your user model is here
from src.shifts.shift_model.shift_model import Shifts    # Assuming your shift model is here
from src.attendance.attendance_schema.attendance_schema import CreateAttendance, UpdateAttendance, DeleteAttendance
import traceback

router = APIRouter()
class APIAttendance:
    @router.post("/attendance")
    def create_attendance(data: CreateAttendance, db: Session = Depends(get_db)):
        try:
            # 1. Check if user exists
            user = db.query(Users).filter(Users.id == data.user_id).first()
            if not user:
                raise HTTPException(status_code=404, detail="User does not exist.")

            # 2. Check if shift exists
            shift = db.query(Shifts).filter(Shifts.shift_id == data.shift_id).first()
            if not shift:
                raise HTTPException(status_code=404, detail="Shift does not exist.")

            # 3. Check if attendance for user and date already exists
            existing_attendance = db.query(Attendance).filter(
                Attendance.user_id == data.user_id,
                Attendance.date == data.date
            ).first()
            if existing_attendance:
                raise HTTPException(status_code=400, detail="Attendance record already exists for this user on this date.")

            # 4. Create new attendance record
            new_attendance = Attendance(
                user_id=data.user_id,
                shift_id=data.shift_id,
                date=data.date,
                clock_in=data.clock_in,
                clock_out=data.clock_out,
                working_hours=data.working_hours,
                status=data.status
            )

            db.add(new_attendance)
            db.commit()
            db.refresh(new_attendance)

            return {"Message": "Attendance record created successfully."}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error {str(e)}")

    @router.get("/attendance")
    def get_all_attendance(db: Session = Depends(get_db)):
        try:
            attendance_list = db.query(Attendance).all()
            return {"total" : len(attendance_list), "data": attendance_list}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error {str(e)}")
        
    @router.put("/attendance/update")
    def update_attendance(data: UpdateAttendance, db: Session = Depends(get_db)):
        try:
            attendance = db.query(Attendance).filter(Attendance.attendance_id == data.attendance_id).first()

            if not attendance:
                raise HTTPException(status_code=404, detail="Attendance record not found.")

            # ✅ Check if the provided shift_id exists before updating it
            if data.shift_id is not None:
                shift = db.query(Shifts).filter(Shifts.shift_id == data.shift_id).first()
                if not shift:
                    raise HTTPException(status_code=404, detail="Provided shift ID does not exist.")
                attendance.shift_id = data.shift_id

            if data.clock_in is not None:
                attendance.clock_in = data.clock_in
            if data.clock_out is not None:
                attendance.clock_out = data.clock_out
            if data.working_hours is not None:
                attendance.working_hours = data.working_hours
            if data.status is not None:
                attendance.status = data.status

            db.commit()
            db.refresh(attendance)

            return {"Message": "Attendance record updated successfully."}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error {str(e)}")

        
    @router.delete("/attendance/delete")
    def delete_attendance(data: DeleteAttendance, db: Session = Depends(get_db)):
        try:
            attendance = db.query(Attendance).filter(Attendance.attendance_id == data.attendance_id).first()

            if not attendance:
                raise HTTPException(status_code=404, detail="Attendance record not found.")

            db.delete(attendance)
            db.commit()

            return {"Message": "Attendance record deleted successfully."}

        except Exception:
            traceback.print_exc()
            raise HTTPException(status_code=500, detail="Internal Server Error")
