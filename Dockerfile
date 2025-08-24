FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock /app/

RUN pip install poetry==1.5.1
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev --no-root

COPY . /app/

CMD ["poetry", "run", "gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]