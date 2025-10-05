# controllers/permissions.py
from sqlalchemy import select
from models.permission import Permission
from schemas.permissions import PermissionCreate
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

async def get_all_permissions(db: AsyncSession) -> List[Permission]:
    """Récupère toutes les permissions."""
    result = await db.execute(select(Permission))
    return result.scalars().all()

async def create_permission(db: AsyncSession, permission_data: PermissionCreate) -> Permission:
    # Vérifie si la permission existe déjà
    result = await db.execute(
        select(Permission).where(Permission.name == permission_data.name)
    )
    existing_permission = result.scalar_one_or_none()
    if existing_permission:
        return existing_permission

    permission = Permission(**permission_data.model_dump())
    db.add(permission)
    await db.commit()
    await db.refresh(permission)
    return permission
