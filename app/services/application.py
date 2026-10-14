from typing import List, Optional

from sqlalchemy.orm import Session, joinedload

from app import models, schemas
from app.services.course import get_course


def calculate_merit(gpa: float) -> float:
    """
    Simple rule‑based merit calculation: higher GPA yields higher merit.
    """
    return gpa * 25  # Scale to 0‑100


def create_application(
    db: Session,
    student_id: int,
    app_in: schemas.ApplicationCreate,
    document_datas: List[dict],
) -> models.Application:
    # Eligibility check
    course = get_course(db, app_in.course_id)
    if not course:
        raise ValueError("Course not found")
    if app_in.gpa < course.eligibility_min_gpa:
        raise ValueError("Student does not meet eligibility criteria")

    application = models.Application(
        student_id=student_id,
        course_id=app_in.course_id,
        gpa=app_in.gpa,
        status=models.ApplicationStatus.SUBMITTED,
        merit_score=calculate_merit(app_in.gpa),
    )
    db.add(application)
    db.flush()  # obtain application.id before adding documents

    # Attach documents
    for doc in document_datas:
        document = models.Document(
            application_id=application.id,
            filename=doc["filename"],
            content_type=doc["content_type"],
            data=doc["data"],
        )
        db.add(document)

    db.commit()
    db.refresh(application)
    return application


def get_application(db: Session, application_id: int) -> Optional[models.Application]:
    return (
        db.query(models.Application)
        .options(joinedload(models.Application.documents))
        .filter(models.Application.id == application_id)
        .first()
    )


def list_applications_by_student(db: Session, student_id: int) -> List[models.Application]:
    return (
        db.query(models.Application)
        .options(joinedload(models.Application.documents))
        .filter(models.Application.student_id == student_id)
        .all()
    )


def list_all_applications(db: Session) -> List[models.Application]:
    return db.query(models.Application).options(joinedload(models.Application.documents)).all()


def update_application_status(
    db: Session, application_id: int, new_status: str
) -> models.Application:
    application = db.query(models.Application).filter(models.Application.id == application_id).first()
    if not application:
        raise ValueError("Application not found")
    if new_status not in models.ApplicationStatus.__members__:
        raise ValueError("Invalid status")
    application.status = models.ApplicationStatus[new_status]
    db.commit()
    db.refresh(application)
    return application
