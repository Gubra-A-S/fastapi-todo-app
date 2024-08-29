from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine
from sql_app.auth import create_access_token, verify_token, Token, TokenData

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
    if form_data.username == "userok" and form_data.password == "test1234":
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
