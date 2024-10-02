from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class Status(Enum):
    """Статусы ответов на запросы."""

    success = 'Success'
    error = 'Error'


class CreateCatResponse(BaseModel):
    """Схема ответа создания объекта Cat."""

    status: Status = Status.success
    message: str


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
