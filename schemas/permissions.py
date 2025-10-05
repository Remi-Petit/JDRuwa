# schemas/permissions.py
from pydantic import BaseModel

class PermissionOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class PermissionCreate(BaseModel):
    name: str
