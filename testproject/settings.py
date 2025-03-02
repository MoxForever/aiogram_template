from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_API_URL: str = "https://api.telegram.org/"
    TELEGRAM_SECRET_TOKEN: str | None = None
    TELEGRAM_WEBHOOK_URL: str | None = None
    TELEGRAM_WEBHOOK_PATH: str = "/telegram"

    DATABASE_REDIS_URL: str
    DATABASE_POSTGRES_URL: str
