FROM python:3.12-slim

WORKDIR /workspace/cats_service

COPY poetry.lock pyproject.toml ./

RUN python3.12 -m pip install poetry && \
    poetry install --no-root

COPY ./src ./src

CMD ["poetry", "run", "uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]