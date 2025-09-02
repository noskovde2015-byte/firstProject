from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from core.logger_settings.logger import logger
from core.config import settings
from core.models import User, Role
from auth.dependencies import get_current_user
from core.models import db_helper
from sqlalchemy import select

from core.schemas.UserSchema import UserRead

router = APIRouter(prefix=settings.api.v1.adminka, tags=["Admin"])

@router.post("")
async def make_admin(
        user_id: int,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(db_helper.session_getter)
):
    logger.info(f"Назначение нового пользователя админом")

    await session.refresh(current_user, ["role"])
    if current_user.role.name != "admin":
        logger.warning(f"Попытка назначения админом без прав от {current_user.email}")
        raise HTTPException(
            status_code=403,
            detail="You are not an admin"
        )

    stmt = select(User).options(selectinload(User.role)).where(User.id == user_id)
    result = await session.execute(stmt)
    target_user = result.scalar_one_or_none()

    if not target_user:
        logger.warning(f"Пользователя не существует")
        raise HTTPException(status_code=404, detail="User not found")


    stmt_role = select(Role).where(Role.name == "admin")
    result_role = await session.execute(stmt_role)
    admin_role = result_role.scalar_one_or_none()

    if not admin_role:
        logger.warning(f"Попытка присвоение несуществующей роли")
        raise HTTPException(status_code=500, detail="Admin role not found")


    if target_user.role.name == "admin":
        logger.warning(f"Попытка назначения админом админа")
        raise HTTPException(status_code=403, detail="User is already admin")

    target_user.role = admin_role
    await session.commit()

    logger.info(f"Пользоваетель {target_user.email} теперь админ")
    return {"message": f"User {target_user.email} is now admin"}


@router.post("/remove")
async def remove_admin(
        user_id: int,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(db_helper.session_getter)
):
    logger.info(f"Снятие админки")
    await session.refresh(current_user, ["role"])

    if current_user.role.name != "admin":
        logger.warning(f"Попытка снятия админки без прав")
        raise HTTPException(
            status_code=403,
            detail="You are not an admin")


    target_user = await session.get(User, user_id)
    if not target_user:
        logger.warning(f"Попытка снятия админки с несуществующего пользователя")
        raise HTTPException(status_code=404,
                            detail="User not found")

    user_role = await session.scalar(select(Role).where(Role.name == "user"))
    if not user_role:
        logger.warning(f"Несуществующая роль")
        raise HTTPException(status_code=500,
                            detail="User role not found")

    if target_user.role.name == "user":
        logger.warning(f"Пользователь уже является user")
        raise HTTPException(status_code=403,
                            detail="User is a user")

    target_user.role = user_role
    await session.commit()
    logger.info(f"Пользователь {target_user.email} тепепь user")
    return {"message": f"User {target_user.email} is now user"}


@router.get("/me")
async def get_current_user_info(
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(db_helper.session_getter)
) -> dict:
    user_data = {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "age": current_user.age,
        "role_id": current_user.role_id
    }

    return user_data





