from fastapi import HTTPException, status
<<<<<<< HEAD
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, selectinload
=======
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session
>>>>>>> 6feef1e5a4c9f86f32c70008f9d4f658015a9872

from app.models.album import Album
from app.models.branch import Branch
from app.schemas.branch import BranchCreate, BranchUpdate


def get_all(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    include_albums: bool = False,
    record_label_id: int | None = None,
) -> list[Branch]:
    try:
        query = db.query(Branch)

        # Keep only branches stocking at least one album of the given label.
        if record_label_id is not None:
            query = (
                query.join(Branch.albums)
                .filter(Album.label_id == record_label_id)
                .distinct()
            )

        if include_albums:
            query = query.options(selectinload(Branch.albums))

        return query.offset(skip).limit(limit).all()
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error in retrieving branches: {str(error)}",
        )


def get_by_id(
    db: Session,
    branch_id: int,
    include_albums: bool = False,
) -> Branch | None:
    try:
        query = db.query(Branch).filter(Branch.id == branch_id)
        if include_albums:
            query = query.options(selectinload(Branch.albums))
        return query.first()
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
