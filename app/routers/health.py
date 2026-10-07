from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.core.database import get_db

router = APIRouter(tags=["health"])

@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    # Comprobación de conexión a la base de datos con SELECT 1
    db.execute(text("SELECT 1"))
    return {
        "status": "healthy",
        "database": "ok",
        "sql_check": "SELECT 1"
    }