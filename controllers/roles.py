# controllers/roles.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from models.role import Role
from models.permission import Permission
from schemas.roles import RoleCreate
from typing import List
from fastapi import HTTPException

async def get_all_roles(db: AsyncSession) -> List[Role]:
    """Récupère tous les rôles avec leurs permissions."""
    result = await db.execute(
        select(Role).options(selectinload(Role.permissions))
    )
    return result.scalars().all()

async def create_role(db: AsyncSession, role_data: RoleCreate) -> Role:
    # Vérifie si un rôle avec ce nom existe déjà
    result = await db.execute(
        select(Role).options(selectinload(Role.permissions)).where(Role.name == role_data.name)
    )
    existing_role = result.scalar_one_or_none()
    if existing_role:
        return existing_role

    # Sinon, crée le nouveau rôle
    role = Role(**role_data.model_dump())
    db.add(role)
    await db.commit()
    await db.refresh(role)
    return result.scalar_one()

async def add_permission_to_role(db: AsyncSession, role_id: int, permission_id: int) -> Role:
    # Récupère le rôle avec ses permissions
    result = await db.execute(
        select(Role).options(selectinload(Role.permissions)).where(Role.id == role_id)
    )
    role = result.scalar_one_or_none()
    permission = await db.get(Permission, permission_id)

    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")

    # Vérifie si la permission est déjà associée au rôle
    if permission in role.permissions:
        return role

    # Ajoute la permission au rôle
    role.permissions.append(permission)
    await db.commit()
    await db.refresh(role)
    return role