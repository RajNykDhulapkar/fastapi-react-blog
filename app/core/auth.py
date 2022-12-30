from sqlalchemy.orm import Session
from app.core.security import verify_password
from typing import Union
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm.session import Session
from app.schemas import user_schema
from jose import jwt
from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")


# SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30


def authenticate_user(db: Session, email: str, password: str) -> Union[bool, user_schema.User]:
    from app.crud.user_crud import get_user_by_email

    user = get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"type": "access_token"})
    to_encode.update({"exp": expire})
    to_encode.update({"iat": datetime.utcnow()})
    to_encode.update({"sub": str(data['sub'])})
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET, algorithm=settings.ALGORITHM)
    return encoded_jwt
