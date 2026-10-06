from sqlalchemy.orm import session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

from app.schemas.branch import BranchCreate
from app.models.branch import Branch

def get_all_branches(db: session, skip: int = 0, limit: int = 100):
    try:
        return db.query(Branch).offset(skip).limit(limit).all()
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error in retrieving branches: {str(error)}",
        )

def create_branch(db: session, branch_data: BranchCreate) -> Branch:
    new_branch = Branch(
        name=branch_data.name,
        description=branch_data.description,
        is_available=branch_data.is_available,
    )
    try:
        db.add(new_branch)
        db.commit()
        db.refresh(new_branch)
        return new_branch
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error in creating branch: {str(error)}",
        )