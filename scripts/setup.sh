#!/bin/bash
# Setup and start all services

echo "Starting Bank API services..."

# Build and start containers
docker-compose up -d --build

echo "⏳ Waiting for services to start..."
sleep 10

# Check service status
echo "Service Status:"
docker-compose ps

echo "Services started! Access URLs:"
echo "  - Django API: http://localhost:8000/api/docs/"
echo "  - Flower: http://localhost:5555"
echo "  - RabbitMQ: http://localhost:15672 (admin/Pass123)"
echo "  - Mailpit: http://localhost:8025"
