from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import Post
from core.schemas.PostSchema import PostCreate, PostUpdate
from sqlalchemy import select, Result, Sequence, delete
from core.logger_settings.logger import logger



async def post_create(
        session: AsyncSession,
        post_data: PostCreate,
        user_id: int
) -> Post:

    post_dict = post_data.model_dump()
    post_dict["priority"] = post_dict["priority"].value

    post = Post(
        **post_dict,
        user_id=user_id
    )

    session.add(post)
    await session.commit()
    await session.refresh(post)
    return post



async def get_posts(session: AsyncSession, user_id: int, categories: str | None = None) -> list[Post]:
    stmt = select(Post).where(Post.user_id == user_id)
    if categories:
        stmt = stmt.where(Post.category == categories)


    result: Result = await session.execute(stmt)
    posts = result.scalars().all()
    return list(posts)




async def check_posts(
        session: AsyncSession
) -> Sequence[Post]:
    stmt = select(Post).order_by(Post.id)
    result: Result = await session.execute(stmt)
    posts = result.scalars().all()
    return posts


async def get_post_by_category(session: AsyncSession,user_id: int, category_name: str) -> list[Post]:
    stmt = select(Post).where(Post.user_id == user_id,Post.category == category_name)
    result: Result = await session.execute(stmt)
    posts = result.scalars().all()

    if not posts:
        logger.warning(f"Поиск по несущуствующей категории {category_name}")
        raise HTTPException(status_code=404, detail="Post not found")

    return list(posts)


async def delete_post(
        session: AsyncSession,
        post_id: int,
        user_id: int,
):
    logger.info(f"Удаление поста {post_id}")

    stmt = select(Post).where(Post.id == post_id)
    result: Result = await session.execute(stmt)
    post = result.scalar_one_or_none()

    if not post:
        logger.warning(f"Пост {post_id} не найден")
        raise HTTPException(status_code=404, detail="Post not found")

    if post.user_id != user_id:
        logger.warning(f"Попытка удаления не своего поста от {post.user_id}")
        raise HTTPException(status_code=403, detail="Нельзя удалить не свой пост")

    await session.delete(post)
    await session.commit()
    logger.info(f"Пост {post_id} успешно удален")

    return {
        "message": "Post deleted successfully",
        "post_id": post_id,
        "title": post.title,
    }


async def update_post(
        session: AsyncSession,
        post_id: int,
        post_data: PostUpdate,
        user_id: int,
):
    logger.info(f"Обновление поста {post_id} пользователем {user_id}")

    stmt = select(Post).where(Post.id == post_id)
    result: Result = await session.execute(stmt)
    post = result.scalar_one_or_none()

    if not post:
        logger.warning(f"Пост {post_id} не найден для обновления")
        raise HTTPException(status_code=404, detail="Post not found")

    if post.user_id != user_id:
        logger.warning(f"Попытка обновления не своего поста от {post.user_id}")
        raise HTTPException(status_code=403, detail="Нельзя удалить не свой пост")

    update_dict = post_data.model_dump(exclude_unset=True)

    if 'priority' in update_dict and update_dict['priority'] is not None:
        update_dict['priority'] = update_dict['priority'].value

    for key, value in update_dict.items():
        setattr(post, key, value)

    session.add(post)
    await session.commit()
    await session.refresh(post)

    logger.info(f"Пост {post_id} успешно обновлен пользователем {user_id}")

    return post


async def active_post(
        session: AsyncSession,
        user_id: int,
):
    stmt = select(Post).where(Post.user_id == user_id, Post.is_active == True)
    result: Result = await session.execute(stmt)
    posts = result.scalars().all()
    return list(posts)

