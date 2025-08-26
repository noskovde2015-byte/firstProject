from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession, async_object_session
from sqlalchemy.orm import object_session

from api.apiv1.crud.post_crud import get_posts, post_create, check_posts, get_post_by_category, delete_post, update_post
from core.config import settings
from core.models import Post, User, db_helper
from core.schemas.PostSchema import PostRead, PostCreate, PostUpdate
from auth.dependencies import get_current_user, get_current_admin
from core.logger_settings.logger import logger



router = APIRouter(prefix=settings.api.v1.post, tags=['Post'])


@router.get('', response_model=list[PostRead])
async def get_all_posts(
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(db_helper.session_getter)
):
    logger.info(f"Запрос своих постов от {current_user.email}")

    posts = await get_posts(
        session=session,
        user_id=current_user.id
    )
    logger.info(f"Вернулось {len(posts)} постов")
    return posts


@router.post("", response_model=PostRead)
async def create_post(
        post_data: PostCreate,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(db_helper.session_getter)
):
    logger.info(f"Создание нового поста от {current_user.email}")
    new_post =  await post_create(
        session=session,
        user_id=current_user.id,
        post_data=post_data
    )
    logger.info(f"Пользователь {current_user.email} успешно создал новый пост")
    return new_post


@router.get("/all_users_posts", response_model=list[PostRead])
async def aye(
        admin: User = Depends(get_current_user),
        session: AsyncSession = Depends(db_helper.session_getter)
):
    logger.info(f"Запрос всех постов от админа {admin.email}")
    await session.refresh(admin, ["role"])
    if admin.role.name != "admin":
        logger.warning(f"Попытка запроса без прав от {admin.email}")
        raise HTTPException(
            status_code=403,
            detail="You are not an admin"
        )

    posts = await check_posts(session=session)
    logger.info(f"Успешно возвращено {len(posts)} постов")
    return posts


@router.get("/by_categories", response_model=list[PostRead])
async def get_posts_by_categories(
        categories: str,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(db_helper.session_getter),
):
    logger.info(f"Запрос постов по категории {categories} от {current_user.email}")

    category_post =  await get_post_by_category(
        session=session,
        category_name=categories,
        user_id=current_user.id
    )
    logger.info(f"Выдано {len(category_post)} по категории {categories}")
    return category_post


@router.delete("")
async def del_post(
        post_id: int,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(db_helper.session_getter),
):
    logger.info(f"Запрос на удаление поста {post_id} от пользователя {current_user.email}")
    try:
        result = await delete_post(
            user_id=current_user.id,
            post_id=post_id,
            session=session,
        )
        logger.info(f"Пользователь {current_user.email} успешно удалил пост '{result['title']}'")
        return result

    except HTTPException as e:
        raise e

    except Exception as e:
        logger.error(
            f"Неожиданная ошибка при удалении поста {post_id} "
            f"пользователем {current_user.email}: {str(e)}"
        )
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )


@router.patch("", response_model=PostRead)
async def update_post_router(
        post_id: int,
        post_data: PostUpdate,
        session: AsyncSession = Depends(db_helper.session_getter),
        current_user: User = Depends(get_current_user),
):

    logger.info(
        f"Запрос на обновление поста {post_id} "
        f"от пользователя {current_user.email}"
    )

    try:
        result = await update_post(
            session=session,
            user_id=current_user.id,
            post_id=post_id,
            post_data=post_data,

        )

        logger.info(
            f"Пользователь {current_user.email} "
           f"успешно обновил пост '{result.title}'")

        return result

    except HTTPException as e:
        raise e

    except Exception as e:
        logger.error(
            f"Неожиданная ошибка при обновлении поста {post_id} "
            f"пользователем {current_user.email}: {str(e)}"
        )
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )
