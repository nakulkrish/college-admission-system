from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from sqlalchemy.orm import Session

from app import schemas, models
from app.core.database import get_db
from app.services import application as application_service
from app.services.auth import get_current_admin_user

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/applications", response_model=List[schemas.ApplicationRead])
def list_all_applications(
    db: Session = Depends(get_db), _: models.User = Depends(get_current_admin_user)
):
    apps = application_service.list_all_applications(db)
    return apps


@router.patch("/applications/{application_id}", response_model=schemas.ApplicationRead)
def update_application_status(
    application_id: int,
    status_update: schemas.ApplicationStatusUpdate,
    db: Session = Depends(get_db),
    _: models.User = Depends(get_current_admin_user),
):
    try:
        application = application_service.update_application_status(
            db, application_id, status_update.status.upper()
        )
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    return application
