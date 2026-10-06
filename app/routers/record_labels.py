from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List
from sqlalchemy.orm import Session

from database.database import get_db
from schemas.record_label import RecordlabelsCreate, RecordLabelsResponse
from controller import book_controller as controller


router = APIRouter(
    prefix="/record_labels",
    tags=["record_label"],
)


@router.get(
    "/", 
    response_model=List[RecordLabelsResponse],
    status_code=status.HTTP_200_OK,
    summary="Retrieve all record labels",
    description="Fetches a list of all record labels in the inventory.",
)

def get_all_record_labels(
    record_label_data: RecordlabelsCreate,
    db: Session = Depends(get_db)
):
    return controller.create_book(db=db, record_label_data=record_label_data)

def create_new_record_label(
    record_label_data: RecordlabelsCreate,
    db: Session = Depends(get_db)
):
    return controller.create_record_label(db=db, record_label_data=record_label_data)

@router.post(
    "/",
    response_model=RecordLabelsResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new record label",
    description="Creates a new record label in the inventory.",
)
def create_new_record_label(
    record_label_data: RecordlabelsCreate,
    db: Session = Depends(get_db)
):
    return controller.create_book(db=db, record_label_data=record_label_data)