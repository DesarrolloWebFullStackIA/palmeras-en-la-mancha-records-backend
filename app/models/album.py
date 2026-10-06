from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

# ORM model for the albums table (main catalog entity).


class Album(Base):
    __tablename__ = "albums"

    # Primary key, auto-incremented integer.
    id: Mapped[int] = mapped_column(primary_key=True)

    # Album title, required field.
    title: Mapped[str] = mapped_column(String(200), nullable=False)

    # Artist name, required field.
    artist: Mapped[str] = mapped_column(String(160), nullable=False)

    # Release year, required field.
    release_year: Mapped[int] = mapped_column(nullable=False)

    # Music genre, optional field.
    genre: Mapped[str | None] = mapped_column(String(60), nullable=True)

    # Public URL returned by Cloudinary, optional field.
    cover_image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Foreign key to record_labels.id. Links each album to one label.
    label_id: Mapped[int] = mapped_column(
        ForeignKey("record_labels.id", ondelete="CASCADE"), nullable=False
    )

    # Many-to-one side: each album belongs to one label.
    record_label: Mapped["RecordLabel"] = relationship(
        "RecordLabel", back_populates="albums"
    )

    # Link to the junction table. Deletes stock rows if this album is deleted.
    album_formats: Mapped[list["AlbumFormat"]] = relationship(
        "AlbumFormat", back_populates="album", cascade="all, delete-orphan"
    )

