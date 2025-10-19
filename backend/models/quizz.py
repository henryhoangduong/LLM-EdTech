from sqlalchemy import UUID, Column, String, TIMESTAMP, INT, ForeignKey, Boolean
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.sql import func
from core.database import Base
from typing import List
from sqlalchemy.orm import mapped_column
import uuid


class Quizz(Base):
    __tablename__ = "quizz"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    name = Column(String)
    description = Column(String)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=func.now())
    course_id: Mapped[INT] = mapped_column(
        ForeignKey("course.id"), nullable=False)
    course: Mapped["Course"] = relationship(back_populates="quizz")
    question: Mapped[List["Question"]] = relationship(back_populates="quizz")


class Question(Base):
    __tablename__ = "question"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    question = Column(String)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=func.now())
    quizz_id: Mapped[String] = mapped_column(ForeignKey("quizz.id"))
    quizz: Mapped["Quizz"] = relationship(back_populates="question")
    option: Mapped[List["Option"]] = relationship(back_populates="question")


class Option(Base):
    __tablename__ = "option"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    option = Column(String)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=func.now())
    is_correct = Column(Boolean, default=False)
    question_id: Mapped[String] = mapped_column(ForeignKey("question.id"))
    question: Mapped["Question"] = relationship(back_populates="option")
