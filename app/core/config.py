from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # App
    APP_NAME: str = "OMI Backend"
    ENV: str = "development"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"

    # Supabase
    SUPABASE_URL: str
    SUPABASE_JWT_SECRET: str

    # Database
    DATABASE_URL: str

    # Twilio
    TWILIO_ACCOUNT_SID: str
    TWILIO_AUTH_TOKEN: str
    TWILIO_WHATSAPP_FROM: str

    class Config:
        env_file = ".env"
        extra = "ignore"   # 🔥 IMPORTANT FIX


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()