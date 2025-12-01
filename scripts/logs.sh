#!/bin/bash
# View logs for all services

if [ "$1" ]; then
    echo "📋 Showing logs for $1..."
    docker-compose logs -f "$1"
else
    echo "📋 Available services:"
    echo "  app, celery_worker, flower, rabbitmq, redis, db, mailpit"
    echo ""
    echo "Usage: ./logs.sh [service_name]"
    echo "Example: ./logs.sh app"
    echo ""
    echo "📋 Recent logs from all services:"
    docker-compose logs --tail=5
fi
