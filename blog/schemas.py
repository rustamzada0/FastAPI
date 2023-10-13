from pydantic import BaseModel
from typing import Optional, List

class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool] = None
    user_id: int


class User(BaseModel):
    name: str
    email: str
    password: str


class ShowUser(BaseModel):
    name: str
    email: str
    blogs: List[Blog]

    class Config:
            orm_mode = True


class ShowBlog(BaseModel):
    title: str
    creator: ShowUser

    class Config:
            orm_mode = True