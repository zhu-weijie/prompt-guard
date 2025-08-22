FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN pip install poetry

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.in-project true && poetry install --no-root --only main

FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /app/.venv ./.venv

ENV PATH="/app/.venv/bin:$PATH"

COPY ./src ./src

CMD ["uvicorn", "src.prompt_guard.main:app", "--host", "0.0.0.0", "--port", "8000"]
