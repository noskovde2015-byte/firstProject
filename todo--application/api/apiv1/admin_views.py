from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.config import settings
from core.models import User, Role
from auth.dependencies import get_current_user
from core.models import db_helper
from sqlalchemy import select


router = APIRouter(prefix=settings.api.v1.adminka, tags=["Admin"])

@router.post("")
async def make_admin(
        user_id: int,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(db_helper.session_getter)
):
    await session.refresh(current_user, ["role"])
    if current_user.role.name != "admin":
        raise HTTPException(
            status_code=403,
            detail="You are not an admin"
        )

    stmt = select(User).options(selectinload(User.role)).where(User.id == user_id)
    result = await session.execute(stmt)
    target_user = result.scalar_one_or_none()

    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")


    stmt_role = select(Role).where(Role.name == "admin")
    result_role = await session.execute(stmt_role)
    admin_role = result_role.scalar_one_or_none()

    if not admin_role:
        raise HTTPException(status_code=500, detail="Admin role not found")


    if target_user.role.name == "admin":
        raise HTTPException(status_code=403, detail="User is already admin")

    target_user.role = admin_role
    await session.commit()

    return {"message": f"User {target_user.email} is now admin"}


@router.post("/remove")
async def remove_admin(
        user_id: int,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(db_helper.session_getter)
):
    await session.refresh(current_user, ["role"])

    if current_user.role.name != "admin":
        raise HTTPException(
            status_code=403,
            detail="You are not an admin")


    target_user = await session.get(User, user_id)
    if not target_user:
        raise HTTPException(status_code=404,
                            detail="User not found")

    user_role = await session.scalar(select(Role).where(Role.name == "user"))
    if not user_role:
        raise HTTPException(status_code=500,
                            detail="User role not found")

    if target_user.role.name == "user":
        raise HTTPException(status_code=403,
                            detail="User is a user")

    target_user.role = user_role
    await session.commit()
    return {"message": f"User {target_user.email} is now user"}





