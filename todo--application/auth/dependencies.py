from datetime import datetime, timezone

from fastapi import Request, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_409_CONFLICT, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND
from jose import jwt, JWTError
from core.models import db_helper, User
from core.config import settings



async def get_current_user(request: Request,session: AsyncSession = Depends(db_helper.session_getter)) -> User:
    token = request.cookies.get('user_access_token')

    if not token:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = jwt.decode(token, settings.auth.SECRET_KEY, algorithms=[settings.auth.ALGORITHM])

        expire = payload.get('exp')
        if not expire or datetime.fromtimestamp(expire, tz=timezone.utc) < datetime.now(timezone.utc):
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Срок действия токена истек",
                headers={"WWW-Authenticate": "Bearer"},
            )


        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Неверный формат токена",
                headers={"WWW-Authenticate": "Bearer"},
            )
        user = await session.get(User, int(user_id))

        if not user:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail="Пользователь не найден"
            )
        return user

    except (JWTError, ValueError) as e:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Неверный токен",
            headers={"WWW-Authenticate": "Bearer"},
        )