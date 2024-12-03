import logging
from typing import ClassVar

from dotenv import find_dotenv, load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


load_dotenv(find_dotenv(".env"))


class DB(BaseSettings):
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "1"
    POSTGRES_DB: str = "postgres"

    @property
    def get_postgres_dsn(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

class Logging:
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    def setup_logging(self):
        logging.basicConfig(level=self.LOG_LEVEL, format=self.LOG_FORMAT)


class AccessToken(BaseSettings):
    LIFETIME_SECONDS: int = 3600


class Secret(BaseSettings):
    RESET_PASSWORD_TOKEN_SECRET: str = "SECRET"
    VERIFICATION_TOKEN_SECRET: str = "SECRET"
    PASSWORD_SALT: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True)

    LOGGING: ClassVar[Logging] = Logging()
    DB: ClassVar[DB] = DB()
    ACCEES_TOKEN: ClassVar[AccessToken] = AccessToken()
    SECRET: ClassVar[Secret] = Secret()


settings = Settings()
settings.LOGGING.setup_logging()
