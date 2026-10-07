from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.controller import formats_controller
from app.core.database import get_db
from app.models.format import Format
from app.schemas.format import (
    FormatCreate,
    FormatResponse,
    FormatUpdate,
    FormatWithAlbumsResponse,
)

router = APIRouter(prefix="/formats", tags=["formats"])


def _dump(format_record: Format, include_albums: bool = False) -> dict:
    """Serialize a format, nesting albums only when explicitly requested."""
    schema = FormatWithAlbumsResponse if include_albums else FormatResponse
    return schema.model_validate(format_record).model_dump()


@router.get(
    "/",
    response_model=list[FormatWithAlbumsResponse],
    summary="Retrieve all formats",
)
def get_all_formats(
    db: Session = Depends(get_db),
    include_albums: bool = Query(False, description="Include nested albums"),
    record_label_id: Optional[int] = Query(
        None, description="Filter formats by record label ID"
    ),
):
    formats = formats_controller.get_all(
        db, include_albums=include_albums, record_label_id=record_label_id
    )
    return [_dump(fmt, include_albums) for fmt in formats]


@router.post(
    "/",
    response_model=FormatWithAlbumsResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new format",
)
def create_format(format: FormatCreate, db: Session = Depends(get_db)):
    return _dump(formats_controller.create(db, format))


@router.get(
    "/{id}",
    response_model=FormatWithAlbumsResponse,
    summary="Retrieve a format",
)
def get_format(
    id: int,
    db: Session = Depends(get_db),
    include_albums: bool = Query(False, description="Include nested albums"),
):
    f = formats_controller.get_by_id(db, id, include_albums=include_albums)
    if not f:
        raise HTTPException(status_code=404, detail="Format not found")
    return _dump(f, include_albums)


@router.put(
    "/{id}",
    response_model=FormatWithAlbumsResponse,
    summary="Update a format",
)
def update_format(id: int, format: FormatUpdate, db: Session = Depends(get_db)):
    f = formats_controller.update(db, id, format)
    if not f:
        raise HTTPException(status_code=404, detail="Format not found")
    return _dump(f)


@router.delete("/{id}", summary="Delete a format")
def delete_format(id: int, db: Session = Depends(get_db)):
    ok = formats_controller.delete(db, id)
    if not ok:
        raise HTTPException(status_code=404, detail="Format not found")
    return {"message": "Format deleted successfully"}
