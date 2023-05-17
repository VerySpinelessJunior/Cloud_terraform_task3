from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Table, ForeignKey, Boolean, ARRAY, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

user_task_table = Table(
    'user_task', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('task_id', Integer, ForeignKey('tasks.id')),
    Column('completed', Boolean, default=False)
)

class Code(BaseModel):
    code: str

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    tasks = relationship("Task", secondary=user_task_table, back_populates="users")
    last_code_runtime = Column(DateTime, default=datetime.utcnow)

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    users = relationship("User", secondary=user_task_table, back_populates="tasks")
    tests = relationship("Test", backref="task")

class Test(Base):
    __tablename__ = "tests"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    input_data = Column(ARRAY(String))
    correct_answer = Column(ARRAY(String))
