from core.database import Base
from sqlalchemy import Column, Integer, String, UUID
from sqlalchemy.orm import relationship
from models.user_course import user_course


class User(Base):
    __tablename__ = "user"

    id = Column(UUID, primary_key=True)
    email = Column(String)
    courses = relationship(
        'Course', secondary=user_course, back_populates='users')
