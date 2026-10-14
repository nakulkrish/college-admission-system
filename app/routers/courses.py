from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas, models
from app.core.database import get_db
from app.services import course as course_service
from app.services.auth import get_current_active_user, get_current_admin_user

router = APIRouter(prefix="/courses", tags=["Courses"])


@router.get("/", response_model=list[schemas.CourseRead])
def list_courses(db: Session = Depends(get_db), _: models.User = Depends(get_current_active_user)):
    courses = course_service.list_courses(db)
    return courses


@router.post("/", response_model=schemas.CourseRead, status_code=status.HTTP_201_CREATED)
def create_course(
    course_in: schemas.CourseCreate,
    db: Session = Depends(get_db),
    admin: models.User = Depends(get_current_admin_user),
):
    course = course_service.create_course(db, course_in)
    return course
