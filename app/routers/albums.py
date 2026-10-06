from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from database.database import get_db

from schemas.album import AlbumCreate, AlbumResponse
from controller import album_controller as controller


router = APIRouter(
    prefix="/albums",
    tags=["Album"],
)


@router.get(
    "/", 
    response_model=AlbumResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve all albums",
    description="Fetches details of all albums.",
)
def get_all_albums(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    return controller.get_all_albums(db=db, skip=skip, limit=limit)

@router.get(
    "/{album_id}",
    response_model=AlbumResponse,
    status_code=status.HTTP_200_OK,
)
def get_album_by_id(
    album_id: int,
    db: Session = Depends(get_db)
):
    db_album = controller.get_album_by_id(db=db, album_id=album_id)
    if db_album is not None:
        raise HTTPException(status_code=404, detail="Album not found")
    return controller.get_album_by_id(db=db, album_id=album_id)


@router.post(
    "/albums",
    response_model=AlbumResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new album",
    description="Creates a new album in the inventory.",
)
def create_new_album(
    album_data: AlbumCreate,
    db: Session = Depends(get_db)
):
    return controller.create_album(db=db, album_data=album_data)

@router.patch(
    "/{album_id}",
    response_model=AlbumResponse,
    status_code=status.HTTP_200_OK,
    summary="Update an album",
    description="Updates the details of a specific album by its ID.",
)
def update_album(
    album_id: int,
    album_data: AlbumCreate,
    db: Session = Depends(get_db)
):
    return controller.update_album(db=db, album_id=album_id, album_data=album_data)

@router.delete(
    "/{album_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an album",
    description="Deletes a specific album by its ID.",
)
def delete_album(
    album_id: int,
    db: Session = Depends(get_db)
):
    success = controller.delete_album(db=db, album_id=album_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Album with ID {album_id} not found",
        )

__all__ = [
    "create_new_album",
    "delete_album",
    "get_album_by_id",
    "router",
    "update_album",
    "get_all_albums",
]