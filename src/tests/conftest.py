from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine

from src.app.core.settings import settings
from src.app.main import app
from src.app.models import Base, Breed, Cat
from src.app.models.db_helper import db_helper


@pytest.fixture(scope='session', autouse=True)
async def setup_database():
    """Инициализация базы данных перед тестами."""
    async_engine = create_async_engine(settings.psql.url)
    async with async_engine.begin() as connection:
        # Создаем все таблицы перед тестами
        await connection.run_sync(Base.metadata.create_all)
    yield
    # После всех тестов можно удалить данные или сбросить базу
    async with async_engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='function')
async def db_session() -> AsyncGenerator:
    """Фикстура для предоставления сессии с откатом изменений после каждого теста."""
    async for session in db_helper.session_dependency():
        yield session
        # Откатываем все изменения после теста
        await session.rollback()


@pytest.fixture(scope='session')
async def cat_payload():
    """Тестовые данные для создания записи в БД."""
    return {
        'color': 'Красный',
        'age_in_months': 10,
        'description': None,
        'breed_name': 'Британский вислоухий',
    }


@pytest.fixture(scope='function', autouse=True)
async def setup_test_data(db_session, cat_payload):
    """Заполняет базу тестовыми данными перед каждым тестом."""
    breed1 = Breed(name=cat_payload['breed_name'])
    db_session.add(breed1)
    await db_session.commit()
    await db_session.refresh(breed1)
    cat1 = Cat(
        breed_id=breed1.id,
        color=cat_payload['color'],
        age_in_months=cat_payload['age_in_months'],
        description=cat_payload['description'],
    )
    db_session.add(cat1)
    await db_session.commit()


@pytest.fixture(scope='function')
async def test_client():
    """Тестовый клиент."""
    async with AsyncClient(
        app=app,
        base_url='http://test',
        timeout=10,
    ) as async_client:
        yield async_client
