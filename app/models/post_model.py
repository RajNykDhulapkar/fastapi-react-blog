from app.database.base_class import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy_utils import URLType

from sqlalchemy.orm import relationship


class Post(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    image_url = Column(URLType)
    author_id = Column(Integer, ForeignKey("user.id"))

    author = relationship("User", back_populates="posts")
