from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.app.core.settings import settings


class DatabaseHelper:
    """Управление подключением к БД."""

    def __init__(self, uri: str, echo: bool = False):
        self.engine = create_async_engine(
            url=uri,
            echo=echo,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def session_dependency(self) -> AsyncGenerator:
        """Создание генератора сессий для DI."""
        async with self.session_factory() as session:
            yield session
            await session.close()


db_helper = DatabaseHelper(
    uri=settings.psql.url,
    echo=False,
)
