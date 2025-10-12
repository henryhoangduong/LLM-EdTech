from sqlalchemy import UUID, Column, Integer, String
from sqlalchemy.orm import relationship

from core.database import Base
from models.user_course import user_course


class User(Base):
    __tablename__ = "user"

    id = Column(UUID, primary_key=True)
    email = Column(String)
    profile_pic = Column(String)
    name = Column(String)
    courses = relationship(
        'Course', secondary=user_course, back_populates='users')
