from sqlalchemy.orm import Session
from database import models


def get_user(db: Session, id: int):
    return db.query(models.User).filter(models.User.id == id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_tests(db: Session):
    return db.query(models.Test).all()