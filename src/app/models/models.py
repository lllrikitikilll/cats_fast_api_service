from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from src.app.models.base import Base


class Cat(Base):
    """Модель кошачих."""

    __tablename__ = 'cat'

    color: Mapped[str] = mapped_column(String(100))
    age_in_months: Mapped[int]
    description: Mapped[str] = mapped_column(String(), nullable=True)
    breed_id: Mapped[int] = mapped_column(ForeignKey('breed.id'))
    breed: Mapped['Breed'] = relationship(back_populates='cats')

    @validates('age_in_months')
    def validate_amount_gt_zero(self, age_in_months) -> int:
        """
        Валидация возраста кота. Проверяет, что возраст больше нуля.

        :param int age_in_months: Возраст кота в месяцах.
        :raises ValueError: Если возраст меньше или равен нулю.
        :return: Возраст кота в месяцах, если он валиден.
        :rtype: int
        """
        if age_in_months <= 0:
            raise ValueError('Возраст должен быть больше нуля')
        return age_in_months


class Breed(Base):
    """Модель категории породы."""

    __tablename__ = 'breed'

    name: Mapped[str] = mapped_column(String(100))
    cats: Mapped[list['Cat']] = relationship(
        back_populates='breed',
    )
