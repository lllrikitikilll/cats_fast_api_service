from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.app.models.models import Cat


class CatService:
    """Сервис CRUD для работы с данными кошачих."""

    async def get_all_cats(self, session: AsyncSession) -> list[Cat]:
        """Запрос всех кошек.

        Args:
            session (AsyncSession): асинхронная сессия

        Returns:
            list[Cat]: Список кошачих из таблицы
        """
        stmt = select(Cat).options(selectinload(Cat.breed))
        result_db: Result = await session.execute(statement=stmt)
        return list(result_db.scalars().all())


cat_service = CatService()


def get_cat_service() -> CatService:
    """Возращает экз. CatService."""
    return cat_service
