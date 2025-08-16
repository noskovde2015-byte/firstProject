from sqlalchemy.ext.asyncio import AsyncSession
from core.models import Post
from core.schemas.PostSchema import PostCreate
from sqlalchemy import select, Result


async def post_create(
        session: AsyncSession,
        post_data: PostCreate,
        user_id: int
) -> Post:

    new_post = Post(**post_data.model_dump(), user_id=user_id)
    session.add(new_post)
    await session.commit()
    await session.refresh(new_post)
    return new_post

async def get_posts(session: AsyncSession, user_id: int) -> list[Post]:
    stmt = select(Post).where(Post.user_id == user_id)
    result: Result = await session.execute(stmt)
    posts = result.scalars().all()
    return list(posts)