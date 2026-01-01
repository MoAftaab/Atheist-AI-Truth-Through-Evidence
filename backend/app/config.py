"""
Configuration management for the application.
Loads environment variables and provides settings.
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Atheist AI API"
    VERSION: str = "1.0.0"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://user:password@localhost:5432/quran_rag"
    )
    
    # Redis Cache (optional)
    REDIS_URL: Optional[str] = os.getenv("REDIS_URL", None)
    CACHE_TTL: int = 3600  # 1 hour
    
    # OpenAI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # CORS
    CORS_ORIGINS: str = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:3000,http://localhost:3001,https://atheist-ai-truth-through-evidence.vercel.app"
    )
    # Note: Vercel preview URLs (e.g., *-*.vercel.app) are handled via allow_origin_regex in main.py
    
    @property
    def cors_origins_list(self) -> list:
        """Parse CORS origins from comma-separated string."""
        if not self.CORS_ORIGINS:
            return ["http://localhost:3000", "http://127.0.0.1:3000"]
        origins = [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]
        # Always include localhost:3000 for development
        if "http://localhost:3000" not in origins:
            origins.append("http://localhost:3000")
        if "http://127.0.0.1:3000" not in origins:
            origins.append("http://127.0.0.1:3000")
        return origins
    
    # Quran Data Paths
    QURAN_JSON_PATH: str = os.getenv("QURAN_JSON_PATH", "quran_full_formatted.json")
    FAISS_INDEX_PATH: str = os.getenv("FAISS_INDEX_PATH", "quran_faiss.index")
    QURAN_METADATA_PATH: str = os.getenv("QURAN_METADATA_PATH", "quran_metadata.json")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()

