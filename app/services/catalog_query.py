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