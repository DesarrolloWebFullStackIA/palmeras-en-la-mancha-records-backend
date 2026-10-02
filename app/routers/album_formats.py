from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session

from database.database import get_db
from schemas.album_format import AlbumFormatCreate, AlbumFormatResponse
from controller import book_controller as controller


router = APIRouter(
    prefix="/album_formats",
    tags=["Album Formats"],
)


@router.get(
    "/", 
    response_model=AlbumFormatResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve all album formats",
    description="Fetches a list of all album formats in the inventory.",
)

def create_new_album_format(
    album_format_data: AlbumFormatCreate,
    db: Session = Depends(get_db)
):
    return controller.create_book(db=db, album_format_data=album_format_data)