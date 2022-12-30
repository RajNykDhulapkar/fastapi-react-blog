from typing import Optional, List, Union

from pydantic import BaseModel, EmailStr, Field
from app.schemas.post_schema import Post


class UserBase(BaseModel):
    name: Optional[str] = Field(example="John Doe", default=None)
    email: EmailStr = Field(example="johndoe@example.com")


class UserInDB(UserBase):
    hashed_password: str


class UserCreate(UserBase):
    password: str = Field(example="password123")


class User(UserBase):
    id: int
    is_active: bool
    posts: List[Post] = []

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Union[int, None] = None
    email: Union[EmailStr, None] = None
