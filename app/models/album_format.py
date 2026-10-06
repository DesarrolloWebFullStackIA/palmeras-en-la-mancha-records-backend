from sqlalchemy import CheckConstraint, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

# Junction table for the N:M inventory (album + format + branch = price/stock).


class AlbumFormat(Base):
    __tablename__ = "album_formats"

    __table_args__ = (
        UniqueConstraint(
            "album_id",
            "format_id",
            "branch_id",
            name="uq_album_format_branch",
        ),
        CheckConstraint(
            "price >= 0",
            name="ck_album_formats_price_non_negative",
        ),
        CheckConstraint(
            "stock >= 0",
            name="ck_album_formats_stock_non_negative",
        ),
    )

    # Primary key, auto-incremented integer.
    id: Mapped[int] = mapped_column(primary_key=True)

    # Link to albums.id. Deleted if the album is deleted.
    album_id: Mapped[int] = mapped_column(
        ForeignKey("albums.id", ondelete="CASCADE"), nullable=False
    )

    # Link to formats.id. Deleted if the format is deleted.
    format_id: Mapped[int] = mapped_column(
        ForeignKey("formats.id", ondelete="CASCADE"), nullable=False
    )

    # Link to branches.id. Deleted if the branch is deleted.
    branch_id: Mapped[int] = mapped_column(
        ForeignKey("branches.id", ondelete="CASCADE"), nullable=False
    )

    # Sale price, required field.
    price: Mapped[float] = mapped_column(nullable=False)

    # Available units, required field.
    stock: Mapped[int] = mapped_column(nullable=False)

    # Reverse links, each mirrors the album_formats side in the parent model.
    album: Mapped["Album"] = relationship("Album", back_populates="album_formats")
    format: Mapped["Format"] = relationship("Format", back_populates="album_formats")
    branch: Mapped["Branch"] = relationship("Branch", back_populates="album_formats")
