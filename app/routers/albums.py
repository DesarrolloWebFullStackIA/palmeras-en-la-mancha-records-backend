from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile, status
from sqlalchemy.orm import Session

from app.controller import album_controller
from app.core.database import get_db
from app.models.album import Album
from app.schemas.album import AlbumCreate, AlbumResponse, AlbumUpdate
from app.schemas.album_filters import AlbumFilters, album_filter_parameters
from app.services.cloudinary_service import CloudinaryService

router = APIRouter(
    prefix="/albums",
    tags=["Albums"],
)


@router.get(
    "/",
    response_model=list[AlbumResponse],
    status_code=status.HTTP_200_OK,
    summary="Search and filter catalog albums",
    description="Retrieve albums with optional dynamic filtering by title, artist, label, format, and branch.",
)
def get_all_albums(
    filters: AlbumFilters = Depends(album_filter_parameters),
    skip: int = Query(0, ge=0, description="Pagination offset"),
    limit: int = Query(100, ge=1, le=100, description="Pagination limit"),
    db: Session = Depends(get_db),
):
    return album_controller.get_filtered_albums(
        db=db,
        filters=filters,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/{album_id}",
    response_model=AlbumResponse,
    status_code=status.HTTP_200_OK,
    summary="Get an album by ID",
    description="Retrieve album details including its associated record label.",
)
def get_album(
    album_id: int,
    db: Session = Depends(get_db),
):
    album = album_controller.get_album_by_id(db=db, album_id=album_id)
    if album is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Album not found",
        )
    return album


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

    album_data = AlbumCreate(
        title=title,
        artist=artist,
        release_year=release_year,
        genre=genre,
        label_id=label_id,
    )

    return await album_controller.create_album(
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

    album_data = AlbumUpdate(
        title=title,
        artist=artist,
        release_year=release_year,
        genre=genre,
        label_id=label_id,
    )

    return await album_controller.update_album(
        db=db,
        album=album,
        album_data=album_data,
        image_url=image_url,
    )
