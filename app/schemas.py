from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

    model_config = ConfigDict(from_attributes=True)


class TokenData(BaseModel):
    user_id: Optional[int] = None
    role: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class UserRead(BaseModel):
    id: int
    email: EmailStr
    full_name: Optional[str] = None
    role: str

    model_config = ConfigDict(from_attributes=True)


class CourseCreate(BaseModel):
    name: str
    description: Optional[str] = None
    seats: int = Field(gt=0)
    fee: float = Field(gt=0)
    eligibility_min_gpa: float = Field(ge=0, le=4.0)

    model_config = ConfigDict(from_attributes=True)


class CourseRead(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    seats: int
    fee: float
    eligibility_min_gpa: float

    model_config = ConfigDict(from_attributes=True)


class DocumentRead(BaseModel):
    id: int
    filename: str
    content_type: str

    model_config = ConfigDict(from_attributes=True)


class ApplicationCreate(BaseModel):
    course_id: int
    gpa: float = Field(ge=0, le=4.0)

    model_config = ConfigDict(from_attributes=True)


class ApplicationRead(BaseModel):
    id: int
    student_id: int
    course_id: int
    gpa: float
    status: str
    merit_score: Optional[float] = None
    created_at: datetime
    documents: List[DocumentRead] = []

    model_config = ConfigDict(from_attributes=True)


class ApplicationStatusUpdate(BaseModel):
    status: str

    model_config = ConfigDict(from_attributes=True)
