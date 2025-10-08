import logging

from core.database import get_db
from fastapi import APIRouter, Depends, HTTPException, Query, status
from middleware.auth import get_current_user
from schemas.schemas import CreateCourseRequest
from services.course_service import CourseService
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)
course_routes = APIRouter()


def get_course_service(db: AsyncSession = Depends(get_db)) -> CourseService:
    return CourseService(db)


@course_routes.get("")
async def get_courses(courseService: CourseService = Depends(get_course_service),
                      page: int = Query(1, ge=1, description="Page number"),
                      limit: int = Query(
                          10, ge=1, le=100, description="Items per page"),
                      user=Depends(get_current_user)):
    try:
        if not user:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="User unauthenticated"
            )
        skip = (page - 1) * limit

        response = await courseService.get_courses(skip=skip, limit=limit, user_id=user.get("id", None))
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error getting courses"
        )


@course_routes.post("")
async def create_course(createcourseRequest: CreateCourseRequest, courseService: CourseService = Depends(get_course_service)):
    try:
        response = await courseService.create_course(
            name=createcourseRequest.name,
            description=createcourseRequest.description
        )
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )


@course_routes.get("/{user_id}")
async def get_courses_by_user(user_id: str, courseService: CourseService = Depends(get_course_service)):
    try:
        return await courseService.get_course_by_user_id(user_id=user_id)
    except Exception as e:
        logger.error(f"Error during get course by user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )


@course_routes.get("/{course_id}/user/add")
async def add_user_to_course(course_id: int,  courseService: CourseService = Depends(get_course_service), user=Depends(get_current_user)):
    try:
        if not user:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="User unauthenticated"
            )
        return await courseService.add_user_to_course(course_id=course_id, user_id=user.get("id", None))
    except Exception as e:
        logger.error(f"Error during get all courses: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )
