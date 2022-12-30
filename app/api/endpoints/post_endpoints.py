from typing import List
from fastapi import APIRouter, Depends
from app.schemas import post_schema
from sqlalchemy.orm.session import Session
from app.crud import post_crud
from app.api import deps
from app.core.config import settings

router = APIRouter()

# route to get list of posts


@router.get("/posts/", response_model=List[post_schema.Post])
def get_posts(db: Session = Depends(deps.get_db)):
    return post_crud.get_posts(db=db)
