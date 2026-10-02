from typing import Optional

from pydantic import BaseModel, ConfigDict

# Shared fields for physical stores (Palmeras Madrid, Palmeras Asturias).


class BranchBase(BaseModel):
    name: str
    address: Optional[str] = None
    phone: Optional[str] = None


# Payload to register a new branch. Name is required.
class BranchCreate(BranchBase):
    name: str


# Payload to edit a branch. All fields optional for partial updates.
class BranchUpdate(BranchBase):
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None


# API response. Reads directly from SQLAlchemy models.
class BranchResponse(BranchBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
