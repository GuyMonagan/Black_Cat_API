FROM python:3.11-slim

WORKDIR /app

ENV POETRY_VERSION=1.6.1
RUN pip install poetry==$POETRY_VERSION

COPY pyproject.toml poetry.lock* ./
RUN poetry config virtualenvs.create false && poetry install --no-root

COPY . .

CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
