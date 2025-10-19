from models.user_course import user_course
from core.database import Base
from sqlalchemy import INT, TIMESTAMP, Boolean, Column, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, Mapped
from typing import List


class Course(Base):
    __tablename__ = 'course'
    id = Column(INT, primary_key=True)
    name = Column(String)
    description = Column(String, default=None)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=func.now())
    users = relationship(
        'User', secondary=user_course, back_populates='courses')
    quizz: Mapped[List["Quizz"]] = relationship(back_populates="course")
