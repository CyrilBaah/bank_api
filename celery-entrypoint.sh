#!/bin/sh

# Wait for database
echo "Waiting for database..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "Database started"

# Wait for RabbitMQ
echo "Waiting for RabbitMQ..."
while ! nc -z rabbitmq 5672; do
  sleep 0.1
done
echo "RabbitMQ started"

# Start Celery worker
celery -A base.celery_app worker --loglevel=info
