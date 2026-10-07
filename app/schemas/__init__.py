# Central export so routers import DTOs from app.schemas in one line.
from .album import AlbumBase, AlbumCreate, AlbumResponse, AlbumUpdate
from .album_format import (
    AlbumFormatBase,
    AlbumFormatCreate,
    AlbumFormatResponse,
    AlbumFormatUpdate,
)
from .branch import BranchCreate, BranchResponse, BranchUpdate, BranchWithAlbumsResponse
from .format import FormatCreate, FormatResponse, FormatUpdate, FormatWithAlbumsResponse
from .record_label import (
    RecordLabelBase,
    RecordLabelCreate,
    RecordLabelResponse,
    RecordLabelUpdate,
    RecordLabelWithAlbumsResponse,
)

__all__ = [
    "RecordLabelBase",
    "RecordLabelCreate",
    "RecordLabelUpdate",
    "RecordLabelResponse",
    "RecordLabelWithAlbumsResponse",
    "FormatCreate",
    "FormatUpdate",
    "FormatResponse",
    "FormatWithAlbumsResponse",
    "BranchCreate",
    "BranchUpdate",
    "BranchResponse",
    "BranchWithAlbumsResponse",
    "AlbumBase",
    "AlbumCreate",
    "AlbumUpdate",
    "AlbumResponse",
    "AlbumFormatBase",
    "AlbumFormatCreate",
    "AlbumFormatUpdate",
    "AlbumFormatResponse",
]
