from typing import List
from pydantic import BaseModel

class Test(BaseModel):
    id: int
    input_data: List[str]
    correct_answer: List[str]

    class Config:
        orm_mode = True

class TaskOut(BaseModel):
    id: int
    title: str
    description: str
    completed: bool
    tests: List[Test] = []

    class Config:
        orm_mode = True

class UserOut(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
