from typing import Optional

from pydantic import BaseModel, ConfigDict
from app.schemas.record_label import RecordLabelResponse

# Shared catalog fields. label_id links each album to one record label.


class AlbumBase(BaseModel):
    title: str
    artist: str
    release_year: int
    genre: Optional[str] = None
    cover_image_url: Optional[str] = None
    label_id: int


# Payload to register a new album. Core fields plus label are required.
class AlbumCreate(AlbumBase):
    title: str
    artist: str
    release_year: int
    label_id: int


# Payload to edit an album. All fields optional for partial updates.
class AlbumUpdate(AlbumBase):
    title: Optional[str] = None
    artist: Optional[str] = None
    release_year: Optional[int] = None
    genre: Optional[str] = None
    cover_image_url: Optional[str] = None
    label_id: Optional[int] = None


# API response. Nests the related label (1:N) inside the album payload.
class AlbumResponse(AlbumBase):
    id: int
    record_label: Optional[RecordLabelResponse] = None

    model_config = ConfigDict(from_attributes=True)
