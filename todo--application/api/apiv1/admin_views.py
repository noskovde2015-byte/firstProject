from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
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


    target_user = await session.get(User, user_id)
    if not target_user:
        raise HTTPException(status_code=404,
                            detail="User not found")

    admin_role = await session.scalar(select(Role).where(Role.name == "admin"))
    if not admin_role:
        raise HTTPException(status_code=500, detail="Admin role not found")

    if target_user.role.name == "admin":
        raise HTTPException(status_code=403,
                            detail="User is an admin")


    target_user.role = admin_role
    await session.commit()

    return {"message": f"User {target_user.email} is now admin"}




