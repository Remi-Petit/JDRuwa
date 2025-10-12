from typing import List
import strawberry
from strawberry.types import Info
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.user_service import UserService
from app.graphql.types.user_type import UserType

MIN_PASSWORD_LENGTH = 6

@strawberry.type
class Query:
    @strawberry.field
    async def users(self, info: Info) -> List[UserType]:
        db: AsyncSession = info.context["db"]
        return await UserService.list_users(db)

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_user(
        self,
        info: Info,
        email: str,
        username: str,
        password: str
    ) -> UserType:
        db: AsyncSession = info.context["db"]

        if len(password) < MIN_PASSWORD_LENGTH:
            raise ValueError(f"Le mot de passe doit contenir au moins {MIN_PASSWORD_LENGTH} caractères")

        return await UserService.create_user(db, email, username, password)
