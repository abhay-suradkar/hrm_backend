from fastapi import FastAPI, HTTPException, Depends, APIRouter, Request
from sqlalchemy.orm import Session
from src.auth.auth_model.auth_model import Users
from src.auth.auth_schema.auth_schema import userSignup, userLogin
from src.db_session.database import get_db
from src.auth.auth_service import auth_service
from src.auth_utils import hash_password, verify_password
from firebase_admin import auth

router = APIRouter()

class authAPI:
    @router.post("/signup/")
    def signup(users : userSignup, db : Session=Depends(get_db)):
        return auth_service.authService.signup_auth(users, db)
    
    @router.post("/login")
    def login(users : userLogin, db : Session=Depends(get_db)):
        return auth_service.authService.login_auth(users, db)
    
    @router.post("firebase-auth")
    async def firebase_auth(request: Request, db: Session=Depends(get_db)):
        data = await request.json()
        id_token = data.get("token")
        phone = data.get("phone")
        status = data.get("status", True)
        role = data.get("role", "user")

        if not id_token:
            raise HTTPException(status_code=400, detail="Token Missing")
        
        try:
            decoded_token = auth.verify_id_token(id_token)

            name = decoded_token.get("name")
            email = decoded_token.get("email")
            
            if not email:
                raise HTTPException(status_code=400, detail="email is not found in token")
            
            users = db.query(Users).filter(Users.email == email).first()

            if not users:
                users = Users(name = name, phone= phone, email= email, status=status,role=role, password=None)
            else:
                users.name = name
                users.phone = phone
                users.role = role
                users.status = status
            db.commit()
            db.refresh(users)

            return {
                "message": "User authenticated successfully",
                "user": {
                "email": users.email,
                "name": users.name,
                "phone": users.phone,
                "status": users.status,
                "role": users.role
                }
            }
        except Exception as e:
            print("firebase token verfication failed:", e)
            raise HTTPException(status_code=500, detail="Invalid firebase token")