# Activate virtual environment
source /home/gitanshuimpex/venv/bin/activate

# Load environment variables
export $(cat /home/gitanshuimpex/gitanshuimpex/.env | xargs)

# Navigate to the project directory
cd /home/gitanshuimpex/gitanshuimpex

# Collect static files
python manage.py collectstatic --noinput

# Apply database migrations
python manage.py migrate

# Start Gunicorn
exec gunicorn gipl_website.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 120
