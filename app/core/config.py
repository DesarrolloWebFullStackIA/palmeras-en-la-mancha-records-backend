from typing import List, Union
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings and environment configuration."""

    PROJECT_NAME: str = "Palmeras en la Mancha Records API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"

    # Database
    DATABASE_URL: str = "sqlite:///./palmeras_records.db"

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: str) -> str:
        """Fix legacy postgres:// scheme used by Render/Heroku to postgresql://."""
        if isinstance(v, str) and v.startswith("postgres://"):
            return v.replace("postgres://", "postgresql://", 1)
        return v

    # Cloudinary Credentials
    CLOUDINARY_CLOUD_NAME: str = ""
    CLOUDINARY_API_KEY: str = ""
    CLOUDINARY_API_SECRET: str = ""
    CLOUDINARY_FOLDER: str = "palmeras_records_covers"

    # CORS
    BACKEND_CORS_ORIGINS: Union[List[str], str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5500",
        "http://localhost:8000",
    ]

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        """Parse comma-separated origin strings into a list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
