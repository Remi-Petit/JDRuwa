from sqlalchemy.ext.asyncio import AsyncSession
from app.db.repositories.user_repo import UserRepository
from app.validations import UserValidator, ValidationError

class UserService:
    @staticmethod
    async def list_users(db: AsyncSession):
        return await UserRepository.get_all(db)

    @staticmethod
    async def create_user(db: AsyncSession, email: str, username: str, password: str):
        """
        Crée un utilisateur avec validations de sécurité renforcées
        Le hashage du mot de passe est maintenant géré automatiquement par le modèle User
        """
        # Validation complète des données utilisateur
        try:
            UserValidator.validate_user_creation(email, username, password)
        except ValidationError as e:
            raise ValueError(str(e))
        
        # Vérification que l'email n'existe pas déjà
        existing_email = await UserRepository.get_by_email(db, email)
        if existing_email:
            raise ValueError("Un utilisateur avec cet email existe déjà")
        
        # Vérification que le nom d'utilisateur n'existe pas déjà
        existing_username = await UserRepository.get_by_username(db, username)
        if existing_username:
            raise ValueError("Ce nom d'utilisateur est déjà pris")
        
        # Création de l'utilisateur - le mot de passe sera hashé automatiquement
        return await UserRepository.create(db, email, username, password)
