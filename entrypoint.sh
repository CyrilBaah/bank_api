#!/bin/sh

# Wait for database
echo "Waiting for database..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "Database started"

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Start server
gunicorn base.wsgi:application --workers 3 --bind 0.0.0.0:8000 

