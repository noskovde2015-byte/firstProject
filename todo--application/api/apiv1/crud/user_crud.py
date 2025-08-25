from fastapi import HTTPException
from sqlalchemy import Result, select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import user
from core.logger_settings.logger import logger
from core.models import User, Post


async def get_all_user(session: AsyncSession) -> list[User]:
    stmt = select(User).order_by(User.id)
    result: Result = await session.execute(stmt)
    users = result.scalars().all()
    return list(users)


async def delete_user(session: AsyncSession, user_id: int, current_user_id: int):
    if user_id == current_user_id:
        logger.warning(f"Попытка удаления самого себя")
        raise HTTPException(
            status_code=403,
            detail="You can not delete yourself"
        )

    stmt_user = select(User).where(User.id == user_id)
    user_result: Result = await session.execute(stmt_user)
    users = user_result.scalar_one_or_none()


    if not users:
        logger.warning(f"Пользователь не найден")
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )


    stmt_post = select(Post).where(Post.user_id == user_id)
    result: Result = await session.execute(stmt_post)
    users_post = result.scalars().all()


    for post in users_post:
        await session.delete(post)


    user_email = users.email


    await session.delete(users)
    await session.commit()

    logger.info(f"Пользователь успешно удален")
    return {
        "message": "User deleted",
        "user_id": user_id,
        "user_email": user_email,
    }


