import os
from dotenv import load_dotenv

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine
from sql_app.auth import create_access_token, verify_token, Token, TokenData

load_dotenv()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8080",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/token", response_model=Token)
def login(form_data: schemas.Login):
    """
    Endpoint to get a token for authentication.

    Accepts a POST with a `schemas.Login` object as the body.
    Returns a `Token` object with the `access_token` and `token_type` fields.
    Raises a `HTTPException` with a 401 status code if the credentials are incorrect.
    """
    valid_username = os.getenv("VALID_USERNAME")
    valid_password = os.getenv("VALID_PASSWORD")

    if form_data.username == valid_username and form_data.password == valid_password:
        access_token = create_access_token(data={"sub": form_data.username})
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

@app.get("/todos")
def read_todos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), token: str = Depends(verify_token)):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    todos = crud.get_todos(db, skip, limit)
    return todos

@app.post("/todos")
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db), token: str = Depends(verify_token)):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    db_todo = crud.create_todo(db, todo)
    return db_todo

@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, done: bool, db: Session = Depends(get_db), token: str = Depends(verify_token)):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    db_todo = crud.update_todo(db, todo_id, done)
    return db_todo
