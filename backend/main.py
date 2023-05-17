from typing import List

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pip._internal.cli.spinners import RateLimiter
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timedelta

from database import models, session
import auth
import docker
from config import Settings
from exceptions import *
from schemas import UserOut, TaskOut, UserCreate, Token

models.Base.metadata.create_all(bind=session.engine)

app = FastAPI()

SECRET_KEY = Settings.SECRET_KEY
ALGORITHM = Settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = Settings.ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(session.get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise AuthInvalidLogin()
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"user": user.id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/register", response_model=UserOut)
def register(user_data: UserCreate, db: Session = Depends(session.get_db)):
    user = db.query(models.User).filter_by(username=user_data.username).first()
    if user:
        raise AuthUserExists()
    new_user = models.User(
        username=user_data.username,
        email=user_data.email,
        password=auth.get_password_hash(user_data.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.put("/tasks/{task_id}/complete", status_code=status.HTTP_204_NO_CONTENT)
def complete_task(task_id: int, db: Session = Depends(session.get_db),
                  current_user: models.User = Depends(auth.get_current_user)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise TaskNotFound()

    user_task = db.execute(models.user_task_table.select().where(models.user_task_table.c.user_id == current_user.id,
                                                                 models.user_task_table.c.task_id == task_id)).first()
    if user_task:
        if user_task.completed == True:
            raise TaskMarked()
        else:
            db.execute(models.user_task_table.update().values(completed=True).where(
                models.user_task_table.c.user_id == current_user.id, models.user_task_table.c.task_id == task_id))
    else:
        db.execute(models.user_task_table.insert().values(user_id=current_user.id, task_id=task_id, completed=True))

    db.commit()
    return

@app.get("/tasks", response_model=List[TaskOut])
def read_tasks(current_user: models.User = Depends(auth.get_current_user), skip: int = 0, limit: int = 100, db: Session = Depends(session.get_db)):
    tasks = db.query(models.Task).offset(skip).limit(limit).all()
    for task in tasks:
        task.completed = task in current_user.tasks
    return tasks


@app.post("/run_code")
async def run_code(code: models.Code, db: Session = Depends(session.get_db), current_user: models.User = Depends(auth.get_current_user)):
    user = db.query(models.User).filter_by(username=current_user.username).first()
    if user.last_code_runtime and user.last_code_runtime > datetime.utcnow() - timedelta(seconds=5):
        raise CodeWait()

    client = docker.from_env()

    user.last_code_runtime = datetime.utcnow()
    db.commit()

    try:
        container = client.containers.run(
            'python-sandbox',
            command=['python', '-c', code.code],
            remove=True,
            mem_limit='512m',  # Ограничение использования памяти
            pids_limit=100,  # Ограничение на количество процессов
            network_disabled=True,  # Отключение сети
            read_only=True,  # Файловая система только для чтения
            cap_drop=['all'],  # Удаление всех Linux capabilities
            security_opt=['no-new-privileges'],  # Запрет повышения привилегий
        )
        return {'output': container.decode('utf-8')}
    except docker.errors.ContainerError as e:
        raise HTTPException(status_code=400, detail=str(e.stderr.decode('utf-8')))