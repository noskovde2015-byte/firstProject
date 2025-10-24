from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_409_CONFLICT
from core.logger_settings.logger import logger
from core.models import db_helper, User, Role
from core.config import settings, ApiV1Prefix
from core.schemas.UserSchema import UserCreate
from sqlalchemy import select
from auth.auth import hash_password




router = APIRouter(prefix=settings.api.v1.reg, tags=["Auth"])


@router.post("")
async def register_api(
        user_data: UserCreate,
        session: AsyncSession = Depends(db_helper.session_getter)
) -> dict:

    logger.info("Регистрация нового пользователя")
    try:
        user = await session.scalar(
            select(User).where(User.email == user_data.email)
        )

        if user is not None:
            logger.warning("Попытка регистрации существующего email")
            raise HTTPException(status_code=HTTP_409_CONFLICT, detail="Email already registered")


        user_role = await session.scalar(
            select(Role).where(Role.name == "user")
        )

        if not user_role:
            user_role = Role(
                name = "user",
                permissions = {"message": "not all root"}
            )
        session.add(user_role)
        await session.commit()
        await session.refresh(user_role)


        new_user = User(
            email=user_data.email,
            name=user_data.name,
            password=hash_password(user_data.password),
            age=user_data.age,
            role_id=user_role.id,
        )

        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        logger.info(f"Пользователь {new_user.email} успешно зарегистрирован")
        return {"message": "User registered"}

    except ValidationError as e:
        logger.error(f"Ошибка валидации данных: {e.errors()}")
        raise HTTPException(
            status_code=422,
            detail=e.errors()
        )