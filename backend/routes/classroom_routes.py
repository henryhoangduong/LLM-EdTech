from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from schemas.classroom import CreateClassroomRequest
from services.classroom_service import ClassRoomService

classroom_routes = APIRouter()


def get_classroom_service(db: AsyncSession = Depends(get_db)) -> ClassRoomService:
    return ClassRoomService(db)


@classroom_routes.get("")
async def get_classrooms(classroomService: ClassRoomService = Depends(get_classroom_service)):
    try:
        response = await classroomService.get_classrooms()
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )


@classroom_routes.get("/{id}")
async def get_classroom_by_id(id: int, classroomService: ClassRoomService = Depends(get_classroom_service)):
    try:
        response = await classroomService.get_classroom_by_id(id)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )


@classroom_routes.post("")
async def create_classroom(createClassroomRequest: CreateClassroomRequest, classroomService: ClassRoomService = Depends(get_classroom_service)):
    try:
        response = await classroomService.create_classroom(
            name=createClassroomRequest.name
        )
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )
