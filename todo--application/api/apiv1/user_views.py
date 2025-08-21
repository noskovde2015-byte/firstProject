from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import db_helper
from core.config import settings
from core.schemas.UserSchema import UserRead
from api.apiv1.crud.user_crud import get_all_user
from core.models import User
from auth.dependencies import get_current_user


router = APIRouter(prefix=settings.api.v1.user, tags=["User"])


@router.get("", response_model=list[UserRead])
async def get_users(
        admin: User = Depends(get_current_user),
        session: AsyncSession = Depends(db_helper.session_getter)):

    await session.refresh(admin, ["role"])
    if admin.role.name != "admin":
        raise HTTPException(
            status_code=403,
            detail="Недостаточно прав",
        )
    return await get_all_user(session=session)