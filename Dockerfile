FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Устанавливаем системные зависимости, необходимые для сборки некоторых пакетов
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    postgresql-client \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*


COPY pyproject.toml poetry.lock /app/

RUN pip install poetry==1.5.1
RUN poetry install --no-dev --no-root

RUN pip install gunicorn

COPY . /app/

CMD ["poetry", "run", "gunicorn", "--bind", "0.0.0.0:8000", "--workers=3", "--log-level=info", "--access-logfile=-", "--error-logfile=-", "core.wsgi:application"]