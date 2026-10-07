from fastapi import HTTPException, status
<<<<<<< HEAD
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, selectinload
=======
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session
>>>>>>> 6feef1e5a4c9f86f32c70008f9d4f658015a9872

from app.models.album import Album
from app.models.album_format import AlbumFormat
from app.models.record_label import RecordLabel
from app.schemas.record_label import RecordLabelCreate, RecordLabelUpdate


def get_all(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    include_albums: bool = False,
    branch_id: int | None = None,
) -> list[RecordLabel]:
    try:
        query = db.query(RecordLabel)

        # Keep only labels with at least one album stocked in the given branch.
        if branch_id is not None:
            query = (
                query.join(RecordLabel.albums)
                .join(Album.album_formats)
                .filter(AlbumFormat.branch_id == branch_id)
                .distinct()
            )

        if include_albums:
            query = query.options(selectinload(RecordLabel.albums))

        return query.offset(skip).limit(limit).all()
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error in retrieving record labels: {str(error)}",
        )


def get_by_id(
    db: Session,
    record_label_id: int,
    include_albums: bool = False,
) -> RecordLabel | None:
    try:
        query = db.query(RecordLabel).filter(RecordLabel.id == record_label_id)
        if include_albums:
            query = query.options(selectinload(RecordLabel.albums))
        return query.first()
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
