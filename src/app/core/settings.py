from pydantic import BaseModel
from pydantic_settings import BaseSettings


class UrlPath(BaseModel):
    """Конфигурация url Проекта."""

    prefix = '/api'


class Setings(BaseSettings):
    """Настройки проекта."""

    url: UrlPath
