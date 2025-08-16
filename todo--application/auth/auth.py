from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result
from core.config import settings
from core.models import User


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) ->str:
    return pwd_context.hash(password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.auth.ACCESS_TOKEN_EXPIRE)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.auth.SECRET_KEY, algorithm=settings.auth.ALGORITHM)


async def authenticate_user(email: str, password: str, session: AsyncSession):
    stmt = select(User).where(User.email == email)
    result: Result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if not user or not verify_password(plain_password=password,hashed_password=user.password):
        return None
    return user