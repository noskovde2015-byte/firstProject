from pydantic import BaseModel, ConfigDict, Field
from core.models.Post import Priority

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