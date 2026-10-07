from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.controller import record_labels_controller
from app.core.database import get_db
from app.models.record_label import RecordLabel
from app.schemas.record_label import (
    RecordLabelCreate,
    RecordLabelResponse,
    RecordLabelUpdate,
    RecordLabelWithAlbumsResponse,
)

router = APIRouter(prefix="/record-labels", tags=["Record Labels"])


def _dump(record_label: RecordLabel, include_albums: bool = False) -> dict:
    """Serialize a label, nesting albums only when explicitly requested."""
    schema = RecordLabelWithAlbumsResponse if include_albums else RecordLabelResponse
    return schema.model_validate(record_label).model_dump()


@router.get(
    "/",
    response_model=list[RecordLabelWithAlbumsResponse],
    summary="Retrieve all record labels",
)
def get_all_record_labels(
    db: Session = Depends(get_db),
    include_albums: bool = Query(False, description="Include nested albums"),
    branch_id: Optional[int] = Query(None, description="Filter labels by branch ID"),
):
    labels = record_labels_controller.get_all(
        db, include_albums=include_albums, branch_id=branch_id
    )
    return [_dump(label, include_albums) for label in labels]


@router.post(
    "/",
    response_model=RecordLabelWithAlbumsResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new record label",
)
def create_record_label(
    record_label: RecordLabelCreate,
    db: Session = Depends(get_db),
):
    return _dump(record_labels_controller.create(db, record_label))


@router.get(
    "/{id}",
    response_model=RecordLabelWithAlbumsResponse,
    summary="Retrieve a record label",
)
def get_record_label(
    id: int,
    db: Session = Depends(get_db),
    include_albums: bool = Query(False, description="Include nested albums"),
):
    rl = record_labels_controller.get_by_id(db, id, include_albums=include_albums)
    if not rl:
        raise HTTPException(status_code=404, detail="Record label not found")
    return _dump(rl, include_albums)


@router.put(
    "/{id}",
    response_model=RecordLabelWithAlbumsResponse,
    summary="Update a record label",
)
def update_record_label(
    id: int,
    record_label: RecordLabelUpdate,
    db: Session = Depends(get_db),
):
    rl = record_labels_controller.update(db, id, record_label)
    if not rl:
        raise HTTPException(status_code=404, detail="Record label not found")
    return _dump(rl)


@router.delete("/{id}", summary="Delete a record label")
def delete_record_label(id: int, db: Session = Depends(get_db)):
    ok = record_labels_controller.delete(db, id)
    if not ok:
        raise HTTPException(status_code=404, detail="Record label not found")
    return {"message": "Record label deleted successfully"}
