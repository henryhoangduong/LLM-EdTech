from sqlalchemy import INT, TIMESTAMP, Boolean, Column, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from core.database import Base


class Classroom(Base):
    __tablename__ = 'classroom'
    id = Column(INT, primary_key=True)
    name = Column(String)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=func.now())

    user_classrooms = relationship("UserClassroom", back_populates="classroom")
