from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

class MessageSettings(BaseModel):
    MESSAGE_LIMIT: int = 5
    TIME_LIMIT: int = 10
    BAN_TIME: int = 60
    

class DatabaseConfig(BaseModel):
    DATABASE_HOST: str
    DATABASE_PORT: str
    DATABASE_NAME: str
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    
    @property
    def db_url(self) -> str:
        return f"postgresql+asyncpg://{self.DATABASE_USERNAME}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
    
    
class BotConfig(BaseModel):
    TOKEN: str
    ID_GROUP: int = 217281485



class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="./.env",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    
    db: DatabaseConfig
    bot: BotConfig
    message_settings: MessageSettings = MessageSettings()


settings = Config()
