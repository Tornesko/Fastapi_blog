from sqlalchemy.orm import Session
from app.models.post import Post
from app.schemas.post import PostCreate
from typing import List
from app.cache.cache import cache


def add_post(db: Session, user_id: int, post_data: PostCreate) -> Post:
    post = Post(text=post_data.text, user_id=user_id)
    db.add(post)
    db.commit()
    db.refresh(post)

    cache.pop(user_id, None)
    return post


def get_user_posts(db: Session, user_id: int) -> List[Post]:
    if user_id in cache:
        return cache[user_id]["data"]

    posts = db.query(Post).filter(Post.user_id == user_id).all()
    cache[user_id] = {
        "data": posts,
        "timestamp": __import__("datetime").datetime.utcnow()
    }
    return posts


def delete_post(db: Session, post_id: int, user_id: int):
    post = db.query(Post).filter(Post.id == post_id, Post.user_id == user_id).first()
    if not post:
        raise Exception("Post not found or access denied.")

    db.delete(post)
    db.commit()

    cache.pop(user_id, None)
