from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.format import Format
from app.schemas.format import FormatCreate, FormatUpdate


def get_all(db: Session, skip: int = 0, limit: int = 100) -> list[Format]:
    try:
        return db.query(Format).offset(skip).limit(limit).all()
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error in retrieving formats: {str(error)}",
        )


def get_by_id(db: Session, format_id: int) -> Format | None:
    try:
        return db.get(Format, format_id)
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error in retrieving format: {str(error)}",
        )


def create(db: Session, format_data: FormatCreate) -> Format:
    new_format = Format(
        name=format_data.name,
        description=format_data.description,
    )
    try:
        db.add(new_format)
        db.commit()
        db.refresh(new_format)
        return new_format
    except IntegrityError:
        db.rollback()
        raise
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error in creating format: {str(error)}",
        )


def update(db: Session, format_id: int, format_data: FormatUpdate) -> Format | None:
    existing_format = get_by_id(db, format_id)
    if existing_format is None:
        return None

    for field, value in format_data.model_dump(exclude_unset=True).items():
        setattr(existing_format, field, value)

    try:
        db.commit()
        db.refresh(existing_format)
        return existing_format
    except IntegrityError:
        db.rollback()
        raise
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error in updating format: {str(error)}",
        )


def delete(db: Session, format_id: int) -> bool:
    existing_format = get_by_id(db, format_id)
    if existing_format is None:
        return False

    try:
        db.delete(existing_format)
        db.commit()
        return True
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error in deleting format: {str(error)}",
        )
