"""App configuration."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    app_name: str = "Cab Service API"
    debug: bool = False
    api_prefix: str = "/api/v1"

    class Config:
        env_file = ".env"


settings = Settings()
