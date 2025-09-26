from core.database import Base
from sqlalchemy import INT, TIMESTAMP, Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class UserCourse(Base):
    __tablename__ = "user_course"

    id = Column(INT, primary_key=True, index=True)

    user_id = Column(INT, ForeignKey("user.id"), nullable=False)
    course_id = Column(INT, ForeignKey("course.id"), nullable=False)
    role_id = Column(INT, ForeignKey("role.id"), nullable=False)

    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    # Relationships (optional, for ORM convenience)
    user = relationship("User", back_populates="user_courses")
    course = relationship("Course", back_populates="user_courses")
    role = relationship("Role", back_populates="user_courses")
