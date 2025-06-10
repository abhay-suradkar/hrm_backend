from src.Designation.design_model.design_model import Designation
from src.Designation.design_schema.design_schema import addDesignation, UpdateDesignation, DeleteDesignation
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException, Depends, APIRouter, Request
from src.db_session.database import get_db
from src.Departments.dep_model.dep_model import Departments
from src.Designation.design_dao.design_dao import DesignDAO
from uuid import UUID

router = APIRouter()

class DesignServie:
    @router.post('/addDesignation')
    def add_designation(designation: addDesignation, db: Session = Depends(get_db)):
        try:
            exisiting_design = DesignDAO.get_design_by_name(db, designation.design_title)
            if exisiting_design:
                raise HTTPException(status_code=400, detail="Desigantion Title already exist")
            
            department = DesignDAO.get_department_by_id(db, designation.dep_id)
            if not department:
                raise HTTPException(status_code=400, detail="Department is not found Create First")
            
            DesignDAO.create_design(db, designation.design_title, designation.description, designation.dep_id)
            return {"message" : "Designation Create Sucessfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error {str(e)}")
        
    @router.get('/getDesignation')    
    def getDesignation(db: Session=Depends(get_db)):
        try:
            designation = DesignDAO.get_all_design(db)
            design_data = [{
                "design_id" : design.design_id,
                "design_title" : design.design_title,
                "description" : design.description,
                "dep_id" : design.dep_id
            } for design in designation ]
            return {"total_Designation" : len(designation), "designation": design_data}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error {str(e)}")
        
    @router.put('/update-Designation')
    def updateDesignation(data: UpdateDesignation, db:Session=Depends(get_db)):
        try:
            designation = DesignDAO.get_design_by_design_id(db, data.design_id)
            if not designation:
                raise HTTPException(status_code=400, detail="Designation is not found")
            
            department = DesignDAO.get_department_by_id(db, data.dep_id)
            if not department:
                raise HTTPException(status_code=400, detail="Department is not found, please create if first")
        
            update_design = DesignDAO.update_design(db, designation, data.design_title, data.description, data.dep_id)
            return{
                "message" : "Designation Updated Sucessfull",
                # "designation_title" : update_design.design_title,
                # "description" : update_design.description,
                # "dep_id" : update_design.dep_id
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error {str(e)}")
        
    @router.delete('/delete-Designation/{design_id}')
    def DeleteDesignation(design_id:UUID, db:Session=Depends(get_db)):
        try:
            designation = DesignDAO.get_design_by_design_id(db, design_id)
            if not designation:
                raise HTTPException(status_code=400, detail="Designation is not found")
            result = DesignDAO.delete_design(db, designation)
            return  result
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error {str(e)}")
