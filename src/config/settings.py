from pydantic_settings import BaseSettings
from typing import Optional
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    # Application
    app_name: str = "videogames-chatbot"
    env: str = "development"
    debug: bool = True
    log_level: str = "INFO"

    # Server
    host: str = "0.0.0.0"
    port: int = 8000

    # API Keys
    anthropic_api_key: str
    steam_api_key: Optional[str] = None  # Optional - most features work without it

    # LLM Configuration
    claude_model: str = "claude-sonnet-4-5"
    max_tokens: int = 4096
    temperature: float = 0.7

    # ChromaDB
    chroma_persist_dir: str = "./chroma_db"

    # Redis Cache
    redis_url: Optional[str] = None
    cache_ttl: int = 3600

    # Steam API
    steam_api_base_url: str = "https://api.steampowered.com"
    steam_store_api_url: str = "https://store.steampowered.com/api"

    # AWS Configuration (for future migration)
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_region: str = "us-east-1"
    s3_bucket_name: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()
