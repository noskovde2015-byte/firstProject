from fastapi import HTTPException
from pydantic import BaseModel, ConfigDict, EmailStr, field_validator, Field

class UserBase(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    email: EmailStr
    age: int = Field(ge=18, le=110)

class UserCreate(UserBase):
    password: str = Field(min_length=6, max_length=50)

    @field_validator("password", mode="before")
    def validate_password(cls, v):
        v = v.strip()

        if len(v) < 6:
            raise HTTPException(status_code=400, detail="Password must be at least 6 characters long")
        return v


class UserRead(UserBase):
    model_config = ConfigDict(
        from_attributes=True
    )
    id: int


