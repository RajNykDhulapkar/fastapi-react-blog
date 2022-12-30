from typing import List
from fastapi import APIRouter, Depends
from app.schemas import post_schema, user_schema
from sqlalchemy.orm.session import Session
from app.crud import post_crud
from app.api import deps
from app.core.config import settings

router = APIRouter()

# route to get list of posts


@router.get("/", response_model=List[post_schema.Post])
def get_posts(db: Session = Depends(deps.get_db), skip: int = 0, limit: int = 100):
    return post_crud.get_posts(db=db, skip=skip, limit=limit)

# route to create a post


@router.post("/", response_model=post_schema.Post)
def create_post_for_user(
    post: post_schema.PostCreate,
    db: Session = Depends(deps.get_db),
    current_user: user_schema.User = Depends(deps.get_current_user),
):
    return post_crud.create_post(db=db, data=post, user_id=current_user.id)
