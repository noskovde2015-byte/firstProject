from sqlalchemy.orm import Mapped, relationship
from typing import TYPE_CHECKING
from .base import Base
if TYPE_CHECKING:
    from .Post import Post

class User(Base):
    __tablename__ = 'users'
    name: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]
    age: Mapped[int]
    posts: Mapped[list["Post"]] = relationship(back_populates="user")




