from src.Departments.dep_model.dep_model import Departments
from src.Departments.dep_schema.dep_schema import AddDep, GetDep
from fastapi import FastAPI, HTTPException, Depends, APIRouter, Request
from sqlalchemy.orm import Session
from src.db_session.database import get_db
from src.auth.auth_model.auth_model import Users
router = APIRouter()

class DepAPI:
    @router.post("/AddDep")
    def AddDep(department :AddDep, db: Session=Depends(get_db)):
        try:
            exisiting_dep_name=db.query(Departments).filter(Departments.dep_name == department.dep_name).first()
            if exisiting_dep_name:
                raise HTTPException(status_code=400, detail="Department is already exisit")
            user = db.query(Users).filter(Users.id == department.dep_head_id).first()
            if not user:
                raise HTTPException(status_code=400, detail="User not found")
            if user.role not in['hr', 'emp']:
                raise HTTPException(status_code=400, detail="User cannot be department head")
            new_dep = Departments (
                dep_name=department.dep_name,
                dep_head_id= department.dep_head_id
            )
            db.add(new_dep)
            db.commit()
            db.refresh(new_dep)
            return {"message": "New Department Add Sucessfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
        
    @router.get('/getDep')
    def getDep(db: Session=Depends(get_db)):
        try:
            departments = db.query(Departments).all()
            depart_data = [{
                "dep_id" : dep.dep_id,
                "dep_name" : dep.dep_name,
                "dep_head_id" : dep.dep_head_id
            } for dep in departments]
            return {"total_department" : len(departments), "departments" : depart_data}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error {str(e)}")