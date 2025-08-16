from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from api.apiv1.crud.post_crud import get_posts, post_create
from core.config import settings
from core.models import Post, User, db_helper
from core.schemas.PostSchema import PostRead, PostCreate
from auth.dependencies import get_current_user


router = APIRouter(prefix=settings.api.v1.post, tags=['Post'])


@router.get('', response_model=list[PostRead])
async def get_all_posts(
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(db_helper.session_getter)
):
    return await get_posts(
        session=session,
        user_id=current_user.id
    )


@router.post("", response_model=PostRead)
async def create_post(
        post_data: PostCreate,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(db_helper.session_getter)
):
    return await post_create(
        session=session,
        user_id=current_user.id,
        post_data=post_data
    )