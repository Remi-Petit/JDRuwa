# controllers/users.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.user import User
from models.role import Role
from fastapi import HTTPException
from sqlalchemy.orm import selectinload

async def add_role_to_user(db: AsyncSession, user_id: int, role_id: int) -> User:
    # Récupère l'utilisateur avec ses rôles
    result = await db.execute(
        select(User).options(selectinload(User.roles)).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    role = await db.get(Role, role_id)

    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    if not role:
        raise HTTPException(status_code=404, detail="Rôle non trouvé")

    if role in user.roles:
        return user

    user.roles.append(role)
    await db.commit()
    await db.refresh(user)
    return user
