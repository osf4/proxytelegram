from typing import Any
from pydantic import BaseModel
from pydantic_settings_yaml import YamlBaseSettings
from pydantic_settings import SettingsConfigDict


class DatabaseConfig(BaseModel):
    host: str
    port: int
    name: str


class BotConfig(BaseModel):
    token: str
    username: str

    supergroup_id: str
    greeting_message: str | None = None

    
    def model_post_init(self, __context: Any):
        if not self.supergroup_id.startswith('@'):
            self.supergroup_id = f'@{self.supergroup_id}'

        if self.username.startswith('@'):
            self.username = self.username[1:]


class Config(YamlBaseSettings):
    database: DatabaseConfig
    bot: BotConfig


    def __model_post_init__(self):
        pass

    model_config = SettingsConfigDict(yaml_file = 'config.yaml',
                                      secrets_dir = '/') # To fix the Pydantic warn