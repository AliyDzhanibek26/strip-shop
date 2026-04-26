#!/bin/sh
set -e

export DJANGO_SETTINGS_MODULE=config.settings.production

python manage.py migrate --noinput
python manage.py collectstatic --noinput

if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
u, _ = User.objects.get_or_create(username='$DJANGO_SUPERUSER_USERNAME')
u.is_staff = True
u.is_superuser = True
u.set_password('$DJANGO_SUPERUSER_PASSWORD')
u.save()
"
fi

python manage.py loaddata fixtures/initial_data.json 2>/dev/null || true

exec gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 2
