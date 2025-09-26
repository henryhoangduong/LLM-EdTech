from typing import Optional

from pydantic import BaseModel, Field


class CreateCourseRequest(BaseModel):
    name: str = Field(description="Course name")
    description: Optional[str]
