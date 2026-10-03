from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Optional
import os


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # App
    APP_NAME: str = "Snape API"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True
    API_PREFIX: str = "/api/v1"

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Database
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/snape",
        description="PostgreSQL async connection string",
    )

    # Redis
    REDIS_URL: str = Field(
        default="redis://localhost:6379/0",
        description="Redis connection string for BullMQ",
    )

    # Auth (Clerk)
    CLERK_SECRET_KEY: str = ""
    CLERK_PUBLISHABLE_KEY: str = ""
    CLERK_WEBHOOK_SECRET: str = ""

    # Search APIs (Free tiers)
    TAVILY_API_KEY: str = ""
    CONTEXT_API_KEY: str = ""
    FIRECRAWL_API_KEY: str = ""
    EXA_API_KEY: str = ""

    # LLM
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    DEFAULT_LLM_MODEL: str = "gpt-4o-mini"
    LLM_TEMPERATURE: float = 0.1

    # Email
    RESEND_API_KEY: str = ""
    FROM_EMAIL: str = "noreply@snape.ai"

    # Frontend URL (for CORS)
    FRONTEND_URL: str = "http://localhost:3000"

    # Job Queue
    JOB_CONCURRENCY: int = 3
    JOB_TIMEOUT_SECONDS: int = 600
    JOB_MAX_RETRIES: int = 2

    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW_SECONDS: int = 60

    # Vector DB
    VECTOR_DIMENSIONS: int = 1536  # OpenAI text-embedding-3-small

    @property
    def is_production(self) -> bool:
        return not self.DEBUG


settings = Settings()