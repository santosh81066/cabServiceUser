"""App configuration. Uses python-dotenv for cPanel / older Python compatibility."""
import os
from pathlib import Path

# Load .env from current working directory (backend folder)
_env_path = Path(__file__).resolve().parent.parent / ".env"
if _env_path.exists():
    from dotenv import load_dotenv
    load_dotenv(_env_path)


class Settings:
    """Application settings (no pydantic-settings for Pydantic v1 compatibility)."""
    app_name: str = os.environ.get("APP_NAME", "Cab Service API")
    debug: str = os.environ.get("DEBUG", "false").lower() in ("1", "true", "yes")
    api_prefix: str = os.environ.get("API_PREFIX", "/api/v1")


settings = Settings()
