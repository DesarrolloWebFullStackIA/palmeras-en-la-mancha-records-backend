from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

# ORM model for the branches table (physical stores like Palmeras Madrid).


class Branch(Base):
    __tablename__ = "branches"

    # Primary key, auto-incremented integer.
    id: Mapped[int] = mapped_column(primary_key=True)

    # Store name, required field.
    name: Mapped[str] = mapped_column(String(120), nullable=False)

    # Store address, optional field.
    address: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Contact phone, optional field.
    phone: Mapped[str | None] = mapped_column(String(30), nullable=True)

    # Link to the junction table. Deletes stock rows if this branch is deleted.
    album_formats: Mapped[list["AlbumFormat"]] = relationship(
        "AlbumFormat", back_populates="branch", cascade="all, delete-orphan"
    )

    # Many-to-many shortcut to every album stocked in this branch (read-only).
    albums: Mapped[list["Album"]] = relationship(
        "Album", secondary="album_formats", viewonly=True
    )
