from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import Base, engine
from app.core.exceptions import register_exception_handlers
from app.routers import album_formats, branches, formats, health, record_labels
from app.routers.albums import router as albums_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager to create database tables on startup."""
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="RESTful API for Palmeras en la Mancha Records music store.",
    lifespan=lifespan,
)

# Mount feature routers under API v1 prefix
app.include_router(albums_router, prefix=settings.API_V1_STR)
app.include_router(record_labels.router, prefix=settings.API_V1_STR)
app.include_router(formats.router, prefix=settings.API_V1_STR)
app.include_router(branches.router, prefix=settings.API_V1_STR)
app.include_router(album_formats.router, prefix=settings.API_V1_STR)

# Mount system diagnostic router
app.include_router(health.router)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Root"], summary="API root status")
def root() -> dict:
    """Root status endpoint providing documentation and health references."""
    return {
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs_url": "/docs",
        "health_url": "/health",
        "status": "online",
    }


register_exception_handlers(app)
