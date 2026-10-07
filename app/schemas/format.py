from pydantic import BaseModel, ConfigDict, Field, ConfigDict,StrictInt, StrictStr

from app.schemas.common import AlbumSummary


class FormatCreate(BaseModel):
    name: StrictStr = Field(
        min_length=2,
        max_length=100
    )
    description: StrictStr | None = Field(
        default=None,
        max_length=255
    )

class FormatUpdate(BaseModel):
    name: StrictStr | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )
    description: StrictStr | None = Field(
        default=None,
        max_length=255
    )


class FormatResponse(BaseModel):
    id: StrictInt
    name: StrictStr
    description: StrictStr | None = None
    
    model_config = ConfigDict(from_attributes=True)


# Response used when the client requests the albums sold in this format.
class FormatWithAlbumsResponse(FormatResponse):
    albums: list[AlbumSummary] = []
