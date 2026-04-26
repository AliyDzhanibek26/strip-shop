#!/bin/sh
set -e

export DJANGO_SETTINGS_MODULE=config.settings.production

echo "DATABASE_URL is set: $([ -n "$DATABASE_URL" ] && echo yes || echo NO)"
echo "PGHOST: ${PGHOST:-not set}"

python manage.py migrate --noinput
python manage.py collectstatic --noinput

if [ -n "$DJANGO_SUPERUSER_USERNAME" ]; then
    python manage.py createsuperuser --noinput 2>/dev/null || true
fi

python manage.py loaddata fixtures/initial_data.json 2>/dev/null || true

exec gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 2
