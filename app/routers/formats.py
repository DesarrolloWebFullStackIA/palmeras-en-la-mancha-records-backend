from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session

from database.database import get_db
from schemas.format import FormatCreate, FormatResponse
from controller import book_controller as controller


router = APIRouter(
    prefix="/Formats",
    tags=["format"],
)


@router.get(
    "/", 
    response_model=FormatResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve all formats",
    description="Fetches a list of all formats in the inventory.",
)

def create_new_format(
    format_data: FormatCreate,
    db: Session = Depends(get_db)
):
    return controller.create_book(db=db, format_data=format_data)