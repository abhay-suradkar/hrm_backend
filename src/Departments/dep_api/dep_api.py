from src.Departments.dep_service import dep_service
from src.Departments.dep_service.dep_service import DepService 
from src.Departments.dep_model.dep_model import Departments
from src.Departments.dep_schema.dep_schema import AddDep, UpdateDep
from fastapi import FastAPI, HTTPException, Depends, APIRouter, Request
from sqlalchemy.orm import Session
from src.db_session.database import get_db
from src.auth.auth_model.auth_model import Users
from uuid import UUID

router = APIRouter()

class DepAPI:
    @router.post("/AddDep")
    def AddDep(department :AddDep, db: Session=Depends(get_db)):
        return dep_service.DepService.AddDep(department, db)
    
    @router.get('/getDep')
    def getDep(db: Session=Depends(get_db)):
        return dep_service.DepService.getDep(db)

    @router.put("/department")
    def get_or_update_department(data: UpdateDep, db: Session = Depends(get_db)):
        return dep_service.DepService.get_or_update_department(data, db)

    @router.delete("/DeleteDep/{dep_id}")
    def DeleteDep(dep_id: UUID, db:Session=Depends(get_db)):
        return dep_service.DepService.DeleteDep(dep_id, db)