# Activate virtual environment
source ../venv/bin/activate
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

# Start Gunicorn server (running on port 8001 for internal use)
exec gunicorn gipl_website.wsgi:application \
  --bind 127.0.0.1:8001 \
  --workers 3 \
  --timeout 120 \
  --log-level info \
  --log-file logs/gunicorn.log

