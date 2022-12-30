from fastapi import APIRouter,  Depends
from typing import List
from app.crud import user_crud
from sqlalchemy.orm.session import Session
from app.schemas import post_schema, user_schema
from app.api import deps
from app.core.config import settings

router = APIRouter()


@router.get("/users/{user_id}/post/", response_model=List[post_schema.Post])
def get_posts_by_user_id_route(user_id: int, db: Session = Depends(deps.get_db)):
    return user_crud.get_posts_by_user_id(db=db, user_id=user_id)
