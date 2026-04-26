#!/bin/sh
set -e

export DJANGO_SETTINGS_MODULE=config.settings.production

echo "DATABASE_URL is set: $([ -n "$DATABASE_URL" ] && echo yes || echo NO)"
echo "PGHOST: ${PGHOST:-not set}"

python manage.py migrate --noinput
python manage.py collectstatic --noinput
exec gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 2
