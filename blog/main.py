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

@app.post('/blogapp')
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    print(request)
    new_blog = models.Blogs(title = request.title, body = request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get('/blogapp')
def blogapp():
    return 'salam'


# @app.post("/users/")
# def create_user(user: models.User, db: Session = Depends(database.SessionLocal)):
#     return crud.create_user(db=db, user=user)


# @app.post("/users/")
# def create_user(user: schemas.UserCreate, db: Session = Depends(database.SessionLocal)):
#     return crud.create_user(db=db, user=user)


@app.on_event("startup")
async def startup():
    models.Base.metadata.create_all(bind=database.engine)