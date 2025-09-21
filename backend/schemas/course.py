from pydantic import BaseModel, Field


class CreateCourseRequest(BaseModel):
    name: str = Field(description="Course name")
