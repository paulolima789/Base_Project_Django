#!/bin/sh

set -e

python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py seed
python manage.py collectstatic --noinput

daphne -b 0.0.0.0 -p ${API_PORT:-8000} core.asgi:application