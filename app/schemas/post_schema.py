from typing import List, Union
from pydantic import BaseModel, Field


class PostBase(BaseModel):
    title: str
    content: Union[str, None] = None


class PostCreate(PostBase):
    title: str = Field(example="My first post")
    content: Union[str, None] = Field(
        example="This is the content of my first post")


class Post(PostBase):
    id: int
    author_id: int

    class Config:
        orm_mode = True
