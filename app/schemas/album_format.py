from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.schemas.branch import BranchResponse
from app.schemas.format import FormatResponse

# Shared inventory fields. Each row prices one format in one branch.


class AlbumFormatBase(BaseModel):
    album_id: int
    format_id: int
    branch_id: int
    price: float
    stock: int


# Payload to register stock. All fields required for the first entry.
class AlbumFormatCreate(AlbumFormatBase):
    album_id: int
    format_id: int
    branch_id: int
    price: float
    stock: int


# Payload to update price or restock. All fields optional for partial updates.
class AlbumFormatUpdate(AlbumFormatBase):
    album_id: Optional[int] = None
    format_id: Optional[int] = None
    branch_id: Optional[int] = None
    price: Optional[float] = None
    stock: Optional[int] = None


# API response. Nests format and branch so the frontend shows names, not just IDs.
class AlbumFormatResponse(AlbumFormatBase):
    id: int
    format: Optional[FormatResponse] = None
    branch: Optional[BranchResponse] = None

    model_config = ConfigDict(from_attributes=True)
