from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import db_helper
from core.config import settings
from core.schemas.UserSchema import UserRead
from api.apiv1.crud.user_crud import get_all_user


router = APIRouter(prefix=settings.api.v1.user, tags=["User"])


@router.get("", response_model=list[UserRead])
async def get_users(session: AsyncSession = Depends(db_helper.session_getter)):
    return await get_all_user(session=session)