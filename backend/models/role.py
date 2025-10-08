from core.database import Base
from sqlalchemy import INT, TIMESTAMP, Boolean, Column, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Role(Base):
    __tablename__ = 'role'
    id = Column(INT, primary_key=True)
    name = Column(String)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=func.now())
    # user_courses = relationship("user_course", back_populates="role")
