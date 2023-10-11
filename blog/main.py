from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import models, database, schemas, crud

app = FastAPI()


def get_db():
    db = database.SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get('/blogapp')
def blogapp():
    return 'salam'


@app.post('/blogapp')
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    print(request)
    new_blog = models.Blogs(title = request.title, body = request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get('/blogs')
def get_all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blogs).all()
    print(blogs)
    return blogs


@app.get('/blog/{id}')
def show_blog(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blogs).filter(models.Blogs.id == id).first()
    print(blog)
    return blog


@app.on_event("startup")
async def startup():
    models.Base.metadata.create_all(bind=database.engine)