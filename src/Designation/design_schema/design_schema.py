from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class addDesignation(BaseModel):
    design_title : str
    description : Optional[str] = None
    dep_id: UUID

class UpdateDesignation(BaseModel):
    design_id: UUID
    design_title : str
    description : str
    dep_id : UUID

class DeleteDesignation(BaseModel):
    design_id: UUID