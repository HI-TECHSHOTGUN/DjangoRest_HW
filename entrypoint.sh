#!/bin/sh
set -e

# миграции и collectstatic
poetry run python manage.py migrate --noinput
poetry run python manage.py collectstatic --noinput

# передать управление на CMD/command из docker-compose
exec "$@"