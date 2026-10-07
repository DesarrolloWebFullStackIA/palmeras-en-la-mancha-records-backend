from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.album import Album
from app.models.album_format import AlbumFormat


def get_catalog(db: Session, limit: int = 100) -> list[Album]:
    

    statement = (
        select(Album)
        .options(
            selectinload(Album.record_label),
            selectinload(Album.album_formats)
            .selectinload(AlbumFormat.format),
            selectinload(Album.album_formats)
            .selectinload(AlbumFormat.branch),
        )
        .order_by(Album.title)
        .limit(limit)
    )

    return list(db.scalars(statement).unique().all())
def get_catalog_without_optimization(db: Session) -> list[Album]:
    """Load albums and their labels using lazy loading."""

    albums = list(
        db.scalars(
            select(Album).order_by(Album.title)
        ).all()
    )

    
    for album in albums:
        _ = album.record_label.name

    return albums


def get_catalog_optimized(db: Session) -> list[Album]:
    """Load albums and their labels efficiently with selectinload."""

    statement = (
        select(Album)
        .options(
            selectinload(Album.record_label)
        )
        .order_by(Album.title)
    )

    albums = list(
        db.scalars(statement).all()
    )

    for album in albums:
        _ = album.record_label.name

    return albums