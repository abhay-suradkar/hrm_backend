from src.db_session.config import DATABASE_URL
from sqlalchemy import create_engine, String, Integer, Column
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set. Check your environment variables or config file.")

Base = declarative_base()
SQLALCHEMY_DATABASE_URL = DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally: 
        db.close()

def init_db():
    from src.auth.auth_model.auth_model import Users
    from src.Departments.dep_model.dep_model import Departments
    from src.Designation.design_model.design_model import Designation
    from src.holidays.holiday_model.holiday_model import Holidays
    from src.shifts.shift_model.shift_model import Shifts
    Base.metadata.create_all(bind=engine)