from pydantic import BaseModel, ConfigDict, Field

from app.schemas.common import AlbumSummary


class BranchCreate(BaseModel):
	name: str = Field(
		min_length=2,
    max_length=100
  )
	address: str | None = Field(
    default=None,
    min_length=5,
    max_length=255
  )
	phone: str = Field(
		min_length=7,
    max_length=20
  )

class BranchUpdate(BaseModel):
	name: str | None = Field(
		default=None, 
    min_length=2, 
    max_length=100
  )
	address: str | None = Field(
		default=None,
    min_length=5,
    max_length=255
  )
	phone: str | None = Field(
		default=None, 
    max_length=20
  )

class BranchResponse(BaseModel):

	id: int
	name: str 
	address: str | None = None
	phone: str | None = None

	model_config = ConfigDict(from_attributes=True)


# Response used when the client requests the albums stocked in this branch.
class BranchWithAlbumsResponse(BranchResponse):
	albums: list[AlbumSummary] = []
