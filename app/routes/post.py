from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.post import PostCreate, PostResponse
from app.services import post_service
from app.auth.dependencies import get_current_user
from app.cache.cache import is_cache_valid
from typing import List

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


MAX_PAYLOAD_SIZE = 1024 * 1024  # 1 MB


@router.post("/add", response_model=PostResponse)
async def add_post(request: Request,
                   post: PostCreate,
                   user_id: int = Depends(get_current_user),
                   db: Session = Depends(get_db)):
    body = await request.body()
    if len(body) > MAX_PAYLOAD_SIZE:
        raise HTTPException(status_code=413, detail="Payload too large")

    new_post = post_service.add_post(db, user_id, post)
    return new_post


@router.get("/all", response_model=List[PostResponse])
def get_posts(user_id: int = Depends(get_current_user),
              db: Session = Depends(get_db)):
    if is_cache_valid(user_id):
        return post_service.get_user_posts(db, user_id)

    return post_service.get_user_posts(db, user_id)


@router.delete("/delete/{post_id}")
def delete_post(post_id: int,
                user_id: int = Depends(get_current_user),
                db: Session = Depends(get_db)):
    try:
        post_service.delete_post(db, post_id, user_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

    return {"message": "Post deleted successfully."}
