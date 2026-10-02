from typing import Optional

from pydantic import BaseModel, ConfigDict

# Shared fields for physical formats (Vinyl, CD, Cassette).


class FormatBase(BaseModel):
    name: str
    description: Optional[str] = None


# Payload to register a new format. Name is required.
class FormatCreate(FormatBase):
    name: str


# Payload to edit a format. All fields optional for partial updates.
class FormatUpdate(FormatBase):
    name: Optional[str] = None
    description: Optional[str] = None


# API response. Reads directly from SQLAlchemy models.
class FormatResponse(FormatBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
