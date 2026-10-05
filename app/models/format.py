from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

# ORM model for the formats table (physical editions like Vinyl, CD).


class Format(Base):
    __tablename__ = "formats"

    # Primary key, auto-incremented integer.
    id: Mapped[int] = mapped_column(primary_key=True)

    # Format name, required and unique to avoid duplicates like "Vinyl" twice.
    name: Mapped[str] = mapped_column(String(60), nullable=False, unique=True)

    # Extra details, optional field.
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Link to the junction table. Deletes stock rows if this format is deleted.
    album_formats: Mapped[list["AlbumFormat"]] = relationship(
        "AlbumFormat", back_populates="format", cascade="all, delete-orphan"
    )
