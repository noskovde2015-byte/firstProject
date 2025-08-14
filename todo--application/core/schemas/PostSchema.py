from pydantic import BaseModel, ConfigDict

class PostBase(BaseModel):
    title: str
    body: str
    is_active: bool = True


class PostCreate(PostBase):
    pass


class PostRead(PostBase):
    id: int
    user_id: int
    model_config = ConfigDict(
        from_attributes=True
    )