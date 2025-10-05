# models/user.py
from datetime import datetime
from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from passlib.context import CryptContext

from .base import Base

_pwd_ctx = CryptContext(schemes=["argon2"], deprecated="auto")

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

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