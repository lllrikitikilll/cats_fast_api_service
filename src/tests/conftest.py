import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.app.core.settings import settings
from src.app.main import app
from src.app.models import Base, Breed, Cat
from src.app.models.db_helper import get_db


@pytest.fixture(scope="function")
async def db_session():
    """Создание новой сессии базы данных с откатом в конце теста."""
    # Создаем асинхронный движок для базы данных
    engine = create_async_engine(settings.psql.url)

    # Создаем асинхронный sessionmaker для управления сессиями
    async_session_factory = async_sessionmaker(
        bind=engine, autocommit=False, autoflush=False, expire_on_commit=False,
    )

    # Создаем таблицы в базе данных
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_factory() as session:
        yield session  # Возвращаем сессию для использования в тестах

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    # Закрываем соединение с базой данных
    await engine.dispose()


@pytest.fixture(scope='function')
def breed_name():
    """Название породы."""
    return "Британский вислоухий"


@pytest.fixture(scope='function')
def cat_id():
    """Id кошки в БД."""
    return 1


@pytest.fixture(scope="function")
def breed_payload(breed_name):
    """Тестовые данные для создания записи в БД."""
    return {
        "name": breed_name,
    }


@pytest.fixture(scope="function")
def cat_payload(breed_payload):
    """Тестовые данные для создания записи в БД."""
    return {
        "color": "Красный",
        "age_in_months": 10,
        "description": None,
    }


@pytest.fixture(scope="function")
def create_cat_payload():
    """Тестовые данные для создания записи в БД."""
    return {
        "color": "Рыжий",
        "age_in_months": 60,
        "description": "Краткое описание",
        "breed_id": 1,
    }


@pytest.fixture(scope="function")
def update_cat_payload():
    """Тестовые данные для создания записи в БД."""
    return {
        "color": "Черный",
        "age_in_months": 10,
        "description": "Измененное описание",
        "breed_id": 1,
    }


@pytest.fixture(scope="function", autouse=True)
async def setup_database(db_session, cat_payload, breed_payload):
    """Инициализация базы данных перед тестами."""
    # Создаем породу
    breed1 = Breed(name=breed_payload["name"])
    db_session.add(breed1)
    await db_session.commit()
    await db_session.refresh(breed1)

    # Создаем кошку
    cat1 = Cat(
        breed_id=breed1.id,
        color=cat_payload["color"],
        age_in_months=cat_payload["age_in_months"],
        description=cat_payload["description"],
    )
    db_session.add(cat1)
    await db_session.commit()


@pytest.fixture(scope="function")
async def test_client(db_session):
    """ТЕстовый клиент с переаписью зависимости бд."""

    async def override_get_db():  # noqa: WPS430
        try:  # noqa: WPS501
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(
        app=app, base_url="http://test", timeout=10,
    ) as async_client:
        yield async_client
