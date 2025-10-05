# controllers/roles.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from models.role import Role
from models.permission import Permission
from schemas.roles import RoleCreate
from typing import List

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
    role = await db.get(Role, role_id)
    permission = await db.get(Permission, permission_id)
    if not role or not permission:
        raise ValueError("Rôle ou permission non trouvé")
    role.permissions.append(permission)
    await db.commit()
    return role
