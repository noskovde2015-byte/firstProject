from enum import Enum

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


class PostRead(PostBase):
    id: int
    user_id: int
    model_config = ConfigDict(
        from_attributes=True
    )