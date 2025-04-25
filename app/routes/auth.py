from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserLogin, TokenResponse
from app.services import auth_service
from app.db.session import SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/signup", response_model=TokenResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    new_user = auth_service.create_user(db, user)
    token = auth_service.create_token_for_user(new_user.id)
    return {"access_token": token}


@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    user_obj = auth_service.authenticate_user(db, user.email, user.password)
    token = auth_service.create_token_for_user(user_obj.id)
    return {"access_token": token}
