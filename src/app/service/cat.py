from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.app.models import Breed, Cat


class CatService:
    """Сервис CRUD для работы с данными кошачих."""

    async def get_all_cats(self, session: AsyncSession):
        """Запрос всех кошек.

        Args:
            session (AsyncSession): асинхронная сессия

        Raises:
            HTTPException: Ошибка 404 если список пустой

        Returns:
            list[Cat]: Список кошачих из таблицы
        """
        stmt = select(Cat).options(selectinload(Cat.breed))
        result_db: Result = await session.execute(statement=stmt)

        try:
            cats = list(result_db.scalars().all())
        except SQLAlchemyError as exp:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Возникла непредвиденная ошибка при получении списка котят.',
            ) from exp

        if not cats:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Котята не найдены.',
            )
        return cats

    async def get_all_breeds(self, session: AsyncSession):
        """Запрос всех кошек.

        Args:
            session (AsyncSession): асинхронная сессия

        Raises:
            HTTPException: Ошибка 404 если список пустой

        Returns:
            list[Breed]: Список пород из таблицы Breed
        """
        stmt = select(Breed)
        result_db: Result = await session.execute(statement=stmt)

        try:
            breeds = list(result_db.scalars().all())
        except SQLAlchemyError as exp:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Возникла непредвиденная ошибка при получении списка пород.',
            ) from exp

        if not breeds:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Породы отсутствуют.',
            )
        return breeds

    async def get_cats_with_breed(self, session: AsyncSession, breed: str):
        """Запрос всех кошек заданной породы.

        Args:
            session (AsyncSession): асинхронная сессия
            breed (str): название породы

        Raises:
            HTTPException: Ошибка 404 если породы нет

        Returns:
            list[Cat]: Список кошек заданной породы
        """
        stmt = select(Cat).options(selectinload(Cat.breed)).join(Breed).where(Breed.name == breed)  # noqa: E501, WPS221
        result_db: Result = await session.execute(statement=stmt)

        try:
            cats = list(result_db.scalars().all())
        except SQLAlchemyError as exp:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Возникла ошибка при получении списка кошек с такой породой.",
            ) from exp

        if not cats:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Порода отсутствуют.',
            )
        return cats

    async def get_cats_with_id(self, session: AsyncSession, cat_id: int):
        """Запрос кошки по id.

        Args:
            session (AsyncSession): асинхронная сессия
            cat_id (int): id кошки в БД

        Raises:
            HTTPException: Ошибка 404 если нет такой записи в БД

        Returns:
            Cat: Список кошек заданной породы
        """
        stmt = select(Cat).where(Cat.id == cat_id).options(selectinload(Cat.breed))  # noqa: WPS221, E501
        result_db: Result = await session.execute(statement=stmt)

        try:
            cat = result_db.scalars().first()
        except SQLAlchemyError as exp:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Возникла ошибка при кошеки с id: {cat_id}.",
            ) from exp

        if not cat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Такой кошки у нас нет.',
            )
        return cat


cat_service = CatService()


def get_cat_service() -> CatService:
    """Возращает экз. CatService."""
    return cat_service
