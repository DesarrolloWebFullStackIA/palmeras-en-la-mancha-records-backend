from sqlalchemy.orm import session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

from app.schemas.record_label import RecordlabelsCreate
from app.models.record_label import RecordLabel

def get_all_record_labels(db: session, skip: int = 0, limit: int = 100):
    try:
        return db.query(RecordLabel).offset(skip).limit(limit).all()
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error in retrieving record labels: {str(error)}",
        )

def create_record_label(db: session, label_data: RecordlabelsCreate) -> RecordLabel:
    new_label = RecordLabel(
        name=label_data.name,
        description=label_data.description,
        is_available=label_data.is_available,
    )
    try:
        db.add(new_label)
        db.commit()
        db.refresh(new_label)
        return new_label
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error in creating record label: {str(error)}",
        )