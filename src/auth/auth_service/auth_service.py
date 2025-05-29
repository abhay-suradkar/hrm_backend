from fastapi import FastAPI, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from src.auth.auth_model.auth_model import Users
from src.auth.auth_schema.auth_schema import userSignup
from src.db_session.database import get_db
from src.auth_utils import hash_password

class authService:
    def signup_auth(users : userSignup, db : Session=Depends(get_db)):
        try:
            exisiting_user = db.query(Users).filter(Users.email == users.email).first()
            if exisiting_user:
                raise HTTPException(status_code=400, detail="User is all ready exist")
            
            if users.password != users.confirm_password:
                raise HTTPException(status_code=400, detail="Password do not match")
            
            hashed_password = hash_password(users.password)

            new_user = Users(name=users.name, phone=users.phone, email=users.email, status=users.status, role=users.role, password=hashed_password)
            db.add(new_user)
            db.commit()
            return {"message" : "User register sucessfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")