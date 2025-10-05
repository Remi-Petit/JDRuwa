# routers/roles.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.roles import RoleOut, RoleCreate
from typing import List
from controllers.roles import get_all_roles, create_role, add_permission_to_role
from database.connect import get_db

router = APIRouter(prefix="/roles", tags=["roles"])

@router.get("", response_model=List[RoleOut])
async def list_roles(db: AsyncSession = Depends(get_db)):
    """Liste tous les rôles."""
    return await get_all_roles(db)

@router.post("", response_model=RoleOut)
async def create_role_endpoint(role_data: RoleCreate, db: AsyncSession = Depends(get_db)):
    return await create_role(db, role_data)

@router.post("/{role_id}/permissions/{permission_id}")
async def assign_permission_to_role(
    role_id: int,
    permission_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await add_permission_to_role(db, role_id, permission_id)
