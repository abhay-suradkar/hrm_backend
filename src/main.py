from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.db_session.database import init_db
from src.auth.auth_api.auth_api import router as authAPI
from src.Departments.dep_api.dep_api import router as DepAPI
from src.Designation.design_api.design_api import router as DesignAPI
from src.holidays.holiday_api.holiday_api import router as HolidayAPI
from src.shifts.shifts_api.shifts_api import router as ShiftAPI
from src.attendance.attendance_api.attendance_api import router as APIAttendance
import os
from dotenv import load_dotenv
import sys
import firebase_admin
from firebase_admin import credentials

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

cred = credentials.Certificate("firebase-private-key.json")
firebase_admin.initialize_app(cred)

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or use your domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()
app.include_router(authAPI)
app.include_router(DepAPI)
app.include_router(DesignAPI)
app.include_router(HolidayAPI)
app.include_router(ShiftAPI)
app.include_router(APIAttendance)