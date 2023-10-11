from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool] = None


@app.get("/")
def index():
    return {"Hello": "World"}


@app.get("/about/{id}")
def about(id: int):
    return {"data": id}


@app.get("/blog")
def home(limit=10, published: bool=True, sort: Optional[str] = None):
    if published:
        return {'data': f'{limit} published blogs from the db'}
    else:
        return {'data': f'{limit} blogs from the db' }


@app.post("/blog")
def create_blog(request: Blog):
    return {'data': request}
    