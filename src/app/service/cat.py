from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.app.models import Breed, Cat
from src.app.schemas import schemas


class CatService:
    """Сервис CRUD для работы с данными кошачих."""

    async def get_all_cats(self, session: AsyncSession):
        """Запрос всех кошек.

        Args:
            session (AsyncSession): асинхронная сессия

        Raises:
            HTTPException: Ошибка 404 если список пустой

        Returns:
            list[Cat]: Список кошачих (Cat) из таблицы
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
            list[Cat]: Список Cat (кошек) заданной породы (breed)
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
            Cat: объект Cat по id из БД
        """
        stmt = select(Cat).where(Cat.id == cat_id).options(selectinload(Cat.breed))  # noqa: WPS221, E501
        result_db: Result = await session.execute(statement=stmt)

        try:
            cat = result_db.scalars().first()
        except SQLAlchemyError as exp:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Возникла ошибка при взятии кошки с id: {cat_id}.",
            ) from exp

        if not cat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Такой кошки у нас нет.',
            )
        return cat

    async def create_cat(
        self, session: AsyncSession, cat_data: schemas.CreateCatDataModel,
    ):
        """Создает новую запись кошки в базе данных.

        Args:
            session (AsyncSession): асинхронная сессия
            cat_data (CreateCatDataModel): данные с полями для записи в БД

        Raises:
            HTTPException: Ошибка 500 ошибка сервера

        Returns:
            schemas.CreateCatResponse: статус запроса
        """
        try:  # noqa: WPS229
            new_cat = Cat(**cat_data.model_dump())

            session.add(new_cat)

            await session.commit()

            return schemas.CreateCatResponse(
                status=schemas.Status.success,
                message="Запись создана",
            )

        except SQLAlchemyError as exp:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Не удалось создать кошку из-за ошибки на сервере.',
            ) from exp

    async def delete_cat(self, session: AsyncSession, cat_id: int):
        """Удаление объекта Cat по id.

        Args:
            session (AsyncSession): асинхронная сессия
            cat_id (int): id кошки в БД

        Raises:
            HTTPException: Ошибка 404 если нет такой записи в БД

        Returns:
            schemas.DeleteCatResponse: статус запроса
        """
        async with session.begin():
            stmt = select(Cat).where(Cat.id == cat_id)
            result_db = await session.execute(stmt)

            cat = result_db.scalar_one_or_none()
            if not cat:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Кошка не найдена.',
                )

            await session.delete(cat)
            await session.commit()
        return schemas.DeleteCatResponse(
            status=schemas.Status.success,
            message="Запись удалена",
        )

    async def update_cat(
        self, session: AsyncSession, cat_id: int, cat_data: schemas.UpdateCatData,
    ):
        """Обновление объекта Cat по id.

        Args:
            session (AsyncSession): асинхронная сессия
            cat_id (int): id кошки в БД
            cat_data (schemas.UpdateCatData): Данные для обновления объекта

        Raises:
            HTTPException: Ошибка 404 если нет такой записи в БД

        Returns:
            schemas.UpdateCatResponse: статус запроса
        """
        async with session.begin():
            stmt = select(Cat).where(Cat.id == cat_id)
            result_db = await session.execute(stmt)

            cat = result_db.scalar_one_or_none()
            if not cat:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Кошка не найдена.',
                )

            for key, value in cat_data.model_dump().items():  # noqa: WPS110
                setattr(cat, key, value)

            await session.commit()
        return schemas.UpdateCatResponse(
            status=schemas.Status.success,
            message="Запись обновлена",
        )


cat_service = CatService()


def get_cat_service() -> CatService:
    """Возращает экз. CatService."""
    return cat_service
