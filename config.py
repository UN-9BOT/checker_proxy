from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from termcolor import cprint


class Settings(BaseSettings):
    used_site: str = Field(description="Сайт для проверки")
    input_file: str = Field(description="Файл с прокси")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


SETTINGS = Settings()  # type: ignore

DATETIME_FORMAT_FN = "%d_%m_%Y__%H_%M_%S"

cprint(f"Settings file loaded:\n{SETTINGS.model_dump_json(indent=1)}", color="blue")
