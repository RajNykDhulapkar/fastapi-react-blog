from sqlalchemy.orm.session import Session
from app.models import post_model
from app.schemas import post_schema


def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(post_model.Post).offset(skip).limit(limit).all()


def create_post(db: Session, data: post_schema.PostCreate, user_id: int):
    db_post = post_model.Post(
        **data.dict(), author_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post
