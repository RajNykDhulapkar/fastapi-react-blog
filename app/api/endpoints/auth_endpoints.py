from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session
from app.core.config import settings

from app.schemas import user_schema
from app.api import deps
from app.core.auth import (
    authenticate_user,
    create_access_token,
)
from app.crud import user_crud

router = APIRouter()


@router.post("/login",  response_model=user_schema.Token)
def login_access_token(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests

    Args:
        db (Session, optional): _description_. Defaults to Depends(deps.get_db).
        form_data (OAuth2PasswordRequestForm, optional): _description_. Defaults to Depends().

    Returns:
        Any: _description_

    Raises:
        HTTPException: _description_
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "Bearer"}


@router.get("/me", response_model=user_schema.User)
def read_users_me(
    current_user: user_schema.User = Depends(deps.get_current_user),
) -> Any:
    """Gets the current logged in user

    Args:
        current_user (User, optional): _description_. Defaults to Depends(deps.get_current_active_user).

    Returns:
        Any: _description_
    """
    return current_user


@router.post("/register",  response_model=user_schema.User, status_code=201)
def register_user(
    *,
    db: Session = Depends(deps.get_db),
    user: user_schema.UserCreate,
) -> Any:
    """Register a new user

    Args:
        db (Session, optional): _description_. Defaults to Depends(deps.get_db).
        user (schemas.UserCreate, optional): _description_. Defaults to Depends().

    Returns:
        Any: _description_
    """
    db_user = user_crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    print(user)
    return user_crud.create_user(db=db, obj_in=user)
