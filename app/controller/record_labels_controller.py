from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.record_label import RecordLabel
from app.schemas.record_label import RecordLabelCreate, RecordLabelUpdate


def get_all(db: Session, skip: int = 0, limit: int = 100) -> list[RecordLabel]:
    try:
        return db.query(RecordLabel).offset(skip).limit(limit).all()
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error in retrieving record labels: {str(error)}",
        )


def get_by_id(db: Session, record_label_id: int) -> RecordLabel | None:
    try:
        return db.get(RecordLabel, record_label_id)
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error in retrieving record label: {str(error)}",
        )


def create(db: Session, record_label_data: RecordLabelCreate) -> RecordLabel:
    new_record_label = RecordLabel(
        name=record_label_data.name,
        country=record_label_data.country,
        website=record_label_data.website,
    )
    try:
        db.add(new_record_label)
        db.commit()
        db.refresh(new_record_label)
        return new_record_label
    except IntegrityError:
        db.rollback()
        raise
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error in creating record label: {str(error)}",
        )


def update(
    db: Session,
    record_label_id: int,
    record_label_data: RecordLabelUpdate,
) -> RecordLabel | None:
    record_label = get_by_id(db, record_label_id)
    if record_label is None:
        return None

    for field, value in record_label_data.model_dump(exclude_unset=True).items():
        setattr(record_label, field, value)

    try:
        db.commit()
        db.refresh(record_label)
        return record_label
    except IntegrityError:
        db.rollback()
        raise
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error in updating record label: {str(error)}",
        )


def delete(db: Session, record_label_id: int) -> bool:
    record_label = get_by_id(db, record_label_id)
    if record_label is None:
        return False

    try:
        db.delete(record_label)
        db.commit()
        return True
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error in deleting record label: {str(error)}",
        )
