from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    DB_USER: str
    DB_PASS: str

    @property
    def ROOT_ABSPATH(self) -> Path:
        return Path(__file__).parent.parent.resolve()

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env")

    SECRET_KEY: str
    ALGORITHM: str


settings = Settings()
