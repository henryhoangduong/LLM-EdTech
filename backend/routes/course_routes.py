from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from schemas.course import CreateCourseRequest
from services.course_service import CourseService

course_routes = APIRouter()


def get_course_service(db: AsyncSession = Depends(get_db)) -> CourseService:
    return CourseService(db)


@course_routes.get("")
async def get_courses(courseService: CourseService = Depends(get_course_service),
                      page: int = Query(1, ge=1, description="Page number"),
                      limit: int = Query(10, ge=1, le=100, description="Items per page"),):
    try:
        skip = (page - 1) * limit
        print("skip: ", skip)
        print("limit: ", limit)
        response = await courseService.get_courses(skip=skip, limit=limit)
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
