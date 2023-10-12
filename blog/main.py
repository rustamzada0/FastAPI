from fastapi import FastAPI, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from typing import List
from passlib.context import CryptContext
from . import models, database, schemas

app = FastAPI()

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = database.SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get('/blogapp')
def blogapp():
    return 'salam'


@app.get('/blogs', response_model=List[schemas.ShowBlog])
def get_all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blogs).all()
    print(blogs)
    return blogs


@app.get('/blog/{id}', status_code=200, response_model=schemas.ShowBlog)
def show_blog(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blogs).filter(models.Blogs.id == id).first()
    print(blog.title, blog.body)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"is not available")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail': 'is not available'}
    
    return blog


@app.get('/user/{id}', status_code=200, response_model=schemas.ShowUser)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id {id} is not available")
    
    return user


@app.post('/blogapp', status_code=status.HTTP_201_CREATED)
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    print(request)
    new_blog = models.Blogs(title = request.title, body = request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.post('/user', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    hashed_password = pwd_cxt.hash(request.password)
    new_user = models.User(name = request.name, email = request.email, password = hashed_password)
    # new_user = models.User(request)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db)):
    print(db)
    db.query(models.Blogs).filter(models.Blogs.id == id).delete(synchronize_session=False)
    db.commit()
    return 'done'


@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    print(request)
    blog = db.query(models.Blogs).filter(models.Blogs.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    # blog.update(title = request.title, body = request.body)
    blog.update(request)
    db.commit()
    return 'update!'


@app.on_event("startup")
async def startup():
    models.Base.metadata.create_all(bind=database.engine)