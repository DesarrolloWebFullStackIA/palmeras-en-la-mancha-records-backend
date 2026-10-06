from sqlalchemy.orm import session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

from app.schemas.album import AlbumCreate, AlbumResponse
from app.models.album import album, album_format


def get_all_albums(db: session, skip: int = 0, limit: int = 100):
    return db.query(album_format).offset(skip).limit(limit).all()

def get_album_by_id(db: session, album_id: int):
    return db.query(album_format).filter(album_format.id == album_id).first()

def delete_album(db: session, album_id: int):
    album = db.query(album_format).filter(album_format.id == album_id).first()
    if not album:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Album with ID {album_id} not found",
        )
    try:
        db.delete(album)
        db.commit()
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error in deleting album: {str(error)}",
        )
