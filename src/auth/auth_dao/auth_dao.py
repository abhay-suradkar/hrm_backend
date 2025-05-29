from sqlalchemy.orm import Session
from src.auth.auth_model.auth_model import Users
from pydantic import  EmailStr

def get_user_by_email(db: Session, email: EmailStr):
        return db.query(Users).filter(Users.email == email).first()

def create_user(db: Session, name: str, phone: str, email: EmailStr, status: bool, role:str, hashed_password: str):
        new_user = Users(
            name=name,
            phone=phone,
            email=email,
            status=status,
            role=role,
            password=hashed_password
        )
        db.add(new_user)
        db.commit()
        return new_user