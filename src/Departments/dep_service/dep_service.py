from src.Departments.dep_model.dep_model import Departments
from src.Departments.dep_schema.dep_schema import AddDep, UpdateDep
from fastapi import FastAPI, HTTPException, Depends, APIRouter, Request
from sqlalchemy.orm import Session
from src.db_session.database import get_db
from src.auth.auth_model.auth_model import Users
from src.Departments.dep_dao.dep_dao import DepDAO
from uuid import UUID
router = APIRouter()

class DepService:
    @router.post("/AddDep")
    def AddDep(department :AddDep, db: Session=Depends(get_db)):
        try:
            exisiting_dep_name=DepDAO.get_dep_by_name(db, department.dep_name)
            if exisiting_dep_name:
                raise HTTPException(status_code=400, detail="Department is already exists")
            
            user = DepDAO.get_dep_by_head_id(db, department.dep_head_id)
            if not user:
                raise HTTPException(status_code=400, detail="User not found")
            if user.role not in['hr', 'emp']:
                raise HTTPException(status_code=400, detail="User cannot be department head")
            
            new_dep = DepDAO.create_dep(db, department.dep_name, department.dep_head_id)
            return {"message": "New Department Add Sucessfully"}
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
        
    @router.get('/getDep')
    def getDep(db: Session=Depends(get_db)):
        try:
            departments = DepDAO.get_dep(db)
            depart_data = [{
                "dep_id" : dep.dep_id,
                "dep_name" : dep.dep_name,
                "dep_head_id" : dep.dep_head_id
            } for dep in departments]
            return {"total_department" : len(departments), "departments" : depart_data}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error {str(e)}")
        
    @router.put("/department")
    def get_or_update_department(data: UpdateDep, db: Session = Depends(get_db)):
        try:
            department = DepDAO.get_dep_by_id(db, data.dep_id)

            if not department:
                raise HTTPException(status_code=404, detail="Department not found")
            
            Update_dep = DepDAO.update_dep(db, department, data.dep_name, data.dep_head_id)
            return {
                "message": "Department updated successfully",
                # "dep_id": Update_dep.dep_id,
                # "dep_name": Update_dep.dep_name,
                # "dep_head_id": Update_dep.dep_head_id
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Servier Error {str(e)}")


    @router.delete("/DeleteDep/{dep_id}")
    def DeleteDep(dep_id: UUID, db:Session=Depends(get_db)):
        try:
            departments= DepDAO.get_dep_by_id(db, dep_id)
            if not departments:
                raise HTTPException(status_code=400, detail="Department not found")
            
            result = DepDAO.delete_dep(db, departments)
            return result

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error {str(e)}")