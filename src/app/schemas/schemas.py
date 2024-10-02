from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class Status(Enum):
    """Статусы ответов на запросы."""

    success = 'Success'
    error = 'Error'


class BaseCatResponse(BaseModel):
    """Базовая схема ответа."""

    status: Status = Status.success
    message: str


class CreateCatResponse(BaseCatResponse):
    """Cсхема ответа создания объекта Cat."""

    pass  # noqa: WPS604, WPS420


class DeleteCatResponse(BaseCatResponse):
    """Cхема ответа удаления объекта Cat."""

    pass  # noqa: WPS604, WPS420


class UpdateCatResponse(BaseCatResponse):
    """Cхема ответа обновления объекта Cat."""

    pass  # noqa: WPS604, WPS420


class BreedBase(BaseModel):
    """Базовая схема модели Breed."""

    id: int
    name: str

    class Config:  # noqa: D106
        from_attributes = True


class CatBase(BaseModel):
    """Базовая схема модели Cat."""

    id: int
    color: str
    age_in_months: int
    description: Optional[str] = None
    breed: BreedBase

    class Config:  # noqa: D106
        from_attributes = True


class UpdateCatData(BaseModel):
    """Схема данных для обновления объекта Cat."""

    color: str
    age_in_months: int
    description: Optional[str] = None
    breed_id: int


class CreateCatDataModel(BaseModel):
    """Схема данных на создание объекта кошачих."""

    color: str
    age_in_months: int
    description: Optional[str] = None
    breed_id: int


class CatListResponseModel(BaseModel):
    """Схема ответа список кошачих."""

    cats: List[CatBase]


class BreedListResponseModel(BaseModel):
    """Схема ответа список пород."""

    breeds: list[BreedBase]
