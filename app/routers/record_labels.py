from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.controller import record_labels_controller
from app.schemas.record_label import RecordLabelCreate, RecordLabelResponse, RecordLabelUpdate

router = APIRouter(prefix="/record_labels", tags=["record_labels"])

@router.get("/", response_model=list[RecordLabelResponse])
def get_all_record_labels(db: Session = Depends(get_db)):
    return record_labels_controller.get_all(db)

@router.post("/", response_model=RecordLabelResponse)
def create_record_label(record_label: RecordLabelCreate, db: Session = Depends(get_db)):
    return record_labels_controller.create(db, record_label)

@router.get("/{id}", response_model=RecordLabelResponse)
def get_record_label(id: int, db: Session = Depends(get_db)):
    rl = record_labels_controller.get_by_id(db, id)
    if not rl:
        raise HTTPException(status_code=404, detail="Record label not found")
    return rl

@router.put("/{id}", response_model=RecordLabelResponse)
def update_record_label(id: int, record_label: RecordLabelUpdate, db: Session = Depends(get_db)):
    rl = record_labels_controller.update(db, id, record_label)
    if not rl:
        raise HTTPException(status_code=404, detail="Record label not found")
    return rl

@router.delete("/{id}")
def delete_record_label(id: int, db: Session = Depends(get_db)):
    ok = record_labels_controller.delete(db, id)
    if not ok:
        raise HTTPException(status_code=404, detail="Record label not found")
    return {"message": "Record label deleted successfully"}