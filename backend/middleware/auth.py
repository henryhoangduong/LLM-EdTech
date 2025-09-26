import logging
from typing import Optional

from core.supabase_client import get_supabase_client
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

logger = logging.getLogger(__name__)

http_bearer = HTTPBearer(auto_error=False)


async def get_current_user(
    request: Request,
    bearer_credentials: Optional[HTTPAuthorizationCredentials] = Depends(
        http_bearer)
):
    token = None
    if bearer_credentials:
        token = bearer_credentials.credentials
    else:
        token = request.cookies.get("sb-access-token")
    if token:
        try:
            supabase = get_supabase_client()
            user_response = supabase.auth.get_user(token)
            if not user_response:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            user_data = {
                "id": user_response.user.id,
                "email": user_response.user.email,
                "auth_type": "jwt",
                "metadata": user_response.user.user_metadata or {},
            }
            logger.debug("User authenticated with bearer token")
            return user_data
        except Exception as e:
            logger.error(f"Bearer token authentication error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
