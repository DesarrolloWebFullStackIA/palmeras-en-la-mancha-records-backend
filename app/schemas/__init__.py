# Central export so routers import DTOs from app.schemas in one line.
from .album import AlbumBase, AlbumCreate, AlbumResponse, AlbumUpdate
from .album_format import (
    AlbumFormatBase,
    AlbumFormatCreate,
    AlbumFormatResponse,
    AlbumFormatUpdate,
)
from .branch import BranchCreate, BranchResponse, BranchUpdate
from .format import FormatCreate, FormatResponse, FormatUpdate
from .record_label import (
    RecordLabelBase,
    RecordLabelCreate,
    RecordLabelResponse,
    RecordLabelUpdate,
)

__all__ = [
    "RecordLabelBase",
    "RecordLabelCreate",
    "RecordLabelUpdate",
    "RecordLabelResponse",
    "FormatCreate",
    "FormatUpdate",
    "FormatResponse",
    "BranchCreate",
    "BranchUpdate",
    "BranchResponse",
    "AlbumBase",
    "AlbumCreate",
    "AlbumUpdate",
    "AlbumResponse",
    "AlbumFormatBase",
    "AlbumFormatCreate",
    "AlbumFormatUpdate",
    "AlbumFormatResponse",
]
