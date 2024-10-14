from pydantic import BaseModel
from pydantic_settings import BaseSettings


class MessageSettings(BaseModel):
    MESSAGE_LIMIT: int = 5
    TIME_LIMIT: int = 10
    BAN_TIME: int = 60


class Config(BaseSettings):
    BOT_TOKEN: str
    DATABASE_HOST: str
    DATABASE_PORT: str
    DATABASE_NAME: str
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

    @property
    def db_url(self) -> str:
        return f"postgresql+psycopg2://{config.DATABASE_USERNAME}:{config.DATABASE_PASSWORD}@{config.DATABASE_HOST}:{config.DATABASE_PORT}/{config.DATABASE_NAME}"

    message_settings: MessageSettings = MessageSettings()


config = Config()
