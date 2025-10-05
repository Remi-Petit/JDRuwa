# routers/auth.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database.connect import get_db
from controllers.auth import register_user, ConflictError
from models.user import User
from schemas.auth import RegisterIn, UserOut, LoginIn, TokenOut

from controllers.auth import authenticate_user, UnauthorizedError

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
        raise HTTPException(status_code=409, detail={"field": ce.field, "message": ce.message})

@router.post("/login", response_model=TokenOut)
async def login(payload: LoginIn, db: AsyncSession = Depends(get_db)):
    try:
        user = await authenticate_user(db=db, email=payload.email, password=payload.password)
        access_token = user.generate_jwt()
        return {"access_token": access_token, "token_type": "bearer"}
    except UnauthorizedError:
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")