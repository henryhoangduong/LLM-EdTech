from sqlalchemy import INT, TIMESTAMP, Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from core.database import Base


class UserClassroom(Base):
    __tablename__ = "user_classroom"

    id = Column(INT, primary_key=True, index=True)

    user_id = Column(INT, ForeignKey("user.id"), nullable=False)
    classroom_id = Column(INT, ForeignKey("classroom.id"), nullable=False)
    role_id = Column(INT, ForeignKey("role.id"), nullable=False)

    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    # Relationships (optional, for ORM convenience)
    user = relationship("User", back_populates="user_classrooms")
    classroom = relationship("Classroom", back_populates="user_classrooms")
    role = relationship("Role", back_populates="user_classrooms")
