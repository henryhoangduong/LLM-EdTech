import logging

from core.database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from middleware.auth import get_current_user
from schemas.auth import SignInRequest, SignUpRequest
from services.auth_service import AuthService
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)
auth_routes = APIRouter()


def get_classroom_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    return AuthService(db)


@auth_routes.post("/login", status_code=status.HTTP_200_OK)
async def login(request: SignInRequest,  authService: AuthService = Depends(get_classroom_service)):
    try:
        response = await authService.login(email=request.email, password=request.password)
        return response
    except Exception as e:
        logger.error(f"Unexpected error during signup: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred",
        )


@auth_routes.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(signUpRequest: SignUpRequest,  authService: AuthService = Depends(get_classroom_service)):
    try:
        response = await authService.signup(email=signUpRequest.email, password=signUpRequest.password,name=signUpRequest.name)
        return response
    except Exception as e:
        logger.error(f"Unexpected error during signup: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred",
        )


@auth_routes.post("/signout", status_code=status.HTTP_200_OK)
async def signout(authService: AuthService = Depends(get_classroom_service)):
    try:
        response = await authService.logout()
        return response
    except Exception as e:
        logger.error(f"Unexpected error during signup: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred",
        )


@auth_routes.get("/currentUser", status_code=status.HTTP_200_OK)
async def get_current_user_info(currentUser: dict = Depends(get_current_user), authService: AuthService = Depends(get_classroom_service)):
    try:
        user = await authService.get_user_by_id(currentUser["id"])
        return user
    except Exception as e:
        logger.error(f"Failed to get user info: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get user information"
        )
