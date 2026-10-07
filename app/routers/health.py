from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db

router = APIRouter(tags=["Diagnostics"])


@router.get("/health", summary="System health check")
def health_check(db: Session = Depends(get_db)) -> dict:
    """Diagnostic health check verifying API uptime and database connectivity."""
    db.execute(text("SELECT 1"))
    return {
        "status": "healthy",
        "database": "connected",
        "environment": settings.ENVIRONMENT,
        "version": settings.VERSION,
    }