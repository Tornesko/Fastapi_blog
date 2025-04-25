from fastapi import FastAPI
from app.routes import auth, post

app = FastAPI(title="MVC FastAPI App")

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(post.router, prefix="/posts", tags=["Posts"])
