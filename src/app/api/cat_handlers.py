from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.core.settings import settings
from src.app.models.db_helper import get_db
from src.app.schemas import schemas
from src.app.service.cat import CatService, get_cat_service

router = APIRouter(
    prefix=settings.url.prefix,
)


@router.get("/cats")
async def get_all_cats(
    session: AsyncSession = Depends(get_db),
    cat_service: CatService = Depends(get_cat_service),
) -> schemas.CatListResponseModel:
    """Получение списка всех котят."""
    cats = await cat_service.get_all_cats(session=session)
    return schemas.CatListResponseModel(cats=cats)


@router.get("/cats/breeds")
async def all_breeds(
    session: AsyncSession = Depends(get_db),
    cat_service: CatService = Depends(get_cat_service),
) -> schemas.BreedListResponseModel:
    """Получение списка пород."""
    breeds = await cat_service.get_all_breeds(session=session)
    return schemas.BreedListResponseModel(breeds=breeds)


@router.get("/cats/breeds/{breed}")
async def cats_with_breed(
    breed: str,
    session: AsyncSession = Depends(get_db),
    cat_service: CatService = Depends(get_cat_service),
) -> schemas.CatListResponseModel:
    """Получение списка кошачих опред. породы."""
    cats = await cat_service.get_cats_with_breed(session=session, breed=breed)
    return schemas.CatListResponseModel(cats=cats)


@router.get("/cats/{cat_id}")
async def cat_info(
    cat_id: int,
    session: AsyncSession = Depends(get_db),
    cat_service: CatService = Depends(get_cat_service),
) -> schemas.CatBase:
    """Получение подробной информации о котенке."""
    return await cat_service.get_cats_with_id(session=session, cat_id=cat_id)


@router.post("/cats", status_code=status.HTTP_201_CREATED)
async def add_cat(
    cat_data: schemas.CreateCatDataModel,
    session: AsyncSession = Depends(get_db),
    cat_service: CatService = Depends(get_cat_service),
) -> schemas.CreateCatResponse:
    """Добавление информации о котенке."""
    return await cat_service.create_cat(session=session, cat_data=cat_data)


@router.patch("/cats/{cat_id}")
async def patch_cat(cat_id: int):
    """Изменение информации о котенке."""
    pass  # noqa: WPS420


@router.delete("/cats/{cat_id}")
async def delete_cat(
    cat_id: int,
    session: AsyncSession = Depends(get_db),
    cat_service: CatService = Depends(get_cat_service),
) -> schemas.DeleteCatResponse:
    """Удалить информацию о котенке."""
    return await cat_service.delete_cat(session=session, cat_id=cat_id)
