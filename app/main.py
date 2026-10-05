from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.core.exceptions import register_exception_handlers

from app.core.config import settings
from app.core.database import Base, engine, get_db

import app.models  # noqa: F401 — registers the 5 tables in Base.metadata




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

# CORS Middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["Diagnostics"], summary="System health check")
def health_check(db: Session = Depends(get_db)) -> dict:
    """Diagnostic health check verifying API uptime and database connectivity."""
    try:
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as exc:
        db_status = f"unhealthy: {str(exc)}"

    return {
        "status": "healthy" if db_status == "connected" else "degraded",
        "database": db_status,
        "environment": settings.ENVIRONMENT,
        "version": settings.VERSION,
    }


@app.get("/", tags=["Root"], summary="API root status")
def root() -> dict:
    """Root status endpoint providing documentation references."""
    return {
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs_url": "/docs",
        "health_url": "/health",
        "status": "online",
    }

register_exception_handlers(app)
