#!/bin/sh
set -e

# миграции и collectstatic (если нужно)
poetry run python manage.py migrate --noinput
poetry run python manage.py collectstatic --noinput

# передать управление на CMD/command из docker-compose
exec "$@"