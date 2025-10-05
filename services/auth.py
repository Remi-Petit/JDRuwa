# services/auth.py
from fastapi import HTTPException, status
from models.user import User

def check_permission(user: User, required_permission: str):
    """Vérifie si l'utilisateur a la permission requise."""
    for role in user.roles:
        for permission in role.permissions:
            if permission.name == required_permission:
                return True
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f"Permission '{required_permission}' requise"
    )
