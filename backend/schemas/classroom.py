from pydantic import BaseModel, Field


class CreateClassroomRequest(BaseModel):
    name: str = Field(description="Classroom name")
    