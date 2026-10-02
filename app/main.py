from fastapi import FastAPI

from app.core.database import Base, engine

# Import all models so Base.metadata knows the 5 tables before create_all.
from app.models.album import Album  # noqa: F401
from app.models.album_format import AlbumFormat  # noqa: F401
from app.models.branch import Branch  # noqa: F401
from app.models.format import Format  # noqa: F401
from app.models.record_label import RecordLabel  # noqa: F401

# Create SQLite file and tables with constraints if they do not exist yet.
Base.metadata.create_all(bind=engine)

# Main application instance.
app = FastAPI(title="Palmeras en la Mancha Records API")


@app.get("/")
def read_root():
    """Health check for the base infrastructure."""
    return {"message": "API de Palmeras en la Mancha Records funcionando correctamente"}
