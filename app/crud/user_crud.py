from app.models import user_model
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from typing import Union
from app.api import deps

from fastapi import HTTPException, Depends, status
from sqlalchemy.orm.session import Session
from jose import jwt, JWTError
from app.schemas import user_schema as schemas
from app.models import user_model as models, post_model
from app.core.auth import oauth2_scheme
from app.core.security import get_password_hash


def get_user(db: Session, user_id: int):
    fields = [models.User.id, models.User.name,
              models.User.email, models.User.is_active]
    user = db.query(
        models.User, *fields).filter(models.User.id == user_id).first()
    return user
# get random


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, obj_in: schemas.UserCreate):
    data = obj_in.dict()
    data.pop("password")
    db_user = models.User(**data)
    db_user.hashed_password = get_password_hash(obj_in.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# crud to get post by user id
def get_posts_by_user_id(db: Session, user_id: int):
    return db.query(post_model.Post).filter(post_model.Post.author_id == user_id).all()
