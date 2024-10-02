from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.app.models.base import Base


class Cat(Base):
    """Модель кошачих."""

    __tablename__ = 'cat'

    color: Mapped[str] = mapped_column(String(100))
    age_in_months: Mapped[int]
    description: Mapped[str] = mapped_column(String(), nullable=True)
    breed_id: Mapped[int] = mapped_column(ForeignKey('breed.id'))
    breed: Mapped['Breed'] = relationship(back_populates='cats')


class Breed(Base):
    """Модель категории породы."""

    __tablename__ = 'breed'

    name: Mapped[str] = mapped_column(String(100))
    cats: Mapped[list['Cat']] = relationship(
        back_populates='breed',
    )
