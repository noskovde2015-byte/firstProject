from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column
from typing import TYPE_CHECKING
from core.models.base import Base

if TYPE_CHECKING:
    from .Post import Post
    from .Role import Role


class User(Base):
    __tablename__ = 'users'
    name: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]
    age: Mapped[int]
    role_id: Mapped[int] = mapped_column(ForeignKey('roles.id'))
    posts: Mapped[list["Post"]] = relationship(back_populates="user")
    role: Mapped["Role"] = relationship(back_populates="users")




