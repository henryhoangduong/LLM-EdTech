import logging

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.supabase_client import get_supabase_client
from models import Course

logger = logging.getLogger(__name__)


class CourseService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.supabase = get_supabase_client()

    async def get_courses_by_student(self, student_id: str):
        pass

    async def get_course_by_id(self, course_id: int):
        try:
            statement = select(Course).where(Course.id == course_id)
            # .options(
            #     joinedload(course.user_courses)
            #     .joinedload(Usercourse.user)
            # ).where(course.id == course_id)
            response = await self.db.execute(statement)
            course = response.unique().scalar_one()
            return course
        except Exception as e:
            logger.error("Error: ", str(e))
            raise ValueError("Error: ", str(e))

    async def get_course_by_teacher(self, teacher_id: str):
        pass

    async def create_course(self, name: str, description: str):
        try:
            course = Course(name=name, description=description)
            self.db.add(course)
            await self.db.flush()
            return course
        except Exception as e:
            logger.error("Error: ", str(e))
            raise ValueError("Error: ", str(e))

    async def get_courses(self, skip: int = 0, limit: int = 10):
        try:
            result = await self.db.execute(select(Course).offset(skip).limit(limit))
            total_result = await self.db.execute(select(func.count()).select_from(Course))
            total = total_result.scalar()
            courses = result.scalars().all()
            return {
                "items": courses,
                "total": total,
                "page": (skip // limit) + 1,
                "page_size": limit,
                "pages": (total + limit - 1) // limit  # ceiling division
            }
        except Exception as e:
            logger.error("Error: ", str(e))
            raise ValueError("Error: ", str(e))

    async def add_student(self, student_id: str):
        try:
            # TODO:     Check if student exists
            # TODO:     Check if student already in the class
            # TODO:     Insert student
            pass
        except Exception as e:
            logger.error("Error: ", str(e))
            raise ValueError("Error: ", str(e))
