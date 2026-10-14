from typing import List

from sqlalchemy.orm import Session

from app import models, schemas


def create_course(db: Session, course_in: schemas.CourseCreate) -> models.Course:
    course = models.Course(**course_in.model_dump())
    db.add(course)
    db.commit()
    db.refresh(course)
    return course


def get_course(db: Session, course_id: int) -> models.Course:
    return db.query(models.Course).filter(models.Course.id == course_id).first()


def list_courses(db: Session) -> List[models.Course]:
    return db.query(models.Course).all()
