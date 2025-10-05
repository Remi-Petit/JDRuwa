# controllers/auth.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.user import User

class ConflictError(Exception):
    def __init__(self, field: str, message: str = "Conflict"):
        self.field = field
        self.message = message
        super().__init__(message)

async def register_user(*, db: AsyncSession, email: str, username: str, password: str) -> User:
    # Unicité
    res = await db.execute(
        select(User).where((User.email == email) | (User.username == username))
    )
    existing = res.scalar_one_or_none()
    if existing:
        field = "email" if existing.email == email else "username"
        raise ConflictError(field, f"{field.capitalize()} déjà utilisé.")

    # Création (setter password déclenche hash)
    user = User(email=email, username=username)
    user.password = password  # write-only, hash automatique

    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
