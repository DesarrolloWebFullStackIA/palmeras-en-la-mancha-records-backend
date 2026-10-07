from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session, joinedload

from app.models.album_format import AlbumFormat
from app.schemas.album_format import AlbumFormatCreate, AlbumFormatUpdate


def get_all(db: Session, skip: int = 0, limit: int = 100) -> list[AlbumFormat]:
    """Retrieve all album format records with eager loading of relationships."""
    try:
        return (
            db.query(AlbumFormat)
            .options(joinedload(AlbumFormat.format), joinedload(AlbumFormat.branch))
            .offset(skip)
            .limit(limit)
            .all()
        )
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error in retrieving album formats: {str(error)}",
        )


def get_by_id(db: Session, album_format_id: int) -> AlbumFormat | None:
    """Retrieve a single album format inventory record by its primary key ID."""
    try:
        return (
            db.query(AlbumFormat)
            .options(joinedload(AlbumFormat.format), joinedload(AlbumFormat.branch))
            .filter(AlbumFormat.id == album_format_id)
            .first()
        )
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error in retrieving album format: {str(error)}",
        )


def create(db: Session, data: AlbumFormatCreate) -> AlbumFormat:
    """Create a new album format record linking album, format, and branch with price and stock."""
    new_item = AlbumFormat(
        album_id=data.album_id,
        format_id=data.format_id,
        branch_id=data.branch_id,
        price=data.price,
        stock=data.stock,
    )
    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return get_by_id(db, new_item.id)
    except IntegrityError:
        db.rollback()
        raise
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error in creating album format: {str(error)}",
        )


def update(
    db: Session, album_format_id: int, data: AlbumFormatUpdate
) -> AlbumFormat | None:
    """Update stock, price, or relational attributes of an album format inventory record."""
    item = db.get(AlbumFormat, album_format_id)
    if item is None:
        return None

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(item, field, value)

    try:
        db.commit()
        db.refresh(item)
        return get_by_id(db, item.id)
    except IntegrityError:
        db.rollback()
        raise
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error in updating album format: {str(error)}",
        )


def delete(db: Session, album_format_id: int) -> bool:
    """Delete an album format inventory record by ID."""
    item = db.get(AlbumFormat, album_format_id)
    if item is None:
        return False

    try:
        db.delete(item)
        db.commit()
        return True
    except IntegrityError:
        db.rollback()
        raise
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error in deleting album format: {str(error)}",
        )

