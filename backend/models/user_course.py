from sqlalchemy import (INTEGER, UUID, Column, DateTime, ForeignKey, String,
                        Table)
from sqlalchemy.sql import func

from core.database import Base

user_course = Table('user_course', Base.metadata,
                    Column('id', INTEGER, primary_key=True),
                    Column('user_id', UUID,
                           ForeignKey('user.id')),
                    Column('course_id', INTEGER, ForeignKey('course.id')),
                    Column('created_at', DateTime(
                        timezone=True), default=func.now()),
                    )
