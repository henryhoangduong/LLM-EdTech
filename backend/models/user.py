from sqlalchemy import INT, TIMESTAMP, UUID, Column, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from core.database import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(UUID, primary_key=True)
    name = Column(String)
    email = Column(String)
    profile_pic = Column(String)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=func.now())
    user_classrooms = relationship("UserClassroom", back_populates="user")
