from pydantic import BaseModel, ConfigDict, Field, ConfigDict,StrictInt, StrictStr


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