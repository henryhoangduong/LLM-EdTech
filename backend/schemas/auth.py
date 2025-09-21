from pydantic import BaseModel, Field
from typing import Optional


class SignUpRequest(BaseModel):
    email: str = Field(..., description="User email")
    password: str = Field(..., description="User password")
    name: Optional[str] = None


class SignInRequest(BaseModel):
    email: str = Field(..., description="User email")
    password: str = Field(..., description="User password")


class SignOutRequest(BaseModel):
    access_token: str = Field(..., description="Access Token")
