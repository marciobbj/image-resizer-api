#!/usr/bin/env bash

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn -w 1 -b :8000 image.wsgi:application