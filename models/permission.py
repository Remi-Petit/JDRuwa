from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .base import Base
from .associations import role_permission

class Permission(Base):
    __tablename__ = "permissions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    roles: Mapped[list["Role"]] = relationship(
        "Role", secondary=role_permission, back_populates="permissions"
    )