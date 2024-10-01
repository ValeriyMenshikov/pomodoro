FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml poetry.lock /app/
COPY app /app/app

RUN pip install poetry
RUN poetry install --no-interaction --no-ansi

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8081", "--reload"]