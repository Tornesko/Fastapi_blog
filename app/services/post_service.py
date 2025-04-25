from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.post import Post
from app.schemas.post import PostCreate
from typing import List
from app.cache.cache import cache


async def add_post(db: AsyncSession, user_id: int, post_data: PostCreate) -> Post:
    post = Post(text=post_data.text, user_id=user_id)
    db.add(post)
    await db.commit()
    await db.refresh(post)

    cache.pop(user_id, None)
    return post


async def get_user_posts(db: AsyncSession, user_id: int) -> List[Post]:
    if user_id in cache:
        return cache[user_id]["data"]

    result = await db.execute(
        select(Post).where(Post.user_id == user_id)
    )
    posts = result.scalars().all()
    cache[user_id] = {
        "data": posts,
        "timestamp": __import__("datetime").datetime.utcnow()
    }
    return posts


async def delete_post(db: AsyncSession, post_id: int, user_id: int):
    result = await db.execute(
        select(Post).where(Post.id == post_id, Post.user_id == user_id)
    )
    post = result.scalars().first()

    if not post:
        raise Exception("Post not found or access denied.")

    await db.delete(post)
    await db.commit()

    cache.pop(user_id, None)
