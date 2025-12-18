from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    ANTHROPIC_API_KEY: str = ""
    APP_NAME: str = "DocuMint"
    DEBUG_MODE: bool = True

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
