from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: SecretStr
    BD_URL: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


config = Settings()
