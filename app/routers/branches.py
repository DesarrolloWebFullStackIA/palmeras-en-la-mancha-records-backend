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
    "/", 
    response_model=BranchResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve all branch",
    description="Fetches a list of all branch in the inventory.",
)

def create_new_branch(
    branch_data: BranchCreate,
    db: Session = Depends(get_db)
):
    return controller.create_book(db=db, branch_data=branch_data)