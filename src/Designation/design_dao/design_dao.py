from uuid import UUID
from src.Designation.design_model.design_model import Designation
from src.Departments.dep_model.dep_model import Departments
from sqlalchemy.orm import Session
from typing import List, Optional

class DesignDAO:
    @staticmethod
    def get_design_by_name(db: Session, design_title: str):
        return db.query(Designation).filter(Designation.design_title == design_title).first()

    @staticmethod
    def get_department_by_id(db: Session, dep_id: UUID):
        return db.query(Departments).filter(Departments.dep_id == dep_id).first()
    
    @staticmethod
    def create_design(db:Session, design_title:str, description:Optional[str], dep_id:UUID):
        new_design = Designation(
                design_title = design_title,
                description = description,
                dep_id = dep_id
        )
        db.add(new_design)
        db.commit()
        db.refresh(new_design)
        return new_design
    
    @staticmethod
    def get_all_design(db: Session):
        return db.query(Designation).all()
    
    @staticmethod
    def get_design_by_design_id(db:Session, design_id:UUID):
        return db.query(Designation).filter(Designation.design_id == design_id).first()
    
    @staticmethod
    def update_design(db: Session, designation, design_title:str, description: Optional[str], dep_id:UUID):
        designation.design_title = design_title
        designation.description = description
        designation.dep_id = dep_id
        db.commit()
        db.refresh(designation)
        return designation
    
    @staticmethod
    def delete_design(db: Session, designation):
        db.delete(designation)
        db.commit()
        return { "message" : "Designation Delete Sucessfully"}