from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.user import UserCreate
from app.auth.jwt import create_access_token
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(
        select(User).where(User.email == email)
    )
    return result.scalars().first()


async def create_user(db: AsyncSession, user_data: UserCreate):
    user = await get_user_by_email(db, user_data.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )

    hashed_password = pwd_context.hash(user_data.password)
    new_user = User(email=user_data.email, password=hashed_password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user



async def authenticate_user(db: AsyncSession, email: str, password: str):
    user = await get_user_by_email(db, email)
    if not user:
        return None
    if not pwd_context.verify(password, user.password):
        return None
    return user


def create_token_for_user(user_id: int):
    return create_access_token(data={"sub": str(user_id)})
