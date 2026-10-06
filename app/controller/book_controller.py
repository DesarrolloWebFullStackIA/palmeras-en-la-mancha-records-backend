from typing import List
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import session
from app.schemas.album_format import Album_FormatCreate
from app.models.album_format import AlbumFormat as album_format
from app.schemas.branch import BranchResponse
from app.schemas.format import FormatResponse


def get_all(db:session,skip:int = 0, limit: int = 100)->List[album_format]:
    try:
        return db.query(album_format).offset(skip).limit(limit).all()
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error in creating album format: {str(error)}",
        )



def create_format(db: session, book_data: Album_FormatCreate) -> album_format:


    new_album_format = Album_FormatCreate(
        nome=book_data.nome,
        description=book_data.description,
        is_available=book_data.is_available,
    )
     
    try:
        db.add(new_album_format)
        db.commit()
        db.refresh(new_album_format)
        return new_album_format
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error in creating album format: {str(error)}",
        )
