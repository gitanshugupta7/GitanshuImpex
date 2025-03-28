#!/bin/bash
python manage.py migrate --noinput
python manage.py collectstatic --noinput
gunicorn gipl_website.wsgi:application --bind 0.0.0.0:$PORT
