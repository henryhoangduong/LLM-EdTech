from core.database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.course import CreateCourseRequest
from services.course_service import CourseService
from sqlalchemy.ext.asyncio import AsyncSession

course_routes = APIRouter()


def get_course_service(db: AsyncSession = Depends(get_db)) -> CourseService:
    return CourseService(db)


@course_routes.get("")
async def get_courses(courseService: CourseService = Depends(get_course_service)):
    try:
        response = await courseService.get_courses()
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )


@course_routes.get("/{id}")
async def get_course_by_id(id: int, courseService: CourseService = Depends(get_course_service)):
    try:
        response = await courseService.get_course_by_id(id)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
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
