from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.controller import album_formats_controller
from app.schemas.album_format import (
    AlbumFormatCreate,
    AlbumFormatResponse,
    AlbumFormatUpdate,
)

router = APIRouter(
    prefix="/album-formats",
    tags=["Album Formats"],
)


@router.get("/", response_model=list[AlbumFormatResponse], status_code=status.HTTP_200_OK)
def get_all_album_formats(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """Retrieve all album format inventory records."""
    return album_formats_controller.get_all(db, skip=skip, limit=limit)


@router.post("/", response_model=AlbumFormatResponse, status_code=status.HTTP_201_CREATED)
def create_album_format(
    album_format_data: AlbumFormatCreate,
    db: Session = Depends(get_db),
):
    """Assign physical edition (album + format + branch) with price and stock."""
    return album_formats_controller.create(db, album_format_data)


@router.get("/{id}", response_model=AlbumFormatResponse, status_code=status.HTTP_200_OK)
def get_album_format(
    id: int,
    db: Session = Depends(get_db),
):
    """Retrieve a specific album format edition by its ID."""
    item = album_formats_controller.get_by_id(db, id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Album format not found",
        )
    return item


@router.put("/{id}", response_model=AlbumFormatResponse, status_code=status.HTTP_200_OK)
def update_album_format(
    id: int,
    album_format_data: AlbumFormatUpdate,
    db: Session = Depends(get_db),
):
    """Update stock and price for a specific album format edition."""
    item = album_formats_controller.update(db, id, album_format_data)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Album format not found",
        )
    return item


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_album_format(
    id: int,
    db: Session = Depends(get_db),
):
    """Delete an album format edition from a branch."""
    ok = album_formats_controller.delete(db, id)
    if not ok:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Album format not found",
        )
    return None