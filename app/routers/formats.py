from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from database.database import get_db
from app.schemas.format import FormatCreate, FormatResponse
from app.controller import book_controller as controller


router = APIRouter(
    prefix="/Formats",
    tags=["format"],
)


@router.get(
    "/", 
    response_model=list[FormatResponse],
    status_code=status.HTTP_200_OK,
    summary="Retrieve all formats",
    description="Fetches a list of all formats in the inventory.",
)

def get_all_formats(
    db: Session = Depends(get_db)
):
    return controller.get_all_books(db=db)

@router.post(
    "/",
    response_model=FormatResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new format",
    description="Creates a new format in the inventory.",
)
def create_new_format(
    format_data: FormatCreate,
    db: Session = Depends(get_db)
):
    return controller.create_book(db=db, book_data=format_data)