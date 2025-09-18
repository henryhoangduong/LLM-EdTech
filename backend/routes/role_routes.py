import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from services.role_service import RoleService

role_routes = APIRouter()
logger = logging.getLogger(__name__)


def get_role_service(db: AsyncSession = Depends(get_db)) -> RoleService:
    return RoleService(db)


@role_routes.get("")
async def get_roles(roleService: RoleService = Depends(get_role_service)):
    try:
        response = await roleService.get_all_roles()
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )


@role_routes.get("/{id}")
async def get_role_by_id(id: str, roleService: RoleService = Depends(get_role_service)):
    try:
        response = await roleService.get_role_by_id(id)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )
