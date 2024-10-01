from typing import List, Optional

from pydantic import BaseModel


class BreedBase(BaseModel):
    """Базовая схема модели Breed."""

    id: int
    name: str

    class Config:  # noqa: D106
        from_attributes = True


class CatBase(BaseModel):
    """Базовая схема модели Cat."""

    color: str
    age_in_months: int
    description: Optional[str] = None
    breed: BreedBase

    class Config:  # noqa: D106
        from_attributes = True


class CatListResponseModel(BaseModel):
    """Схема ответа список кошачих."""

    cats: List[CatBase]
