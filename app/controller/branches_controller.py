from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.branch import Branch
from app.schemas.branch import BranchCreate, BranchUpdate


def get_all(db: Session, skip: int = 0, limit: int = 100) -> list[Branch]:
    try:
        return db.query(Branch).offset(skip).limit(limit).all()
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error in retrieving branches: {str(error)}",
        )


def get_by_id(db: Session, branch_id: int) -> Branch | None:
    try:
        return db.get(Branch, branch_id)
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error in retrieving branch: {str(error)}",
        )


def create(db: Session, branch_data: BranchCreate) -> Branch:
    new_branch = Branch(
        name=branch_data.name,
        address=branch_data.address,
        phone=branch_data.phone,
    )
    try:
        db.add(new_branch)
        db.commit()
        db.refresh(new_branch)
        return new_branch
    except IntegrityError:
        db.rollback()
        raise
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error in creating branch: {str(error)}",
        )


def update(db: Session, branch_id: int, branch_data: BranchUpdate) -> Branch | None:
    existing_branch = get_by_id(db, branch_id)
    if existing_branch is None:
        return None

    for field, value in branch_data.model_dump(exclude_unset=True).items():
        setattr(existing_branch, field, value)

    try:
        db.commit()
        db.refresh(existing_branch)
        return existing_branch
    except IntegrityError:
        db.rollback()
        raise
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error in updating branch: {str(error)}",
        )


def delete(db: Session, branch_id: int) -> bool:
    existing_branch = get_by_id(db, branch_id)
    if existing_branch is None:
        return False

    try:
        db.delete(existing_branch)
        db.commit()
        return True
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error in deleting branch: {str(error)}",
        )
