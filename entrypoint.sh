#!/bin/sh

set -e

echo "Applying database migrations..."
poetry run python manage.py migrate

echo "Starting Gunicorn..."
poetry run gunicorn --bind 0.0.0.0:8000 config.wsgi:application