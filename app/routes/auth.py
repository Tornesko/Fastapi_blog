from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserLogin, TokenResponse
from app.services import auth_service
from app.db.session import SessionLocal

router = APIRouter()


async def get_db():
    async with SessionLocal() as session:
        yield session


@router.post("/signup")
async def signup(user: UserCreate, db: AsyncSession = Depends(get_db)):
    new_user = await auth_service.create_user(db, user)
    token = auth_service.create_token_for_user(new_user.id)
    return {"access_token": token}


@router.post("/login", response_model=TokenResponse)
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    user_obj = await auth_service.authenticate_user(db, user.email, user.password)
    token = auth_service.create_token_for_user(user_obj.id)
    return {"access_token": token}
