from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.controller import fetch_or_404
from app.core.exceptions import BadRequestError, NotFoundError
from app.models import Album, AlbumFormat, Format
from app.schemas import AlbumFormatCreate, AlbumFormatUpdate

RESOURCE = "Album format"


def list_editions(
    db: Session,
    album_id: int | None = None,
    format_id: int | None = None,
    skip: int = 0,
    limit: int = 100,
) -> list[AlbumFormat]:
    """Return the editions, optionally narrowed to one album or one format.

    The two filters are what let the frontend ask for "every edition of this
    album" or "every album that exists in this format".
    """
    statement = select(AlbumFormat).options(joinedload(AlbumFormat.format))
    if album_id is not None:
        statement = statement.where(AlbumFormat.album_id == album_id)
    if format_id is not None:
        statement = statement.where(AlbumFormat.format_id == format_id)
    statement = statement.order_by(
        AlbumFormat.album_id, AlbumFormat.format_id
    )
    return list(db.scalars(statement.offset(skip).limit(limit)).unique())


def get_edition(db: Session, album_id: int, format_id: int) -> AlbumFormat:
    """Return one edition by its composite key, or raise `NotFoundError`.

    `db.get` receives a tuple for a composite primary key. `fetch_or_404` cannot
    be reused here because it assumes a single-column key.
    """
    edition = db.get(AlbumFormat, (album_id, format_id))
    if edition is None:
        raise NotFoundError(
            f"{RESOURCE} not found: album {album_id} has no edition in "
            f"format {format_id}."
        )
    return edition


def create_edition(db: Session, payload: AlbumFormatCreate) -> AlbumFormat:
    """Create one edition once both parents exist and the pair is still free."""
    require_parents(db, payload.album_id, payload.format_id)
    require_pair_available(db, payload.album_id, payload.format_id)

    edition = AlbumFormat(**payload.model_dump())
    db.add(edition)
    db.commit()
    db.refresh(edition)
    return get_edition(db, edition.album_id, edition.format_id)


def update_edition(
    db: Session,
    album_id: int,
    format_id: int,
    payload: AlbumFormatUpdate,
) -> AlbumFormat:
    """Update the edition, or move it to another album/format pair."""
    edition = get_edition(db, album_id, format_id)

    changes = payload.model_dump(exclude_unset=True)
    target_album = changes.get("album_id", album_id)
    target_format = changes.get("format_id", format_id)

    if (target_album, target_format) != (album_id, format_id):
        require_parents(db, target_album, target_format)
        require_pair_available(
            db,
            target_album,
            target_format,
            exclude=(album_id, format_id),
        )

    for field, value in changes.items():
        setattr(edition, field, value)

    db.commit()
    db.refresh(edition)
    return get_edition(db, edition.album_id, edition.format_id)


def delete_edition(db: Session, album_id: int, format_id: int) -> None:
    """Remove one edition. The album and the format themselves are untouched.

    Deleting the album would cascade over its editions anyway, and deleting a
    format that is in use is refused upstream by `app.controllers.formats`.
    """
    db.delete(get_edition(db, album_id, format_id))
    db.commit()


def require_parents(db: Session, album_id: int, format_id: int) -> None:
    """Prove both parents exist before this table starts referencing them.

    This is the referential check of the task: without it the caller would get a
    raw foreign key violation naming neither column.
    """
    fetch_or_404(db, Album, album_id, "Album")
    fetch_or_404(db, Format, format_id, "Format")


def require_pair_available(
    db: Session,
    album_id: int,
    format_id: int,
    *,
    exclude: tuple[int, int] | None = None,
) -> None:
    """Raise `BadRequestError` if this exact pair is already registered.

    The composite primary key already rejects the duplicate, but it does it with
    a raw `IntegrityError` that names neither the album nor the format. `exclude`
    skips the row being moved so an edition does not collide with itself.
    """
    statement = select(AlbumFormat.album_id).where(
        AlbumFormat.album_id == album_id,
        AlbumFormat.format_id == format_id,
    )
    if exclude is not None:
        statement = statement.where(
            (AlbumFormat.album_id != exclude[0]) | (AlbumFormat.format_id != exclude[1])
        )
    if db.scalar(statement.limit(1)) is not None:
        raise BadRequestError(
            f"Album {album_id} is already released in format {format_id}."
        )


__all__ = [
    "RESOURCE",
    "create_edition",
    "delete_edition",
    "get_edition",
    "list_editions",
    "require_pair_available",
    "require_parents",
    "update_edition",
]