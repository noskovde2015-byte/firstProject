from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import db_helper
from core.config import settings
from core.schemas.UserSchema import UserRead
from api.apiv1.crud.user_crud import get_all_user, delete_user
from core.models import User
from auth.dependencies import get_current_user
from core.logger_settings.logger import logger



router = APIRouter(prefix=settings.api.v1.user, tags=["User"])


@router.get("", response_model=list[UserRead])
async def get_users(
        admin: User = Depends(get_current_user),
        session: AsyncSession = Depends(db_helper.session_getter)):

    logger.info(f"Запрос пользователей от {admin.email}")

    await session.refresh(admin, ["role"])
    if admin.role.name != "admin":
        logger.warning(f"Попытка доступа без прав от {admin.email}")
        raise HTTPException(
            status_code=403,
            detail="Недостаточно прав",
        )
    logger.info(f"{admin.email} вывел список всех пользователей")
    return await get_all_user(session=session)


@router.delete("/delete")
async def delete_user_router(
        user_id: int,
        session: AsyncSession = Depends(db_helper.session_getter),
        current_user: User = Depends(get_current_user),
):
    logger.info(f"Запрос на удаление пользователя {user_id} от {current_user.email}")
    await session.refresh(current_user, ["role"])

    if current_user.role.name != "admin":
        logger.warning(f"Попытка удаления без прав от {current_user.email}")
        raise HTTPException(
            status_code=403,
            detail="You are not an admin")


    return await delete_user(
        session=session,
        current_user_id=current_user.id,
        user_id=user_id,
    )