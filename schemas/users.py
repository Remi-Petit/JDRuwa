# schemas/users.py
from pydantic import BaseModel, EmailStr
from typing import List

class UserOut(BaseModel):
    id: int
    email: EmailStr
    username: str
    roles: List[str] = []

    class Config:
        from_attributes = True  # Pour Pydantic v2
