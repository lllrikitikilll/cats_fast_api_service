from fastapi import APIRouter

router = APIRouter(
    prefix='/api',
)


@router.post('/breeds')
async def breeds():
    """Получение списка пород."""
    pass  # noqa: WPS420


@router.post('/cats')
async def cats():
    """Получение списка всех котят."""
    pass  # noqa: WPS420


@router.post('/cats/{id}')
async def cat_info():
    """Получение подробной информации о котенке."""
    pass  # noqa: WPS420


@router.post('/cats')
async def add_cat():
    """Добавление информации о котенке."""
    pass  # noqa: WPS420


@router.patch('/cats/{id}')
async def patch_cat():
    """Изменение информации о котенке."""
    pass  # noqa: WPS420


@router.delete('/cats/{id}')
async def delete_cat():
    """Удалить информацию о котенке."""
    pass  # noqa: WPS420
