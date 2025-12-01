#!/bin/bash
# Run Django migrations

echo "🔄 Running Django migrations..."

# Make migrations
docker exec bank python manage.py makemigrations

# Apply migrations
docker exec bank python manage.py migrate

# Create superuser (optional)
if [ "$1" = "--superuser" ]; then
    echo "👤 Creating superuser..."
    docker exec -it bank python manage.py createsuperuser
fi

echo "✅ Migrations complete!"
