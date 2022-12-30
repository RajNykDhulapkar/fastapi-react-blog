from app.models import user_model
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from typing import Union

from fastapi import HTTPException, Depends, status
from sqlalchemy.orm.session import Session
from jose import jwt, JWTError
from app.schemas import user_schema as schemas
from app.models import user_model as models, post_model
from app.core.auth import oauth2_scheme
from app.core.security import get_password_hash


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


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


async def get_current_user(db: Session, token: str = Depends(oauth2_scheme)) -> schemas.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=0, username=email)
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(db, token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: schemas.User = Depends(get_current_user)) -> schemas.User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


# crud to get post by user id
def get_posts_by_user_id(db: Session, user_id: int):
    return db.query(post_model.Post).filter(post_model.Post.author_id == user_id).all()
