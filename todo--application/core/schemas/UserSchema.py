from pydantic import BaseModel, ConfigDict

class UserBase(BaseModel):
    name: str
    email: str
    age: int

class UserCreate(UserBase):
    email: str


class UserRead(UserBase):
    model_config = ConfigDict(
        from_attributes=True
    )
    id: int


