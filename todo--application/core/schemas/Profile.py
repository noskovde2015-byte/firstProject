from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ProfileBase(BaseModel):
    name: str
    age: Optional[int] = None
    post_count: Optional[int] = 0
    avatar_url: Optional[str] = None
    email: str
    created_at: Optional[datetime] = None


class ProfileCreate(ProfileBase):
    pass


class ProfileRead(ProfileBase):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int


