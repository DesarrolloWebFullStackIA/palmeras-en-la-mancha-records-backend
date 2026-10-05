from pydantic import BaseModel, ConfigDict, Field


class RecordLabelBase(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=100
    )


class RecordLabelCreate(RecordLabelBase):
    name: str = Field(
        min_length=2,
        max_length=100
    )
    country: str = Field(
        min_length=2,
        max_length=100
    )
    website: str | None = Field(
        default=None,
        max_length=255
    )


class RecordLabelUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )
    country: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )
    website: str | None = Field(
        default=None,
        min_length=2,
        max_length=255
    )


class RecordLabelResponse(RecordLabelBase):
    id: int = Field(
        gt=0
    )
    name: str
    country: str
    website: str | None = Field(
        default=None,
        max_length=255
    )

    model_config = ConfigDict(
        from_attributes=True
    )