from src.Designation.design_model.design_model import Designation
from src.Designation.design_schema.design_schema import addDesignation, UpdateDesignation, DeleteDesignation
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException, Depends, APIRouter, Request
from src.db_session.database import get_db
from src.Departments.dep_model.dep_model import Departments
from uuid import UUID

router = APIRouter()

class DesignServie:
    @router.post('/addDesignation')
    def add_designation(designation: addDesignation, db: Session = Depends(get_db)):
        try:
            exisiting_Designation_name = db.query(Designation).filter(Designation.design_title == designation.design_title).first()
            if exisiting_Designation_name:
                raise HTTPException(status_code=400, detail="Desigantion Title already exist")
            dep = db.query(Departments).filter(Departments.dep_id == designation.dep_id).first()
            if not dep:
                raise HTTPException(status_code=400, detail="Department is not found Create First")
            new_design = Designation(
                design_title = designation.design_title,
                description = designation.description,
                dep_id = designation.dep_id
            )
            db.add(new_design)
            db.commit()
            db.refresh(new_design)
            return {"message" : "Designation Create Sucessfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error {str(e)}")
        
    @router.get('/getDesignation')    
    def getDesignation(db: Session=Depends(get_db)):
        try:
            designation = db.query(Designation).all()
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
            designation = db.query(Designation).filter(Designation.design_id == data.design_id).first()
            if not designation:
                raise HTTPException(status_code=400, detail="Designation is not found")
            
            designation_dep_id = db.query(Departments).filter(Departments.dep_id == data.dep_id).first()
            if not designation_dep_id:
                raise HTTPException(status_code=400, detail=f"Department is not found, please create if first")
        
            designation.design_title = data.design_title
            designation.description = data.description
            designation.dep_id = data.dep_id
            db.commit()
            db.refresh(designation)
            return{
                "message" : "Designation Updated Sucessfull",
                "designation_title" : designation.design_title,
                "description" : designation.description,
                "dep_id" : designation.dep_id
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error {str(e)}")
        
    @router.delete('/delete-Designation/{design_id}')
    def DeleteDesignation(design_id:UUID, db:Session=Depends(get_db)):
        try:
            designaion = db.query(Designation).filter(Designation.design_id == design_id).first()
            if not designaion:
                raise HTTPException(status_code=400, detail="Designation is not found")
            db.delete(designaion)
            db.commit()
            return {
                "message" : "Designation Delete Sucessfully"
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error {str(e)}")
