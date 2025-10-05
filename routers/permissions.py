# routers/permissions.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.permissions import PermissionOut, PermissionCreate
from typing import List
from controllers.permissions import get_all_permissions, create_permission
from database.connect import get_db

router = APIRouter(prefix="/permissions", tags=["permissions"])

@router.get("", response_model=List[PermissionOut])
async def list_permissions(db: AsyncSession = Depends(get_db)):
    """Liste toutes les permissions."""
    return await get_all_permissions(db)

@router.post("", response_model=PermissionOut)
async def create_permission_endpoint(
    permission_data: PermissionCreate, db: AsyncSession = Depends(get_db)
):
    return await create_permission(db, permission_data)
