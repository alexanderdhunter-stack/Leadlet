"""Application configuration."""
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    app_name: str = "Leadlet"
    debug: bool = False

    # Database
    database_url: str = "sqlite:///./leadlet.db"

    # Anthropic API
    anthropic_api_key: str = ""
    anthropic_model: str = "claude-sonnet-4-20250514"

    # File uploads
    max_upload_size_mb: int = 50
    allowed_image_types: list[str] = ["image/jpeg", "image/png", "image/webp", "image/gif"]

    # Security
    secret_key: str = "change-me-in-production"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
