from typing import Callable

from fastapi import Request, HTTPException
from jose import jwt, JWTError
from starlette import status

from core.config import settings

async def aut_middleware(
    request: Request,
    call_next: Callable,
):
    public_paths = [
        "/docs",
        "/",
        "/redoc",
        "/openapi.json",
        "/auth/login",
        "/auth/register",
        "/api/v1/register",
        "/api/v1/login"
    ]


    if request.method == "OPTIONS" or request.url.path in public_paths:
        return await call_next(request)

    token = request.cookies.get("user_access_token")
    if not token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, settings.auth.SECRET_KEY, algorithms=[settings.auth.ALGORITHM])
        request.state.user_id = payload["sub"]

        if "sub" not in payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный формат токена"

            )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невалидный токен"
        )
    return await call_next(request)

