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


cat_service = CatService()


def get_cat_service() -> CatService:
    """Возращает экз. CatService."""
    return cat_service
