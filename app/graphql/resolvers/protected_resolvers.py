import strawberry
from strawberry.types import Info
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.repositories.user_repo import UserRepository
from app.graphql.types.user_type import UserType

@strawberry.type
class ProtectedQueries:
    @strawberry.field
    async def me(self, info: Info) -> UserType:
        db: AsyncSession = info.context["db"]
        user_id = info.context.get("user_id")
        if not user_id:
            raise ValueError("Non autorisé. Token JWT manquant ou invalide.")

        return await UserRepository.get_by_id(db, int(user_id))
