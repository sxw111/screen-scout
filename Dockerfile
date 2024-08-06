FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml poetry.lock /app/
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-dev

COPY . .

ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

CMD ["poetry", "run", "uvicorn", "screenscout.main:app", "--host", "0.0.0.0", "--port", "8000"]
