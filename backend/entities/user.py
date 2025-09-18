from sqlalchemy import Boolean, Column, Float, Integer, String

from backend.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String)
    password = Column(String)
    