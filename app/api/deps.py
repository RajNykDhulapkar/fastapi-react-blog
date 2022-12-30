from typing import Generator
from fastapi import Depends, HTTPException, status

from app.database import SessionLocal
from sqlalchemy.orm.session import Session
from app.crud import user_crud
from app.core.auth import oauth2_scheme
from jose import jwt, JWTError
from app.core.config import settings
from app.schemas import user_schema


def get_db() -> Generator:
    db = SessionLocal()
    db.current_user_id = None
    try:
        yield db
    finally:
        db.close()


async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> user_schema.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False},
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = user_schema.TokenData(id=user_id)
    except JWTError:
        raise credentials_exception

    user = user_crud.get_user(db, user_id=token_data.id)
    if user is None:
        raise credentials_exception
    return user
