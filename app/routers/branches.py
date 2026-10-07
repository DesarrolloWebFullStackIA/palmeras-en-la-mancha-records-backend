from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.controller import branches_controller
from app.schemas.branch import BranchCreate, BranchResponse, BranchUpdate

router = APIRouter(prefix="/branches", tags=["Branches"])

@router.get("/", response_model=list[BranchResponse])
def get_all_branches(db: Session = Depends(get_db)):
    return branches_controller.get_all(db)

@router.post("/", response_model=BranchResponse, status_code=status.HTTP_201_CREATED)
def create_branch(branch: BranchCreate, db: Session = Depends(get_db)):
    return branches_controller.create(db, branch)

@router.get("/{id}", response_model=BranchResponse)
def get_branch(id: int, db: Session = Depends(get_db)):
    b = branches_controller.get_by_id(db, id)
    if not b:
        raise HTTPException(status_code=404, detail="Branch not found")
    return b

@router.put("/{id}", response_model=BranchResponse)
def update_branch(id: int, branch: BranchUpdate, db: Session = Depends(get_db)):
    b = branches_controller.update(db, id, branch)
    if not b:
        raise HTTPException(status_code=404, detail="Branch not found")
    return b

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_branch(id: int, db: Session = Depends(get_db)):
    ok = branches_controller.delete(db, id)
    if not ok:
        raise HTTPException(status_code=404, detail="Branch not found")
    return None