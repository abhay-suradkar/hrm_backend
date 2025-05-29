from fastapi import FastAPI, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from src.auth.auth_model.auth_model import Users
from src.auth.auth_schema.auth_schema import userSignup
from src.db_session.database import get_db
from src.auth.auth_service import auth_service
from src.auth_utils import hash_password
router = APIRouter()

class authAPI:
    @router.post("/signup/")
    def signup(users : userSignup, db : Session=Depends(get_db)):
        return auth_service.authService.signup_auth(users, db)