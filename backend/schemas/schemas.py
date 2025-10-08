from typing import List, Optional

from pydantic import BaseModel, Field


class SignUpRequest(BaseModel):
    email: str = Field(..., description="User email")
    password: str = Field(..., description="User password")
    name: Optional[str] = None


class SignInRequest(BaseModel):
    email: str = Field(..., description="User email")
    password: str = Field(..., description="User password")


class SignOutRequest(BaseModel):
    access_token: str = Field(..., description="Access Token")


class CreateCourseRequest(BaseModel):
    name: str = Field(description="Course name")
    description: Optional[str]


class Query(BaseModel):
    message: str


class Query(BaseModel):
    message: str


class BulkIngestionRequest(BaseModel):
    folder_paths: List[str]
