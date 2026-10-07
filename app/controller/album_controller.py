from sqlalchemy.orm import Session, joinedload, selectinload

from app.controller.album_formats_controller import get_by_id
from app.models.album import Album
from app.schemas.album import AlbumCreate


async def create_album(
    db: Session,
    album_data: AlbumCreate,
    image_url: str | None = None,
) -> Album:
    """Create an album and optionally store its Cloudinary image URL."""

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
    album_data,
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
        album.label_id = album_data.label_id

    if image_url is not None:
        album.cover_image_url = image_url

    db.commit()
    db.refresh(album)

    return album

def delete(db: Session, id: int):
    db_obj = get_by_id(db, id)
    if not db_obj:
        return False
    db.delete(db_obj)
    db.commit()
    return True

def get_all(db: Session, include_relations: bool = False):
    query = db.query(Album)

    if include_relations:
        query = query.options(
            joinedload(Album.record_label),
            joinedload(Album.branch),
            selectinload(Album.formats)
        )

    return query.all()

def get_by_id(db: Session, id: int, include_relations: bool = False):
    query = db.query(Album).filter(Album.id == id)

    if include_relations:
        query = query.options(
            joinedload(Album.record_label),
            joinedload(Album.branch),
            selectinload(Album.formats)
        )

    return query.first()

def create(db: Session, album):
    db_obj = Album(
        title=album.title,
        record_label_id=album.record_label_id,
        branch_id=album.branch_id
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update(db: Session, id: int, album):
    db_obj = get_by_id(db, id)
    if not db_obj:
        return None
    db_obj.title = album.title
    db_obj.record_label_id = album.record_label_id
    db_obj.branch_id = album.branch_id
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete(db: Session, id: int):
    db_obj = get_by_id(db, id)
    if not db_obj:
        return False
    db.delete(db_obj)
    db.commit()
    return True