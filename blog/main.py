from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import models, database, schemas, crud

app = FastAPI()

# @app.post('/blogapp')
# def blogapp(title):
#     return title


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