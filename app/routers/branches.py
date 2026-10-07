from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.controller import branches_controller
from app.core.database import get_db
from app.models.branch import Branch
from app.schemas.branch import (
    BranchCreate,
    BranchResponse,
    BranchUpdate,
    BranchWithAlbumsResponse,
)

router = APIRouter(prefix="/branches", tags=["Branches"])


def _dump(branch: Branch, include_albums: bool = False) -> dict:
    """Serialize a branch, nesting albums only when explicitly requested."""
    schema = BranchWithAlbumsResponse if include_albums else BranchResponse
    return schema.model_validate(branch).model_dump()


@router.get(
    "/",
    response_model=list[BranchWithAlbumsResponse],
    summary="Retrieve all branches",
)
def get_all_branches(
    db: Session = Depends(get_db),
    include_albums: bool = Query(False, description="Include nested albums"),
    record_label_id: Optional[int] = Query(
        None, description="Filter branches by record label ID"
    ),
):
    branches = branches_controller.get_all(
        db, include_albums=include_albums, record_label_id=record_label_id
    )
    return [_dump(branch, include_albums) for branch in branches]


@router.post(
    "/",
    response_model=BranchWithAlbumsResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new branch",
)
def create_branch(branch: BranchCreate, db: Session = Depends(get_db)):
    return _dump(branches_controller.create(db, branch))


@router.get(
    "/{id}",
    response_model=BranchWithAlbumsResponse,
    summary="Retrieve a branch",
)
def get_branch(
    id: int,
    db: Session = Depends(get_db),
    include_albums: bool = Query(False, description="Include nested albums"),
):
    b = branches_controller.get_by_id(db, id, include_albums=include_albums)
    if not b:
        raise HTTPException(status_code=404, detail="Branch not found")
    return _dump(b, include_albums)


@router.put(
    "/{id}",
    response_model=BranchWithAlbumsResponse,
    summary="Update a branch",
)
def update_branch(id: int, branch: BranchUpdate, db: Session = Depends(get_db)):
    b = branches_controller.update(db, id, branch)
    if not b:
        raise HTTPException(status_code=404, detail="Branch not found")
    return _dump(b)


@router.delete("/{id}", summary="Delete a branch")
def delete_branch(id: int, db: Session = Depends(get_db)):
    ok = branches_controller.delete(db, id)
    if not ok:
        raise HTTPException(status_code=404, detail="Branch not found")
    return {"message": "Branch deleted successfully"}
