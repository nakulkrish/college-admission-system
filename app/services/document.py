from typing import List

from sqlalchemy.orm import Session

from app import models


def get_documents_by_application(db: Session, application_id: int) -> List[models.Document]:
    return (
        db.query(models.Document)
        .filter(models.Document.application_id == application_id)
        .all()
    )
