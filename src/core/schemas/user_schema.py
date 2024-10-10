from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserCreateRequest(BaseModel):
    """Schema for creating a new user."""
    name: str = Field(..., min_length=1, max_length=50, description="User's name")
    email: EmailStr = Field(..., description="User's email address")
    age: int = Field(..., gt=0, lt=99, description="User's age")

class UserUpdateRequest(BaseModel):
    """Schema for updating an existing user."""
    name: Optional[str] = Field(None, min_length=1, max_length=50, description="User's name")
    email: Optional[EmailStr] = Field(None, description="User's email address")
    age: Optional[int] = Field(None, gt=0, lt=120, description="User's age")
