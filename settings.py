from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    redis_host: str = Field(..., env="REDIS_HOST")
    redis_port: int = Field(6379, env="REDIS_PORT")
    redis_db: int = Field(0, env="REDIS_DB")
    redis_password: str = Field(None, env="REDIS_PASSWORD")

    class Config:
        env_file = ".env"  # Specify the .env file location


# Instantiate settings
settings = Settings()