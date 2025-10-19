import logging
import uuid

from sqlalchemy import func, insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from models.cousre import Course
from core.supabase_client import get_supabase_client
from models.quizz import Quizz, Question, Option
from schemas.schemas import CreateQuizzQuestionOptionRequest
logger = logging.getLogger(__name__)


class QuizzService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.supabase = get_supabase_client()

    async def create_quizz(self, name: str, description: str, course_id):
        try:
            course = await self.db.execute(
                select(Course).filter(Course.id == course_id))
            course = course.scalar_one_or_none()
            if course is None:
                raise ValueError(f"Course with id {course_id} not found")
            quizz = Quizz(name=name, description=description,
                          course_id=course.id)
            self.db.add(quizz)
            return quizz
        except Exception as e:
            logger.error("Error: ", str(e))
            raise ValueError("Error: ", str(e))

    async def get_quizz_by_course_id(self, course_id: int):
        try:
            quizz = await self.db.execute(
                select(Quizz).filter(Quizz.course_id == course_id))
            quizz = quizz.scalars().all()
            return quizz
        except Exception as e:
            logger.error("Error: ", str(e))
            raise ValueError("Error: ", str(e))

    async def create_quizz_question(self, course_id: int, quizz_id: str):
        try:
            course = await self.db.execute(
                select(Course).filter(Course.id == course_id))

            course = course.scalar_one_or_none()

            if not course:
                raise ValueError(f"Course with id {course_id} not found")

            existing_quizzes = await self.db.execute(
                select(Quizz).join(Course, Quizz.course_id == Course.id)
            )

            existing_quizzes = existing_quizzes.scalars().all()

            quizz = await self.db.execute(
                select(Quizz).filter(Quizz.id == quizz_id)
            )

            quizz = quizz.scalar_one_or_none()

            if not quizz:
                raise ValueError(f"Quizz with id {quizz_id} not found")

            exists = any(exising_quizz.id ==
                         quizz.id for exising_quizz in existing_quizzes)

            if not exists:
                raise ValueError(
                    f"Quizz with id {quizz_id} not found in current course")

            question = Question(question="Question",
                                quizz_id=quizz_id)

            self.db.add(question)

            await self.db.commit()

            return question
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            raise ValueError(f"Error: {str(e)}")

    async def get_quizz_question(self, course_id: str, quizz_id: str):
        try:
            course = await self.db.execute(
                select(Course).filter(Course.id == course_id))

            course = course.scalar_one_or_none()

            if not course:
                raise ValueError(f"Course with id {course_id} not found")

            existing_quizzes = await self.db.execute(
                select(Quizz).join(Course, Quizz.course_id == Course.id)
            )

            existing_quizzes = existing_quizzes.scalars().all()

            quizz = await self.db.execute(
                select(Quizz).filter(Quizz.id == quizz_id)
            )

            quizz = quizz.scalar_one_or_none()

            if not quizz:
                raise ValueError(f"Quizz with id {quizz_id} not found")

            exists = any(exising_quizz.id ==
                         quizz.id for exising_quizz in existing_quizzes)

            if not exists:
                raise ValueError(
                    f"Quizz with id {quizz_id} not found in current course")

            questions = await self.db.execute(
                select(Question).filter(Question.quizz_id == quizz_id)
            )

            questions = questions.scalars().all()

            return questions
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            raise ValueError(f"Error: {str(e)}")

    async def create_quizz_question_option(self, course_id: str, quizz_id: str, queesiton_id: str, req: CreateQuizzQuestionOptionRequest):
        try:
            course = await self.db.execute(
                select(Course).filter(Course.id == course_id))

            course = course.scalar_one_or_none()

            if not course:
                raise ValueError(f"Course with id {course_id} not found")

            existing_quizzes = await self.db.execute(
                select(Quizz).join(Course, Quizz.course_id == Course.id)
            )

            existing_quizzes = existing_quizzes.scalars().all()

            quizz = await self.db.execute(
                select(Quizz).filter(Quizz.id == quizz_id)
            )

            quizz = quizz.scalar_one_or_none()

            if not quizz:
                raise ValueError(f"Quizz with id {quizz_id} not found")

            exists = any(exising_quizz.id ==
                         quizz.id for exising_quizz in existing_quizzes)

            if not exists:
                raise ValueError(
                    f"Quizz with id {quizz_id} not found in current course")

            question = await self.db.execute(
                select(Question).filter(Question.id == queesiton_id)
            )

            question = question.scalar_one_or_none()

            if not question:
                raise ValueError(
                    f"Question with id {queesiton_id} not found"
                )
            for item in req.options:
                option = Option(option=item.option, is_correct=item.is_correct)
                self.db.add(option)
                await self.db.commit()
            return True
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            raise ValueError(f"Error: {str(e)}")
