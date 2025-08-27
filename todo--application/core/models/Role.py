from sqlalchemy import Column, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from core.models.base import Base


if TYPE_CHECKING:
    from .User import User



class Role(Base):
    __tablename__ = 'roles'
    __table_args__ = (
        {'extend_existing': True},
    )
    name: Mapped[str] = mapped_column(unique=True)
    permissions: Mapped[dict] = mapped_column(JSON, default={})
    users: Mapped[list["User"]] = relationship(back_populates="role")
