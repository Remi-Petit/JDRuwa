# routers/auth.py
from fastapi import APIRouter, Depends
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database.connect import get_db
from controllers.auth import register_user, ConflictError
from models.user import User
from schemas.auth import RegisterIn, UserOut

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserOut, status_code=201)
async def register(payload: RegisterIn, db: AsyncSession = Depends(get_db)):
    try:
        user: User = await register_user(
            db=db,
            email=payload.email,
            username=payload.username,
            password=payload.password,
        )
        return user
    except ConflictError as ce:
        # 409 avec info du champ en conflit
        raise HTTPException(status_code=409, detail={"field": ce.field, "message": ce.message})