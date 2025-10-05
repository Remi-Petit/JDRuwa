# routers/users.py
from fastapi import APIRouter, Depends, HTTPException
from config.auth import get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.user import User
from controllers.users import add_role_to_user
from database.connect import get_db
from typing import List
from schemas.users import UserOut

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=List[UserOut])
async def get_all_users(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Seuls les utilisateurs authentifiés peuvent lister les utilisateurs."""
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users

@router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Récupère un utilisateur par son ID."""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return user

@router.post("/{user_id}/roles/{role_id}", response_model=UserOut)
async def assign_role_to_user(
    user_id: int,
    role_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await add_role_to_user(db, user_id, role_id)