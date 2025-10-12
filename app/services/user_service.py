from passlib.hash import argon2
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.repositories.user_repo import UserRepository

class UserService:
    @staticmethod
    async def list_users(db: AsyncSession):
        return await UserRepository.get_all(db)

    @staticmethod
    async def create_user(db: AsyncSession, email: str, username: str, password: str):
        """
        Crée un utilisateur avec mot de passe haché via Argon2
        """
        # Argon2 n'a pas de limite comme bcrypt
        hashed = argon2.hash(password)
        return await UserRepository.create(db, email, username, hashed)

    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """
        Vérifie un mot de passe contre son hash Argon2
        """
        return argon2.verify(password, hashed)
