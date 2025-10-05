# schemas/roles.py
from pydantic import BaseModel
from typing import List

class RoleOut(BaseModel):
    id: int
    name: str
    permissions: List[str] = []

    class Config:
        from_attributes = True

class RoleCreate(BaseModel):
    name: str
