from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from typing import List

from sqlalchemy.orm import Session

from app import schemas, models
from app.core.database import get_db
from app.services import application as application_service
from app.services.auth import get_current_active_user

router = APIRouter(prefix="/applications", tags=["Applications"])


@router.post(
    "/",
    response_model=schemas.ApplicationRead,
    status_code=status.HTTP_201_CREATED,
)
def submit_application(
    course_id: int = Form(...),
    gpa: float = Form(...),
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    if current_user.role != models.UserRole.STUDENT:
        raise HTTPException(status_code=403, detail="Only students can submit applications")
    # Read files once
    document_datas = []
    for upload in files:
        data = upload.file.read()
        document_datas.append(
            {
                "filename": upload.filename,
                "content_type": upload.content_type,
                "data": data,
            }
        )
    app_in = schemas.ApplicationCreate(course_id=course_id, gpa=gpa)
    try:
        application = application_service.create_application(
            db, current_user.id, app_in, document_datas
        )
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    return application


@router.get("/me", response_model=List[schemas.ApplicationRead])
def list_my_applications(
    db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)
):
    apps = application_service.list_applications_by_student(db, current_user.id)
    return apps


@router.get("/{application_id}", response_model=schemas.ApplicationRead)
def get_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    application = application_service.get_application(db, application_id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    if (
        current_user.role == models.UserRole.STUDENT
        and application.student_id != current_user.id
    ):
        raise HTTPException(status_code=403, detail="Not authorized")
    return application
