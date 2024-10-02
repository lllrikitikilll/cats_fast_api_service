from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.app.core.settings import settings

engine = create_async_engine(url=settings.psql.url)

session_factory = async_sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


async def get_db():
    """Создание генератора сессий."""
    async with session_factory() as session:
        yield session
        await session.close()
