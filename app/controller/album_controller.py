from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.album import Album
from app.models.record_label import RecordLabel
from app.schemas.album import AlbumCreate, AlbumUpdate


def _get_label_or_404(db: Session, label_id: int) -> RecordLabel:
    """Fetch the record label or raise 404 for an unknown foreign key."""
    label = db.get(RecordLabel, label_id)
    if label is None:
        raise HTTPException(status_code=404, detail="Record label not found")
    return label


async def create_album(
    db: Session,
    album_data: AlbumCreate,
    image_url: str | None = None,
) -> Album:
    """Create an album and optionally store its Cloudinary image URL."""
    _get_label_or_404(db, album_data.label_id)

    album = Album(
        title=album_data.title,
        artist=album_data.artist,
        release_year=album_data.release_year,
        genre=album_data.genre,
        label_id=album_data.label_id,
        cover_image_url=image_url,
    )

    db.add(album)
    db.commit()
    db.refresh(album)

    return album


async def update_album(
    db: Session,
    album: Album,
    album_data: AlbumUpdate,
    image_url: str | None = None,
) -> Album:
    """Update an album and optionally its Cloudinary image URL."""
    if album_data.title is not None:
        album.title = album_data.title

    if album_data.artist is not None:
        album.artist = album_data.artist

    if album_data.release_year is not None:
        album.release_year = album_data.release_year

    if album_data.genre is not None:
        album.genre = album_data.genre

    if album_data.label_id is not None:
        _get_label_or_404(db, album_data.label_id)
        album.label_id = album_data.label_id

    if image_url is not None:
        album.cover_image_url = image_url

    db.commit()
    db.refresh(album)

    return album
