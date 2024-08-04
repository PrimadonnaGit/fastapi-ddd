import os

from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Board DDD Project"
    ENVIRONMENT: str
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"


class LocalSettings(Settings):
    DATABASE_URL: str = "sqlite:///./local.db"
    SECRET_KEY: str = "your-secret-key"


class TestSettings(Settings):
    DATABASE_URL: str = "sqlite:///./test.db"
    SECRET_KEY: str = "your-secret-key"


class ProdSettings(Settings):
    DATABASE_URL: str
    SECRET_KEY: str


def get_settings():
    env = os.getenv("ENVIRONMENT")

    if env == "local":
        return LocalSettings()
    elif env == "test":
        return TestSettings()
    elif env == "prod":
        return ProdSettings()
    else:
        raise ValueError("Invalid environment")


settings = get_settings()
