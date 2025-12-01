#!/bin/bash
# Test all services

echo "🧪 Testing Bank API services..."

services=(
    "Django API:http://localhost:8000/api/docs/"
    "Flower:http://localhost:5555"
    "RabbitMQ:http://localhost:15672"
    "Mailpit:http://localhost:8025"
)

for service in "${services[@]}"; do
    name=$(echo $service | cut -d: -f1)
    url=$(echo $service | cut -d: -f2-)
    
    if curl -s -o /dev/null -w "%{http_code}" "$url" | grep -q "200"; then
        echo "✅ $name is working"
    else
        echo "❌ $name is not responding"
    fi
done

echo "🔍 Testing Celery..."
docker exec bank python -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings')
django.setup()
from base.celery_app import app
i = app.control.inspect()
stats = i.stats()
if stats:
    print('✅ Celery workers active')
else:
    print('❌ No Celery workers')
"
