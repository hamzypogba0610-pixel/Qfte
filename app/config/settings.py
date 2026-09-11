from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    telegram_bot_token: str = ""
    database_url: str = "postgresql+asyncpg://qfte:qftepass@localhost:5432/qfte"
    redis_url: str = "redis://localhost:6379"
    env: str = "development"

    class Config:
        env_file = ".env"


settings = Settings()
