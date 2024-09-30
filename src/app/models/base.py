from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Базовый класс наследования моделей."""

    id: Mapped[int] = mapped_column(primary_key=True)
