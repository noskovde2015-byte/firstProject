from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from enum import Enum
from core.models.base import Base

if TYPE_CHECKING:
    from .User import User






class Post(Base):
    __tablename__ = 'posts'

    title: Mapped[str]
    body: Mapped[str]
    priority: Mapped[str] = mapped_column(default="medium")
    category: Mapped[str] = mapped_column(default="general")
    is_active: Mapped[bool] = mapped_column(nullable=True, default=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped["User"] = relationship(back_populates="posts")