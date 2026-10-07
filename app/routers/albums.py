from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.controller.album_controller import create_album, update_album
from app.core.database import get_db
from app.models.album import Album
from app.schemas.album import AlbumCreate, AlbumUpdate
from app.services.cloudinary_service import CloudinaryService

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
