from fastapi import HTTPException
from sqlalchemy.orm import Session, selectinload

from app.models.album import Album
from app.models.album_format import AlbumFormat
from app.models.format import Format
from app.models.record_label import RecordLabel
from app.schemas.album import AlbumCreate, AlbumUpdate
from app.schemas.album_filters import AlbumFilters


def _get_label_or_404(db: Session, label_id: int) -> RecordLabel:
    """Fetch the record label or raise 404 for an unknown foreign key."""
    label = db.get(RecordLabel, label_id)
    if label is None:
        raise HTTPException(status_code=404, detail="Record label not found")
    return label


def get_filtered_albums(
    db: Session,
    filters: AlbumFilters,
    skip: int = 0,
    limit: int = 100,
) -> list[Album]:
    """Retrieve albums matching optional dynamic search filters.

    Supports partial case-insensitive filtering for title and artist,
    exact matching for label_id, partial case-insensitive matching for label_name,
    format_id, format_name, and branch_id. Ensures unique distinct albums.
    """
    query = db.query(Album)

    if filters.title:
        query = query.filter(Album.title.ilike(f"%{filters.title}%"))

    if filters.artist:
        query = query.filter(Album.artist.ilike(f"%{filters.artist}%"))

    if filters.label_id:
        query = query.filter(Album.label_id == filters.label_id)

    if filters.label_name:
        query = query.join(Album.record_label).filter(
            RecordLabel.name.ilike(f"%{filters.label_name}%")
        )

    # Check if any inventory / format / branch filters are active
    if filters.format_id or filters.format_name or filters.branch_id:
        query = query.join(Album.album_formats)

        if filters.format_id:
            query = query.filter(AlbumFormat.format_id == filters.format_id)

        if filters.format_name:
            query = query.join(AlbumFormat.format).filter(
                Format.name.ilike(f"%{filters.format_name}%")
            )

        if filters.branch_id:
            query = query.filter(AlbumFormat.branch_id == filters.branch_id)

    query = (
        query.distinct()
        .options(selectinload(Album.record_label))
        .order_by(Album.title.asc())
        .offset(skip)
        .limit(limit)
    )

    return query.all()


def get_album_by_id(db: Session, album_id: int) -> Album | None:
    """Retrieve a single album by ID including its record label."""
    return (
        db.query(Album)
        .options(selectinload(Album.record_label))
        .filter(Album.id == album_id)
        .first()
    )


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
