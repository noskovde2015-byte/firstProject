from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class PostBase(BaseModel):
    title: str
    body: str
    is_active: bool = True
    priority: Priority = Priority.MEDIUM
    category: str = Field(default="general", max_length=50)


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: str | None = None
    body: str | None = None
    is_active: bool | None = None
    priority: Priority | None = None
    category: str | None = None


class PostRead(PostBase):
    id: int
    user_id: int
    model_config = ConfigDict(
        from_attributes=True
    )