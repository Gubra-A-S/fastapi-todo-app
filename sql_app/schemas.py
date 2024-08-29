from datetime import datetime
from pydantic import BaseModel


class TodoBase(BaseModel):
    content: str
    due: datetime


class TodoCreate(TodoBase):
    pass


class Todo(TodoBase):
    id: int
    done: bool = False

    class Config:
        orm_mode = True


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str
