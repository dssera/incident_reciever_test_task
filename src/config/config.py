from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    DATABASE_URL_SYNC: str
    SERVICE_SOURCE: str = "default"
    TELEGRAM_BOT_TOKEN: str
    SERVICE_URL: str

    class Config:
        env_file = ".env"

settings = Settings()
