#!/bin/sh
set -e

export DJANGO_SETTINGS_MODULE=config.settings.production

python manage.py migrate --noinput
python manage.py collectstatic --noinput
exec gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 2
