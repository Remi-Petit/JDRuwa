import strawberry
from strawberry.types import Info
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.repositories.user_repo import UserRepository
from app.services.auth_service import create_access_token

@strawberry.type
class AuthMutations:
    @strawberry.mutation
    async def login(self, info: Info, email: str, password: str) -> str:
        db: AsyncSession = info.context["db"]

        user = await UserRepository.get_by_email(db, email)
        if not user or not user.verify_password(password):
            raise ValueError("Utilisateur ou mot de passe incorrect")

        return create_access_token(str(user.id))
