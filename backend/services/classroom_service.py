import logging

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from core.supabase_client import get_supabase_client
from models import Classroom, UserClassroom

logger = logging.getLogger(__name__)


class ClassRoomService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.supabase = get_supabase_client()

    async def get_classrooms_by_student(self, student_id: str):
        pass

    async def get_classroom_by_id(self, classroom_id: int):
        try:
            statement = select(Classroom).options(
                joinedload(Classroom.user_classrooms)
                .joinedload(UserClassroom.user)
            ).where(Classroom.id == classroom_id)
            response = await self.db.execute(statement)
            classroom = response.unique().scalar_one()
            return classroom
        except Exception as e:
            logger.error("Error: ", str(e))
            raise ValueError("Error: ", str(e))

    async def get_classroom_by_teacher(self, teacher_id: str):
        pass

    async def create_classroom(self, name: str):
        try:
            classroom = Classroom(name=name)
            self.db.add(classroom)
            await self.db.flush()
            return classroom
        except Exception as e:
            logger.error("Error: ", str(e))
            raise ValueError("Error: ", str(e))

    async def get_classrooms(self):
        try:
            response = await self.db.execute(select(Classroom))
            return response.scalars().all()
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
