
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    gemini_api_key: str
    langchain_api_key: str = ""
    langchain_tracing_v2: bool = False
    langchain_project: str = "restaurant-mgr-dev"

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[2] / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )



settings = Settings()

