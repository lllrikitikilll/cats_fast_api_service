# Cats Service API

Этот проект представляет собой API для работы с кошками, построенный с использованием FastAPI и SQLAlchemy. Он позволяет выполнять операции CRUD (создание, чтение, обновление и удаление)


## Запуск приложения

Запуск производится в контейнерах с сервисом postgres. Для запуска используется Docker
```bash
docker compose up -d
```
Далее производится обновления миграций алембик до последней версии
```bash
docker exec -i cats_service poetry run alembic upgrade head
```

B наполенение БД тестовыми данными:
```bash
docker exec -i postgresql psql -U postgres_user -d postgres_db -f test_data.sql
```

Документация Swagger будет доступна по ссылке:
```
http://localhost:8000/docs/
```

## Тестирование.

Для тестов требуется запустить отдельную БД с postgres в контейнере, сам сервис запускается не в контейнере, а непостредственно на хосте (Так мне пока удобно):
```bash
docker compose -f .\docker-compose.test.yml up -d 
```


Установка зависимостей. Затем запустить сами тесты:
```bash
poetry install
pytest
```