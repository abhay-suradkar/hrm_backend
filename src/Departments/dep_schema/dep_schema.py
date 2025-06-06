from pydantic import BaseModel
from uuid import UUID

class AddDep(BaseModel):
    dep_name: str
    dep_head_id: UUID   # ✅ this matches your model and API usage

class GetDep(BaseModel):
    dep_id: UUID
    dep_name: str
    dep_head_id: UUID