from fastapi import FastAPI, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from src.auth.auth_model.auth_model import Users
from src.auth.auth_schema.auth_schema import userSignup, userLogin
from src.db_session.database import get_db
from src.auth_utils import hash_password, verify_password
from src.auth.auth_dao.auth_dao import get_user_by_email, create_user

class authService:
    def signup_auth(users : userSignup, db : Session=Depends(get_db)):
        try:
            exisiting_user = get_user_by_email(db, users.email)
            if exisiting_user:
                raise HTTPException(status_code=400, detail="User is all ready exist")
            
            if users.password != users.confirm_password:
                raise HTTPException(status_code=400, detail="Password do not match")
            
            hashed_password = hash_password(users.password)

            create_user(
                db=db,
                name=users.name,
                phone=users.phone,
                email=users.email,
                status=users.status,
                role=users.role,
                hashed_password=hashed_password
            )
            
            return {"message" : "User register sucessfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
        
    def login_auth(users : userLogin, db : Session=Depends(get_db)):
        try:
            exisiting_user= get_user_by_email(db, users.email)
            if not exisiting_user:
                raise HTTPException(status_code=400, detail="Invalid Email")
            
            if not verify_password(users.password, exisiting_user.password):
                raise HTTPException(status_code=400, detail="Invalid Password")
            return{"message" : "User Login sucessfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
