python manage.py collectstatic --noinput
python manage.py migrate
gunicorn gipl_website.wsgi:application --bind 0.0.0.0:$PORT
