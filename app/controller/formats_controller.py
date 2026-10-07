from fastapi import HTTPException, status
<<<<<<< HEAD
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, selectinload
=======
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session
>>>>>>> 6feef1e5a4c9f86f32c70008f9d4f658015a9872

from app.models.album import Album
from app.models.format import Format
from app.schemas.format import FormatCreate, FormatUpdate


def get_all(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    include_albums: bool = False,
    record_label_id: int | None = None,
) -> list[Format]:
    try:
        query = db.query(Format)

        # Keep only formats used by at least one album of the given label.
        if record_label_id is not None:
            query = (
                query.join(Format.albums)
                .filter(Album.label_id == record_label_id)
                .distinct()
            )

        if include_albums:
            query = query.options(selectinload(Format.albums))

        return query.offset(skip).limit(limit).all()
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error in retrieving formats: {str(error)}",
        )


def get_by_id(
    db: Session,
    format_id: int,
    include_albums: bool = False,
) -> Format | None:
    try:
        query = db.query(Format).filter(Format.id == format_id)
        if include_albums:
            query = query.options(selectinload(Format.albums))
        return query.first()
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
