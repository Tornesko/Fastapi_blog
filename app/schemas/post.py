from pydantic import BaseModel, constr


class PostCreate(BaseModel):
    text: constr(min_length=1, max_length=1024)


class PostResponse(BaseModel):
    id: int
    text: str

    class Config:
        orm_mode = True
