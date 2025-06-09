from src.Designation.design_services import design_services
from src.Designation.design_model.design_model import Designation
from src.Designation.design_schema.design_schema import addDesignation, UpdateDesignation, DeleteDesignation
from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends, APIRouter
from src.db_session.database import get_db
from src.Departments.dep_model.dep_model import Departments
from uuid import UUID

router = APIRouter()

class DesignAPI:
    @router.post('/addDesignation')
    def add_designation(designation: addDesignation, db: Session = Depends(get_db)):
        return design_services.DesignServie.add_designation(designation, db)

    @router.get('/getDesignation')    
    def getDesignation(db: Session=Depends(get_db)):
        return design_services.DesignServie.getDesignation(db)

    @router.put('/update-Designation')
    def updateDesignation(data: UpdateDesignation, db:Session=Depends(get_db)):
        return design_services.DesignServie.updateDesignation(data, db)

    @router.delete('/delete-Designation/{design_id}')
    def DeleteDesignation(design_id:UUID, db:Session=Depends(get_db)):
        return design_services.DesignServie.DeleteDesignation(design_id, db)
    