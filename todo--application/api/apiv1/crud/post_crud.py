from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import Post
from core.schemas.PostSchema import PostCreate
from sqlalchemy import select, Result, Sequence
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
