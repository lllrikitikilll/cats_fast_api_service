from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresConfig(BaseModel):
    """Конфигурация для Postgres."""

    user: str
    password: str
    host: str
    port: str
    db: str

    @property
    def url(self):  # noqa: W293, D102
        return f'postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}'  # noqa: WPS221, WPS305, E501


class UrlPath(BaseModel):
    """Конфигурация url Проекта."""

    prefix: str


class Settings(BaseSettings):
    """Настройки проекта."""

    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_nested_delimiter='__',
        env_prefix='APP_CONFIG__',
    )
    psql: PostgresConfig
    url: UrlPath


settings = Settings()  # type: ignore [call-arg]
