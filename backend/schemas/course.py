from pydantic import BaseModel, Field
from typing import Optional


class CreateCourseRequest(BaseModel):
    name: str = Field(description="Course name")
    description: Optional[str]
