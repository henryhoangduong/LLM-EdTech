import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from schemas.auth import SignInRequest, SignUpRequest
from services.auth_service import AuthService

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
        response = await authService.signup(email=signUpRequest.email, password=signUpRequest.password)
        return response
    except Exception as e:
        logger.error(f"Unexpected error during signup: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred",
        )


@auth_routes.post("/signout", status_code=status.HTTP_200_OK)
async def signout(signInRequest: SignInRequest,  authService: AuthService = Depends(get_classroom_service)):
    try:
        response = await authService.logout()
        return response
    except Exception as e:
        logger.error(f"Unexpected error during signup: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred",
        )
