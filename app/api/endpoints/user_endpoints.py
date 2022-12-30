from fastapi import APIRouter,  Depends
from typing import List
from app.crud import user_crud
from sqlalchemy.orm.session import Session
from app.schemas import post_schema, user_schema
from app.api import deps
from app.core.config import settings

router = APIRouter()


@router.post("/users/{user_id}/posts/", response_model=post_schema.Post)
def create_item_for_user(
    user_id: int, item: post_schema.PostCreate, db: Session = Depends(deps.get_db)
):
    return user_crud.create_user_item(db=db, item=item, user_id=user_id)

# route to get posts by user id


@router.get("/users/{user_id}/posts/", response_model=List[post_schema.Post])
def get_posts_by_user_id_route(user_id: int, db: Session = Depends(deps.get_db)):
    return user_crud.get_posts_by_user_id(db=db, user_id=user_id)
