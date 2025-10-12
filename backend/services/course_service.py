import logging
import uuid

from sqlalchemy import func, insert, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from core.supabase_client import get_supabase_client
from models import Course, user_course
from models.user import User

logger = logging.getLogger(__name__)


class CourseService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.supabase = get_supabase_client()

    async def get_courses_by_student(self, student_id: str):
        pass

    async def get_course_by_id(self, course_id: int, user_id: str):
        try:
            statement = select(Course).where(Course.id == course_id)
            response = await self.db.execute(statement)
            course = response.unique().scalar_one()
            if course:
                user_course_ = self.db.execute(
                    select(user_course).filter_by(user_id=user_id, course_id=course_id))
                if not user_course_:
                    logger.error("User does not exist in course")
                    raise
            return course
        except Exception as e:
            logger.error("Error: ", str(e))
            raise ValueError("Error: ", str(e))

    async def get_course_by_teacher(self, teacher_id: str):
        pass

    async def create_course(self, name: str, description: str, user_id: str):
        try:
            course = Course(name=name, description=description)
            self.db.add(course)
            await self.db.flush()

            insert_statement = insert(user_course).values(
                user_id=user_id, course_id=course.id)
            await self.db.execute(insert_statement)
            await self.db.commit()
            return course
        except SQLAlchemyError as e:
            await self.db.rollback()
            logger.error(f"Database error: {str(e)}")
            raise
        except Exception as e:
            logger.error("Error: ", str(e))
            raise ValueError("Error: ", str(e))

    async def get_courses(self, skip: int = 0, limit: int = 10, user_id: str = ""):
        try:
            result = await self.db.execute(select(Course)
                                           .join(user_course, Course.id == user_course.c.course_id)
                                           .where(user_course.c.user_id == uuid.UUID(user_id))
                                           .offset(skip).limit(limit)
                                           )
            total_result = await self.db.execute(select(func.count()).select_from(Course)
                                                 .join(user_course, Course.id == user_course.c.course_id)
                                                 .where(user_course.c.user_id == uuid.UUID(user_id))
                                                 )
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

    async def add_user_to_course(self, course_id: int, user_id: str):
        try:
            user_id_uuid = uuid.UUID(user_id)
            course_result = await self.db.execute(
                select(Course).filter(Course.id == course_id)
            )
            course = course_result.scalar_one_or_none()
            if not course:
                raise ValueError(f"Course with id {course_id} not found")

            user_result = await self.db.execute(
                select(User).filter(User.id == user_id_uuid)
            )
            user = user_result.scalar_one_or_none()
            if not user:
                raise ValueError(f"User with id {user_id_uuid} not found")
            existing = await self.db.execute(
                select(user_course).filter_by(
                    user_id=user_id_uuid, course_id=course_id)
            )
            if existing.first():
                logger.info(
                    f"User {user_id_uuid} is already enrolled in course {course_id}")
                return {"message": "User already enrolled in course"}
            await self.db.execute(
                insert(user_course).values(
                    user_id=user_id_uuid, course_id=course_id)
            )
            await self.db.commit()

            logger.info(f"User {user_id_uuid} added to course {course_id}")
            return {"message": "User successfully added to course"}
        except SQLAlchemyError as e:
            await self.db.rollback()
            logger.error(f"Database error: {str(e)}")
            raise
        except Exception as e:
            logger.error("Error: ", str(e))
            raise ValueError("Error: ", str(e))

    async def get_course_by_user_id(self, user_id: str):
        try:
            query = (
                select(Course)
                .join(user_course, Course.id == user_course.c.course_id)
                .where(user_course.c.user_id == user_id)
            )
            result = await self.db.execute(query)
            courses = result.scalars().all()
            return courses
        except SQLAlchemyError as e:
            await self.db.rollback()
            logger.error(f"Database error: {str(e)}")
            raise
        except Exception as e:
            logger.error("UnexpecErrted error: %s", str(e))
            raise
