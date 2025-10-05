from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .base import Base
from .associations import user_role, role_permission

class Role(Base):
    __tablename__ = "roles"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    permissions: Mapped[list["Permission"]] = relationship(
        "Permission", secondary=role_permission, back_populates="roles"
    )
    users: Mapped[list["User"]] = relationship(
        "User", secondary=user_role, back_populates="roles"
    )