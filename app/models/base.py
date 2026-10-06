"""Shared declarative helpers for every ORM model."""

from datetime import datetime, timezone

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column


def utcnow() -> datetime:
    """Return the current UTC time as a naive datetime for SQLite compatibility."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


class TimestampMixin:
    """Add `created_at` and `updated_at` columns maintained by the ORM."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=utcnow,
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=utcnow,
        onupdate=utcnow,
        nullable=False,
    )
