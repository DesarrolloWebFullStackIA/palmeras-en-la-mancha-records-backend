from pydantic import BaseModel, ConfigDict


class SchemaBase(BaseModel):

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )


# Lightweight album projection used to nest albums under labels, formats and
# branches without pulling the full AlbumResponse (which nests the label back).
class AlbumSummary(SchemaBase):
    id: int
    title: str
    artist: str
    release_year: int
    genre: str | None = None
    cover_image_url: str | None = None
    label_id: int