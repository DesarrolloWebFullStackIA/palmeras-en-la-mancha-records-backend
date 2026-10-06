from sqlalchemy.orm import session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from app.models.album_format import AlbumFormat as album_format
from app.schemas.album_format import Album_FormatCreate

def get_all_formats(db: session, skip: int = 0, limit: int = 100):
    try:
        return db.query(album_format).offset(skip).limit(limit).all()
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error in retrieving album formats: {str(error)}",
        )
def create_format(db: session, format_data: Album_FormatCreate) -> album_format:
    new_format = album_format(
        nome=format_data.nome,
        description=format_data.description,
        is_available=format_data.is_available,
    )
    try:
        db.add(new_format)
        db.commit()
        db.refresh(new_format)
        return new_format
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error in creating album format: {str(error)}",
        )