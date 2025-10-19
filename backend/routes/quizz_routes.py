import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from services.quizz.quizz_service import QuizzService
from middleware.auth import get_current_user
from schemas.schemas import CreateQuizzRequest, CreateQuizzQuestionOptionRequest

quizz_routes = APIRouter()
logger = logging.getLogger(__name__)


def get_quizz_service(db: AsyncSession = Depends(get_db)) -> QuizzService:
    return QuizzService(db)


@quizz_routes.post("/course/{course_id}")
async def create_quizz(course_id: int, createQuizz: CreateQuizzRequest, quizzService: QuizzService = Depends(get_quizz_service), user=Depends(get_current_user)):
    try:
        # if not user:
        #     raise HTTPException(
        #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        #         detail="User unauthenticated"
        #     )
        response = await quizzService.create_quizz(createQuizz.name, createQuizz.description, course_id)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )


@quizz_routes.get("/course/{course_id}")
async def get_quizz_by_course_id(course_id: int, user=Depends(get_current_user), quizzService: QuizzService = Depends(get_quizz_service)):
    try:
        # if not user:
        #     raise HTTPException(
        #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        #         detail="User unauthenticated"
        #     )
        response = await quizzService.get_quizz_by_course_id(course_id=course_id)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )


@quizz_routes.post("/course/{course_id}/quizz/{quizz_id}/question")
async def create_quizz_question(course_id: int, quizz_id: str, quizzService: QuizzService = Depends(get_quizz_service)):
    try:
        response = await quizzService.create_quizz_question(course_id, quizz_id)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )


@quizz_routes.get("/course/{course_id}/quizz/{quizz_id}/question")
async def get_quizz_question(course_id: int, quizz_id: str, quizzService: QuizzService = Depends(get_quizz_service)):
    try:
        response = await quizzService.get_quizz_question(course_id, quizz_id)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )


@quizz_routes.post("/course/{course_id}/quizz/{quizz_id}/question/{question_id}")
async def create_quizz_question_option(course_id: int, quizz_id: str, createQuizzQuestionOptionRequest: CreateQuizzQuestionOptionRequest, question_id: str,  quizzService: QuizzService = Depends(get_quizz_service)):
    try:
        response = await quizzService.create_quizz_question_option(course_id, 
                                                                   quizz_id, 
                                                                   question_id, 
                                                                   createQuizzQuestionOptionRequest
                                                                )
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )
