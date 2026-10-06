from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session

from database.database import get_db
from schemas.branch import BranchCreate, BranchResponse
from controller import book_controller as controller


router = APIRouter(
    prefix="/branchs",
    tags=["branch"],
)


@router.get(
    "/{branch_id}", 
    response_model=BranchResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve a specific branch",
    description="Fetches details of a specific branch by its ID.",
)

def get_album(
    album_id: int,
    db: Session = Depends(get_db)
):
    album = controller.get_album(db=db, album_id=album_id)
    if not album:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Album with ID {album_id} not found")
    return album

@router.delete(
    "/{branch_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a branch",
    description="Deletes a specific branch by its ID.",
)
def delete_album(
    album_id: int,
    db: Session = Depends(get_db)
):
    success = controller.delete_album(db=db, album_id=album_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Album with ID {album_id} not found",
        )