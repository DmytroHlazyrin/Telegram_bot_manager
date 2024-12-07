from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = True

    # Database settings
    DATABASE_URL: str

    # Security settings
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Telegram API
    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_API_URL: str = "https://api.telegram.org"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
