from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.controller import album_controller
from app.core.database import get_db
from typing import Optional, List
from app.schemas.album import AlbumBase, AlbumCreate, AlbumResponse, AlbumUpdate
from app.controller import album_controller as controller


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
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.controller.album_controller import create_album,update_album
from app.services.cloudinary_service import CloudinaryService
from app.models.album import Album

router = APIRouter(
    prefix="/albums",
    tags=["Albums"],
)


@router.post("/")
async def create_album_endpoint(
    title: str = Form(...),
    artist: str = Form(...),
    release_year: int = Form(...),
    label_id: int = Form(...),
    genre: str | None = Form(None),
    image: UploadFile | None = File(None),
    db: Session = Depends(get_db),
):
    image_url = None

    if image:
        cloudinary_service = CloudinaryService()
        image_url = await cloudinary_service.upload_image(image)

    from app.schemas.album import AlbumCreate

    album_data = AlbumCreate(
        title=title,
        artist=artist,
        release_year=release_year,
        genre=genre,
        label_id=label_id,
    )

    return await create_album(
        db=db,
        album_data=album_data,
        image_url=image_url,
    )

@router.put("/{album_id}")
async def update_album_endpoint(
    album_id: int,
    title: str | None = Form(None),
    artist: str | None = Form(None),
    release_year: int | None = Form(None),
    label_id: int | None = Form(None),
    genre: str | None = Form(None),
    image: UploadFile | None = File(None),
    db: Session = Depends(get_db),
):
    album = db.query(Album).filter(Album.id == album_id).first()

    if album is None:
        raise HTTPException(status_code=404, detail="Album not found")

    image_url = None

    if image:
        cloudinary_service = CloudinaryService()
        image_url = await cloudinary_service.upload_image(image)

    from app.schemas.album import AlbumUpdate

    album_data = AlbumUpdate(
        title=title,
        artist=artist,
        release_year=release_year,
        genre=genre,
        label_id=label_id,
    )

    return await update_album(
        db=db,
        album=album,
        album_data=album_data,
        image_url=image_url,
    )

@router.get("/", response_model=List[AlbumBase])
def get_all_albums(
    db: Session = Depends(get_db),
    include_relations: bool = Query(True, description="Incluye record_label, branch y formats para pintar tarjetas")
):
    return album_controller.get_all(db, include_relations=include_relations)

@router.get("/{id}", response_model=AlbumResponse)
def get_album(
    id: int,
    db: Session = Depends(get_db),
    include_relations: bool = Query(True, description="Incluye relaciones para vista detalle")
):
    album = album_controller.get_by_id(db, id, include_relations=include_relations)
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")
    return album

@router.post("/", response_model=AlbumResponse)
def create_album(album: AlbumCreate, db: Session = Depends(get_db)):
    return album_controller.create(db, album)

@router.put("/{id}", response_model=AlbumResponse)
def update_album(id: int, album: AlbumUpdate, db: Session = Depends(get_db)):
    updated = album_controller.update(db, id, album)
    if not updated:
        raise HTTPException(status_code=404, detail="Album not found")
    return updated

@router.delete("/{id}")
def delete_album(id: int, db: Session = Depends(get_db)):
    ok = album_controller.delete(db, id)
    if not ok:
        raise HTTPException(status_code=404, detail="Album not found")
    return {"message": "Album deleted successfully"}