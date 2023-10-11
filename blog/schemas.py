from pydantic import BaseModel
from typing import Optional

class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool] = None


class UserCreate(BaseModel):
    username: str
    email: str
    full_name: str
