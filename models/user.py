# models/user.py
from datetime import datetime, timedelta
from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .associations import user_role
from passlib.context import CryptContext
from jose import jwt
from config.env import get_settings

from .base import Base

settings = get_settings()

_pwd_ctx = CryptContext(schemes=["argon2"], deprecated="auto")

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    roles: Mapped[list["Role"]] = relationship(
        "Role", secondary=user_role, back_populates="users"
    )

    @property
    def password(self) -> str:
        raise AttributeError("password is write-only")

    @password.setter
    def password(self, raw: str) -> None:
        if not raw or len(raw) < 8:
            raise ValueError("Le mot de passe doit contenir au moins 8 caractères.")
        self.password_hash = _pwd_ctx.hash(raw)

    def verify_password(self, raw: str) -> bool:
        return _pwd_ctx.verify(raw, self.password_hash)
    
    def generate_jwt(self) -> str:
        """Génère un JWT pour cet utilisateur."""
        expires = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {
            "sub": str(self.id),
            "email": self.email,
            "username": self.username,
            "exp": expires,
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)