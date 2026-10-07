from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

# ORM model for the record_labels table (1:N side, one label produces many albums).


class RecordLabel(Base):
    __tablename__ = "record_labels"

    # Primary key, auto-incremented integer.
    id: Mapped[int] = mapped_column(primary_key=True)

    # Label name, required and indexed for text search.
    name: Mapped[str] = mapped_column(String(120), nullable=False, index=True)

    # Country of origin, optional field.
    country: Mapped[str | None] = mapped_column(String(60), nullable=True)

    # Official website URL, optional field.
    website: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # One-to-many link to albums. back_populates keeps both sides in sync.
    # Cascade deletes orphan albums when their label is deleted.
    albums: Mapped[list["Album"]] = relationship(
        "Album", back_populates="record_label", cascade="all, delete-orphan"
    )
