import logging
import random

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from core.supabase_client import get_supabase_client
from models.user import User

logger = logging.getLogger(__name__)


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.supabase = get_supabase_client()

    async def signup(self, email: str, password: str, name: Optional[str]):
        try:
            response = self.supabase.auth.sign_up(
                {
                    "email": email,
                    "password": password,
                }
            )
            idx = random.randint(1, 100)  # inclusive range
            random_avatar = f"https://avatar.iran.liara.run/public/{idx}.png"
            user = User(
                email=response.user.email,
                id=response.user.id,
                profile_pic=random_avatar,
                name=name)
            self.db.add(user)
            self.db.flush()
            return response
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            raise ValueError(f"Sign in failed: {str(e)}")

    async def login(self, email: str, password: str):
        try:
            response = self.supabase.auth.sign_in_with_password(
                {"email": email, "password": password}
            )
            return response
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            raise ValueError(f"Error: {str(e)}")

    async def get_user_by_id(self, id: str):
        try:
            statement = select(User).where(User.id == id)
            response = await self.db.execute(statement)
            user = response.scalar_one_or_none()
            return user
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            raise ValueError(f"Error: {str(e)}")

    async def logout(self):
        try:
            self.supabase.auth.sign_out()
            return
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            raise ValueError(f"Error: {str(e)}")

    async def google_sign(self):
        try:
            pass
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            raise ValueError(f"Error: {str(e)}")

    async def google_signin_callback(code: str):
        try:
            pass
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            raise ValueError(f"Error: {str(e)}")
