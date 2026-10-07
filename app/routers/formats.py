from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.controller import formats_controller
from app.schemas.format import FormatCreate, FormatResponse, FormatUpdate

router = APIRouter(prefix="/formats", tags=["formats"])

@router.get("/", response_model=list[FormatResponse])
def get_all_formats(db: Session = Depends(get_db)):
    return formats_controller.get_all(db)

@router.post("/", response_model=FormatResponse)
def create_format(format: FormatCreate, db: Session = Depends(get_db)):
    return formats_controller.create(db, format)

@router.get("/{id}", response_model=FormatResponse)
def get_format(id: int, db: Session = Depends(get_db)):
    f = formats_controller.get_by_id(db, id)
    if not f:
        raise HTTPException(status_code=404, detail="Format not found")
    return f

@router.put("/{id}", response_model=FormatResponse)
def update_format(id: int, format: FormatUpdate, db: Session = Depends(get_db)):
    f = formats_controller.update(db, id, format)
    if not f:
        raise HTTPException(status_code=404, detail="Format not found")
    return f

@router.delete("/{id}")
def delete_format(id: int, db: Session = Depends(get_db)):
    ok = formats_controller.delete(db, id)
    if not ok:
        raise HTTPException(status_code=404, detail="Format not found")
    return {"message": "Format deleted successfully"}