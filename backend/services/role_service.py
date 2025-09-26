import logging

from core.supabase_client import get_supabase_client
from models.role import Role
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class RoleService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.supabase = get_supabase_client()

    async def get_all_roles(self):
        try:
            response = await self.db.execute(select(Role))
            return response.scalars().all()
        except Exception as e:
            logger.error("Error: ", str(e))
            raise ValueError("Error: ", str(e))

    async def get_role_by_id(self, role_id):
        try:
            statement = select(Role).where(Role.id == role_id)
            response = await self.db.execute(statement)
            return response.scalars().all()
        except Exception as e:
            logger.error("Error: ", str(e))
            raise ValueError("Error: ", str(e))
