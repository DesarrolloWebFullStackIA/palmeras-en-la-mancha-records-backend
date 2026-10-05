from typing import Annotated
from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field


class AlbumFilters(BaseModel):

    model_config = ConfigDict(extra="forbid")

    title: str | None = Field(
        default=None,
        description="Busca albums por título.",
        examples=["Sueño"],
    )
    artist: str | None = Field(
        default=None,
        description="Busca albums por artista.",
        examples=["Vetusta Morla"],
    )
    label_id: int | None = Field(
        default=None,
        gt=0,
        description="Busca albums por ID de la discográfica.",
        examples=[1],
    )
    label_name: str | None = Field(
        default=None,
        description="Busca albums por nombre de la discográfica.",
        examples=["Sub Pop"],
    )
    format_id: int | None = Field(
        default=None,
        gt=0,
        description="Busca albums por ID del formato físico.",
        examples=[1],
    )
    format_name: str | None = Field(
        default=None,
        description="Busca albums por nombre del formato físico.",
        examples=['12" Vinyl'],
    )
    branch_id: int | None = Field(
        default=None,
        gt=0,
        description="Busca albums por ID de la sucursal.",
        examples=[1],
    )


def album_filter_parameters(
    title: Annotated[str | None, Query(
        description="Título parcial, sin distinguir mayúsculas/minúsculas.",
        examples=["Sueño"],
    )] = None,
    artist: Annotated[str | None, Query(
        description="Artista parcial, sin distinguir mayúsculas/minúsculas.",
        examples=["Vetusta Morla"],
    )] = None,
    label_id: Annotated[int | None, Query(
        gt=0,
        description="ID de la discográfica.",
        examples=[1],
    )] = None,
    label_name: Annotated[str | None, Query(
        description="Nombre de la discográfica.",
        examples=["Sub Pop"],
    )] = None,
    format_id: Annotated[int | None, Query(
        gt=0,
        description="ID del formato físico.",
        examples=[1],
    )] = None,
    format_name: Annotated[str | None, Query(
        description="Nombre del formato físico.",
        examples=['12" Vinyl'],
    )] = None,
    branch_id: Annotated[int | None, Query(
        gt=0,
        description="ID de la sucursal.",
        examples=[1],
    )] = None,
):
    
    return AlbumFilters(
        title=title,
        artist=artist,
        label_id=label_id,
        label_name=label_name,
        format_id=format_id,
        format_name=format_name,
        branch_id=branch_id,
    )
