from uuid import UUID
from sqlalchemy.orm import Session
from src.Departments.dep_model.dep_model import Departments
from src.auth.auth_model.auth_model import Users

class DepDAO:
    @staticmethod
    def get_dep_by_name(db: Session, dep_name: str):
        return db.query(Departments).filter(Departments.dep_name == dep_name).first()
    
    @staticmethod
    def get_dep_by_head_id(db: Session, dep_head_id: UUID):
        return db.query(Users).filter(Users.id == dep_head_id).first()
    
    @staticmethod
    def create_dep(db: Session, dep_name:str, dep_head_id: UUID ):
        new_dep = Departments (dep_name=dep_name,dep_head_id= dep_head_id)
        db.add(new_dep)
        db.commit()
        db.refresh(new_dep)
        return new_dep
    
    @staticmethod
    def get_dep(db:Session):
        return db.query(Departments).all()

    @staticmethod
    def get_dep_by_id(db: Session, dep_id:UUID):
        return db.query(Departments).filter(Departments.dep_id == dep_id).first()
                
    @staticmethod
    def update_dep(db:Session, department, dep_name, dep_head_id):
        department.dep_name = dep_name
        department.dep_head_id = dep_head_id
        db.commit()
        db.refresh(department)
        return department

    @staticmethod
    def delete_dep(db, departments):
        db.delete(departments)
        db.commit()
        return {"message" : "Department Delete Sucessfully"}